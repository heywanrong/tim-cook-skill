#!/usr/bin/env python3
"""
Combined Step 2+3: Synthesize speech and play with pre-buffering.

Default mode: pre-buffers ~15s of audio, then starts playback while
synthesis continues in background. Smooth playback even when RTF > 1.

Usage:
    python3 tts_stream.py --text-file /tmp/cook_response.txt
    python3 tts_stream.py --text "Hello, this is Tim Cook."
    python3 tts_stream.py --text-file /tmp/cook_response.txt --save output/response.wav
    python3 tts_stream.py --text-file /tmp/cook_response.txt --prebuffer 20
"""

import argparse
import contextlib
import io
import os
import queue
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
REFERENCE_AUDIO = SKILL_DIR / "cook.wav"
DEFAULT_OUTPUT_DIR = SKILL_DIR / "output"
MODEL_ID = "openbmb/VoxCPM2"


def check_dependencies():
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
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
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
            hf_model_id=MODEL_ID, load_denoiser=False, optimize=True,
        )
    print(f"[TTS] Model loaded in {time.time() - t0:.1f}s")
    return model


def truncate_text(text, max_words):
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


def stream_with_prebuffer(model, text, timesteps=6, prebuffer_secs=15):
    """Pre-buffer audio, then play while synthesis continues in background."""
    import numpy as np
    import sounddevice as sd

    ref_audio = str(REFERENCE_AUDIO)
    if not os.path.exists(ref_audio):
        print(f"[ERROR] Reference audio not found: {ref_audio}")
        sys.exit(1)

    sr = model.tts_model.sample_rate
    audio_queue = queue.Queue()
    all_chunks = []
    t0 = time.time()

    # --- Synthesis runs in background thread ---
    def synthesis_worker():
        for chunk in model.generate_streaming(
            text=text,
            reference_wav_path=ref_audio,
            cfg_value=2.0,
            inference_timesteps=timesteps,
        ):
            chunk_f32 = chunk.astype(np.float32)
            all_chunks.append(chunk_f32)
            audio_queue.put(chunk_f32)
        audio_queue.put(None)  # sentinel: done

    synth_thread = threading.Thread(target=synthesis_worker, daemon=True)
    synth_thread.start()

    # --- Pre-buffer phase ---
    target_samples = int(prebuffer_secs * sr)
    buffered_samples = 0
    prebuffer_chunks = []
    synthesis_finished_early = False

    print(f"[TTS] Synthesizing (timesteps={timesteps}), "
          f"pre-buffering {prebuffer_secs}s before playback...")

    while buffered_samples < target_samples:
        chunk = audio_queue.get()
        if chunk is None:
            synthesis_finished_early = True
            break
        prebuffer_chunks.append(chunk)
        buffered_samples += len(chunk)
        print(f"\r[TTS] Buffered {buffered_samples / sr:.1f}s / {prebuffer_secs}s "
              f"({time.time() - t0:.0f}s elapsed)", end="", flush=True)

    print()
    print(f"[PLAY] Starting playback ({buffered_samples / sr:.1f}s buffered)...")

    # --- Playback: pre-buffered chunks first, then live ---
    stream = sd.OutputStream(samplerate=sr, channels=1, dtype="float32",
                             blocksize=4096)
    stream.start()

    try:
        for chunk in prebuffer_chunks:
            stream.write(chunk.reshape(-1, 1))

        if not synthesis_finished_early:
            while True:
                chunk = audio_queue.get()
                if chunk is None:
                    break
                stream.write(chunk.reshape(-1, 1))
    finally:
        stream.stop()
        stream.close()

    synth_thread.join()

    total_time = time.time() - t0
    full_wav = np.concatenate(all_chunks)
    total_duration = len(full_wav) / sr

    print(f"[TTS] Done: {total_duration:.1f}s audio, {len(all_chunks)} chunks, "
          f"{total_time:.1f}s total (RTF={total_time / total_duration:.2f})")

    return full_wav, sr


def save_audio(wav, sr, save_path=None):
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
        description="Synthesize Cook voice with pre-buffered playback")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Text to synthesize")
    group.add_argument("--text-file", type=str, help="Path to text file")
    parser.add_argument("--save", "-s", type=str, default=None,
                        help="Custom save path (default: auto-save to output/)")
    parser.add_argument("--max-words", type=int, default=500,
                        help="Max words for TTS (default: 500)")
    parser.add_argument("--timesteps", type=int, default=6,
                        help="Diffusion steps (default: 6, range: 4-30)")
    parser.add_argument("--prebuffer", type=int, default=30,
                        help="Seconds of audio to buffer before playback (default: 30)")
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

    wav, sr = stream_with_prebuffer(
        model, text, timesteps=args.timesteps, prebuffer_secs=args.prebuffer)

    save_audio(wav, sr, save_path=args.save)
    print("[STREAM] Complete.")


if __name__ == "__main__":
    main()
