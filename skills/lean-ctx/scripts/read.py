#!/usr/bin/env python3
"""
lean-ctx read — Read a file with optimal compression mode.
"""

import argparse
import os
import subprocess
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
    parser = argparse.ArgumentParser(description="Read a file using lean-ctx compression")
    parser.add_argument("file", help="Path to file")
    parser.add_argument("-m", "--mode", default="full",
                        choices=["full", "map", "signatures", "diff", "aggressive", "entropy"],
                        help="Compression mode (default: full)")
    parser.add_argument("--lines", help="Specific line ranges, e.g., '10-50,80-90'")
    parser.add_argument("--fresh", action="store_true",
                        help="Bypass cache and re-read full file")
    args = parser.parse_args()

    lean_ctx = find_lean_ctx_bin()
    if not lean_ctx:
        print("[ERROR] lean-ctx binary not found.", file=sys.stderr)
        sys.exit(1)

    cmd = [lean_ctx, "read", args.file, "-m", args.mode]
    if args.lines:
        cmd.extend(["-m", f"lines:{args.lines}"])
    if args.fresh:
        cmd.append("--fresh")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        print(result.stdout, end='')
        if result.stderr:
            print(result.stderr, end='', file=sys.stderr)
        sys.exit(result.returncode)
    except subprocess.TimeoutExpired:
        print(f"[ERROR] lean-ctx read timed out", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
