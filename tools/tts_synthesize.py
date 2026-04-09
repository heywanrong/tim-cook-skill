#!/usr/bin/env python3
"""
Step 2: Synthesize speech from text using VoxCPM2 + Cook reference audio.

Reads text from a file, generates a WAV file, and prints the output path.
Does NOT play the audio — that is handled by audio_play.py.

Usage:
    python3 tts_synthesize.py --text-file /tmp/cook_response.txt
    python3 tts_synthesize.py --text-file /tmp/cook_response.txt --output /path/to/out.wav
    python3 tts_synthesize.py --text "Hello, this is Tim Cook."
"""

import argparse
import contextlib
import io
import os
import re
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
REFERENCE_AUDIO = SKILL_DIR / "cook.wav"
DEFAULT_OUTPUT_DIR = SKILL_DIR / "output"
MODEL_ID = "openbmb/VoxCPM2"


def check_dependencies():
    """Check and install required Python packages."""
    required = ["voxcpm", "soundfile", "numpy"]
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"[ENV] Installing missing packages: {', '.join(missing)}")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install"] + missing,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("[ENV] Installation complete.")


def check_model_available():
    """Check if VoxCPM2 model is already cached locally."""
    from huggingface_hub import try_to_load_from_cache
    result = try_to_load_from_cache(MODEL_ID, "config.json")
    if result is None or isinstance(result, type(None)):
        return False
    return True


def download_model_if_needed():
    """Download VoxCPM2 model if not already cached."""
    try:
        cached = check_model_available()
    except Exception:
        cached = False

    if cached:
        print(f"[MODEL] VoxCPM2 already cached, skipping download.")
    else:
        print(f"[MODEL] VoxCPM2 not found locally. Downloading from HuggingFace...")
        print(f"[MODEL] This may take a while on first run (~4GB)...")
        from huggingface_hub import snapshot_download
        snapshot_download(MODEL_ID)
        print(f"[MODEL] Download complete.")


def load_model():
    """Load VoxCPM2 model (suppress library debug output)."""
    from voxcpm import VoxCPM

    print("[TTS] Loading model...")
    t0 = time.time()
    with contextlib.redirect_stderr(io.StringIO()):
        model = VoxCPM.from_pretrained(
            hf_model_id=MODEL_ID,
            load_denoiser=False,
            optimize=True,
        )
    print(f"[TTS] Model loaded in {time.time() - t0:.1f}s")
    return model


def truncate_text(text, max_words):
    """Truncate text to max_words at the nearest sentence boundary."""
    cjk_chars = len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', text))
    is_cjk = cjk_chars > len(text) * 0.3

    if is_cjk:
        if len(text) <= max_words:
            return text
        truncated = text[:max_words]
        for sep in ['。', '！', '？', '；', '\n']:
            idx = truncated.rfind(sep)
            if idx > max_words * 0.5:
                truncated = truncated[:idx + 1]
                break
        print(f"[TTS] Text truncated from {len(text)} to {len(truncated)} chars")
        return truncated
    else:
        words = text.split()
        if len(words) <= max_words:
            return text
        truncated = ' '.join(words[:max_words])
        for sep in ['. ', '! ', '? ', '.\n', '\n']:
            idx = truncated.rfind(sep)
            if idx > len(truncated) * 0.5:
                truncated = truncated[:idx + len(sep.rstrip())]
                break
        print(f"[TTS] Text truncated from {len(words)} to ~{len(truncated.split())} words")
        return truncated


def generate_speech(model, text, output_path):
    """Generate speech using VoxCPM2 with Cook's voice as reference."""
    import soundfile as sf

    ref_audio = str(REFERENCE_AUDIO)
    if not os.path.exists(ref_audio):
        print(f"[ERROR] Reference audio not found: {ref_audio}")
        sys.exit(1)

    print(f"[TTS] Synthesizing speech...")
    t0 = time.time()
    wav = model.generate(
        text=text,
        reference_wav_path=ref_audio,
        cfg_value=2.0,
        inference_timesteps=10,
    )
    elapsed = time.time() - t0
    sr = model.tts_model.sample_rate
    duration = len(wav) / sr

    print(f"[TTS] Generated {duration:.1f}s audio in {elapsed:.1f}s")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    sf.write(output_path, wav, sr)
    print(f"[TTS] Saved to {output_path}")

    return output_path, duration


def generate_output_path(output_arg):
    """Generate a timestamped output path if none specified."""
    if output_arg:
        return output_arg
    os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return str(DEFAULT_OUTPUT_DIR / f"cook_tts_{timestamp}.wav")


def main():
    os.environ["TQDM_DISABLE"] = "1"

    parser = argparse.ArgumentParser(description="Synthesize Cook voice via VoxCPM2")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Text to synthesize")
    group.add_argument("--text-file", type=str, help="Path to text file to synthesize")
    parser.add_argument("--output", "-o", type=str, default=None, help="Output wav path")
    parser.add_argument("--max-words", type=int, default=500,
                        help="Max words for TTS (default: 500)")
    args = parser.parse_args()

    if args.text_file:
        with open(args.text_file, "r", encoding="utf-8") as f:
            text = f.read().strip()
    else:
        text = args.text

    if not text:
        print("[ERROR] Empty text input.")
        sys.exit(1)

    text = truncate_text(text, args.max_words)
    output_path = generate_output_path(args.output)

    check_dependencies()
    download_model_if_needed()
    model = load_model()
    generate_speech(model, text, output_path)

    # Print output path on last line for downstream parsing
    print(f"[OUTPUT] {output_path}")


if __name__ == "__main__":
    main()
