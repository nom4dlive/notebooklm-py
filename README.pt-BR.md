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

NotebookLM é um mecanismo **fundamentado**: o Gemini faz a leitura pesada e responde a partir das *suas* fontes com citações. O padrão vencedor é deixá-lo fazer a análise cara enquanto seu agente (Claude Code, Codex, …) orquestra e cuida da última milha — usando o NotebookLM como uma **camada de síntese de token zero + memória que um agente dirige em um loop**, e extraindo artefatos estruturados **para fora** em massa e em formatos mais ricos e scriptáveis.

### 🪙 Gaste Menos Tokens — Deixe o NotebookLM Fazer o Pensamento Caro

- **Descarga de pesquisa com token zero** — Jogue 30 documentos em um notebook, deixe o Gemini fazer a análise pesada, e faça seu agente gastar tokens apenas no polimento final. O agente apenas orquestra (`create` → `source add` → `ask`); o raciocínio acontece no lado do servidor. *[Na natureza: guia de quatro fluxos para impedir que o Claude Code queime tokens](https://x.com/hooeem/status/2042293751805329445).*

- **Destilação de conhecimento → habilidade permanente** — Execute [Pesquisa Profunda](docs/cli-reference.md#source-add-research) ou carregue um corpus de documentos, deixe o Gemini condensar, e incorpore o resultado em um `SKILL.md` que seu agente carrega na inicialização — **construa uma vez, reutilize com zero tokens de runtime**, versionado no git e imune à deriva da UI.

- **Habilidades auto-validadas** — Faça o NotebookLM gerar um quiz direto das suas fontes para avaliar uma habilidade de agente contra a verdade fundamental. *[Na natureza: habilidade que marcou 4/10 e depois 10/10 após iteração](https://x.com/nurijanian/status/2037136490157986277).*

### 💾 Dê Memória ao Seu Agente

- **Memória persistente entre sessões** — Mantenha um notebook "Cérebro Mestre"; um passo de fechamento anexa decisões e correções como notas, consultadas no início da próxima sessão.

- **Memória fundamentada para agentes de codificação** — Exponha docs/RFCs/arquitetura internos via [servidor MCP](docs/mcp-guide.md) para que um agente responda a partir do *seu* código com citações — alternativa zero-infra a banco de dados vetorial. *[Na natureza: "cérebro do projeto" que agentes consultam antes de codificar](https://medium.com/@pradeep00271/every-software-project-needs-a-project-brain-5cbc33917160).*

- **Consulte suas próprias notas / diário** — Carregue anos de notas diárias e `ask` por respostas **citadas** através da sua própria história. *[Na natureza: conversando com um ano de notas diárias](https://artemxtech.substack.com/p/notebooklm-has-a-knowledge-graph).*

### 📞 Transforme Fontes em Respostas e Artefatos

- **Base de conhecimento fundamentada (RAG)** — Carregue docs de produto, FAQs, RFCs e tickets, depois `ask --json` por respostas **fundamentadas e citadas**. *[Na natureza: OpenClaw raspou 524 páginas e auditou para 269 fontes limpas](https://x.com/onenewbite/status/2024819940327379286).*

- **Reproposição multi-formato** — Um conjunto de fontes, todos os formatos: podcast, vídeo, slides, relatório, quiz, flashcards.

- **Exportações em massa** — Mapas mentais como JSON, quizzes como JSON/Markdown/HTML, tabelas como CSV, relatórios como Markdown — **em massa, para arquivos locais**.

- **Sincronização com Obsidian** — Artefatos baixados caem como arquivos no seu grafo de conhecimento; habilidades da comunidade resolvem citações em `[[wikilinks]]`. *[Na natureza: "Claude Code + NotebookLM + Obsidian = MODO DEUS"](https://www.youtube.com/watch?v=kU3qYQ7ACMA).*

### 🚨 Execute Sem Supervisão, em Escala ou em Movimento

- **Gerador de runbook de incidente** — Em um alerta, crie notebook com docs relevantes, faça perguntas diagnósticas e gere briefing-doc automatizado.

- **Construtor de currículo / estudos** — Raspe ementa, crie notebook por tópico, gere em massa podcasts, quizzes e flashcards.

- **Briefings de áudio agendados** — Combine `auth refresh --quiet` (cron/systemd) com `generate audio` para publicar briefing personalizado em feed de podcast.

- **NotebookLM do celular, dirigido por agente** — Auto-hospede [conector MCP remoto](docs/mcp-guide.md#remote-deployment-docker--a-tunnel) atrás de túnel Cloudflare/Tailscale e adicione como conector personalizado no claude.ai mobile.

**Novo aqui?** Comece com: [Claude Code + NotebookLM = TRAPAÇA (vídeo)](https://www.youtube.com/watch?v=usTeU4Uh0iM) · [5 demos + 50 casos de uso](https://aiblewmymind.substack.com/p/notebooklm-claude-code-use-cases).

## Formas de Uso

| Método | Melhor Para |
|--------|----------|
| **API Python** | Integração em aplicações, fluxos assíncronos, pipelines personalizados |
| **CLI** | Scripts shell, tarefas rápidas, automação CI/CD |
| **Servidor MCP** | Claude Desktop/Code, Codex — local via stdio, ou conector remoto (túnel Cloudflare/Tailscale) acessível via claude.ai e ChatGPT, inclusive mobile |
| **Servidor REST** | Automação local sobre rotas HTTP protegidas sem invocar CLI por chamada |
| **Integração com Agentes** | Claude Code, Codex, agentes LLM, automação por linguagem natural |

## Recursos Principais

### Cobertura Completa do NotebookLM

| Categoria | Capacidades |
|----------|--------------|
| **Notebooks** | Criar, listar, renomear, excluir |
| **Fontes** | URLs, YouTube, arquivos (PDF, texto, Markdown, Word, EPUB, áudio, vídeo, imagens), Google Drive, texto colado; atualizar, obter guia/texto completo |
| **Chat** | Perguntas, histórico de conversação, personas personalizadas, prompts iniciais sugeridos |
| **Notas** | Criar, listar, renomear, excluir, salvar respostas de chat, salvar histórico de conversação |
| **Rótulos de Fonte** | Rótulos de tópico gerados por IA ou manuais; adicionar/remover associação; filtrar por rótulo |
| **Pesquisa** | Agentes de pesquisa web e Drive (modos rápido/profundo) com importação automática |
| **Compartilhamento** | Links públicos/privados, permissões (visualizador/editor), controle de nível de visualização |

### Geração de Conteúdo (Todos os Tipos de Artefatos)

| Tipo | Opções | Formato de Download |
|------|---------|-----------------|
| **Audio Overview** | 4 formatos (deep-dive, brief, critique, debate), 3 durações, 50+ idiomas | MP3 |
| **Video Overview** | 4 formatos (explainer, brief, cinematic, short), 8 estilos visuais | MP4 |
| **Slide Deck** | Detalhado ou apresentador, duração ajustável; revisão individual de slides | PDF, PPTX |
| **Infográfico** | 3 orientações, 3 níveis de detalhe | PNG |
| **Quiz** | Quantidade e dificuldade configuráveis | JSON, Markdown, HTML |
| **Flashcards** | Quantidade e dificuldade configuráveis | JSON, Markdown, HTML |
| **Relatório** | Briefing doc, guia de estudo, post de blog, prompt personalizado | Markdown |
| **Tabela de Dados** | Estrutura personalizada via linguagem natural | CSV |
| **Mapa Mental** | Árvore hierárquica — dois tipos: JSON baseado em notas ou mapa interativo de estúdio | JSON |

### Além da Interface Web

- **Downloads em lote** de todos os artefatos de um tipo
- **Exportação de Quiz/Flashcard** em JSON, Markdown ou HTML
- **Extração de mapa mental** como JSON hierárquico
- **Tabelas de dados** como CSV
- **Slides** como PPTX editável ou PDF
- **Revisão de slides individuais** com prompts em linguagem natural
- **Personalização de relatórios** com instruções extras
- **Salvar histórico completo de chat** como nota
- **Acesso ao texto completo** de qualquer fonte
- **Compartilhamento programático** sem interface

## Instalação

Guia completo em **[docs/installation.md](docs/installation.md)** (seis personas, matriz de extras, notas de plataforma).

### Início Rápido

```bash
# Recomendado: uv tool ou pipx (ambiente isolado, sem conflitos)
uv tool install "notebooklm-py[browser]"   # ou: pipx install "notebooklm-py[browser]"
notebooklm login                           # baixa Chromium (~170 MB), login no Google
notebooklm auth check --test --json        # verifique: espere "status": "ok"
```

**Por que `uv tool` / `pipx`?** Ambiente isolado, `notebooklm` no PATH, upgrade/desinstalação com uma linha, funciona em macOS Homebrew e Debian/Ubuntu (evita erro PEP 668).

**Prefere `pip`?** Funciona dentro de virtualenv:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install "notebooklm-py[browser]"
```

**Como biblioteca** (sem Playwright/Chromium):

```bash
uv add notebooklm-py                    # ou: pip install notebooklm-py
```

Problemas no Linux? Veja [solução](docs/troubleshooting.md#linux). **Contribuidores:** [CONTRIBUTING.md](CONTRIBUTING.md).

### Autenticação & Acesso

- **Três maneiras de obter cookies** — Login Playwright (padrão), importar de navegador já logado (`login --browser-cookies chrome`), ou **token mestre** durável.
- **Token mestre** — Cria cookies sob demanda sem navegador por sessão (`login --master-token --account voce@exemplo.com`), recupera sessões expiradas automaticamente — ideal para servidores, CI e conector MCP remoto.
- **Múltiplos perfis** — Troque entre contas Google sem re-autenticar.

### Configuração para Agentes

**Opção 1 — Instalação via CLI:**

```bash
notebooklm skill install
```

Instala habilidade em `~/.claude/skills/notebooklm` e `~/.agents/skills/notebooklm`.

**Opção 2 — Via `npx`:**

```bash
npx skills add teng-lin/notebooklm-py
```

Busca [SKILL.md](SKILL.md) diretamente do GitHub.

## Início Rápido

<p align="center">
  <a href="https://asciinema.org/a/767284" target="_blank"><img src="https://asciinema.org/a/767284.svg" width="600" /></a>
  <br>
  <em>Sessão de 16 minutos condensada em 30 segundos</em>
</p>

### CLI

```bash
# 1. Autenticar (abre navegador)
notebooklm login
# Ou usar Microsoft Edge (para orgs que exigem Edge para SSO)
# notebooklm login --browser msedge
# Ou reutilizar cookies de sessão já logada
# notebooklm login --browser-cookies chrome
# notebooklm login --browser-cookies 'chrome::Profile 1'

# 2. Criar notebook
notebooklm create --name "Meu Projeto"

# 3. Adicionar fontes
notebooklm source add-url "https://exemplo.com/doc"
notebooklm source add-file ./relatorio.pdf
notebooklm source add-youtube "https://youtube.com/watch?v=..."

# 4. Fazer pergunta com citações
notebooklm ask "Quais são os pontos principais?" --citations

# 5. Gerar podcast
notebooklm generate audio --format deep-dive --wait
notebooklm download audio

# 6. Gerar quiz para estudo
notebooklm generate quiz --quantity 10 --difficulty medium
notebooklm download quiz --format markdown
```

### API Python

```python
from notebooklm import NotebookLMClient

async with NotebookLMClient() as client:
    # Criar notebook
    notebook = await client.create_notebook("Meu Projeto")
    
    # Adicionar fonte
    await notebook.add_url("https://exemplo.com/doc")
    
    # Perguntar
    answer = await notebook.ask("Resumo dos pontos principais?")
    print(answer.text)
    print(answer.citations)  # Fontes citadas
    
    # Gerar podcast
    task = await notebook.generate_audio(format="deep-dive")
    await task.wait()
    mp3_path = await notebook.download_audio(task.id)
    print(f"Podcast salvo em: {mp3_path}")
```

### Servidor REST (para Frontends)

```bash
# Iniciar servidor
notebooklm-server --host 0.0.0.0 --port 8000

# Habilitar Swagger/OpenAPI
export NOTEBOOKLM_SERVER_ENABLE_DOCS=1
notebooklm-server

# Acessar documentação
# http://localhost:8000/docs
```

**Exemplo frontend React:**

```javascript
const response = await fetch('http://localhost:8000/v1/notebooks', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer SEU_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ name: 'Meu Projeto' })
});
const notebook = await response.json();
```

Veja [FRONTEND_GUIDE.md](deploy/FRONTEND_GUIDE.md) para integração completa.

### Servidor MCP (para Claude Code / Codex)

```bash
# Local via stdio (adicionar ao config do Claude)
# ~/.config/claude/claude_desktop_config.json ou ~/.claude.json
{
  "mcpServers": {
    "notebooklm": {
      "command": "notebooklm-mcp"
    }
  }
}

# Remoto via túnel (acessível do claude.ai mobile)
docker compose -f deploy/docker-compose.yml up -d
```

Agora no Claude Code:
```
@notebooklm Crie um notebook sobre arquitetura de microsserviços
@notebooklm Adicione https://martinfowler.com/articles/microservices.html
@notebooklm Gere um quiz com 10 perguntas difíceis
```

## Docker & Implantação

### Subir Servidor REST em VPS/VM

```bash
cd deploy

# 1. Criar perfil com token mestre
notebooklm login --master-token --account voce@exemplo.com

# 2. Configurar .env
cat > .env << EOF
NOTEBOOKLM_SERVER_TOKEN=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
NOTEBOOKLM_PROFILE_DIR=/caminho/absoluto/para/perfil
NOTEBOOKLM_UID=$(id -u)
NOTEBOOKLM_GID=$(id -g)
NOTEBOOKLM_SERVER_PORT=8000
EOF

# 3. Subir com Docker Compose
docker compose -f docker-compose.server.yml up -d --build

# 4. Testar
curl -H "Authorization: Bearer $(grep NOTEBOOKLM_SERVER_TOKEN .env | cut -d= -f2)" \
     http://localhost:8000/healthz
```

### Túnel para Acesso Externo

**Cloudflare:**

```bash
export CF_TUNNEL_TOKEN=SEU_TOKEN
docker compose -f deploy/docker-compose.full.yml --profile cloudflare up -d
```

**Tailscale:**

```bash
export TS_AUTHKEY=SUA_CHAVE
docker compose -f deploy/docker-compose.full.yml --profile tailscale up -d
```

Veja [deploy/README.md](deploy/README.md) para detalhes completos.

## Documentação

- **[Guia de Instalação](docs/installation.md)** — Todas as personas, plataformas, extras
- **[Referência da CLI](docs/cli-reference.md)** — Todos os comandos, opções, exemplos
- **[API Python](docs/python-api.md)** — Classes, métodos, padrões assíncronos
- **[Guia MCP](docs/mcp-guide.md)** — Configuração local/remota, tunnels, troubleshooting
- **[Guia para Frontends](deploy/FRONTEND_GUIDE.md)** — Integração React/Vue/Mobile, SSE, WebSockets
- **[Arquitetura](docs/architecture.md)** — Visão geral do sistema, módulos, fluxos
- **[Solução de Problemas](docs/troubleshooting.md)** — Erros comuns, debugging, workarounds
- **[Limites de Quota](docs/quota-limits.md)** — Limites do NotebookLM por conta/tipo
- **[Segurança](docs/security.md)** — Modelo de ameaças, melhores práticas, hardening

## Roadmap & Melhorias Recentes

### ✅ Implementado (v0.8.1+)

- **Streaming em Tempo Real (SSE)** — Endpoint `/v1/notebooks/{id}/artifacts/{task_id}/stream` para updates push automáticos, elimina polling ineficiente
- **Endpoint de Capabilities Dinâmicas** — `GET /v1/server/capabilities` retorna todos os recursos suportados, formatos, idiomas, limites
- **Servidor REST Completo** — Todos os endpoints `/v1/*` cobrem 100% dos recursos do NotebookLM
- **Dockerização Completa** — Dockerfiles dedicados para servidores REST e MCP, compose unificado com perfis para tunnels
- **Documentação PT-BR** — README e guias técnicos em português do Brasil
- **OpenAPI/Swagger** — Habilitável via `NOTEBOOKLM_SERVER_ENABLE_DOCS=1` para geração automática de clients
- **Middleware CORS** — Configurável via `NOTEBOOKLM_SERVER_CORS_ORIGINS` para frontends web

### 🚧 Em Desenvolvimento

- WebSockets para status em tempo real bidirecional
- Upload chunked para arquivos grandes (>10MB)
- Webhooks para notificações backend-to-backend
- Gestão de sessões de conversa (contexto de chat)
- Normalização de erros específicos do Google

## Contribuição

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes de desenvolvimento, testes, PRs.

**Scripts úteis:**

```bash
# Rodar testes
pytest tests/

# Verificar tipo
mypy src/notebooklm

# Formatar código
ruff format src/notebooklm

# Build local
pip install -e ".[dev]"
```

## Licença

[MIT](LICENSE) — Use livremente em projetos pessoais e comerciais.

## Aviso Legal

Esta biblioteca **não é afiliada ao Google** e usa APIs não documentadas que podem mudar sem aviso. Use por sua conta e risco. Ideal para protótipos, pesquisa e automação pessoal. Não use em produção crítica sem monitoramento ativo.

---

**Feito com ❤️ pela comunidade** · [GitHub](https://github.com/teng-lin/notebooklm-py) · [PyPI](https://pypi.org/project/notebooklm-py/)
