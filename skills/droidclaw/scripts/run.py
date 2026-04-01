#!/usr/bin/env python3
"""
droidclaw run — Execute a goal on Android device.
"""

import argparse
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Run a droidclaw goal on Android")
    parser.add_argument("goal", help="Plain English goal description")
    parser.add_argument("--max-steps", type=int, default=30, help="Maximum actions")
    parser.add_argument("--delegate", choices=["chatgpt", "gemini", "google"], help="On-device AI delegate")
    parser.add_argument("--adb-path", default=os.environ.get("DROIDCLAW_ADB_PATH", "adb"), help="ADB binary")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    # Check prerequisites
    try:
        subprocess.run([args.adb_path, "version"], capture_output=True, timeout=2)
    except:
        print("[ERROR] adb not found. Install Android platform-tools.", file=sys.stderr)
        return 1

    # Check bun
    try:
        subprocess.run(["bun", "--version"], capture_output=True, timeout=2)
    except:
        print("[ERROR] bun not found. Install: curl -fsSL https://bun.sh/install | bash", file=sys.stderr)
        return 1

    # Build command
    repo_path = "/root/.openclaw/workspace/external/droidclaw"
    cmd = ["bun", "run", "src/kernel.ts", args.goal]
    env = os.environ.copy()
    env["DROIDCLAW_ADB_PATH"] = args.adb_path
    env["DROIDCLAW_MAX_STEPS"] = str(args.max_steps)
    if args.delegate:
        env["DROIDCLAW_DELEGATE"] = args.delegate

    try:
        result = subprocess.run(cmd, cwd=repo_path, env=env, capture_output=True, text=True, timeout=600)
        print(result.stdout)
        if result.stderr and args.output == "text":
            print(result.stderr, file=sys.stderr)
        if result.returncode != 0:
            print(f"[ERROR] droidclaw failed: {result.stderr}", file=sys.stderr)
            return 1
        return 0
    except subprocess.TimeoutExpired:
        print("[ERROR] Goal timed out (10 minutes)", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
