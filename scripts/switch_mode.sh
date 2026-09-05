#!/bin/bash
# Sovereign AI Stack — CPU/GPU Mode Switcher
# Usage: ./scripts/switch_mode.sh [cpu|gpu]

set -e

cd "$(dirname "$0")/.."

MODE="${1:-}"

if [[ -z "$MODE" ]]; then
  echo "Usage: $0 [cpu|gpu]"
  echo ""
  echo "Example:"
  echo "  $0 cpu    # Switch to CPU-only mode (slow, always works)"
  echo "  $0 gpu    # Switch to GPU mode (fast, requires NVIDIA driver)"
  exit 1
fi

if [[ "$MODE" != "cpu" && "$MODE" != "gpu" ]]; then
  echo "❌ Invalid mode: $MODE"
  echo "Use 'cpu' or 'gpu'"
  exit 1
fi

echo "🔄 Switching to $MODE mode..."
echo ""

case "$MODE" in
  cpu)
    echo "📋 Configuration:"
    echo "  • Execution: CPU-only"
    echo "  • Speed: ~7 t/s (slow)"
    echo "  • Driver: Not required"
    echo "  • Status: ✅ Works everywhere"
    echo ""

    # Update .env.mode
    sed -i 's/^EXECUTION_MODE=.*/EXECUTION_MODE=cpu/' .env.mode
    sed -i 's/^OLLAMA_CPU_ONLY=.*/OLLAMA_CPU_ONLY=1/' .env.mode
    sed -i 's/^GPU_DEVICE_COUNT=.*/GPU_DEVICE_COUNT=0/' .env.mode

    echo "✏️ Updated .env.mode with CPU settings"
    echo ""

    # Stop and restart
    echo "⏹️ Stopping services..."
    docker compose down 2>/dev/null || true
    sleep 2

    echo "🚀 Starting in CPU mode..."
    export OLLAMA_CPU_ONLY=1
    export GPU_DEVICE_COUNT=0
    docker compose up -d

    echo ""
    echo "✅ CPU mode enabled"
    echo "   Wait 30-60s for Ollama to load models"
    echo "   Then test: curl -X POST http://localhost:8888/query -d '{\"query\":\"Bonjour\",\"complexity\":1.0}'"
    ;;

  gpu)
    echo "📋 Configuration:"
    echo "  • Execution: GPU-accelerated"
    echo "  • Speed: ~50+ t/s (fast)"
    echo "  • Driver: NVIDIA 570 required"
    echo "  • Status: ⚠️ Requires manual driver installation"
    echo ""

    # Check if GPU available
    if ! command -v nvidia-smi &> /dev/null; then
      echo "⚠️ NVIDIA driver not found!"
      echo ""
      echo "To install NVIDIA driver 570:"
      echo "  sudo apt update && sudo apt install -y nvidia-driver-570"
      echo "  sudo reboot"
      echo "  nvidia-smi  # Verify installation"
      echo ""
      echo "Then run: $0 gpu"
      exit 1
    fi

    echo "✅ NVIDIA driver detected!"
    nvidia-smi --query-gpu=name --format=csv,noheader
    echo ""

    # Update .env.mode
    sed -i 's/^EXECUTION_MODE=.*/EXECUTION_MODE=gpu/' .env.mode
    sed -i 's/^OLLAMA_CPU_ONLY=.*/OLLAMA_CPU_ONLY=0/' .env.mode
    sed -i 's/^GPU_DEVICE_COUNT=.*/GPU_DEVICE_COUNT=1/' .env.mode

    echo "✏️ Updated .env.mode with GPU settings"
    echo ""

    # Stop and restart
    echo "⏹️ Stopping services..."
    docker compose down 2>/dev/null || true
    sleep 2

    echo "🚀 Starting in GPU mode..."
    export OLLAMA_CPU_ONLY=0
    export GPU_DEVICE_COUNT=1
    docker compose up -d

    echo ""
    echo "✅ GPU mode enabled"
    echo "   Wait 30-60s for Ollama to load models on GPU"
    echo "   Monitor GPU: watch -n 2 nvidia-smi"
    echo "   Test: curl -X POST http://localhost:8888/query -d '{\"query\":\"Bonjour\",\"complexity\":1.0}'"
    ;;
esac

echo ""
echo "📊 Current Mode: $(grep '^EXECUTION_MODE=' .env.mode | cut -d= -f2)"
echo ""
