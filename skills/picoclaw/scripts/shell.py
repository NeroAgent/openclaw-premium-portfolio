#!/usr/bin/env python3
"""
picoclaw shell — Interactive REPL for picoclaw.
"""

import argparse
import os
import subprocess
import sys

def find_picoclaw_bin():
    bin_path = os.environ.get("PICOCLAW_BIN", "picoclaw")
    for path in [f"{os.environ.get('HOME')}/.local/bin/picoclaw", "/usr/local/bin/picoclaw"]:
        if os.path.isfile(path):
            return path
    return None

def main():
    parser = argparse.ArgumentParser(description="Start picoclaw interactive shell")
    args = parser.parse_args()

    picoclaw = find_picoclaw_bin()
    if not picoclaw:
        print("[ERROR] picoclaw binary not found", file=sys.stderr)
        return 1

    try:
        # Run picoclaw in interactive mode (if supported)
        subprocess.run([picoclaw, "shell"])
        return 0
    except KeyboardInterrupt:
        print("\n[INFO] Exit")
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
