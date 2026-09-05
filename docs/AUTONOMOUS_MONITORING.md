# Autonomous Health Monitoring

## Overview

The sovereign AI stack includes autonomous health monitoring that:
- Checks all 6 services every 5 minutes (configurable)
- Logs results to `logs/health_monitor_<timestamp>.log`
- Automatically restarts unhealthy services via `docker compose restart`
- Performs post-recovery verification
- No human intervention required for transient failures

## Running the Monitor

### Option 1: Background Daemon (recommended)

```bash
cd /home/user/sovereign-ai
nohup ./scripts/health_monitor_loop.sh > logs/monitor.out 2>&1 &
echo "Monitor PID: $!"
```

### Option 2: Foreground (for debugging)

```bash
./scripts/health_monitor_loop.sh
```

### Option 3: Custom Interval

```bash
HEALTH_CHECK_INTERVAL=60 ./scripts/health_monitor_loop.sh  # Check every 60s
```

## Health Checks

| Service | Check Method | Recovery Action |
|---------|-------------|----------------|
| PostgreSQL | `pg_isready -U claude` | `docker compose restart postgres` |
| Ollama | `GET /api/tags` | `docker compose restart ollama` |
| Prometheus | `GET /-/healthy` | `docker compose restart prometheus` |
| LangGraph | `GET /health` (status=healthy) | `docker compose restart langgraph` |
| Agent Anone | `GET /health` (status=healthy) | `docker compose restart anone` |
| T5 API Key | `$ANTHROPIC_API_KEY` env check | Manual (set env var) |

## Log Files

Health logs are written to `logs/health_monitor_YYYYMMDD_HHMMSS.log`

```bash
# Tail live log
tail -f logs/health_monitor_*.log | grep -v "^$"

# Find failures
grep "✗" logs/health_monitor_*.log

# Find recoveries
grep "recovery" logs/health_monitor_*.log
```

## SLO Targets

| Metric | Target |
|--------|--------|
| Service availability | 99.5% (≤3.6 hours downtime/month) |
| T1–T2 cascade latency | <500ms p95 |
| T5 cloud fallback latency | <5s p95 (including anonymization) |
| PII anonymization success | >99.9% |
| Auto-recovery success rate | >90% for transient failures |

## Architecture

```
Health Monitor Loop (every 5m)
├── check_postgres   → pg_isready
├── check_ollama     → /api/tags
├── check_prometheus → /-/healthy
├── check_langgraph  → /health
├── check_anone      → /health
└── check_t5_api_key → env var
       ↓ (if failures)
Recovery Loop
├── docker compose restart <service>
├── sleep 15s
└── post-recovery re-check
```
