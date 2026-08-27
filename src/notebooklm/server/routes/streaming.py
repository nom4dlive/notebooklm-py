"""Server-Sent Events (SSE) endpoint for real-time artifact status updates.

This module provides a streaming endpoint that pushes artifact generation
progress updates to connected clients, eliminating the need for inefficient
polling loops in frontends.

Design highlights:

- **SSE Stream**: Uses Server-Sent Events for unidirectional server-to-client streaming
- **Auto-reconnect**: Clients automatically reconnect on connection loss
- **Progress Updates**: Pushes state changes (PENDING → IN_PROGRESS → COMPLETED/FAILED)
- **Heartbeat**: Sends periodic keepalive comments to prevent timeout
- **Cleanup**: Automatically closes stream when task reaches terminal state
"""

from __future__ import annotations

import asyncio
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse

from ..._app import artifacts as artifact_core
from ...client import NotebookLMClient
from ...types import GenerationState
from .._context import get_client, get_pending
from .._pending import PendingRegistry

__all__ = ["router"]

router = APIRouter(tags=["streaming"])

# Heartbeat interval in seconds (send comment to keep connection alive)
HEARTBEAT_INTERVAL = 15.0

# Poll interval when checking for status updates (internal, not exposed to client)
STATUS_POLL_INTERVAL = 2.0


async def _sse_event_stream(
    notebook_id: str,
    task_id: str,
    client: NotebookLMClient,
    pending: PendingRegistry,
) -> Any:
    """Generate SSE events for artifact status updates.
    
    Yields properly formatted SSE messages:
    - event: status\n data: {json_payload}
    - event: heartbeat\n data: {timestamp}
    - event: end\n data: {final_state}
    """
    import json
    from datetime import datetime
    
    last_state: GenerationState | None = None
    
    async def generate_events():
        nonlocal last_state
        
        while True:
            try:
                # Check current status
                status = await artifact_core.poll_artifact(client, notebook_id, task_id)
                current_state = status.status
                
                # Send update if state changed or first poll
                if current_state != last_state:
                    last_state = current_state
                    
                    # Build payload
                    view = artifact_core.status_view(status)
                    payload = {
                        "notebook_id": notebook_id,
                        "task_id": task_id,
                        "status": status.status.value,
                        "is_terminal": status.is_terminal,
                        "view": view,
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                    }
                    
                    yield f"event: status\ndata: {json.dumps(payload)}\n\n"
                    
                    # If terminal state, send final event and close
                    if status.is_terminal:
                        # Drop from pending registry if terminal
                        pending.drop(notebook_id, task_id)
                        
                        yield f"event: end\ndata: {json.dumps({
                            'task_id': task_id,
                            'final_status': status.status.value,
                            'timestamp': datetime.utcnow().isoformat() + "Z",
                        })}\n\n"
                        break
                
                # Wait before next poll
                await asyncio.sleep(STATUS_POLL_INTERVAL)
                
            except Exception as exc:
                # Send error event
                import json
                yield f"event: error\ndata: {json.dumps({'error': str(exc)})}\n\n"
                break
    
    # Wrap with heartbeat
    return stream_with_heartbeat(generate_events())


async def stream_with_heartbeat(event_generator: Any) -> Any:
    """Wrap an event generator with periodic heartbeat comments."""
    import time
    
    heartbeat_task: asyncio.Task[None] | None = None
    queue: asyncio.Queue[str | None] = asyncio.Queue()
    
    async def heartbeat_loop():
        """Send heartbeat comments periodically."""
        try:
            while True:
                await asyncio.sleep(HEARTBEAT_INTERVAL)
                # SSE comment (line starting with :) keeps connection alive
                await queue.put(": heartbeat\n\n")
        except asyncio.CancelledError:
            pass
    
    async def forward_events():
        """Forward events from generator to queue."""
        try:
            async for event in event_generator:
                await queue.put(event)
        finally:
            # Signal end of stream
            await queue.put(None)
    
    # Start both tasks
    heartbeat_task = asyncio.create_task(heartbeat_loop())
    forward_task = asyncio.create_task(forward_events())
    
    try:
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item
    finally:
        # Cancel heartbeat task
        if heartbeat_task:
            heartbeat_task.cancel()
            try:
                await heartbeat_task
            except asyncio.CancelledError:
                pass
        # Cancel forward task if still running
        if not forward_task.done():
            forward_task.cancel()
            try:
                await forward_task
            except asyncio.CancelledError:
                pass


@router.get("/v1/notebooks/{notebook_id}/artifacts/{task_id}/stream")
async def stream_artifact_status(
    notebook_id: str,
    task_id: str,
    request: Request,
    client: Annotated[NotebookLMClient, Depends(get_client)],
    pending: Annotated[PendingRegistry, Depends(get_pending)],
) -> StreamingResponse:
    """Stream real-time artifact generation status via Server-Sent Events.
    
    This endpoint establishes a long-lived connection that pushes status updates
    as the artifact generation progresses. Clients should use the EventSource API:
    
    ```javascript
    const eventSource = new EventSource(
      `/v1/notebooks/${notebookId}/artifacts/${taskId}/stream`,
      { headers: { 'Authorization': `Bearer ${token}` } }
    );
    
    eventSource.addEventListener('status', (event) => {
      const data = JSON.parse(event.data);
      console.log('Status update:', data);
    });
    
    eventSource.addEventListener('end', (event) => {
      const data = JSON.parse(event.data);
      console.log('Generation complete:', data);
      eventSource.close();
    });
    
    eventSource.addEventListener('error', (event) => {
      console.error('Stream error:', event);
      eventSource.close();
    });
    ```
    
    The stream automatically closes when the task reaches a terminal state
    (COMPLETED, FAILED, REMOVED).
    
    Returns:
        StreamingResponse with text/event-stream content type
    """
    return StreamingResponse(
        _sse_event_stream(notebook_id, task_id, client, pending),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        },
    )
