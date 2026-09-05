#!/bin/bash
# Sovereign AI Stack — Check Current Execution Mode

cd "$(dirname "$0")/.."

if [[ ! -f .env.mode ]]; then
  echo "❌ .env.mode not found"
  exit 1
fi

MODE=$(grep '^EXECUTION_MODE=' .env.mode | cut -d= -f2)
CPU_ONLY=$(grep '^OLLAMA_CPU_ONLY=' .env.mode | cut -d= -f2)
GPU_COUNT=$(grep '^GPU_DEVICE_COUNT=' .env.mode | cut -d= -f2)

echo "=========================================="
echo "  Sovereign AI Stack — Execution Mode"
echo "=========================================="
echo ""

if [[ "$MODE" == "cpu" ]]; then
  echo "🟢 Current Mode: CPU-ONLY"
  echo ""
  echo "  Execution:  CPU (Intel/AMD processor)"
  echo "  Speed:      ~7 tokens/second (slow)"
  echo "  GPU Used:   No (GPU_DEVICE_COUNT=$GPU_COUNT)"
  echo "  Driver:     Not required"
  echo "  Status:     ✅ Working"
  echo ""
  echo "To switch to GPU:"
  echo "  1. Install NVIDIA driver: sudo apt install -y nvidia-driver-570"
  echo "  2. Reboot: sudo reboot"
  echo "  3. Run: ./scripts/switch_mode.sh gpu"
else
  echo "🟢 Current Mode: GPU-ACCELERATED"
  echo ""
  echo "  Execution:  GPU (NVIDIA RTX 3090)"
  echo "  Speed:      ~50+ tokens/second (fast)"
  echo "  GPU Used:   Yes (GPU_DEVICE_COUNT=$GPU_COUNT)"
  echo "  Driver:     NVIDIA 570"
  echo "  Status:     ✅ Working"
  echo ""
  if command -v nvidia-smi &> /dev/null; then
    echo "GPU Status:"
    nvidia-smi --query-gpu=name,memory.total,memory.used,temperature.gpu --format=csv,noheader | while read line; do
      echo "  $line"
    done
  fi
  echo ""
  echo "To switch to CPU:"
  echo "  ./scripts/switch_mode.sh cpu"
fi

echo ""
echo "Service Status:"
docker compose ps --format "table {{.Service}}\t{{.Status}}" 2>/dev/null || echo "  (Docker services not running)"
echo ""
