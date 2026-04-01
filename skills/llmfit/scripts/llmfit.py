#!/usr/bin/env python3
"""
llmfit — Hardware-aware LLM model selector.
"""

import argparse
import json
import os
import subprocess
import sys

def find_llmfit_bin():
    bin_path = os.environ.get("LLMFIT_BIN", "llmfit")
    try:
        subprocess.run([bin_path, "--version"], capture_output=True, timeout=2)
        return bin_path
    except:
        for path in [f"{os.environ.get('HOME')}/.cargo/bin/llmfit", "/usr/local/bin/llmfit"]:
            if os.path.isfile(path):
                return path
        return None

def main():
    parser = argparse.ArgumentParser(description="Find the right LLM model for your hardware")
    parser.add_argument("--format", choices=["json", "table", "csv"], default="table",
                        help="Output format")
    parser.add_argument("--provider", help="Filter by provider (ollama, huggingface, etc.)")
    parser.add_argument("--min-quality", type=float, default=0.0, help="Minimum quality score (0-1)")
    parser.add_argument("--max-ram", type=float, help="Maximum RAM required (GB)")
    parser.add_argument("--sort", default="quality", help="Sort by field (quality, speed, ram, context)")
    parser.add_argument("--limit", type=int, help="Limit number of results")
    args = parser.parse_args()

    llmfit = find_llmfit_bin()
    if not llmfit:
        print("[ERROR] llmfit binary not found. Install: cargo install llmfit", file=sys.stderr)
        return 1

    # Build command
    cmd = [llmfit, "--output", args.format]
    if args.provider:
        cmd.extend(["--provider", args.provider])
    if args.min_quality > 0:
        cmd.extend(["--min-quality", str(args.min_quality)])
    if args.max_ram:
        cmd.extend(["--max-ram", str(args.max_ram)])
    if args.sort:
        cmd.extend(["--sort", args.sort])
    if args.limit:
        cmd.extend(["--limit", str(args.limit)])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"[ERROR] {result.stderr}", file=sys.stderr)
            return 1
        print(result.stdout)
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
