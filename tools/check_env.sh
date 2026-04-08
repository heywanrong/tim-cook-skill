#!/bin/bash
# Tim Cook TTS Environment Check
# Verifies all dependencies for VoxCPM2 voice synthesis

set -e

echo "=== Tim Cook TTS Environment Check ==="
echo ""

# 1. Python version
echo "[1/5] Python version..."
PYTHON_VERSION=$(python3 --version 2>&1)
echo "  $PYTHON_VERSION"
PYTHON_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
if [ "$PYTHON_MINOR" -lt 10 ]; then
    echo "  ERROR: Python >= 3.10 required"
    exit 1
fi
echo "  OK"

# 2. CUDA
echo "[2/5] CUDA availability..."
python3 -c "
import torch
if torch.cuda.is_available():
    print(f'  CUDA {torch.version.cuda} — {torch.cuda.get_device_name(0)}')
    print(f'  VRAM: {torch.cuda.get_device_properties(0).total_mem / 1024**3:.1f} GB')
elif torch.backends.mps.is_available():
    print('  MPS (Apple Silicon) available')
else:
    print('  WARNING: No GPU detected. CPU inference will be very slow.')
" 2>/dev/null || echo "  WARNING: PyTorch not installed yet. Run: pip install torch"

# 3. Key packages
echo "[3/5] Required packages..."
for pkg in voxcpm soundfile numpy torch torchaudio; do
    if python3 -c "import $pkg" 2>/dev/null; then
        ver=$(python3 -c "import $pkg; print(getattr($pkg, '__version__', 'ok'))" 2>/dev/null)
        echo "  $pkg: $ver"
    else
        echo "  $pkg: NOT INSTALLED"
    fi
done

# 4. Reference audio
echo "[4/5] Reference audio..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REF_AUDIO="$SCRIPT_DIR/../cook.wav"
if [ -f "$REF_AUDIO" ]; then
    echo "  cook.wav found: $(du -h "$REF_AUDIO" | cut -f1)"
else
    echo "  ERROR: cook.wav not found at $REF_AUDIO"
    exit 1
fi

# 5. Model cache
echo "[5/5] VoxCPM2 model cache..."
python3 -c "
from huggingface_hub import try_to_load_from_cache
result = try_to_load_from_cache('openbmb/VoxCPM2', 'config.json')
if result and not isinstance(result, type(None)):
    print('  VoxCPM2 model cached')
else:
    print('  VoxCPM2 not yet downloaded (will download on first run)')
" 2>/dev/null || echo "  Cannot check (huggingface_hub not installed)"

echo ""
echo "=== Check Complete ==="
