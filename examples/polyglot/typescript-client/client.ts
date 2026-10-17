/**
 * Ready-to-run TypeScript Client for NotebookLM-py REST Server.
 *
 * Requirements:
 * 1. notebooklm REST server running: `uv run python -m notebooklm.server --port 8000`
 * 2. Node.js 18+ (native fetch supported)
 */

export interface Notebook {
  id: string;
  title: string;
  sources_count?: number;
  created_at?: string;
}

export interface AskResponse {
  answer: string;
  conversation_id: string;
  references?: Array<{
    source_id: string;
    start_char: number;
    end_char: number;
  }>;
}

export interface ClientOptions {
  baseUrl?: string;
  profile?: string;
  timeoutMs?: number;
}

export class NotebookLMClient {
  private baseUrl: string;
  private profile?: string;
  private timeoutMs: number;

  constructor(options: ClientOptions = {}) {
    this.baseUrl = (options.baseUrl || "http://127.0.0.1:8000").replace(/\/+$/, "");
    this.profile = options.profile;
    this.timeoutMs = options.timeoutMs || 60000;
  }

  private async request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${path.startsWith("/") ? path : `/${path}`}`;
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      Accept: "application/json",
      ...(options.headers as Record<string, string>),
    };

    if (this.profile) {
      headers["X-NotebookLM-Profile"] = this.profile;
    }

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const res = await fetch(url, {
        ...options,
        headers,
        signal: controller.signal,
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`NotebookLM API Error [HTTP ${res.status}]: ${errorText}`);
      }

      return (await res.json()) as T;
    } finally {
      clearTimeout(timer);
    }
  }

  /**
   * List all notebooks in the active profile.
   */
  async listNotebooks(): Promise<Notebook[]> {
    return this.request<Notebook[]>("/v1/notebooks");
  }

  /**
   * Create a new notebook.
   */
  async createNotebook(title: string): Promise<Notebook> {
    return this.request<Notebook>("/v1/notebooks", {
      method: "POST",
      body: JSON.stringify({ title }),
    });
  }

  /**
   * Add a web URL source to a notebook.
   */
  async addSourceUrl(notebookId: string, url: string): Promise<{ id: string; status: string }> {
    return this.request<{ id: string; status: string }>(`/v1/notebooks/${notebookId}/sources`, {
      method: "POST",
      body: JSON.stringify({ type: "url", url }),
    });
  }

  /**
   * Ask a question grounded on notebook sources.
   */
  async ask(notebookId: string, question: string): Promise<AskResponse> {
    return this.request<AskResponse>(`/v1/notebooks/${notebookId}/ask`, {
      method: "POST",
      body: JSON.stringify({ question }),
    });
  }
}

// Example usage
async function runExample() {
  const client = new NotebookLMClient({
    baseUrl: "http://127.0.0.1:8000",
    profile: "default",
  });

  try {
    console.log("Listing notebooks...");
    const notebooks = await client.listNotebooks();
    console.log(`Found ${notebooks.length} notebooks.`);

    if (notebooks.length > 0) {
      const target = notebooks[0];
      console.log(`Asking question to notebook: "${target.title}" (${target.id})...`);
      const response = await client.ask(target.id, "Qual o objetivo central deste material?");
      console.log("\n--- Resposta ---");
      console.log(response.answer);
    }
  } catch (err: any) {
    console.error("Execution failed:", err.message);
  }
}

declare const require: any;
declare const module: any;

if (typeof require !== "undefined" && typeof module !== "undefined" && require.main === module) {
  runExample();
}

