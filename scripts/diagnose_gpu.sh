#!/bin/bash
# scripts/diagnose_gpu.sh
set -e

echo "=== GPU Diagnostic Report ===" > /tmp/gpu_diag.log
echo "Timestamp: $(date)" >> /tmp/gpu_diag.log
echo "" >> /tmp/gpu_diag.log

echo "1. Checking GPU hardware:" >> /tmp/gpu_diag.log
lspci | grep -i nvidia >> /tmp/gpu_diag.log || echo "No GPU detected" >> /tmp/gpu_diag.log

echo "" >> /tmp/gpu_diag.log
echo "2. NVIDIA drivers installed:" >> /tmp/gpu_diag.log
dpkg -l | grep nvidia-driver >> /tmp/gpu_diag.log || echo "No nvidia-driver packages" >> /tmp/gpu_diag.log

echo "" >> /tmp/gpu_diag.log
echo "3. Kernel modules (nvidia):" >> /tmp/gpu_diag.log
lsmod | grep nvidia >> /tmp/gpu_diag.log || echo "nvidia module not loaded" >> /tmp/gpu_diag.log

echo "" >> /tmp/gpu_diag.log
echo "4. nvidia-smi status:" >> /tmp/gpu_diag.log
nvidia-smi >> /tmp/gpu_diag.log 2>&1 || echo "nvidia-smi failed" >> /tmp/gpu_diag.log

echo "" >> /tmp/gpu_diag.log
echo "5. DKMS status (nvidia):" >> /tmp/gpu_diag.log
dkms status | grep nvidia >> /tmp/gpu_diag.log 2>&1 || echo "No DKMS status for nvidia" >> /tmp/gpu_diag.log

echo "" >> /tmp/gpu_diag.log
echo "6. Secure Boot status:" >> /tmp/gpu_diag.log
mokutil --sb-state >> /tmp/gpu_diag.log 2>&1 || echo "mokutil not available" >> /tmp/gpu_diag.log

cat /tmp/gpu_diag.log
cat /tmp/gpu_diag.log > docs/GPU_RECOVERY_LOG.md
