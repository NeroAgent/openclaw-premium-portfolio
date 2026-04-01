#!/usr/bin/env python3
"""
ollama list-models — Show downloaded models.
"""

import argparse
import json
import os
import subprocess
import sys

def find_ollama_bin():
    bin_path = os.environ.get("OLLAMA_BIN", "ollama")
    # Check if in PATH
    try:
        subprocess.run([bin_path, "--version"], capture_output=True, timeout=2)
        return bin_path
    except:
        # Try common locations
        for path in [f"{os.environ.get('HOME')}/.local/bin/ollama", "/usr/local/bin/ollama"]:
            if os.path.isfile(path):
                return path
        return None

def main():
    parser = argparse.ArgumentParser(description="List downloaded Ollama models")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    ollama = find_ollama_bin()
    if not ollama:
        print("[ERROR] ollama binary not found. Install from https://ollama.com/download", file=sys.stderr)
        return 1

    try:
        result = subprocess.run([ollama, "list"], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print(f"[ERROR] {result.stderr}", file=sys.stderr)
            return 1
        lines = result.stdout.strip().split("\n")[1:]  # skip header
        models = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 3:
                name = parts[0]
                size_gb = parts[1] if len(parts) == 3 else " ".join(parts[1:-1])
                modified = parts[-1]
                models.append({"name": name, "size": size_gb, "modified": modified})
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

    if args.output == "json":
        print(json.dumps({"models": models}, indent=2))
        return 0

    print(f"📦 Downloaded models ({len(models)}):\n")
    for m in models:
        print(f"  {m['name']}")
        print(f"    Size: {m['size']}")
        print(f"    Modified: {m['modified']}")
        print()
    return 0

if __name__ == "__main__":
    sys.exit(main())
