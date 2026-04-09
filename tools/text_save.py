#!/usr/bin/env python3
"""
Step 1: Save Tim Cook's response text to a file.

Usage:
    python3 text_save.py --text "We believe deeply in privacy."
    python3 text_save.py --text "..." --output /tmp/cook_response.txt
"""

import argparse
import os
import sys


DEFAULT_OUTPUT = "/tmp/cook_response.txt"


def main():
    parser = argparse.ArgumentParser(description="Save Cook response text to file")
    parser.add_argument("--text", type=str, required=True, help="Response text to save")
    parser.add_argument("--output", "-o", type=str, default=DEFAULT_OUTPUT,
                        help=f"Output text file path (default: {DEFAULT_OUTPUT})")
    args = parser.parse_args()

    if not args.text.strip():
        print("[ERROR] Empty text input.")
        sys.exit(1)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(args.text)

    print(f"[TEXT] Saved {len(args.text)} chars to {args.output}")


if __name__ == "__main__":
    main()
