#!/usr/bin/env python3
"""
picoclaw run — Execute a natural language goal.
"""

import argparse
import os
import subprocess
import sys

def find_picoclaw_bin():
    bin_path = os.environ.get("PICOCLAW_BIN", "picoclaw")
    for path in [f"{os.environ.get('HOME')}/.local/bin/picoclaw", "/usr/local/bin/picoclaw"]:
        if os.path.isfile(path):
            return path
    return None

def main():
    parser = argparse.ArgumentParser(description="Run a picoclaw goal")
    parser.add_argument("goal", help="Natural language description of task")
    parser.add_argument("--dry-run", action="store_true", help="Show commands without executing")
    parser.add_argument("--force", action="store_true", help="Skip confirmations")
    parser.add_argument("--max-steps", type=int, default=5, help="Maximum commands to generate")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    picoclaw = find_picoclaw_bin()
    if not picoclaw:
        print("[ERROR] picoclaw binary not found. Build from https://github.com/openclaw/picoclaw", file=sys.stderr)
        return 1

    cmd = [picoclaw, args.goal, "--max-steps", str(args.max_steps)]
    if args.dry_run:
        cmd.append("--dry-run")
    if args.force:
        cmd.append("--force")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if args.output == "json":
            # picoclaw might output JSON if flag given; otherwise wrap text
            try:
                data = {"output": result.stdout, "error": result.stderr, "exit_code": result.returncode}
                print(json.dumps(data, indent=2))
            except:
                print(result.stdout)
        else:
            print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
        return result.returncode
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    import json
    sys.exit(main())
