#!/bin/bash
# T3 vLLM Initialization Monitor
# Captures logs and GPU metrics during startup to diagnose initialization hangs

set -e

LOG_DIR="/opt/claude/sovereign-ai/logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
T3_LOG="$LOG_DIR/t3_startup_${TIMESTAMP}.log"
GPU_LOG="$LOG_DIR/gpu_metrics_${TIMESTAMP}.log"
CURL_LOG="$LOG_DIR/api_health_${TIMESTAMP}.log"

mkdir -p "$LOG_DIR"

echo "=== T3 vLLM Initialization Monitor ===" | tee "$T3_LOG"
echo "Start time: $(date)" | tee -a "$T3_LOG"
echo "T3 Log: $T3_LOG"
echo "GPU Log: $GPU_LOG"
echo "Health Log: $CURL_LOG"
echo ""

# Background GPU monitoring
(
  while true; do
    {
      echo "=== $(date '+%Y-%m-%d %H:%M:%S') ==="
      nvidia-smi --query-gpu=timestamp,index,memory.used,memory.total,utilization.gpu,utilization.memory --format=csv
      echo ""
    } >> "$GPU_LOG"
    sleep 5
  done
) &
GPU_PID=$!

# Background API health check
(
  attempt=0
  while true; do
    {
      attempt=$((attempt + 1))
      echo "[Attempt $attempt] $(date '+%Y-%m-%d %H:%M:%S')"
      curl -v http://localhost:8001/v1/models 2>&1 | head -20
      echo "---"
    } >> "$CURL_LOG"
    sleep 10
  done
) &
CURL_PID=$!

# Stream vLLM logs
echo "Streaming vLLM-T3 logs (Ctrl+C to stop monitoring):"
docker compose logs -f vllm-t3 2>&1 | tee -a "$T3_LOG" &
DOCKER_PID=$!

# Wait for user interrupt
trap "kill $GPU_PID $CURL_PID $DOCKER_PID 2>/dev/null; echo 'Monitoring stopped'; echo 'Logs saved to: $LOG_DIR'" EXIT

wait $DOCKER_PID
