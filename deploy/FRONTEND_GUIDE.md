# Guia do Servidor REST para Frontends

Este documento descreve como conectar aplicações frontend (web, mobile, desktop) ao servidor REST do NotebookLM para acessar **todos** os recursos da plataforma via API.

## 📋 **Índice**

1. [Visão Geral](#visão-geral)
2. [Instalação Rápida](#instalação-rápida)
3. [Autenticação](#autenticação)
4. [Endpoints Principais](#endpoints-principais)
5. [Exemplos de Uso](#exemplos-de-uso)
6. [Geração de Artefatos](#geração-de-artefatos)
7. [Túneis para Acesso Público](#túneis-para-acesso-público)
8. [Segurança](#segurança)

---

## 🎯 **Visão Geral**

O servidor REST expõe todos os recursos do NotebookLM através de uma API HTTP/JSON padronizada:

| Recurso | Endpoint Base | Descrição |
|---------|---------------|-----------|
| **Notebooks** | `POST /v1/notebooks` | Criar, listar, gerenciar notebooks |
| **Fontes** | `POST /v1/notebooks/{id}/sources/*` | URLs, PDFs, YouTube, Google Drive, texto |
| **Chat** | `POST /v1/notebooks/{id}/chat` | Conversas com o notebook |
| **Artefatos** | `POST /v1/notebooks/{id}/artifacts` | Podcasts, vídeos, slides, quizzes, etc. |
| **Pesquisa** | `POST /v1/notebooks/{id}/research` | Pesquisa automatizada na web/Drive |
| **Compartilhamento** | `POST /v1/notebooks/{id}/share/*` | Compartilhar notebooks |

### **Formato de Resposta**

Todas as respostas seguem o padrão:

```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

Em caso de erro:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "AUTH_ERROR",
    "message": "Invalid or missing bearer token"
  }
}
```

---

## 🚀 **Instalação Rápida**

### **Pré-requisitos**

1. **Perfil do Google autenticado** no host:
   ```bash
   # No host (fora do Docker):
   pip install notebooklm-py[browser]
   notebooklm login --master-token
   ```

2. **Docker e Docker Compose** instalados

### **Passo a Passo**

```bash
cd deploy/

# 1. Gerar arquivo .env.server com token
make setup-server

# 2. Editar .env.server e preencher:
#    - NOTEBOOKLM_PROFILE_DIR=/caminho/para/perfil
#    - CF_TUNNEL_TOKEN (se usar Cloudflare) OU TS_AUTHKEY (se usar Tailscale)

# 3. Subir o servidor
make up-server

# 4. Testar saúde
make test-server
```

### **Verificação**

```bash
# O servidor estará em:
# - Localhost: http://localhost:8000
# - Health check: curl -H "Authorization: Bearer <TOKEN>" http://localhost:8000/healthz
```

---

## 🔐 **Autenticação**

### **Bearer Token**

Todas as requisições devem incluir o header:

```http
Authorization: Bearer <NOTEBOOKLM_SERVER_TOKEN>
```

**Exemplo em JavaScript:**

```javascript
const TOKEN = process.env.NOTEBOOKLM_SERVER_TOKEN;

async function apiRequest(endpoint, options = {}) {
  const response = await fetch(`http://localhost:8000${endpoint}`, {
    ...options,
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error?.message || 'Request failed');
  }
  
  return response.json();
}
```

### **CORS (Cross-Origin Resource Sharing)**

Para frontends web rodando em domínios diferentes, configure no `.env.server`:

```bash
NOTEBOOKLM_SERVER_CORS_ORIGINS=https://meufrontend.com,https://app.exemplo.com
NOTEBOOKLM_SERVER_ENABLE_DOCS=1  # Habilita Swagger UI para debug
```

---

## 📡 **Endpoints Principais**

### **1. Server Info**

```http
GET /v1/server/info?include_account=true
```

Retorna versão do servidor e status de autenticação:

```json
{
  "server": "notebooklm-server",
  "version": "0.8.1",
  "auth": {
    "authenticated": true,
    "storage_exists": true,
    "json_valid": true,
    "cookies_present": true,
    "sid_cookie": true,
    "profile": "server"
  },
  "account": {
    "email": "usuario@gmail.com",
    "authuser": "0",
    "available": true,
    "notebook_limit": 100,
    "source_limit": 50,
    "tier": "FREE"
  }
}
```

### **2. Health Check**

```http
GET /healthz
```

Retorna `ok` se o servidor estiver saudável.

---

### **3. Criar Notebook**

```http
POST /v1/notebooks
Content-Type: application/json

{
  "title": "Meu Notebook de Pesquisa",
  "description": "Notas sobre IA generativa"
}
```

**Resposta:**

```json
{
  "success": true,
  "data": {
    "notebook_id": "abc123...",
    "title": "Meu Notebook de Pesquisa",
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

---

### **4. Listar Notebooks**

```http
GET /v1/notebooks?limit=10&offset=0
```

---

### **5. Adicionar Fontes**

#### **URL**

```http
POST /v1/notebooks/{notebook_id}/sources/url
Content-Type: application/json

{
  "url": "https://exemplo.com/artigo"
}
```

#### **Texto Direto**

```http
POST /v1/notebooks/{notebook_id}/sources/text
Content-Type: application/json

{
  "title": "Minhas Anotações",
  "text": "Conteúdo do texto aqui..."
}
```

#### **Upload de PDF**

```http
POST /v1/notebooks/{notebook_id}/sources/pdf
Content-Type: multipart/form-data

file: (binary PDF)
```

#### **YouTube**

```http
POST /v1/notebooks/{notebook_id}/sources/youtube
Content-Type: application/json

{
  "url": "https://youtube.com/watch?v=VIDEO_ID"
}
```

#### **Google Drive**

```http
POST /v1/notebooks/{notebook_id}/sources/drive
Content-Type: application/json

{
  "drive_id": "FILE_ID_DO_DRIVE"
}
```

---

### **6. Chat / Conversas**

```http
POST /v1/notebooks/{notebook_id}/chat
Content-Type: application/json

{
  "message": "Resuma os principais pontos deste notebook",
  "turn_id": "opcional-uuid-para-streaming"
}
```

**Resposta (streaming opcional):**

```json
{
  "success": true,
  "data": {
    "answer": "Os principais pontos são...",
    "citations": [
      {
        "source_id": "src_123",
        "start_index": 0,
        "end_index": 150
      }
    ]
  }
}
```

---

## 🎨 **Geração de Artefatos**

### **Tipos de Artefatos Suportados**

| Tipo | Formatos | Duração/Estilos | Downloads |
|------|----------|-----------------|-----------|
| **audio** | `deep-dive`, `brief`, `critique`, `debate` | `short`, `medium`, `long` | MP3 |
| **video** | `explainer`, `brief`, `cinematic`, `short` | Vários estilos | MP4 |
| **slide-deck** | `detailed`, `presenter` | - | PDF, PPTX |
| **quiz** | - | Quantidade, dificuldade | JSON, MD, HTML |
| **flashcards** | - | Quantidade | JSON, MD, HTML |
| **infographic** | `portrait`, `landscape`, `square` | `basic`, `detailed`, `comprehensive` | PNG |
| **data-table** | - | Colunas personalizadas | CSV |
| **mind-map** | - | Árvore hierárquica | JSON |
| **report** | `briefing`, `study-guide`, `blog-post` | - | MD |

### **Fluxo de Geração**

1. **Iniciar geração** (retorna `task_id`)
2. **Poll de status** (até `completed`)
3. **Download** do artefato

### **Exemplo: Gerar Podcast de Áudio**

```http
POST /v1/notebooks/{notebook_id}/artifacts
Content-Type: application/json

{
  "artifact_type": "audio",
  "format": "deep-dive",
  "duration": "medium",
  "language": "pt-BR"
}
```

**Resposta:**

```json
{
  "success": true,
  "data": {
    "task_id": "task_abc123...",
    "status": "pending",
    "artifact_type": "audio"
  }
}
```

### **Poll de Status**

```http
GET /v1/notebooks/{notebook_id}/artifacts/task_abc123...
```

**Respostas possíveis:**

```json
// Pendente
{
  "success": true,
  "data": {
    "task_id": "task_abc123...",
    "status": "pending",
    "progress": 0.3
  }
}

// Concluído
{
  "success": true,
  "data": {
    "task_id": "task_abc123...",
    "status": "completed",
    "download_url": "/v1/notebooks/{id}/artifacts/download?task_id=..."
  }
}
```

### **Download do Artefato**

```http
POST /v1/notebooks/{notebook_id}/artifacts/download
Content-Type: application/json

{
  "task_id": "task_abc123..."
}
```

Retorna o arquivo binário (MP3, MP4, PDF, etc.).

---

### **Exemplo: Gerar Quiz**

```http
POST /v1/notebooks/{notebook_id}/artifacts
Content-Type: application/json

{
  "artifact_type": "quiz",
  "num_questions": 10,
  "difficulty": "medium",
  "output_format": "json"
}
```

---

### **Exemplo: Gerar Vídeo**

```http
POST /v1/notebooks/{notebook_id}/artifacts
Content-Type: application/json

{
  "artifact_type": "video",
  "format": "explainer",
  "style": "cinematic",
  "language": "pt-BR"
}
```

---

## 🔍 **Pesquisa Automatizada**

```http
POST /v1/notebooks/{notebook_id}/research
Content-Type: application/json

{
  "query": "últimas notícias sobre IA generativa",
  "search_type": "web",  // ou "drive"
  "import_results": true
}
```

**Resposta:**

```json
{
  "success": true,
  "data": {
    "results": [
      {
        "title": "Artigo sobre IA",
        "url": "https://...",
        "snippet": "...",
        "imported_as_source": true,
        "source_id": "src_456"
      }
    ]
  }
}
```

---

## 🌐 **Túneis para Acesso Público**

### **Cloudflare Tunnel**

1. Crie um tunnel no dashboard da Cloudflare
2. Copie o token do tunnel
3. No `.env.server`:
   ```bash
   TUNNEL=cloudflare
   CF_TUNNEL_TOKEN=<token>
   ```
4. No dashboard da Cloudflare, adicione rota:
   - **Public Hostname**: `notebooklm.seudominio.com`
   - **Service**: `http://notebooklm-rest:8000`

### **Tailscale Funnel**

1. No admin console do Tailscale:
   - Ative MagicDNS + HTTPS certificates
   - Em Settings → Funnel, adicione `"funnel"` à policy
2. Gere auth key em Settings → Keys
3. No `.env.server`:
   ```bash
   TUNNEL=tailscale
   TS_AUTHKEY=tskey-auth-xxxxx
   ```
4. Acesse via: `https://notebooklm-rest.<tailnet>.ts.net`

---

## 🔒 **Segurança**

### **Melhores Práticas**

1. **Use conta Google descartável** para servidores públicos
2. **Token forte**: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
3. **TLS obrigatório**: Nunca exponha sem Cloudflare/Tailscale/reverse proxy
4. **Rate limiting**: Configure no `.env.server`:
   ```bash
   NOTEBOOKLM_SERVER_RATE_LIMIT_REQUESTS=100
   NOTEBOOKLM_SERVER_RATE_LIMIT_WINDOW=60
   ```

### **Variáveis de Ambiente Sensíveis**

| Variável | Sensibilidade | Descrição |
|----------|---------------|-----------|
| `NOTEBOOKLM_SERVER_TOKEN` | 🔴 Crítico | Token de autenticação |
| `CF_TUNNEL_TOKEN` | 🟠 Alto | Token do tunnel Cloudflare |
| `TS_AUTHKEY` | 🟠 Alto | Chave de auth Tailscale |
| `NOTEBOOKLM_PROFILE_DIR` | 🔴 Crítico | Contém master_token.json |

---

## 📚 **Exemplo Completo em React**

```tsx
// src/api/notebooklm.ts
const API_BASE = 'http://localhost:8000';
const TOKEN = import.meta.env.VITE_NOTEBOOKLM_TOKEN;

export async function createNotebook(title: string) {
  const res = await fetch(`${API_BASE}/v1/notebooks`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ title }),
  });
  const data = await res.json();
  if (!data.success) throw new Error(data.error.message);
  return data.data;
}

export async function generatePodcast(notebookId: string) {
  // 1. Iniciar geração
  const startRes = await fetch(`${API_BASE}/v1/notebooks/${notebookId}/artifacts`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      artifact_type: 'audio',
      format: 'deep-dive',
      duration: 'medium',
      language: 'pt-BR',
    }),
  });
  const startData = await startRes.json();
  const taskId = startData.data.task_id;

  // 2. Poll de status
  while (true) {
    await new Promise(r => setTimeout(r, 2000));
    const statusRes = await fetch(`${API_BASE}/v1/notebooks/${notebookId}/artifacts/${taskId}`, {
      headers: { 'Authorization': `Bearer ${TOKEN}` },
    });
    const statusData = await statusRes.json();
    
    if (statusData.data.status === 'completed') {
      // 3. Download
      const downloadRes = await fetch(`${API_BASE}/v1/notebooks/${notebookId}/artifacts/download`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${TOKEN}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ task_id: taskId }),
      });
      const blob = await downloadRes.blob();
      const url = URL.createObjectURL(blob);
      return url; // URL do MP3
    }
    
    if (statusData.data.status === 'failed') {
      throw new Error('Geração falhou');
    }
  }
}
```

---

## 🛠️ **Debug e Logs**

```bash
# Ver logs do servidor
make logs-server

# Acessar Swagger UI (se habilitado)
# http://localhost:8000/docs

# Testar health
curl -H "Authorization: Bearer <TOKEN>" http://localhost:8000/healthz

# Ver info do servidor
curl -H "Authorization: Bearer <TOKEN>" http://localhost:8000/v1/server/info
```

---

## ⚠️ **Limitações e Avisos**

1. **APIs não oficiais**: O Google pode mudar endpoints sem aviso
2. **Quotas do NotebookLM**: Limites da plataforma se aplicam
3. **Sessão expira**: Cookies podem expirar; use `--master-token` para renovação automática
4. **Beta**: Esta biblioteca é beta; APIs podem mudar entre versões

---

## 📞 **Suporte**

- **Documentação completa**: `/docs` no repositório
- **Issues**: GitHub Issues do projeto
- **Exemplos**: Diretório `/examples` no repositório
