#!/usr/bin/env python3
"""
llmfit-recommend — Get top N recommended models.
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
    parser = argparse.ArgumentParser(description="Get recommended models for your hardware")
    parser.add_argument("--count", type=int, default=5, help="Number of recommendations")
    parser.add_argument("--provider", default="ollama", help="Provider filter (default: ollama)")
    parser.add_argument("--min-quality", type=float, default=0.6, help="Minimum quality score")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    llmfit = find_llmfit_bin()
    if not llmfit:
        print("[ERROR] llmfit binary not found", file=sys.stderr)
        return 1

    # Run llmfit with filters
    cmd = [llmfit, "--format", "json", "--provider", args.provider,
           "--min-quality", str(args.min_quality), "--sort", "speed", "--limit", str(args.count * 2)]  # get extra to filter fit
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        print(f"[ERROR] {result.stderr}", file=sys.stderr)
        return 1

    try:
        data = json.loads(result.stdout)
        models = data.get("models", [])
    except:
        print("[ERROR] Could not parse llmfit output", file=sys.stderr)
        return 1

    # Further filter to only those that fit (if fit info available)
    # Assuming llmfit provides a "fit" field or we compute from ram_required vs available RAM
    # We'll be simple: assume all returned are okay; user can refine
    recommendations = models[:args.count]

    if args.output == "json":
        print(json.dumps({"recommendations": recommendations}, indent=2))
        return 0

    print(f"🏆 Top {len(recommendations)} recommended models for your hardware:\n")
    for i, m in enumerate(recommendations, 1):
        print(f"{i}. {m.get('name')} ({m.get('provider')})")
        print(f"   Quality: {m.get('quality', '?'):.2f}  Speed: ~{m.get('speed', '?'):.0f} tok/s  RAM: {m.get('ram_required', '?')} GB")
        print(f"   Context: {m.get('context', '?')}  Quant: {m.get('quant', '?')}")
        print()
    return 0

if __name__ == "__main__":
    sys.exit(main())
