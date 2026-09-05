#!/bin/bash
# scripts/check_docker_gpu.sh
# Check if Docker can access NVIDIA GPU

echo "=== Docker GPU Capability Check ==="
echo ""

echo "1. NVIDIA Container Toolkit version:"
if command -v nvidia-container-cli &>/dev/null; then
    nvidia-container-cli --version
else
    echo "   nvidia-container-cli not found (install nvidia-container-toolkit)"
fi

echo ""
echo "2. Docker NVIDIA runtime availability:"
if docker info 2>/dev/null | grep -q "nvidia"; then
    echo "   ✓ NVIDIA runtime found in Docker"
    docker info 2>/dev/null | grep -i nvidia
else
    echo "   ✗ NVIDIA runtime NOT found in Docker"
fi

echo ""
echo "3. Test container with GPU flag:"
if docker run --rm --gpus all nvidia/cuda:12.0-base-ubuntu22.04 nvidia-smi 2>&1; then
    echo "✓ Docker GPU access SUCCESS"
else
    echo "✗ Docker GPU access FAILED (GPU not available or toolkit not installed)"
    echo "  Fix: sudo apt-get install -y nvidia-container-toolkit && sudo systemctl restart docker"
fi

echo ""
echo "4. Ollama container GPU status:"
if docker ps --format '{{.Names}}' 2>/dev/null | grep -q ollama; then
    OLLAMA_CONTAINER=$(docker ps --format '{{.Names}}' | grep ollama | head -1)
    echo "   Container: $OLLAMA_CONTAINER"
    docker exec "$OLLAMA_CONTAINER" nvidia-smi 2>&1 | head -10 || \
        echo "   nvidia-smi not available in Ollama container (CPU-only mode)"
else
    echo "   Ollama container not running"
fi
