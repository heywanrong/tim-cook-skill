#!/usr/bin/env python3
"""
Combined Step 2+3: Synthesize speech with progress, then play seamlessly.

Uses streaming synthesis for progress feedback, then plays the complete
audio in one pass via sounddevice — zero stuttering guaranteed.

On fast GPUs (RTF < 1), use --live for true real-time streaming playback.

Usage:
    python3 tts_stream.py --text-file /tmp/cook_response.txt
    python3 tts_stream.py --text "Hello, this is Tim Cook."
    python3 tts_stream.py --text-file /tmp/cook_response.txt --save output/response.wav
    python3 tts_stream.py --text-file /tmp/cook_response.txt --live  # real-time streaming
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


def synthesize_with_progress(model, text, timesteps=6):
    """Streaming synthesis with progress — returns complete audio array."""
    import numpy as np

    ref_audio = str(REFERENCE_AUDIO)
    if not os.path.exists(ref_audio):
        print(f"[ERROR] Reference audio not found: {ref_audio}")
        sys.exit(1)

    sr = model.tts_model.sample_rate
    all_chunks = []
    total_samples = 0
    chunk_idx = 0
    t0 = time.time()

    print(f"[TTS] Synthesizing (timesteps={timesteps})...")

    for chunk in model.generate_streaming(
        text=text,
        reference_wav_path=ref_audio,
        cfg_value=2.0,
        inference_timesteps=timesteps,
    ):
        chunk_idx += 1
        all_chunks.append(chunk)
        total_samples += len(chunk)
        duration_so_far = total_samples / sr
        elapsed = time.time() - t0
        print(f"\r[TTS] {duration_so_far:.1f}s audio generated ({elapsed:.0f}s elapsed, "
              f"chunk {chunk_idx})", end="", flush=True)

    print()  # newline after progress

    full_wav = np.concatenate(all_chunks)
    total_duration = len(full_wav) / sr
    total_time = time.time() - t0

    print(f"[TTS] Synthesis done: {total_duration:.1f}s audio in {total_time:.1f}s "
          f"(RTF={total_time / total_duration:.2f})")

    return full_wav, sr


def play_seamless(wav, sr):
    """Play audio in one pass — zero stuttering."""
    import sounddevice as sd

    duration = len(wav) / sr
    print(f"[PLAY] Playing {duration:.1f}s audio...")
    sd.play(wav, sr)
    sd.wait()
    print(f"[PLAY] Done.")


def synthesize_and_play_live(model, text, timesteps=6):
    """True streaming: play chunks as they arrive. May stutter if RTF > 1."""
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

    print(f"[LIVE] Streaming synthesis + playback (timesteps={timesteps})...")
    print(f"[LIVE] Note: may stutter if synthesis is slower than real-time (RTF > 1)")

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
            all_chunks.append(chunk)

            if chunk_idx == 1:
                print(f"[LIVE] First audio in {time.time() - t0:.1f}s")

            audio_data = chunk.astype(np.float32).reshape(-1, 1)
            stream.write(audio_data)
    finally:
        stream.stop()
        stream.close()

    full_wav = np.concatenate(all_chunks)
    total_duration = len(full_wav) / sr
    print(f"[LIVE] Done: {total_duration:.1f}s audio, {chunk_idx} chunks, "
          f"{time.time() - t0:.1f}s total")

    return full_wav, sr


def save_audio(wav, sr, save_path=None):
    """Save audio to file."""
    import soundfile as sf

    if not save_path:
        os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        save_path = str(DEFAULT_OUTPUT_DIR / f"cook_tts_{timestamp}.wav")

    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
    sf.write(save_path, wav, sr)
    print(f"[TTS] Saved to {save_path}")
    print(f"[OUTPUT] {save_path}")
    return save_path


def main():
    os.environ["TQDM_DISABLE"] = "1"

    parser = argparse.ArgumentParser(
        description="Synthesize Cook voice and play seamlessly")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Text to synthesize")
    group.add_argument("--text-file", type=str, help="Path to text file")
    parser.add_argument("--save", "-s", type=str, default=None,
                        help="Custom save path (default: auto-save to output/)")
    parser.add_argument("--max-words", type=int, default=500,
                        help="Max words for TTS (default: 500)")
    parser.add_argument("--timesteps", type=int, default=6,
                        help="Diffusion steps (default: 6, range: 4-30)")
    parser.add_argument("--live", action="store_true",
                        help="True real-time streaming (may stutter if RTF > 1)")
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

    if args.live:
        wav, sr = synthesize_and_play_live(model, text, timesteps=args.timesteps)
    else:
        wav, sr = synthesize_with_progress(model, text, timesteps=args.timesteps)
        play_seamless(wav, sr)

    save_audio(wav, sr, save_path=args.save)
    print("[STREAM] Complete.")


if __name__ == "__main__":
    main()
