#!/bin/bash
# scripts/health_monitor_loop.sh
# Autonomous health monitoring with self-recovery
# Run as: nohup ./scripts/health_monitor_loop.sh > logs/monitor.out 2>&1 &

set -euo pipefail

mkdir -p logs

HEALTH_LOG="logs/health_monitor_$(date +%Y%m%d_%H%M%S).log"
INTERVAL=${HEALTH_CHECK_INTERVAL:-300}  # default: 5 minutes

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$HEALTH_LOG"; }

check_postgres() {
    if docker exec sovereign-ai-postgres-1 pg_isready -U claude &>/dev/null 2>&1; then
        log "✓ PostgreSQL OK"
        return 0
    else
        log "✗ PostgreSQL DOWN"
        return 1
    fi
}

check_ollama() {
    if curl -sf http://localhost:11434/api/tags | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('models',[])),' models')" 2>/dev/null; then
        log "✓ Ollama OK"
        return 0
    else
        log "✗ Ollama DOWN"
        return 1
    fi
}

check_prometheus() {
    if curl -sf http://localhost:9090/-/healthy | grep -q "OK" &>/dev/null; then
        log "✓ Prometheus OK"
        return 0
    else
        log "✗ Prometheus DOWN"
        return 1
    fi
}

check_langgraph() {
    local status
    status=$(curl -sf http://localhost:8888/health 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('status','unknown'))" 2>/dev/null || echo "unreachable")
    if [ "$status" = "healthy" ]; then
        log "✓ LangGraph OK (cascade: T1→T5)"
        return 0
    else
        log "✗ LangGraph DOWN (status=$status)"
        return 1
    fi
}

check_anone() {
    local status
    status=$(curl -sf http://localhost:8080/health 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('status','unknown'))" 2>/dev/null || echo "unreachable")
    if [ "$status" = "healthy" ]; then
        log "✓ Agent Anone OK"
        return 0
    else
        log "✗ Agent Anone DOWN (T5 PII will be bypassed)"
        return 1
    fi
}

check_t5_api_key() {
    if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
        log "✓ ANTHROPIC_API_KEY set (T5 cloud ready)"
        return 0
    else
        log "✗ ANTHROPIC_API_KEY missing (T5 unavailable)"
        return 1
    fi
}

recover_service() {
    local service="$1"
    log "⚠ Attempting recovery for: $service"
    docker compose restart "$service" 2>&1 | tee -a "$HEALTH_LOG" || true
    sleep 10
}

run_health_cycle() {
    local failed_services=()

    log ""
    log "=== Health Check Cycle: $(date) ==="

    check_postgres  || failed_services+=("postgres")
    check_ollama    || failed_services+=("ollama")
    check_prometheus || failed_services+=("prometheus")
    check_langgraph || failed_services+=("langgraph")
    check_anone     || failed_services+=("anone")
    check_t5_api_key || true  # Don't restart for missing API key

    if [ ${#failed_services[@]} -gt 0 ]; then
        log ""
        log "⚠ ${#failed_services[@]} service(s) unhealthy: ${failed_services[*]}"
        log "  Initiating autonomous recovery..."
        for svc in "${failed_services[@]}"; do
            recover_service "$svc"
        done
        # Re-check after recovery
        sleep 15
        log "--- Post-recovery re-check ---"
        for svc in "${failed_services[@]}"; do
            case "$svc" in
                postgres) check_postgres || log "  ✗ $svc still down after recovery" ;;
                ollama) check_ollama || log "  ✗ $svc still down after recovery" ;;
                prometheus) check_prometheus || log "  ✗ $svc still down after recovery" ;;
                langgraph) check_langgraph || log "  ✗ $svc still down after recovery" ;;
                anone) check_anone || log "  ✗ $svc still down after recovery" ;;
            esac
        done
    else
        log "✓ All services healthy"
    fi
}

log "=== Sovereign AI Health Monitor Started ==="
log "Log file: $HEALTH_LOG"
log "Check interval: ${INTERVAL}s"

# Run first check immediately, then on interval
while true; do
    run_health_cycle
    log "Next check in ${INTERVAL}s..."
    sleep "$INTERVAL"
done
