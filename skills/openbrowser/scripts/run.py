#!/usr/bin/env python3
"""
openbrowser run — Execute a natural language web task.
"""

import argparse
import os
import subprocess
import sys
import json

def find_openbrowser_bin():
    bin_path = os.environ.get("OPENBROWSER_BIN")
    if bin_path and os.path.isfile(bin_path):
        return bin_path
    # Look in typical locations
    for path in [
        "/root/.openclaw/workspace/external/openbrowser/packages/cli/dist/index.js",
        "/usr/local/bin/open-browser",
        os.path.expanduser("~/.bun/bin/open-browser"),
    ]:
        if os.path.isfile(path):
            return path
    # Try to find via bun
    try:
        result = subprocess.run(["bun", "--bun", "x", "open-browser", "--help"], capture_output=True, timeout=2)
        # If we got here, bun can run open-browser; we'll use bun x
        return "bun:x:open-browser"
    except:
        pass
    return None

def main():
    parser = argparse.ArgumentParser(description="Run an openbrowser agent task")
    parser.add_argument("task", help="Natural language task description")
    parser.add_argument("--model", default="gpt-4o", help="LLM model (default: gpt-4o)")
    parser.add_argument("--provider", choices=["openai", "anthropic", "google"], default="openai",
                        help="LLM provider (default: openai)")
    parser.add_argument("--headless", action="store_true", help="Run headless (no visible browser)")
    parser.add_argument("--no-headless", action="store_true", help="Show browser window")
    parser.add_argument("--max-steps", type=int, default=25, help="Maximum agent steps")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    bin_spec = find_openbrowser_bin()
    if not bin_spec:
        print("[ERROR] openbrowser binary not found. Install Bun and dependencies:", file=sys.stderr)
        print("  1) Install Bun: curl -fsSL https://bun.sh/install | bash", file=sys.stderr)
        print("  2) cd /root/.openclaw/workspace/external/openbrowser && bun install", file=sys.stderr)
        print("  3) bun run build", file=sys.stderr)
        sys.exit(1)

    # Build command
    if bin_spec.startswith("bun:"):
        # bun x open-browser
        cmd = ["bun", "x", "open-browser", "run", args.task]
    else:
        cmd = [bin_spec, "run", args.task]

    cmd.extend(["--model", args.model])
    cmd.extend(["--provider", args.provider])
    cmd.extend(["--max-steps", str(args.max_steps)])
    if args.headless:
        cmd.append("--headless")
    if args.no_headless:
        cmd.append("--no-headless")
    if args.verbose:
        cmd.append("--verbose")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if args.output == "json":
            # Try to parse output as JSON if the agent returns structured data; else wrap
            try:
                parsed = json.loads(result.stdout)
                print(json.dumps({"result": parsed}, indent=2))
            except:
                print(json.dumps({"raw": result.stdout}, indent=2))
        else:
            print(result.stdout, end='')
        if result.stderr and args.verbose:
            print(result.stderr, end='', file=sys.stderr)
        sys.exit(result.returncode)
    except subprocess.TimeoutExpired:
        print("[ERROR] Task timed out after 5 minutes", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
