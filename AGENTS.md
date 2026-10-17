# Repository Guidelines

**Status:** Active
**Last Updated:** 2026-09-07

## Structure & Modules

`src/notebooklm/` contains the async client (`client.py`) and typed exports (`__init__.py`).
- **Internal:** `_*.py` and `_*/` (`_app/`, `_auth/`, `_runtime/`, `_sources.py`, `_artifacts.py`).
- **Adapters & Wire:** `cli/` (Click), `mcp/` (FastMCP), `server/` (FastAPI), `rpc/` (batchexecute RPC facade), `_android/` (gRPC session & codecs).
- **Tests & Data:** `tests/unit/`, `tests/integration/` (VCR), `tests/server/`, `tests/e2e/`, `tests/_guardrails/`, `tests/_fault_server/`, `tests/cassettes/` (`web/`, `android/`). Examples in `examples/`, tools in `scripts/`.

## Development Commands

Canonical contributor install (full guide: [docs/installation.md](docs/installation.md)):

```bash
uv sync --frozen --extra browser --extra dev --extra markdown \
        --extra mcp --extra server --extra impersonate
source .venv/bin/activate
uv run playwright install chromium

uv run pytest
uv run pytest -n auto --dist loadgroup  # faster parallel run
uv run ruff check .
uv run ruff format --check .
uv run mypy src/notebooklm
```

## Conventions & Testing

- **Style:** Python 3.10+, 4 spaces, double quotes, 100-char line limit (Ruff enforced).
- **Naming:** `snake_case` modules and tests (`test_<behavior>.py`). Preserve public/internal split (`_*.py`).
- **Testing:** Unit logic in `tests/unit/`, REST in `tests/server/`, VCR replay in `tests/integration/` (record: `NOTEBOOKLM_VCR_RECORD=1 uv run pytest tests/integration/ -v`), e2e in `tests/e2e/`. 90% coverage gate.
- **Commits/PRs:** Conventional commits (`feat(cli):`, `fix:`, `refactor:`, `style:`). Link issues and report test runs.

## Parallel & Autonomous Agents

- Prefer `--json` output and pass explicit notebook IDs instead of relying on stateful `notebooklm use`.
- Isolate concurrent runs with `NOTEBOOKLM_PROFILE=agent-<id>` (`~/.notebooklm/profiles/<name>/`) or `NOTEBOOKLM_HOME=/tmp/agent-<id>`.
- In headless environments, authenticate with `notebooklm login --browser-cookies <browser>` (requires `pip install "notebooklm-py[cookies]"`).


---

# Reversa

> Framework de Engenharia Reversa instalado neste projeto.

## Como usar

Use o fluxo adequado no chat:

- `reversa` — descobrir e documentar um sistema existente
- `reversa-new` — criar PRD e specs para um projeto novo
- `reversa-forward` — implementar ou evoluir código a partir das specs
- `reversa-migrate` — planejar a migração de um sistema legado
- `reversa-docs` — gerar o mini-site visual da documentação
- `reversa-agents-help` — consultar o catálogo completo de agentes

## Comportamento ao ativar

Quando o usuário digitar `reversa` sozinho em uma mensagem:

1. Ative o skill `reversa` disponível em `.agents/skills/reversa/SKILL.md`
2. Leia o SKILL.md na íntegra e siga exatamente as instruções do Reversa

## Regra não-negociável

Por padrão, nunca apague, modifique ou sobrescreva arquivos pré-existentes do projeto legado:
o Reversa escreve apenas em `.reversa/`, `_reversa_sdd/`, `_reversa_docs/`, `_reversa_forward/`, `_reversa_bugs/` e `_reversa_refactor/`.
A única exceção é a política configurável abaixo, controlada exclusivamente pelo usuário.

Antes de criar, modificar ou apagar qualquer arquivo fora das pastas próprias do Reversa, leia `.reversa/reversa-config.json` e obedeça ao resultado:

- Arquivo ausente, JSON inválido ou campo com tipo errado: trate como `allowLegacyEdits: false` (falha segura, nenhuma escrita fora das pastas do Reversa).
- `allowLegacyEdits: false`: recuse a escrita, informando o caminho recusado, o estado atual da config e o que o usuário deve editar para liberar.
- `allowLegacyEdits: true` com `allowedPaths` não vazio: escreva apenas em caminhos que casem com algum glob da lista (globs relativos à raiz do projeto, com `/`, suportando `*` e `**`).
- `allowLegacyEdits: true` com `allowedPaths` vazio ou ausente: projeto liberado; avise uma vez por sessão que a liberação é irrestrita.

Nunca crie nem edite `.reversa/reversa-config.json` por iniciativa própria: pedido na conversa não é liberação implícita, alterações nesse arquivo são ato exclusivo do usuário.
