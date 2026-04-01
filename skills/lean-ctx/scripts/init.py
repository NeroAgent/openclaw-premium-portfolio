#!/usr/bin/env python3
"""
lean-ctx init — Install shell hook for automatic compression.
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
    parser = argparse.ArgumentParser(description="Install lean-ctx shell hook")
    parser.add_argument("--global", dest="global_install", action="store_true",
                        help="Install globally for the current user")
    parser.add_argument("--agent", choices=["claude", "cursor", "gemini", "codex", "windsurf", "cline"],
                        help="Install integration for a specific agent/editor")
    args = parser.parse_args()

    lean_ctx = find_lean_ctx_bin()
    if not lean_ctx:
        print("[ERROR] lean-ctx binary not found.", file=sys.stderr)
        sys.exit(1)

    cmd = [lean_ctx, "init"]
    if args.global_install:
        cmd.append("--global")
    if args.agent:
        cmd.extend(["--agent", args.agent])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        print(result.stdout, end='')
        if result.stderr:
            print(result.stderr, end='', file=sys.stderr)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
