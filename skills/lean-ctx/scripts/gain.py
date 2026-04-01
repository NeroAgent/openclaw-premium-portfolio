#!/usr/bin/env python3
"""
lean-ctx gain — Show token savings statistics.
"""

import argparse
import os
import subprocess
import json
import sys

def find_lean_ctx_bin():
    bin_path = os.environ.get("LEAN_CTX_BIN")
    if bin_path and os.path.isfile(bin_path):
        return bin_path
    for path in os.environ.get("PATH", "").split(":"):
        candidate = os.path.join(path, "lean-ctx")
        if os.path.isfile(candidate):
            return candidate
    return None

def main():
    parser = argparse.ArgumentParser(description="Show token savings statistics")
    parser.add_argument("--graph", action="store_true", help="Show 30-day savings chart")
    parser.add_argument("--daily", action="store_true", help="Show day-by-day breakdown")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--weekly", action="store_true", help="Weekly report")
    args = parser.parse_args()

    lean_ctx = find_lean_ctx_bin()
    if not lean_ctx:
        print("[ERROR] lean-ctx binary not found.", file=sys.stderr)
        sys.exit(1)

    cmd = [lean_ctx, "gain"]
    if args.graph:
        cmd.append("--graph")
    if args.daily:
        cmd.append("--daily")
    if args.weekly:
        cmd.append("--week")
    if args.json:
        cmd.append("--json")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        print(result.stdout, end='')
        if result.stderr:
            print(result.stderr, end='', file=sys.stderr)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
