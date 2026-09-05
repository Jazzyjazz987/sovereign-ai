#!/bin/bash
# Stack startup with automatic logging
# Usage: ./scripts/startup_with_logging.sh

set -e

LOG_DIR="/opt/claude/sovereign-ai/logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
STARTUP_LOG="$LOG_DIR/stack_startup_${TIMESTAMP}.log"

mkdir -p "$LOG_DIR"

{
  echo "=== Sovereign AI Stack Startup ==="
  echo "Time: $(date)"
  echo "Log directory: $LOG_DIR"
  echo ""

  echo "Pulling latest container images..."
  docker compose pull 2>&1 | tail -5
  echo ""

  echo "Starting stack..."
  docker compose up -d
  echo ""

  echo "Waiting for T1/T2 (Ollama) to be healthy..."
  for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
      echo "✅ Ollama (T1/T2) ready"
      break
    fi
    echo "  Waiting... ($i/30)"
    sleep 2
  done
  echo ""

  echo "Checking T3 status..."
  docker compose exec -T vllm-t3 curl -s http://localhost:8001/v1/models 2>/dev/null | jq . && echo "✅ T3 ready" || echo "⏳ T3 initializing (see monitor logs)"
  echo ""

  echo "Stack status:"
  docker compose ps
  echo ""

  echo "To monitor T3 initialization:"
  echo "  ./scripts/monitor_t3.sh"
  echo ""
  echo "To view recent logs:"
  echo "  ls -ltr $LOG_DIR"

} | tee "$STARTUP_LOG"
