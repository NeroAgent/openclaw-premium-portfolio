#!/usr/bin/env python3
"""
ollama embed — Generate embeddings.
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
    parser = argparse.ArgumentParser(description="Generate embeddings with Ollama")
    parser.add_argument("model", help="Model name (must support embeddings)")
    parser.add_argument("text", help="Text to embed")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    ollama = find_ollama_bin()
    if not ollama:
        print("[ERROR] ollama binary not found", file=sys.stderr)
        return 1

    cmd = [ollama, "embed", args.model, args.text]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"[ERROR] {result.stderr}", file=sys.stderr)
            return 1

        if args.output == "json":
            # Output likely a JSON array of floats
            try:
                embedding = json.loads(result.stdout)
                print(json.dumps({"embedding": embedding, "dimensions": len(embedding)}, indent=2))
            except:
                print(result.stdout)
        else:
            print(result.stdout[:200] + "...")  # truncate for display
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
