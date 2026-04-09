#!/usr/bin/env python3
"""
Step 0: Print a one-time disclaimer before Cook starts speaking.

This runs BEFORE any response text is generated, so the disclaimer
never leaks into the text that gets sent to voice synthesis.

Usage:
    python3 disclaimer.py
"""


def main():
    print()
    print("─" * 60)
    print("  NOTE: Speaking from Tim Cook's perspective, based on")
    print("  public statements and interviews — not his actual views.")
    print("─" * 60)
    print()


if __name__ == "__main__":
    main()
