#!/usr/bin/env python3
"""
ollama rm — Remove a model.
"""

import argparse
import os
import subprocess
import sys

def find_ollama_bin():
    bin_path = os.environ.get("OLLAMA_BIN", "ollama")
    try:
        subprocess.run([bin_path, "--version"], capture_output=True, timeout=2)
        return bin_path
    except:
        for path in [f"{os.environ.get('HOME')}/.local/bin/ollama", "/usr/local/bin/ollama"]:
            if os.path.isfile(path):
                return path
        return None

def main():
    parser = argparse.ArgumentParser(description="Remove an Ollama model")
    parser.add_argument("model", help="Model name to remove")
    parser.add_argument("--confirm", action="store_true", help="Skip confirmation")
    args = parser.parse_args()

    ollama = find_ollama_bin()
    if not ollama:
        print("[ERROR] ollama binary not found", file=sys.stderr)
        return 1

    if not args.confirm:
        resp = input(f"Delete model '{args.model}'? This cannot be undone. (yes/no): ").strip().lower()
        if resp not in ("yes", "y"):
            print("Cancelled.")
            return 0

    cmd = [ollama, "rm", args.model]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print(f"[ERROR] {result.stderr}", file=sys.stderr)
            return 1
        print(f"[OK] Model {args.model} removed")
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
