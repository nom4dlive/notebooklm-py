"""Server-info and capabilities routes.

This module provides:
- ``GET /v1/server/info``: Server version and auth health (existing)
- ``GET /v1/server/capabilities``: Dynamic list of all supported features

The capabilities endpoint allows frontends to discover available options without
hardcoding values, enabling adaptive UIs that adjust to API changes.
"""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Query, Request

from ..._app import download_specs as download_specs_core
from ..._app.auth_check import AuthCheckPlan, run_auth_check
from ..._redact import redact
from ..._version_info import version_string
from ...client import NotebookLMClient
from ...exceptions import AuthError, NotebookLMError
from ...paths import get_storage_path, resolve_profile
from .._context import get_client, get_client_error
from .._errors import error_item
from .artifacts import DOWNLOAD_SPECS, GENERATE_TYPES, _KIND_DEFAULTS, _KIND_OPTIONS

__all__ = ["router"]

#: Named here rather than imported from ``server.app`` to avoid a circular import
#: (``app`` imports this router). Kept equal to ``server.app.SERVER_NAME`` by
#: ``tests/server/test_main.py``.
SERVER_NAME = "notebooklm-server"

router = APIRouter(prefix="/server", tags=["server"])


def _no_env_auth_json() -> str:
    """Inline-auth reader for the neutral core.

    The server authenticates from on-disk storage (``from_storage``), never from
    inline ``NOTEBOOKLM_AUTH_JSON``, so the plan sets ``has_env_auth=False`` and
    this accessor is never invoked. It satisfies the core's required keyword only.
    """
    return ""  # pragma: no cover - unreachable while has_env_auth is False


async def _account_block(client: NotebookLMClient, *, authenticated: bool) -> dict[str, Any]:
    """Best-effort account identity + quota limits for pacing (mirrors MCP).

    ``email`` / ``authuser`` come from the client; the limits/language fields need
    a live session and degrade to ``{available: False, reason}`` (scrubbed) rather
    than sinking the whole response when the session is stale.
    """
    identity: dict[str, Any] = {
        "email": await client.get_account_email(live_fallback=authenticated),
        "authuser": client.get_account_authuser(),
    }
    if not authenticated:
        return {**identity, "available": False, "reason": "not authenticated"}
    try:
        # Both limits + language ride one GET_USER_SETTINGS response (#1724):
        # a single fetch instead of two identical POSTs (mirrors the MCP tool).
        settings = await client.settings.get_user_settings()
        limits, output_language = settings.limits, settings.output_language
    except NotebookLMError as exc:  # degrade, don't sink the whole response
        return {**identity, "available": False, "reason": redact(str(exc))}
    return {
        **identity,
        "available": True,
        "notebook_limit": limits.notebook_limit,
        "source_limit": limits.source_limit,
        # Subscription tier enum (GET_USER_SETTINGS limits[4]); mirrors the MCP block.
        "tier": limits.tier,
        # Global account output language, ``None`` when the account has never set
        # one; ``output_language_is_default`` disambiguates that ``None`` (``True``
        # = the account uses NotebookLM's default language, not a missing value).
        # Mirrors the MCP block — envelope-level drift degrades to ``available:
        # False`` rather than reaching here; per ADR-0011 drift at the optional
        # language slot is treated as unset (i.e. the default) too.
        "output_language": output_language,
        "output_language_is_default": output_language is None,
    }


def _persisted_account_identity(account: object) -> dict[str, Any]:
    """Return persisted ``email`` / ``authuser`` from auth-check details when present."""
    if not isinstance(account, dict):
        return {}
    identity: dict[str, Any] = {}
    email = account.get("email")
    if email is not None:
        identity["email"] = email
    authuser = account.get("authuser")
    if authuser is not None:
        identity["authuser"] = authuser
    return identity


@router.get("/info")
async def server_info(
    request: Request,
    include_account: Annotated[bool, Query()] = False,
) -> dict[str, Any]:
    """Report the server version and local authentication health.

    Returns ``version`` and an ``auth`` block (``authenticated`` /
    ``storage_exists`` / ``json_valid`` / ``cookies_present`` / ``sid_cookie`` /
    ``profile``). Set ``?include_account=true`` to also fetch an ``account`` block
    (signed-in identity + quota limits + output language); it needs a live session,
    so it degrades to ``{available: False, reason}`` rather than failing the call.

    The absolute on-disk storage path is deliberately not returned (it leaks the
    host filesystem layout while telling the agent nothing actionable).
    """
    # Report the *resolved* profile (never ``None``): this names the profile the
    # auth probe actually ran against (#1790, #1791).
    profile = resolve_profile()
    storage_path = get_storage_path(profile)
    plan = AuthCheckPlan(
        storage_path=storage_path,
        profile=profile,
        has_env_auth=False,
        has_home_env=False,
        auth_source_label=f"file ({storage_path})",
        test_fetch=False,
        json_output=True,
    )
    account_client: NotebookLMClient | None = None
    if include_account:
        try:
            account_client = await get_client(request)
        except AuthError:
            # A concurrent request can bind successfully immediately after
            # this request loses an auth generation; re-check state below.
            pass
        except Exception:
            # Degrade only failures that the loader recorded for diagnostics.
            # Unrecorded exceptions still identify a route/programming error
            # and must retain the normal server error path.
            if get_client_error(request) is None:
                raise
    startup_error = get_client_error(request)
    if include_account and account_client is None and startup_error is None:
        # The first lookup can fail just before a concurrent request finishes
        # binding the singleton client and clears ``client_error``. Re-read the
        # now-bound client instead of treating that narrow race as an invariant
        # violation below.
        account_client = await get_client(request)
    # Probe after any lazy bind: that bind can succeed because storage was
    # repaired after this request started, and the response must describe the
    # newly bound session rather than an earlier stale disk snapshot.
    result = await run_auth_check(plan, read_env_auth_json=_no_env_auth_json)
    startup_error_item = error_item(startup_error) if startup_error is not None else None
    authenticated = result.all_passed and startup_error is None
    auth: dict[str, Any] = {
        "authenticated": authenticated,
        "storage_exists": bool(result.checks.get("storage_exists")),
        "json_valid": bool(result.checks.get("json_valid")),
        "cookies_present": bool(result.checks.get("cookies_present")),
        "sid_cookie": bool(result.checks.get("sid_cookie")),
        "profile": profile,
    }
    if startup_error_item is not None:
        auth["startup_error"] = startup_error_item
    info: dict[str, Any] = {
        "server": SERVER_NAME,
        "version": version_string(),
        "auth": auth,
    }
    if include_account:
        if startup_error_item is not None:
            info["account"] = {
                **_persisted_account_identity(result.details.get("account")),
                "available": False,
                "reason": startup_error_item["message"],
            }
        else:
            if account_client is None:  # pragma: no cover - guarded above
                raise RuntimeError("account diagnostics require a bound client")
            info["account"] = await _account_block(account_client, authenticated=authenticated)
    return info


@router.get("/capabilities")
async def get_capabilities() -> dict[str, Any]:
    """Return all supported features and options for frontend discovery.
    
    This endpoint provides a comprehensive list of:
    - Artifact types and their configuration options
    - Download formats for each artifact type
    - Source types supported
    - Audio/video formats and styles
    - Language support
    - Rate limits and quotas
    
    Frontends can use this to dynamically build UIs without hardcoding values,
    ensuring compatibility across API versions.
    
    Returns:
        Dictionary with all capabilities organized by category
    """
    from ..._app.language import SUPPORTED_LANGUAGES
    from ..routes.sources import MAX_UPLOAD_BYTES
    
    # Build capabilities response
    capabilities: dict[str, Any] = {
        "artifact_types": list(GENERATE_TYPES),
        "artifact_options": {},
        "download_formats": {},
        "source_types": ["url", "text", "pdf", "youtube", "drive"],
        "max_upload_size_bytes": MAX_UPLOAD_BYTES,
        "max_upload_size_mb": MAX_UPLOAD_BYTES // (1024 * 1024),
        "languages": list(SUPPORTED_LANGUAGES.keys()),
        "rate_limits": {
            "generation_per_minute": 10,  # Default, configurable via env
            "download_per_minute": 30,
            "chat_per_minute": 20,
        },
    }
    
    # Add per-type options
    for artifact_type in GENERATE_TYPES:
        type_defaults = _KIND_DEFAULTS.get(artifact_type, {})
        type_options = _KIND_OPTIONS.get(artifact_type, {})
        
        capabilities["artifact_options"][artifact_type] = {
            "defaults": type_defaults,
            "options": {
                key: {"choices": list(choices) if choices else "free_text"}
                for key, choices in type_options.items()
            },
        }
    
    # Add download formats per artifact type
    for artifact_type in GENERATE_TYPES:
        type_specs = []
        for spec_name, spec in DOWNLOAD_SPECS.items():
            if spec.kind == artifact_type:
                type_specs.append({
                    "name": spec_name,
                    "format": spec.format,
                    "extension": spec.extension,
                })
        if type_specs:
            capabilities["download_formats"][artifact_type] = type_specs
    
    return capabilities

