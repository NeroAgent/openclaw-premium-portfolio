#!/usr/bin/env python3
"""
ollama pull — Download a model.
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
    parser = argparse.ArgumentParser(description="Pull/download an Ollama model")
    parser.add_argument("model", help="Model name (e.g., llama3.2:3b)")
    parser.add_argument("--stream", action="store_true", help="Stream download progress")
    args = parser.parse_args()

    ollama = find_ollama_bin()
    if not ollama:
        print("[ERROR] ollama binary not found", file=sys.stderr)
        return 1

    cmd = [ollama, "pull", args.model]
    if not args.stream:
        print(f"[INFO] Pulling model {args.model} (this may take a while)...")
    try:
        # Stream output to show progress
        result = subprocess.run(cmd, stdout=sys.stdout if args.stream else None, stderr=subprocess.PIPE, text=True, timeout=1800)
        if result.returncode != 0:
            print(f"[ERROR] Pull failed: {result.stderr}", file=sys.stderr)
            return 1
        if not args.stream:
            print(f"[OK] Model {args.model} downloaded")
        return 0
    except subprocess.TimeoutExpired:
        print("[ERROR] Pull timed out after 30 minutes", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
