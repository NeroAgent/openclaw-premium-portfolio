#!/usr/bin/env python3
"""
droidclaw delegate — Delegate a query to on-device AI (ChatGPT/Gemini/Google).
"""

import argparse
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Delegate query to on-device AI via droidclaw")
    parser.add_argument("query", help="Question or task")
    parser.add_argument("--app", choices=["chatgpt", "gemini", "google"], required=True, help="Which app to use")
    parser.add_argument("--adb-path", default=os.environ.get("DROIDCLAW_ADB_PATH", "adb"))
    args = parser.parse_args()

    repo_path = "/root/.openclaw/workspace/external/droidclaw"
    # droidclaw kernel with a special delegate prefix? We'll just use run with goal that implies delegation.
    # Actually, we can construct a goal that says "Using {app}, answer: {query}"
    goal = f"Using {args.app}, {args.query}"
    cmd = ["bun", "run", "src/kernel.ts", goal]
    env = os.environ.copy()
    env["DROIDCLAW_ADB_PATH"] = args.adb_path
    env["DROIDCLAW_DELEGATE"] = args.app

    try:
        result = subprocess.run(cmd, cwd=repo_path, env=env, capture_output=True, text=True, timeout=300)
        print(result.stdout)
        if result.returncode != 0:
            print(f"[ERROR] {result.stderr}", file=sys.stderr)
            return 1
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
