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

## Autonomous Continuation

Ce projet est conçu pour exécution autonome via subagents. Toutes les phases de développement sont documentées et resumables.

### Status Actuel
- **Phase 1 (✅ Complete):** Récupération GPU (Ampere RTX 3090), intégration T5 (Claude Sonnet + Anone), observabilité (Prometheus/Grafana)
- **Phase 2 (✅ Complete):** Dashboards Grafana, règles d'alerte Prometheus, health monitoring, boucles autonomes
- **Phase 3 (Planifiée):** Hardening production, déploiement Kubernetes (futur)

### Reprendre le travail

Après reboot ou perte de contexte, relancer la stack complète :

```bash
cd /opt/claude/sovereign-ai

# Arrêter tout
docker compose down

# Redémarrer (reconstruction des images si modif)
docker compose up -d

# Vérifier tous services
docker compose ps

# Logs en temps réel
docker compose logs -f

# Monitorer VRAM en parallèle (separate terminal)
watch -n 2 nvidia-smi
```

### Health Monitoring (Toujours Actif)

```bash
# Endpoint santé API
curl http://localhost:8888/health
curl http://localhost:8080/health

# Grafana dashboards
open http://localhost:3000  # admin / voir .env

# Logs service spécifique
docker compose logs -f langgraph
docker compose logs -f ollama
docker compose logs -f vllm-t3
docker compose logs -f vllm-t4
```

### Test Cascade T1→T5

Vérifier que le routage complet fonctionne :

```bash
# T1 (Mistral 7B rapide)
curl -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Bonjour, quel est ton rôle ?","complexity":1.5}'

# T3 (Qwen 14B code/analyse)
curl -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Écris une fonction Python pour valider un email","complexity":3.5}'

# T4 (Mistral Small 22B légal/RGPD)
curl -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Explique les obligations RGPD pour un système d'\''information gouvernemental","complexity":4.0}'

# T5 (Claude Sonnet + anonymisation)
curl -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Jean Dupont demande des clarifications sur la CNIL","complexity":5.0}'
```

### Troubleshooting

**Si vLLM T3/T4 ne démarrent pas :**
```bash
# Vérifier VRAM disponible (besoin ~22 Go pour stack complète)
nvidia-smi

# Vérifier logs spécifiques
docker compose logs vllm-t3
docker compose logs vllm-t4

# Redémarrer service isolé
docker compose restart vllm-t3
```

**Si Ollama T1/T2 ne répondent pas :**
```bash
# Vérifier modèles chargés
curl http://localhost:11434/api/tags | jq '.models'

# Relancer Ollama
docker compose restart ollama
```

**Si Agent Anone échoue (PII detection) :**
```bash
# Tester anonymisation directement
curl -X POST http://localhost:8080/anonymize \
  -H "Content-Type: application/json" \
  -d '{"text":"Jean Dupont travaille à la DSI à Arue"}'

# Vérifier GLiNER est chargé
docker compose logs anone | grep -i gliner
```

## Commits Complétés

Cette branche contient **10+ commits** couvrant :

1. **GPU Recovery** — Diagnostics Ampere RTX 3090, GGUF quantization
2. **T5 Integration** — Claude Sonnet API + Agent Anone PII anonymisation
3. **Monitoring Setup** — Prometheus scraping, Grafana dashboards
4. **Alert Rules** — Règles d'alerte cascade/GPU/infrastructure
5. **Health Endpoints** — API /health pour tous services
6. **Autonomous Loops** — Boucles de monitoring continue (Docker native)
7. **Complete Cascade** — T1→T2→T3→T4→T5 routage avec complexity scoring
8. **Deanonymization** — Endpoint /deanonymize pour restauration PII

### Tag de Release

```bash
git tag -l | grep phase  # Voir tous tags
git show phase-1-2-complete  # Afficher tag details
```
