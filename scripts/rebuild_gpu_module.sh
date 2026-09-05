#!/bin/bash
# scripts/rebuild_gpu_module.sh
# Non-interactive GPU module rebuild for NVIDIA driver

set -e

echo "=== NVIDIA DKMS Module Rebuild ==="

# Check current status
echo "1. Checking DKMS status..."
dkms status | grep nvidia || echo "No DKMS entry found"

# Check kernel version
KERNEL_VERSION=$(uname -r)
echo "2. Current kernel: $KERNEL_VERSION"

# Check if driver is installed
NVIDIA_DRIVER=$(dpkg -l | grep "nvidia-driver-" | grep -oP 'nvidia-driver-\K[0-9]+' | head -1)
if [ -z "$NVIDIA_DRIVER" ]; then
  echo "ERROR: No nvidia-driver package found"
  exit 1
fi
echo "3. Driver version: nvidia-driver-$NVIDIA_DRIVER"

# Try to rebuild module (requires sudo)
echo "4. Checking if rebuild is needed..."
if dkms status | grep -q "installed"; then
  echo "✓ DKMS module already built and installed"
  exit 0
else
  echo "⚠ DKMS module needs rebuild"
  echo "   Attempting rebuild (this requires sudo)..."
  echo "   Command: sudo dkms install -m nvidia -v $(dkms status | grep nvidia | grep -oP '\K[0-9.]+' | head -1) -k $KERNEL_VERSION"
  echo "   OR run: sudo dkms autoinstall"
  exit 2  # Exit code 2 = needs sudo intervention
fi
