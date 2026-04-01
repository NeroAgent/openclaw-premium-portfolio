#!/usr/bin/env python3
"""
droidclaw workflow — Run a predefined workflow file.
"""

import argparse
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Run a droidclaw workflow")
    parser.add_argument("workflow_file", help="Path to workflow YAML")
    parser.add_argument("--adb-path", default=os.environ.get("DROIDCLAW_ADB_PATH", "adb"))
    args = parser.parse_args()

    if not os.path.isfile(args.workflow_file):
        print(f"[ERROR] Workflow file not found: {args.workflow_file}", file=sys.stderr)
        return 1

    repo_path = "/root/.openclaw/workspace/external/droidclaw"
    cmd = ["bun", "run", "src/workflow.ts", args.workflow_file]
    env = os.environ.copy()
    env["DROIDCLAW_ADB_PATH"] = args.adb_path

    try:
        result = subprocess.run(cmd, cwd=repo_path, env=env, capture_output=True, text=True, timeout=600)
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
