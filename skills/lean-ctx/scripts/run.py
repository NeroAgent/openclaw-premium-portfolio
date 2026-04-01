#!/usr/bin/env python3
"""
lean-ctx run — Execute a shell command with compression.
"""

import argparse
import os
import subprocess
import json
import sys
import shlex

def find_lean_ctx_bin():
    """Find the lean-ctx binary."""
    # Check environment override
    bin_path = os.environ.get("LEAN_CTX_BIN")
    if bin_path and os.path.isfile(bin_path):
        return bin_path
    # Look in PATH
    for path in os.environ.get("PATH", "").split(":"):
        candidate = os.path.join(path, "lean-ctx")
        if os.path.isfile(candidate):
            return candidate
    return None

def main():
    parser = argparse.ArgumentParser(description="Run a command with lean-ctx compression")
    parser.add_argument("command", help="Shell command to run (quoted)")
    parser.add_argument("--show-original", action="store_true", help="Show raw output as well")
    parser.add_argument("--json", action="store_true", help="Output stats as JSON")
    args = parser.parse_args()

    lean_ctx = find_lean_ctx_bin()
    if not lean_ctx:
        print("[ERROR] lean-ctx binary not found. Install it first (cargo install lean-ctx) or set LEAN_CTX_BIN.", file=sys.stderr)
        sys.exit(1)

    # Build the command: lean-ctx -c <command> [args...]
    # Split the command string into words (respect quotes)
    try:
        command_parts = shlex.split(args.command)
    except ValueError as e:
        print(f"[ERROR] Failed to parse command: {e}", file=sys.stderr)
        sys.exit(1)
    if not command_parts:
        print("[ERROR] No command provided", file=sys.stderr)
        sys.exit(1)
    cmd = [lean_ctx, "-c"] + command_parts

    # Debug: print command and environment
    print(f"DEBUG: cmd = {cmd}", file=sys.stderr)
    print(f"DEBUG: PATH = {os.environ.get('PATH')}", file=sys.stderr)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, env=os.environ.copy())
        output = result.stdout
        stderr = result.stderr

        # Print output (compressed)
        print(output, end='')

        # Show original if requested
        if args.show_original:
            print("\n--- ORIGINAL ---")
            # Run raw command for comparison
            raw = subprocess.run(args.command, shell=True, capture_output=True, text=True, timeout=30)
            print(raw.stdout, end='')

        # Stats could be extracted from stderr if lean-ctx prints them; for now we just rely on its own output.
        if args.json:
            stats = {
                "command": args.command,
                "compressed_bytes": len(output.encode()),
                # We could attempt to compute original size by running raw command, but that doubles runtime; skip.
            }
            print("\n--- JSON STATS ---")
            print(json.dumps(stats, indent=2))

        sys.exit(result.returncode)
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Command timed out: {args.command}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
