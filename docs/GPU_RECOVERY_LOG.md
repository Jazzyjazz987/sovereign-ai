# GPU Diagnostic Report

**Timestamp:** Sat Sep  5 09:37:37 UTC 2026

## 1. GPU Hardware Detection
```
No NVIDIA GPU detected via lspci
```

## 2. NVIDIA Driver Packages
```
No nvidia-driver packages installed
```

## 3. Kernel Modules (nvidia)
```
nvidia module not loaded
```

## 4. nvidia-smi Status
```
./scripts/diagnose_gpu.sh: line 31: nvidia-smi: command not found
nvidia-smi failed or not installed
```

## 5. DKMS Status (nvidia)
```
No DKMS status for nvidia (dkms may not be installed)
```

## 6. Secure Boot Status
```
./scripts/diagnose_gpu.sh: line 41: mokutil: command not found
mokutil not available
```

## 7. Container Runtime GPU Support
```
No NVIDIA runtime in Docker info
```

## Recovery Status

**STATUS: GPU UNAVAILABLE** - Running in CPU-only mode

### Recommended Recovery Steps
1. Check kernel module: `sudo modprobe nvidia`
2. Rebuild DKMS: `sudo dkms autoinstall`
3. Verify Secure Boot is disabled (prevents unsigned module loading)
4. If no GPU hardware: continue with CPU-only mode (OLLAMA_CPU_ONLY=1)
