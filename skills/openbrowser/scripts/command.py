#!/usr/bin/env python3
"""
openbrowser command — Execute a direct browser command.
"""

import argparse
import os
import subprocess
import json
import sys

def find_openbrowser_bin():
    bin_path = os.environ.get("OPENBROWSER_BIN")
    if bin_path and os.path.isfile(bin_path):
        return bin_path
    for path in [
        "/root/.openclaw/workspace/external/openbrowser/packages/cli/dist/index.js",
        "/usr/local/bin/open-browser",
        os.path.expanduser("~/.bun/bin/open-browser"),
    ]:
        if os.path.isfile(path):
            return path
    try:
        subprocess.run(["bun", "--bun", "x", "open-browser", "--help"], capture_output=True, timeout=2)
        return "bun:x:open-browser"
    except:
        return None

def main():
    parser = argparse.ArgumentParser(description="Execute a direct openbrowser command")
    parser.add_argument("cmd", choices=["open", "click", "type", "screenshot", "extract", "eval", "state", "sessions"],
                        help="Command to execute")
    parser.add_argument("args", nargs="*", help="Arguments for the command")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    bin_spec = find_openbrowser_bin()
    if not bin_spec:
        print("[ERROR] openbrowser not found.", file=sys.stderr)
        sys.exit(1)

    if bin_spec.startswith("bun:"):
        base_cmd = ["bun", "x", "open-browser"]
    else:
        base_cmd = [bin_spec]

    # Map to subcommand
    full_cmd = base_cmd + [args.cmd] + args.args

    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=60)
        if args.output == "json":
            # Try to parse as JSON, else wrap
            try:
                data = json.loads(result.stdout)
                print(json.dumps({"result": data}, indent=2))
            except:
                print(json.dumps({"raw": result.stdout}))
        else:
            print(result.stdout, end='')
        if result.stderr:
            print(result.stderr, end='', file=sys.stderr)
        sys.exit(result.returncode)
    except subprocess.TimeoutExpired:
        print("[ERROR] Command timed out", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
