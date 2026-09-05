#!/bin/bash
# scripts/check_docker_gpu.sh
# Check if Docker can access NVIDIA GPU

echo "=== Docker GPU Capability Check ==="

echo "1. NVIDIA Container Toolkit version:"
which nvidia-container-cli && nvidia-container-cli --version || echo "nvidia-container-cli not found"

echo ""
echo "2. Docker NVIDIA runtime:"
docker run --rm --gpus all ubuntu nvidia-smi 2>&1 | head -20 || echo "Docker GPU access failed"

echo ""
echo "3. Test container with GPU flag:"
docker run --rm --gpus=1 --entrypoint nvidia-smi ubuntu:latest || echo "Failed (GPU not available)"
