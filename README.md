# Sovereign AI Stack — DSI Polynésie française

Stack Docker Compose complète : T1→T5 orchestration + API + observabilité.

## Quick Start

### 1. Remplir les secrets
```bash
cd /opt/claude/sovereign-ai
nano .env
# Remplir obligatoirement :
# - HF_TOKEN (Hugging Face)
# - ANTHROPIC_API_KEY (Claude Sonnet)
# - LITELLM_MASTER_KEY
# - POSTGRES_PASSWORD
# - GRAFANA_PASSWORD
```

### 2. Démarrer la stack
```bash
docker compose build
docker compose up -d
docker compose ps
```

### 3. Vérifier les services
```bash
# Ollama models
curl http://localhost:11434/api/tags | jq .

# LangGraph health
curl http://localhost:8888/health

# Agent Anone health
curl http://localhost:8080/health

# Grafana
open http://localhost:3000  # admin / password in .env
```

### 4. Test cascade T1→T5
```bash
# Query LangGraph
curl -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Bonjour, quel est ton rôle ?"}'

# Test PII anonymisation
curl -X POST http://localhost:8080/anonymize \
  -H "Content-Type: application/json" \
  -d '{"text":"Jean Dupont travaille à la DSI"}'
```

## Architecture

- **Ollama** (11434) : T1 + T2 (Mistral 7B + Llama 8B)
- **vLLM-T3** (8001) : Qwen 14B AWQ (code, Graph API)
- **vLLM-T4** (8002) : Mistral Small 22B AWQ (legal, RGPD)
- **LiteLLM** (4000) : OpenAI-compatible router
- **LangGraph** (8888) : Orchestrateur cascade
- **Agent Anone** (8080) : PII anonymisation (GLiNER)
- **PostgreSQL** : State persistence + LiteLLM logs
- **Prometheus** (9090) + **Grafana** (3000) : Observabilité

## Development

Voir `/opt/claude/CLAUDE.md` pour les workflows de développement local.
