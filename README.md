# notebooklm-py
<p align="left">
  <img src="https://raw.githubusercontent.com/teng-lin/notebooklm-py/main/notebooklm-py.png" alt="notebooklm-py logo" width="128">
</p>

**Uma Habilidade Completa do Google Gemini Notebook e API Python Não Oficial.** Acesso programático total aos recursos do NotebookLM — incluindo capacidades que a interface web não expõe — via Python, CLI e agentes de IA como Claude Code, Codex e OpenClaw.

> **Nota (Julho 2026):** O Google renomeou **NotebookLM** para **[Gemini Notebook](https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/)**. Continua sendo o mesmo produto independente (agora também acessível dentro do app Gemini), links existentes redirecionam automaticamente, e esta biblioteca continua funcionando com o mesmo serviço subjacente. O pacote mantém o nome `notebooklm-py`.

[![PyPI version](https://img.shields.io/pypi/v/notebooklm-py.svg)](https://pypi.org/project/notebooklm-py/)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://pypi.org/project/notebooklm-py/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/teng-lin/notebooklm-py/actions/workflows/test.yml/badge.svg)](https://github.com/teng-lin/notebooklm-py/actions/workflows/test.yml)
<p>
  <a href="https://trendshift.io/repositories/19116" target="_blank"><img src="https://trendshift.io/api/badge/repositories/19116" alt="teng-lin%2Fnotebooklm-py | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
</p>

**Código & Desenvolvimento**: <https://github.com/teng-lin/notebooklm-py>

> **⚠️ Biblioteca Não Oficial - Use por Sua Conta e Risco**
>
> Esta biblioteca usa **APIs não documentadas do Google** que podem mudar sem aviso prévio.
>
> - **Não afiliada ao Google** - Este é um projeto da comunidade
> - **APIs podem quebrar** - O Google pode alterar endpoints internos a qualquer momento
> - **Limites de taxa se aplicam** - Uso intensivo pode ser limitado
>
> Ideal para protótipos, pesquisa e projetos pessoais. Veja [Solução de Problemas](docs/troubleshooting.md) para dicas de depuração.

## O Que Você Pode Construir

🤖 **Ferramentas para Agentes de IA** - Integre o NotebookLM no Claude Code, Codex e outros agentes LLM. Inclui uma [habilidade NotebookLM](SKILL.md) raiz para descoberta via GitHub e `npx skills add`, suporte local a `notebooklm skill install` para Claude Code e diretórios de habilidade `.agents`, e orientações específicas para Codex em [`AGENTS.md`](AGENTS.md).

📚 **Automação de Pesquisa** - Importe fontes em massa (URLs, PDFs, YouTube, Google Drive), execute consultas de pesquisa web/Drive com importação automática e extraia insights programaticamente. Construa pipelines de pesquisa repetíveis.

🎙️ **Geração de Conteúdo** - Gere Audio Overviews (podcasts), vídeos, apresentações de slides, quizzes, flashcards, infográficos, tabelas de dados, mapas mentais e guias de estudo. Controle total sobre formatos, estilos e saída.

📥 **Downloads & Exportação** - Baixe todos os artefatos gerados localmente (MP3, MP4, PDF, PNG, CSV, JSON, Markdown). Exporte para Google Docs/Sheets. **Recursos que a interface web não oferece**: downloads em lote, exportação de quiz/flashcard em múltiplos formatos, extração de mapa mental como JSON.

## Casos de Uso e Receitas

NotebookLM é um mecanismo **fundamentado**: o Gemini faz a leitura pesada e responde a partir das *suas* fontes com citações. O padrão vencedor é deixá-lo fazer a análise cara enquanto seu agente (Claude Code, Codex, …) orquestra e cuida da última milha — usando o NotebookLM como uma **camada de síntese de token zero + memória que um agente dirige em um loop**, e extraindo artefatos estruturados **para fora** em massa e em formatos mais ricos e scriptáveis. Receitas que as pessoas constroem em cima desta biblioteca, agrupadas pelo que usam o NotebookLM *como*:

**Gaste menos tokens** — deixe o NotebookLM fazer o pensamento caro:

- **🪙 Descarga de pesquisa com token zero** — Jogue 30 documentos em um notebook, deixe o Gemini fazer a análise pesada, e faça seu agente gastar tokens apenas no polimento final. O agente apenas orquestra (`create` → `source add` → `ask`); o raciocínio acontece no lado do servidor. *Na natureza: [um guia de quatro fluxos para impedir que o Claude Code queime tokens no NotebookLM](https://x.com/hooeem/status/2042293751805329445).*
- **🧠 Destilação de conhecimento → uma habilidade permanente** — Execute [Pesquisa Profunda](docs/cli-reference.md#source-add-research) (`source add-research "seu tópico" --mode deep`) ou carregue um corpus de documentos, deixe o Gemini do NotebookLM condensar, e incorpore o resultado em um `SKILL.md` que seu agente carrega na inicialização — **construa uma vez, reutilize com zero tokens de runtime ou chamadas de rede**, versionado no git e imune à deriva da UI. Um especialista de domínio empacotado sem curadoria manual de fontes. (Despejar docs brutos em uma habilidade achata a hierarquia; o NotebookLM condensando primeiro é o que funciona.)
- **✅ Habilidades auto-validadas** — Faça o NotebookLM gerar o *conjunto de avaliação* — um quiz direto das suas fontes — para avaliar uma habilidade de agente contra a verdade fundamental em vez de perguntas de teste que você viesaria. Construa a habilidade, execute contra as avaliações escritas pelo NotebookLM, itere até passar. *Na natureza: [uma habilidade que marcou 4/10 na primeira passada e 10/10 após uma iteração, avaliada por um quiz gerado pelo NotebookLM](https://x.com/nurijanian/status/2037136490157986277).*

**Dê memória ao seu agente** — recall persistente e fundamentado:

- **💾 Memória persistente entre sessões** — Mantenha um notebook "Cérebro Mestre"; um passo de fechamento anexa as decisões e correções de cada sessão como notas (`note create` / `ask --save-as-note`), e uma linha no seu `CLAUDE.md` consulta isso (`ask`) no início da próxima sessão. Armazenamento e recall vivem na infraestrutura do Google.
- **🧩 Memória fundamentada para agentes de codificação** — Exponha um notebook dos seus docs/RFCs/arquitetura internos via [servidor MCP](docs/mcp-guide.md) (ou `ask` simples) para que um agente responda a partir do *seu* código com citações em vez de palpites plausíveis — uma alternativa de infraestrutura zero para montar seu próprio banco de dados vetorial e pipeline de embeddings. *Na natureza: [transformando um notebook no "cérebro do projeto" fundamentado em fontes que um agente de codificação consulta antes de escrever código](https://medium.com/@pradeep00271/every-software-project-needs-a-project-brain-5cbc33917160).*
- **🪞 Consulte suas próprias notas / diário** — Carregue anos de notas diárias, registros de reuniões ou um diário e `ask` por respostas **citadas** *através da sua própria história* — surfaced padrões de longo prazo que uma busca por palavras-chave não consegue (ex.: um resumo semanal sintetizado a partir de 282 notas diárias, cada afirmação vinculada à entrada de onde veio). *Na natureza: [conversando com um ano de notas diárias como base de conhecimento citada](https://artemxtech.substack.com/p/notebooklm-has-a-knowledge-graph).*

**Transforme suas fontes em respostas e artefatos** — respostas citadas, mídia gerada e exportações:

- **📞 Base de conhecimento fundamentada / oráculo de solução de problemas (RAG)** — Carregue docs de produto, FAQs, RFCs e tickets passados, depois `ask --json` por respostas **fundamentadas nas fontes e citadas** para suporte, plantão ou Q&A interno. Ou faça um agente apontar para os docs de uma ferramenta em movimento rápido — mais do que o agente pode manter em contexto — como um **oráculo de solução de problemas** que consulta no momento em que encontra um erro. *Na natureza: [OpenClaw dirigiu a biblioteca para raspar todas as 524 páginas de `docs.openclaw.ai`, deduplicar traduções duplicadas e auditar para 269 fontes limpas (faltando/extra/duplicado = 0)](https://x.com/onenewbite/status/2024819940327379286).*
- **🔁 Reproposição de conteúdo multi-formato** — Um conjunto de fontes, todos os formatos: `generate audio` (podcast), `generate video`, `generate slide-deck`, mais um rascunho de blog `generate report`, `generate quiz` e `generate flashcards` — expanda um único notebook através de canais.
- **📤 Exportações em massa e scriptáveis** — Extraia mapas mentais como JSON, flashcards/quizzes como JSON/Markdown/HTML, tabelas de dados como CSV e relatórios como Markdown — **em massa, para arquivos locais, direto para Anki, sua ferramenta de mapeamento mental ou um repositório** (`download <tipo>` / `download <tipo> --all`). A metade programática de "obter dados *para fora*" da biblioteca, não apenas "colocar fontes para dentro".
- **🕸️ Sincronização com Obsidian / grafo de conhecimento** — Execute a CLI a partir da raiz do seu vault para que artefatos baixados (relatórios, JSON de mapa mental, transcrições) caiam como arquivos no seu grafo de conhecimento; habilidades da comunidade construídas nesta biblioteca até resolvem marcadores de citação do NotebookLM em `[[wikilinks]]` do Obsidian. Combine com uma visão geral de podcast para um digesto de áudio das suas notas. *Na natureza: ["Claude Code + NotebookLM + Obsidian = MODO DEUS"](https://www.youtube.com/watch?v=kU3qYQ7ACMA).*

**Execute sem supervisão, em escala ou em movimento** — agendado, headless e remoto:

- **🚨 Gerador de runbook de incidente** — Em um alerta, crie um notebook com os docs relevantes, faça perguntas diagnósticas direcionadas e gere um relatório de briefing-doc (`generate report --format briefing-doc --wait`, depois `download report`) como um runbook automatizado.
- **📚 Construtor de currículo / conjunto de estudos** — Raspe uma ementa ou roadmap de desenvolvedor, crie um notebook por tópico (com ritmo deliberado para evitar limites de taxa) e gere em massa podcasts, quizzes e flashcards para cada.
- **📰 Briefings de áudio agendados** — Combine `auth refresh --quiet` (cron/launchd/systemd) com `generate audio` para publicar um briefing personalizado fresco em um feed de podcast em uma agenda.
- **📱 NotebookLM do seu celular, dirigido por agente** — Auto-hospede o [conector MCP remoto](docs/mcp-guide.md#remote-deployment-docker--a-tunnel) atrás de um túnel Cloudflare/Tailscale e adicione-o como um conector personalizado **na web** (Conectores claude.ai, ou ChatGPT com Modo Desenvolvedor). Depois dirija o conjunto completo de ferramentas — pesquisa profunda, ingestão de fontes, geração de estúdio, Q&A citado — a partir do **app móvel claude.ai** em movimento (conectores MCP do ChatGPT são apenas web), encadeado com suas outras ferramentas MCP, em vez de pular entre apps.

Estes combinam primitivas ordinárias da biblioteca — veja a [Referência da CLI](docs/cli-reference.md) e a [API Python](docs/python-api.md). A cola do lado do agente (habilidades, agendamento, layout do vault) vive na sua própria configuração, não neste pacote. Contagens de fontes por notebook dependem do nível da sua conta Google — divida entre notebooks se atingir um limite.

**Novo aqui?** Comece com um passeio: [Claude Code + NotebookLM = TRAPAÇA (vídeo)](https://www.youtube.com/watch?v=usTeU4Uh0iM) · [5 demos + 50 casos de uso, com prompts](https://aiblewmymind.substack.com/p/notebooklm-claude-code-use-cases).

## Ways to Use

| Method | Best For |
|--------|----------|
| **Python API** | Application integration, async workflows, custom pipelines |
| **CLI** | Shell scripts, quick tasks, CI/CD automation |
| **MCP Server** | Claude Desktop/Code, Codex, etc. — locally via stdio, or as a self-hosted remote connector (behind a Cloudflare/Tailscale tunnel) reachable from claude.ai and ChatGPT, mobile included. |
| **REST Server** | Local automation over guarded HTTP routes without spawning a CLI process per call |
| **Agent Integration** | Claude Code, Codex, LLM agents, natural language automation |

### API backends

The default backend is the established Web (`batchexecute`) transport. This
release also provides an opt-in Android backend that uses NotebookLM's mobile
gRPC service and bearer authentication. Select it for the CLI with
`--backend android` (or `NOTEBOOKLM_BACKEND=android`), or for the Python API
with `NotebookLMClient.from_storage(backend="android")` / `NotebookLMClient(...,
backend="android")`.

Install the Android runtime explicitly; it is intentionally not included in
the `all` extra:

```bash
pip install "notebooklm-py[android,browser]"
notebooklm login --master-token --account you@example.com
notebooklm --backend android list --json
```

Android reads `master_token.json` from the selected profile and mints
short-lived mobile bearer tokens as needed, so typed namespace calls do not
depend on a browser-cookie session, Web build labels, or Web RPC IDs. All
eleven public namespaces are available without falling back to the Web
transport. Because the durable master token is a powerful full-account
credential, use a dedicated account and protect the profile carefully. See the
[Android backend guide](docs/android/README.md) for setup and protocol details.

## Features

### Complete NotebookLM Coverage

| Category | Capabilities |
|----------|--------------|
| **Notebooks** | Create, copy (including sources and Studio artifacts), list, rename, delete |
| **Sources** | URLs, YouTube, files (PDF, text, Markdown, Word, EPUB, audio, video, images), Google Drive, pasted text; refresh, get guide/fulltext |
| **Chat** | Questions, conversation history, custom personas, suggested starter prompts |
| **Notes** | Create, list, rename, delete, save chat answers, save conversation history |
| **Source Labels** | AI-generated or manual topic labels; add/remove source membership; filter sources by label |
| **Research** | Web and Drive research agents (fast/deep modes) with auto-import |
| **Sharing** | Public/private links, user permissions (viewer/editor), view level control |

### Content Generation (All Artifact Types)

| Type | Options | Download Format |
|------|---------|-----------------|
| **Audio Overview** | 4 formats (deep-dive, brief, critique, debate), 3 lengths, 50+ languages | MP3 |
| **Video Overview** | 4 formats (explainer, brief, cinematic, short), 8 visual styles (+ auto/custom), plus a dedicated `cinematic-video` CLI alias | MP4 |
| **Slide Deck** | Detailed or presenter format, adjustable length; individual slide revision | PDF, PPTX |
| **Infographic** | 3 orientations, 3 detail levels | PNG |
| **Quiz** | Configurable quantity and difficulty | JSON, Markdown, HTML |
| **Flashcards** | Configurable quantity and difficulty | JSON, Markdown, HTML |
| **Report** | Briefing doc, study guide, blog post, or custom prompt | Markdown |
| **Data Table** | Custom structure via natural language | CSV |
| **Mind Map** | Hierarchical node tree — **two kinds**: note-backed JSON or the newer interactive studio map (`--kind` / `MindMapKind`) | JSON |

### Beyond the Web UI

Programmatic, batch, and local-file capabilities the API/CLI make easy — several in richer formats, or at a scale, than clicking through the web app:

- **Batch downloads** - Download all artifacts of a type at once
- **Quiz/Flashcard export** - Get structured JSON, Markdown, or HTML files
- **Mind map data extraction** - Export hierarchical JSON for visualization tools
- **Data table CSV export** - Download structured tables as spreadsheets
- **Slide deck as PPTX or PDF** - Download editable PowerPoint or PDF files
- **Slide revision** - Modify individual slides with natural-language prompts
- **Report template customization** - Append extra instructions to built-in format templates
- **Save chat history to notes** - Persist a whole Q&A conversation (not just a single answer) as a notebook note
- **Source fulltext access** - Retrieve the indexed text content of any source
- **Programmatic sharing** - Manage permissions without the UI

## Installation

The full install guide — six personas (agent, end-user, library, headless, contributor, power-user), optional extras matrix, platform notes — lives in **[docs/installation.md](docs/installation.md)**.

**Quickest start** (CLI users and AI agents) — install the CLI with `uv tool` (recommended) or `pipx`:

```bash
uv tool install "notebooklm-py[browser]"   # or: pipx install "notebooklm-py[browser]"
notebooklm login                           # first run auto-downloads Chromium (~170 MB), then Google sign-in
notebooklm auth check --test --json        # verify: expect "status": "ok"
```

**Why `uv tool` / `pipx`?** They install the CLI into its own isolated environment and put `notebooklm` on your `PATH` — no dependency clashes with other tools, a one-line upgrade (`uv tool upgrade notebooklm-py`) or uninstall, and, crucially, they work on modern macOS (Homebrew Python) and Debian/Ubuntu where a system-wide `pip install` is blocked with `error: externally-managed-environment` ([PEP 668](https://peps.python.org/pep-0668/)). No `uv` yet? `curl -LsSf https://astral.sh/uv/install.sh | sh` (or `brew install uv` / `winget install astral-sh.uv`).

**Prefer plain `pip`?** It works the same **inside a virtualenv** (and directly on Windows, where Python isn't externally-managed):

```bash
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install "notebooklm-py[browser]"
```

**As a library** (embedded in your app — no Playwright, no Chromium):

```bash
uv add notebooklm-py                    # or, inside a virtualenv: pip install notebooklm-py
```

If `playwright install chromium` fails on Linux with `TypeError: onExit is not a function`, see the [Linux workaround](docs/troubleshooting.md#linux). **Contributors:** see [CONTRIBUTING.md](CONTRIBUTING.md).


### Authentication & Access

Flexible auth for local dev, headless servers, and multi-tenant setups:

- **Three ways to get cookies** - Interactive Playwright login (default), import from an already-signed-in browser (`login --browser-cookies chrome`, no Playwright), or a durable **master token**.
- **Master-token auth** - Mints fresh web cookies **on demand** with no per-session browser (`login --master-token --account you@example.com`), so it self-heals expired sessions unattended — the auth model for servers, CI, and the remote MCP connector (claude.ai / ChatGPT).
- **Multi-account profiles** - Switch between Google accounts without re-authenticating.

### Agent Setup

**Option 1 — CLI install**:

```bash
notebooklm skill install
```

Installs the skill into `~/.claude/skills/notebooklm` and `~/.agents/skills/notebooklm`.

**Option 2 — `npx` install** (via the open skills ecosystem):

```bash
npx skills add teng-lin/notebooklm-py
```

Fetches the canonical [SKILL.md](SKILL.md) directly from GitHub.

## Quick Start

<p align="center">
  <a href="https://asciinema.org/a/767284" target="_blank"><img src="https://asciinema.org/a/767284.svg" width="600" /></a>
  <br>
  <em>16-minute session compressed to 30 seconds</em>
</p>

### CLI

```bash
# 1. Authenticate (opens browser)
notebooklm login
# Or use Microsoft Edge (for orgs that require Edge for SSO)
# notebooklm login --browser msedge
# Or reuse cookies from an already-logged-in browser session
# notebooklm login --browser-cookies chrome
# notebooklm login --browser-cookies 'chrome::Profile 1'  # one Chromium profile
# (combine with --profile to populate a specific profile;
#  use --account / --all-accounts after auth inspect when several
#  Google accounts are signed in)

# 2. Create a notebook and add sources
notebooklm create "My Research"
notebooklm use <notebook_id>
notebooklm source add "https://en.wikipedia.org/wiki/Artificial_intelligence"
notebooklm source add "./paper.pdf"

# 3. Chat with your sources
notebooklm ask "What are the key themes?"
notebooklm ask --prompt-file ./long_question.txt  # Read question from file

# 4. Generate content (use --prompt-file for long prompts)
notebooklm generate audio "make it engaging" --wait
notebooklm generate video --style whiteboard --wait
notebooklm generate cinematic-video "documentary-style summary" --wait
notebooklm generate quiz --difficulty hard
notebooklm generate flashcards --quantity more
notebooklm generate slide-deck
notebooklm generate infographic --orientation portrait
notebooklm generate mind-map                       # interactive studio map (default); --kind note-backed for the JSON tree
notebooklm generate data-table "compare key concepts"

# 5. Download artifacts
notebooklm download audio ./podcast.m4a
notebooklm download video ./overview.mp4
notebooklm download cinematic-video ./documentary.mp4
notebooklm download quiz --format markdown ./quiz.md
notebooklm download flashcards --format json ./cards.json
notebooklm download slide-deck ./slides.pdf
notebooklm download infographic ./infographic.png
notebooklm download mind-map ./mindmap.json
notebooklm download data-table ./data.csv
```

Other useful CLI commands:

```bash
notebooklm auth check --test         # Diagnose auth/cookie issues
notebooklm auth refresh --quiet      # One-shot cookie keepalive (for cron / launchd / systemd)
notebooklm auth refresh --browser-cookies chrome  # Re-extract and repair account routing
notebooklm auth inspect --browser 'chrome::Profile 1'  # Preview one Chromium profile
notebooklm agent show codex          # Print bundled Codex instructions
notebooklm agent show claude         # Print bundled Claude Code skill template
notebooklm language list             # List supported output languages
notebooklm metadata --json           # Export notebook metadata and sources
notebooklm share status              # Inspect sharing state
notebooklm source add-research "AI" --import-all  # web research + import found sources
notebooklm skill status              # Check local agent skill installation
notebooklm profile list              # List all Google account profiles
notebooklm profile switch work       # Switch active account profile
```

Use `--prompt-file PATH` with `ask`, prompt-based `generate` commands, and `source add-research` when the text is too long for the shell command line. This reads prompt/query text from a file and is separate from `source add ./file.pdf`, which still uploads that file as a NotebookLM source.

### Python API

```python
import asyncio
from notebooklm import NotebookLMClient, MindMapKind


async def main():
    async with NotebookLMClient.from_storage() as client:
        # Create notebook and add sources
        nb = await client.notebooks.create("Research")
        await client.sources.add_url(nb.id, "https://example.com", wait=True)

        # Chat with your sources
        result = await client.chat.ask(nb.id, "Summarize this")
        print(result.answer)

        # Generate content (podcast, video, quiz, etc.)
        status = await client.artifacts.generate_audio(nb.id, instructions="make it fun")
        await client.artifacts.wait_for_completion(nb.id, status.task_id)
        await client.artifacts.download_audio(nb.id, "podcast.m4a")

        # Generate quiz and download as JSON
        status = await client.artifacts.generate_quiz(nb.id)
        await client.artifacts.wait_for_completion(nb.id, status.task_id)
        await client.artifacts.download_quiz(nb.id, "quiz.json", output_format="json")

        # Generate a mind map via the unified client.mind_maps API (issue #1256) —
        # two kinds: the newer MindMapKind.INTERACTIVE studio map (shown; polled to
        # completion by default) or MindMapKind.NOTE_BACKED JSON. Both export via:
        mm = await client.mind_maps.generate(nb.id, kind=MindMapKind.INTERACTIVE)
        await client.artifacts.download_mind_map(nb.id, "mindmap.json", mm.id)


asyncio.run(main())
```

## Documentation

- **[Installation](docs/installation.md)** - Environment, extras, login, and deployment setup
- **[Android Backend](docs/android/README.md)** - Mobile gRPC setup, credentials, and protocol notes
- **[CLI Reference](docs/cli-reference.md)** - Complete command documentation
- **[Python API](docs/python-api.md)** - Full API reference
- **[MCP Guide](docs/mcp-guide.md)** - MCP server setup, transports, and tool reference
- **[REST API Server](docs/installation.md#rest-api-server)** - Experimental localhost FastAPI server
- **[Configuration](docs/configuration.md)** - Storage and settings
- **[Quota & Tier Limits](docs/quota-limits.md)** - Per-tier notebook/source/studio limits and how they map to `AccountLimits.tier`
- **[Release Guide](docs/releasing.md)** - Release checklist and packaging verification
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions
- **[Credential Security](docs/security.md)** - Secret handling and trust boundaries
- **[API Stability](docs/stability.md)** - Versioning policy and stability guarantees
- **[Upgrading to v0.8.0](docs/upgrading-to-0.8.0.md)** - Breaking-change migration guide for the v0.8.0 error-and-return contract

### For Contributors

- **[Architecture](docs/architecture.md)** - Architectural overview and design principles
- **[Development Guide](docs/development.md)** - Architecture, testing, and releasing
- **[RPC Development](docs/rpc-development.md)** - Protocol capture and debugging
- **[RPC Reference](docs/rpc-reference.md)** - Payload structures
- **[Changelog](CHANGELOG.md)** - Version history and release notes
- **[Security](SECURITY.md)** - Security policy and credential handling

## License

MIT License. See [LICENSE](LICENSE) for details.
