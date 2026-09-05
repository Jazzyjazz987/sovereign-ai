# Autonomous Health Monitoring

**Autonomous health monitoring with self-recovery for the Sovereign AI Stack.**

This system continuously monitors all 7 services and automatically restarts the entire stack if any service becomes unhealthy. Designed for unattended operation with minimal manual intervention.

---

## Overview

The `health_monitor_loop.sh` script implements a continuous monitoring loop that:

1. **Monitors 7 services** every 5 minutes
2. **Detects unhealthy services** via HTTP health endpoints and service checks
3. **Automatically recovers** by restarting the entire stack
4. **Logs all activity** to a timestamped log file
5. **Tracks failure counts** per service

| Service | Port | Health Check | Tier |
|---------|------|--------------|------|
| PostgreSQL | 5432 | `pg_isready -U claude` | Database |
| Ollama (T1/T2) | 11434 | `GET /api/tags` | Model Engine |
| LiteLLM | 4000 | `GET /health` | Router |
| Agent Anone | 8080 | `GET /health` | PII Proxy |
| LangGraph | 8888 | `GET /health` | Orchestrator |
| Prometheus | 9090 | `GET /-/healthy` | Metrics |
| Grafana | 3000 | `GET /api/health` | Dashboards |

---

## Quick Start

### Run in foreground (for testing)
```bash
cd /opt/claude/sovereign-ai
./scripts/health_monitor_loop.sh
```

You'll see:
```
=========================================
Autonomous Health Monitor Started
Timestamp: 2026-09-04 12:34:56
Log file: /opt/claude/sovereign-ai/logs/health_monitor_20260904_123456.log
Check interval: 300s (5 minutes)
Services monitored: 7
  - postgres
  - ollama
  - litellm
  - anone
  - langgraph
  - prometheus
  - grafana
=========================================

2026-09-04 12:34:56 === Health Check Cycle ===
  ✓ postgres: UP
  ✓ ollama: UP
  ✓ litellm: UP
  ✓ anone: UP
  ✓ langgraph: UP
  ✓ prometheus: UP
  ✓ grafana: UP
✓ All services healthy
```

### Run in background (production)
```bash
# Using nohup
nohup /opt/claude/sovereign-ai/scripts/health_monitor_loop.sh > /dev/null 2>&1 &

# OR using systemd service (recommended — see section below)
```

### Run as systemd service (recommended for servers)
Create `/etc/systemd/system/sovereign-ai-monitor.service`:

```ini
[Unit]
Description=Sovereign AI Health Monitor
After=docker.service

[Service]
Type=simple
User=jwilliams
WorkingDirectory=/opt/claude/sovereign-ai
ExecStart=/opt/claude/sovereign-ai/scripts/health_monitor_loop.sh
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable sovereign-ai-monitor
sudo systemctl start sovereign-ai-monitor

# Monitor logs
sudo journalctl -u sovereign-ai-monitor -f
```

---

## Health Check Details

### PostgreSQL
```bash
docker exec sovereign-ai-postgres-1 pg_isready -U claude
```
Verifies database is accepting connections.

### Ollama (T1/T2)
```bash
curl -s http://localhost:11434/api/tags
```
Confirms model engine is responsive.

### LiteLLM (Router)
```bash
curl -s http://localhost:4000/health
```
Confirms LLM router/gateway is healthy.

### Agent Anone (PII Proxy)
```bash
curl -s http://localhost:8080/health
```
Confirms anonymization proxy is running.

### LangGraph (Orchestrator)
```bash
curl -s http://localhost:8888/health
```
Confirms cascade orchestrator is healthy.

### Prometheus (Metrics)
```bash
curl -s http://localhost:9090/-/healthy
```
Confirms metrics collection is running.

### Grafana (Dashboards)
```bash
curl -s http://localhost:3000/api/health
```
Confirms visualization dashboard is running.

---

## Recovery Strategy

When any service is detected as **DOWN**:

1. **Log warning** to `logs/health_monitor_TIMESTAMP.log`
2. **Execute**: `docker compose restart`
3. **Wait**: 15 seconds for services to stabilize
4. **Verify**: Re-run all health checks
5. **Report**: Log success or remaining issues

### Example Recovery Log

```
2026-09-04 12:40:00 === Health Check Cycle ===
  ✓ postgres: UP
  ✓ ollama: UP
  ✗ langgraph: DOWN (failures: 1)
  ✓ prometheus: UP
  ✓ grafana: UP

⚠ WARNING: 1 service(s) unhealthy
Attempting autonomous recovery...
  - Restarting langgraph...

Executing: docker compose restart
Waiting 15 seconds for services to stabilize...

Verifying recovery...
2026-09-04 12:40:15 === Health Check Cycle ===
  ✓ postgres: UP
  ✓ ollama: UP
  ✓ langgraph: UP
  ✓ prometheus: UP
  ✓ grafana: UP

✓ All services recovered successfully
```

---

## Log Files

### Location
```
/opt/claude/sovereign-ai/logs/health_monitor_YYYYMMDD_HHMMSS.log
```

### View recent logs
```bash
# Latest monitor log
tail -f logs/health_monitor_*.log | grep -E "Health Check|WARNING|✓|✗"

# All logs with summary
ls -ltr logs/health_monitor_*.log
tail -20 logs/health_monitor_*.log
```

### Grep useful patterns
```bash
# Find all warnings
grep "WARNING" logs/health_monitor_*.log

# Find service downs
grep "DOWN" logs/health_monitor_*.log

# Find recovery events
grep "recovery\|recovered" logs/health_monitor_*.log

# Count failures by service
grep "failures:" logs/health_monitor_*.log | sort | uniq -c

# View status at specific time
grep "2026-09-04 12:4" logs/health_monitor_*.log
```

---

## SLO Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Service Availability | 99.5% | 5-minute detection + 15s recovery |
| Time to Recovery | < 30s | Detection (5m) + restart (15s) + verification |
| Failure Detection | 100% | All 7 services monitored |
| False Positives | < 1% | Timeout-based, no flaky checks |
| Log Retention | 30 days | Archive older logs monthly |

---

## Failure Count Tracking

The monitor tracks consecutive failures per service:

```
FAILURE_COUNT["postgres"] = 0    # Last check succeeded
FAILURE_COUNT["ollama"] = 3      # Last 3 checks failed
FAILURE_COUNT["langgraph"] = 1   # Just went down
```

This allows future enhancements (e.g., restart after N consecutive failures, alert on N > 5).

---

## Graceful Shutdown

The monitor responds to SIGTERM and SIGINT (Ctrl+C):

```bash
# Kill background monitor
kill %1                    # foreground job
kill $(pgrep -f health_monitor_loop.sh)

# Output when shutting down
2026-09-04 12:50:00
Monitor shutting down at 2026-09-04 12:50:00
```

---

## Troubleshooting

### "curl: command not found"
The health checks use `curl` for HTTP endpoints. Ensure Docker container `curl` is available:
```bash
docker exec sovereign-ai-postgres-1 curl --version
docker exec sovereign-ai-ollama-1 curl --version
```

If missing, modify checks to use `docker exec <container> curl` or install curl in containers.

### "postgres container not found"
The monitor assumes Docker Compose container naming: `sovereign-ai-<service>-1`

Verify actual container names:
```bash
docker ps | grep sovereign-ai
```

If names differ, update the `check_postgres()` function:
```bash
check_postgres() {
    if docker exec <your-actual-container-name> pg_isready -U claude > /dev/null 2>&1; then
        ...
    fi
}
```

### "docker compose restart fails"
Ensure the script runs from the correct directory with docker-compose.yml present:
```bash
cd /opt/claude/sovereign-ai
ls -la docker-compose.yml
```

### Monitor process exits unexpectedly
Check logs for errors:
```bash
tail -50 logs/health_monitor_*.log
```

If running as systemd service:
```bash
sudo journalctl -u sovereign-ai-monitor -n 50
```

---

## Performance Impact

- **CPU**: Negligible (8 curl requests + 1 pg_isready every 5 minutes)
- **Memory**: ~5 MB resident
- **Network**: ~500 bytes per check cycle
- **Disk**: ~10 KB per day (logs)

Safe to run continuously on production systems.

---

## Future Enhancements

Possible improvements (not yet implemented):

1. **Smarter recovery** — Restart individual services instead of full stack
2. **Alerts** — Email/Slack notifications on recovery events
3. **Metrics export** — Prometheus metrics for monitoring system health
4. **Threshold-based restart** — Only restart after N consecutive failures
5. **Service dependencies** — Respect Docker Compose `depends_on` ordering
6. **Rollback logic** — Detect cascade failures and roll back to last known good state
7. **Health history** — Track uptime trends per service

---

## References

- [Docker Compose Health Checks](https://docs.docker.com/compose/compose-file/05-services/#healthcheck)
- [Prometheus Health Endpoint](https://prometheus.io/docs/prometheus/latest/management_api/)
- [Grafana Health API](https://grafana.com/docs/grafana/latest/http_api/other/#health)

---

**Last updated:** 2026-09-04  
**Status:** Operational  
**Contact:** DSI Polynésie française
