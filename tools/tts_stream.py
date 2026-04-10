#!/usr/bin/env python3
"""
Combined Step 2+3: Synthesize speech AND play simultaneously (streaming).

Uses sounddevice to write audio chunks directly to the system audio output
as they are generated — no temp files, no subprocess spawning, no gaps.

Usage:
    python3 tts_stream.py --text-file /tmp/cook_response.txt
    python3 tts_stream.py --text "Hello, this is Tim Cook."
    python3 tts_stream.py --text-file /tmp/cook_response.txt --save output/response.wav
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
    required = ["voxcpm", "soundfile", "numpy", "sounddevice"]
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
    from huggingface_hub import try_to_load_from_cache
    result = try_to_load_from_cache(MODEL_ID, "config.json")
    return result is not None and not isinstance(result, type(None))


def download_model_if_needed():
    try:
        cached = check_model_available()
    except Exception:
        cached = False

    if cached:
        print("[MODEL] VoxCPM2 already cached.")
    else:
        print("[MODEL] Downloading VoxCPM2 (~4GB)...")
        from huggingface_hub import snapshot_download
        snapshot_download(MODEL_ID)
        print("[MODEL] Download complete.")


def load_model():
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


def stream_and_play(model, text, save_path=None, timesteps=6):
    """Generate speech in streaming mode, playing via sounddevice output stream."""
    import numpy as np
    import sounddevice as sd

    ref_audio = str(REFERENCE_AUDIO)
    if not os.path.exists(ref_audio):
        print(f"[ERROR] Reference audio not found: {ref_audio}")
        sys.exit(1)

    sr = model.tts_model.sample_rate
    all_chunks = []
    chunk_idx = 0
    t0 = time.time()

    print(f"[STREAM] Starting streaming synthesis (timesteps={timesteps})...")

    # Open a continuous audio output stream — no gaps between chunks
    stream = sd.OutputStream(samplerate=sr, channels=1, dtype="float32")
    stream.start()

    try:
        for chunk in model.generate_streaming(
            text=text,
            reference_wav_path=ref_audio,
            cfg_value=2.0,
            inference_timesteps=timesteps,
        ):
            chunk_idx += 1
            chunk_duration = len(chunk) / sr

            if chunk_idx == 1:
                first_chunk_time = time.time() - t0
                print(f"[STREAM] First audio in {first_chunk_time:.1f}s "
                      f"({chunk_duration:.1f}s of audio)")

            all_chunks.append(chunk)

            # Write directly to audio output buffer — seamless, no gaps
            audio_data = chunk.astype(np.float32).reshape(-1, 1)
            stream.write(audio_data)

    finally:
        # Wait for remaining audio in buffer to finish playing
        stream.stop()
        stream.close()

    total_time = time.time() - t0
    full_wav = np.concatenate(all_chunks)
    total_duration = len(full_wav) / sr

    print(f"[STREAM] Done: {total_duration:.1f}s audio, "
          f"{chunk_idx} chunks, {total_time:.1f}s total")

    # Always save the complete audio
    if not save_path:
        os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        save_path = str(DEFAULT_OUTPUT_DIR / f"cook_tts_{timestamp}.wav")

    import soundfile as sf
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
    sf.write(save_path, full_wav, sr)
    print(f"[STREAM] Saved to {save_path}")
    print(f"[OUTPUT] {save_path}")

    return total_duration


def main():
    os.environ["TQDM_DISABLE"] = "1"

    parser = argparse.ArgumentParser(
        description="Stream Cook voice: synthesize and play simultaneously")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Text to synthesize")
    group.add_argument("--text-file", type=str, help="Path to text file")
    parser.add_argument("--save", "-s", type=str, default=None,
                        help="Save complete audio to this path (optional)")
    parser.add_argument("--max-words", type=int, default=500,
                        help="Max words for TTS (default: 500)")
    parser.add_argument("--timesteps", type=int, default=6,
                        help="Diffusion steps (default: 6, range: 4-30)")
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

    check_dependencies()
    download_model_if_needed()
    model = load_model()
    stream_and_play(model, text, save_path=args.save, timesteps=args.timesteps)

    print("[STREAM] Complete.")


if __name__ == "__main__":
    main()
