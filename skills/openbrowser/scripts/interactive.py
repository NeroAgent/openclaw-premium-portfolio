#!/usr/bin/env python3
"""
openbrowser interactive — Start interactive REPL.
"""

import argparse
import os
import subprocess
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
    parser = argparse.ArgumentParser(description="Start openbrowser interactive REPL")
    args = parser.parse_args()

    bin_spec = find_openbrowser_bin()
    if not bin_spec:
        print("[ERROR] openbrowser not found. Install dependencies first.", file=sys.stderr)
        sys.exit(1)

    if bin_spec.startswith("bun:"):
        cmd = ["bun", "x", "open-browser", "interactive"]
    else:
        cmd = [bin_spec, "interactive"]

    try:
        # Run in foreground; pass through signals
        subprocess.run(cmd)
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n[INFO] REPL terminated")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
