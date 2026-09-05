#!/bin/bash
# Autonomous health monitoring with self-recovery
# Continuously monitors 7 services and restarts unhealthy ones
# Usage: ./scripts/health_monitor_loop.sh
# To run in background: nohup ./scripts/health_monitor_loop.sh > /dev/null 2>&1 &

set -e

HEALTH_LOG_DIR="/opt/claude/sovereign-ai/logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
HEALTH_LOG="$HEALTH_LOG_DIR/health_monitor_${TIMESTAMP}.log"

mkdir -p "$HEALTH_LOG_DIR"

# Color codes for readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# List of services to monitor
SERVICES=("postgres" "ollama" "litellm" "anone" "langgraph" "prometheus" "grafana")

# Health check status tracking
declare -A SERVICE_HEALTH
declare -A FAILURE_COUNT

# Initialize failure counters
for service in "${SERVICES[@]}"; do
    FAILURE_COUNT[$service]=0
done

log_message() {
    local msg="$1"
    echo -e "$msg" | tee -a "$HEALTH_LOG"
}

check_postgres() {
    if docker exec sovereign-ai-postgres-1 pg_isready -U claude > /dev/null 2>&1; then
        SERVICE_HEALTH["postgres"]="UP"
        FAILURE_COUNT["postgres"]=0
        return 0
    else
        SERVICE_HEALTH["postgres"]="DOWN"
        ((FAILURE_COUNT["postgres"]++))
        return 1
    fi
}

check_ollama() {
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        SERVICE_HEALTH["ollama"]="UP"
        FAILURE_COUNT["ollama"]=0
        return 0
    else
        SERVICE_HEALTH["ollama"]="DOWN"
        ((FAILURE_COUNT["ollama"]++))
        return 1
    fi
}

check_litellm() {
    if curl -s http://localhost:4000/health > /dev/null 2>&1; then
        SERVICE_HEALTH["litellm"]="UP"
        FAILURE_COUNT["litellm"]=0
        return 0
    else
        SERVICE_HEALTH["litellm"]="DOWN"
        ((FAILURE_COUNT["litellm"]++))
        return 1
    fi
}

check_anone() {
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        SERVICE_HEALTH["anone"]="UP"
        FAILURE_COUNT["anone"]=0
        return 0
    else
        SERVICE_HEALTH["anone"]="DOWN"
        ((FAILURE_COUNT["anone"]++))
        return 1
    fi
}

check_langgraph() {
    if curl -s http://localhost:8888/health > /dev/null 2>&1; then
        SERVICE_HEALTH["langgraph"]="UP"
        FAILURE_COUNT["langgraph"]=0
        return 0
    else
        SERVICE_HEALTH["langgraph"]="DOWN"
        ((FAILURE_COUNT["langgraph"]++))
        return 1
    fi
}

check_prometheus() {
    if curl -s http://localhost:9090/-/healthy > /dev/null 2>&1; then
        SERVICE_HEALTH["prometheus"]="UP"
        FAILURE_COUNT["prometheus"]=0
        return 0
    else
        SERVICE_HEALTH["prometheus"]="DOWN"
        ((FAILURE_COUNT["prometheus"]++))
        return 1
    fi
}

check_grafana() {
    if curl -s http://localhost:3000/api/health > /dev/null 2>&1; then
        SERVICE_HEALTH["grafana"]="UP"
        FAILURE_COUNT["grafana"]=0
        return 0
    else
        SERVICE_HEALTH["grafana"]="DOWN"
        ((FAILURE_COUNT["grafana"]++))
        return 1
    fi
}

perform_health_checks() {
    log_message "$(date '+%Y-%m-%d %H:%M:%S') === Health Check Cycle ==="

    check_postgres || true
    check_ollama || true
    check_litellm || true
    check_anone || true
    check_langgraph || true
    check_prometheus || true
    check_grafana || true

    # Log status of all services
    for service in "${SERVICES[@]}"; do
        local status="${SERVICE_HEALTH[$service]}"
        local count="${FAILURE_COUNT[$service]}"
        if [ "$status" = "UP" ]; then
            log_message "  ${GREEN}✓${NC} $service: UP"
        else
            log_message "  ${RED}✗${NC} $service: DOWN (failures: $count)"
        fi
    done
}

perform_recovery() {
    local unhealthy=0

    for service in "${SERVICES[@]}"; do
        if [ "${SERVICE_HEALTH[$service]}" = "DOWN" ]; then
            ((unhealthy++))
        fi
    done

    if [ $unhealthy -gt 0 ]; then
        log_message ""
        log_message "${YELLOW}⚠ WARNING: $unhealthy service(s) unhealthy${NC}"
        log_message "Attempting autonomous recovery..."

        # Log unhealthy services
        for service in "${SERVICES[@]}"; do
            if [ "${SERVICE_HEALTH[$service]}" = "DOWN" ]; then
                log_message "  - Restarting $service..."
            fi
        done

        log_message ""
        log_message "Executing: docker compose restart"
        cd /opt/claude/sovereign-ai
        docker compose restart >> "$HEALTH_LOG" 2>&1

        log_message "Waiting 15 seconds for services to stabilize..."
        sleep 15

        # Verify recovery
        log_message "Verifying recovery..."
        perform_health_checks

        # Check if all services are back up
        local recovered=0
        for service in "${SERVICES[@]}"; do
            if [ "${SERVICE_HEALTH[$service]}" = "UP" ]; then
                ((recovered++))
            fi
        done

        if [ $recovered -eq ${#SERVICES[@]} ]; then
            log_message "${GREEN}✓ All services recovered successfully${NC}"
        else
            log_message "${YELLOW}⚠ Some services still unhealthy after restart${NC}"
        fi
    else
        log_message "${GREEN}✓ All services healthy${NC}"
    fi
}

main_loop() {
    log_message "========================================="
    log_message "Autonomous Health Monitor Started"
    log_message "Timestamp: $(date)"
    log_message "Log file: $HEALTH_LOG"
    log_message "Check interval: 300s (5 minutes)"
    log_message "Services monitored: ${#SERVICES[@]}"
    for service in "${SERVICES[@]}"; do
        log_message "  - $service"
    done
    log_message "========================================="
    log_message ""

    # Initial health check
    perform_health_checks

    # Main monitoring loop
    while true; do
        log_message ""
        sleep 300  # Check every 5 minutes

        perform_health_checks
        perform_recovery

        log_message ""
    done
}

# Trap signals for graceful shutdown
trap 'log_message ""; log_message "Monitor shutting down at $(date)"; exit 0' SIGTERM SIGINT

# Start main loop
main_loop
