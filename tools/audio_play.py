#!/usr/bin/env python3
"""
Step 3: Play a WAV/audio file.

Usage:
    python3 audio_play.py --file /path/to/audio.wav
    python3 audio_play.py --file output/cook_tts_20260408_141622.wav
"""

import argparse
import os
import subprocess
import sys


def play_audio(filepath):
    """Play audio file via platform-native player."""
    if not os.path.exists(filepath):
        print(f"[ERROR] Audio file not found: {filepath}")
        sys.exit(1)

    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"[PLAY] Loading {filepath} ({size_mb:.1f} MB)")

    if sys.platform == "darwin":
        print("[PLAY] Playing via afplay...")
        subprocess.run(["afplay", filepath])
    elif sys.platform == "linux":
        for cmd in ["aplay", "paplay", "ffplay -nodisp -autoexit"]:
            try:
                print(f"[PLAY] Playing via {cmd.split()[0]}...")
                subprocess.run(cmd.split() + [filepath])
                break
            except FileNotFoundError:
                continue
        else:
            print(f"[PLAY] No audio player found. File saved at: {filepath}")
            return
    else:
        print(f"[PLAY] Auto-play not supported on this platform. File: {filepath}")
        return

    print("[PLAY] Done.")


def main():
    parser = argparse.ArgumentParser(description="Play an audio file")
    parser.add_argument("--file", "-f", type=str, required=True,
                        help="Path to audio file to play")
    args = parser.parse_args()

    play_audio(args.file)


if __name__ == "__main__":
    main()
