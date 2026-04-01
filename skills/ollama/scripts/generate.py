#!/usr/bin/env python3
"""
ollama generate — Generate text completion.
"""

import argparse
import json
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
    parser = argparse.ArgumentParser(description="Generate text with Ollama")
    parser.add_argument("model", help="Model name")
    parser.add_argument("prompt", help="Input prompt")
    parser.add_argument("--system", help="System prompt")
    parser.add_argument("--format", choices=["json"], help="Output format")
    parser.add_argument("--raw", action="store_true", help="Raw mode (no chat template)")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    ollama = find_ollama_bin()
    if not ollama:
        print("[ERROR] ollama binary not found", file=sys.stderr)
        return 1

    cmd = [ollama, "generate", args.model, "--prompt", args.prompt]
    if args.system:
        cmd.extend(["--system", args.system])
    if args.format:
        cmd.extend(["--format", args.format])
    if args.raw:
        cmd.append("--raw")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print(f"[ERROR] {result.stderr}", file=sys.stderr)
            return 1

        if args.output == "json" or args.format == "json":
            try:
                parsed = json.loads(result.stdout)
                print(json.dumps(parsed, indent=2))
            except:
                print(result.stdout)
        else:
            print(result.stdout)
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
