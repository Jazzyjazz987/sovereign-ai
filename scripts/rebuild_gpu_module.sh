#!/bin/bash
# scripts/rebuild_gpu_module.sh
# Non-interactive GPU module rebuild helper for NVIDIA driver

set -e

echo "=== NVIDIA DKMS Module Rebuild ==="

# 1. Check current DKMS status
echo "1. Checking DKMS status..."
if ! command -v dkms &>/dev/null; then
    echo "   dkms not installed. Install with: sudo apt-get install dkms"
    exit 1
fi
dkms status | grep nvidia || echo "   No DKMS entry found for nvidia"

# 2. Check kernel version
KERNEL_VERSION=$(uname -r)
echo "2. Current kernel: $KERNEL_VERSION"

# 3. Check if driver package is installed
NVIDIA_DRIVER=$(dpkg -l 2>/dev/null | grep "nvidia-driver-" | grep -oP 'nvidia-driver-\K[0-9]+' | head -1)
if [ -z "$NVIDIA_DRIVER" ]; then
    echo "ERROR: No nvidia-driver package found"
    echo "Install with: sudo apt-get install nvidia-driver-<version>"
    exit 1
fi
echo "3. Driver version: nvidia-driver-$NVIDIA_DRIVER"

# 4. Check if rebuild is needed
echo "4. Checking if rebuild is needed..."
if dkms status 2>/dev/null | grep -q "installed"; then
    echo "✓ DKMS module already built and installed"
    echo "  Verifying nvidia-smi..."
    nvidia-smi && echo "✓ GPU fully operational" || echo "⚠ Module installed but nvidia-smi failed"
    exit 0
else
    echo "⚠ DKMS module needs rebuild"
    echo "  Rebuild command (requires sudo):"
    NVIDIA_VERSION=$(dkms status 2>/dev/null | grep nvidia | grep -oP 'nvidia/\K[0-9.]+' | head -1)
    if [ -n "$NVIDIA_VERSION" ]; then
        echo "    sudo dkms install -m nvidia -v $NVIDIA_VERSION -k $KERNEL_VERSION"
    else
        echo "    sudo dkms autoinstall"
    fi
    echo "  After rebuild, load module:"
    echo "    sudo modprobe nvidia"
    exit 2  # Exit code 2 = needs sudo intervention
fi
