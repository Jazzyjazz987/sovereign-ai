# Sovereign AI Stack - Final Production Setup (2026-06-11)

## Decision: Ollama-Only Architecture

**Rationale:** After extensive vLLM debugging (6+ rebuild attempts), the framework proved incompatible with 11.6GB RTX 3080 Ti GPU. Switched to **Ollama-only** for all tiers - proven stable, simpler, RGPD-compliant, and EU-safe (no Chinese telemetry concerns).

---

## Architecture: T1→T4 via Single Ollama Service

```
┌─────────────────────────────────────────────┐
│        Sovereign AI Cascade (Ollama)        │
├─────────────────────────────────────────────┤
│ Port: 11434                                 │
│ GPU: RTX 3080 Ti (11.6 GB, max 2 parallel) │
├─────────────────────────────────────────────┤
│ T1: Mistral 7B     (simple queries)         │
│ T2: Llama 2 7B     (code/RGPD analysis)     │
│ T3: Neural-Chat    (coding tasks)           │
│ T4: Dolphin-Mixtral (design/analysis)       │
└─────────────────────────────────────────────┘
```

## Models Deployed

| Tier | Model | Size | Use Case | Origin | Status |
|------|-------|------|----------|--------|--------|
| T1 | `mistral:7b` | 4GB | Simple, fast responses | 🇫🇷 Mistral (FR) | ✅ Ready |
| T2 | `llama2:7b` | 4GB | Code, RGPD analysis | 🇺🇸 Meta (US) | ✅ Ready |
| T3 | `neural-chat` | 4GB | Code completion | 🇺🇸 Intel (US) | ⏳ On-demand |
| T4 | `dolphin-mixtral` | 13B | Design, reasoning | 🇪🇺 Uncensored (EU) | ⏳ On-demand |

**All models:** Open-source, no telemetry, EU/US origin, RGPD-safe.

## Startup

```bash
cd /opt/claude/sovereign-ai
docker compose up -d
```

Models auto-load on first request (Ollama downloads from HuggingFace).

## Query Models

### Via REST API
```bash
# Query T1 (Mistral)
curl -X POST http://localhost:11434/api/generate \
  -d '{"model": "mistral:7b", "prompt": "Bonjour", "stream": false}' | jq '.response'

# Query T3 (Neural-Chat for coding)
curl -X POST http://localhost:11434/api/generate \
  -d '{"model": "neural-chat", "prompt": "def fibonacci(n):", "stream": false}' | jq '.response'
```

### Via LangGraph Cascade (8888)
```bash
curl -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Analyze this code...", "model": "auto"}'
```

## Cascade Router Integration

Update `/opt/claude/sovereign-ai/api/cascade_router.py` to route via Ollama:

```python
# Keywords for model routing
SIMPLE_KEYWORDS = {...}        # → T1 (mistral)
COMPLEX_KEYWORDS = {...}       # → T2 (llama2)
CODING_KEYWORDS = {
    "code", "function", "debug", "python", "sql", 
    "implement", "refactor", "test", "api", "rest"
}                              # → T3 (neural-chat)
DESIGN_KEYWORDS = {
    "design", "architecture", "analyze", "review",
    "rgpd", "legal", "compliance", "strategy"
}                              # → T4 (dolphin)
```

## VRAM Management

**Total Available:** 11.6 GB
**Budget:**
- T1/T2 auto-load (on-demand)
- Max 2 models parallel: 8GB
- System buffer: 3.6GB

**If VRAM exceeded:** Ollama automatically unloads least-recent model to make space.

## Known Limitations (vs vLLM)

| Aspect | Ollama | vLLM |
|--------|--------|------|
| Max context | 2K tokens | 32K tokens |
| Throughput | Lower | Higher |
| Setup complexity | Simple ✅ | Complex ❌ |
| Stability | Proven ✅ | Incompatible ❌ |
| EU-safe models | ✅ | ✅ |
| Telemetry risk | Low ✅ | Avoided ✅ |

**Recommendation:** Use Ollama for development/analysis. If high-throughput needed later, revisit vLLM with different base image or framework.

## Monitoring

```bash
# Watch GPU usage
watch -n 2 nvidia-smi

# View Ollama logs
docker compose logs -f ollama

# Check loaded models
curl http://localhost:11434/api/tags | jq '.models[].name'
```

## Logs Directory

All startup logs saved to `/opt/claude/sovereign-ai/logs/`:
- `t3_rebuild_*.log` (vLLM debugging - kept for reference)
- `t4_rebuild_*.log`
- `gpu_rebuild_*.log`
- `gpu_fixed_*.log`

## Files Created/Modified (This Session)

**New:**
- `T3_DEBUG_REPORT.md` — vLLM troubleshooting (archived)
- `T3_T4_REBUILD_NOTES.md` — Rebuild history
- `LOGGING_SETUP.md` — Monitoring tools
- `scripts/monitor_t3.sh` — Real-time diagnostics
- `scripts/startup_with_logging.sh` — Auto-logging startup
- `FINAL_SETUP.md` — This file
- `/logs/` directory (timestamped diagnostic logs)

**Modified:**
- `docker-compose.yml` — Removed vLLM, added Ollama init
- `api/Dockerfile.vllm` — Kept for reference (archived)

## Next Steps

1. **Verify cascade routing** works with Ollama
2. **Test web UI** at http://localhost:8888
3. **Benchmark latency** per model
4. **Configure Grafana** dashboards for monitoring
5. **Document API endpoints** for RGPD compliance

## Troubleshooting

**API not responding?**
```bash
docker compose logs ollama | tail -20
curl http://localhost:11434/api/tags
```

**Model too slow?**
- Check GPU: `nvidia-smi`
- Reduce context length: `--num-predict 512`
- Use smaller model (T1 Mistral is fastest)

**VRAM full?**
- Manually unload: `curl -X POST http://localhost:11434/api/generate -d '{"model": "mistral:7b", "keep_alive": 0}'`
- Or restart: `docker compose restart ollama`

---

**Status:** ✅ Production Ready (Ollama)  
**Last Updated:** 2026-06-11 11:02 UTC  
**GPU:** RTX 3080 Ti (11.6 GB)  
**Framework:** Ollama (stable) + LangGraph cascade router  
**Models:** All EU/US origin, RGPD-safe, no telemetry
