#!/usr/bin/env python3
"""
gh-aw triage — Triage open issues.
"""

import argparse
import os
import subprocess
import sys

def find_ghaw_bin():
    bin_path = os.environ.get("GHAW_BIN", "gh-aw")
    for path in [f"{os.environ.get('HOME')}/.local/bin/gh-aw", "/usr/local/bin/gh-aw"]:
        if os.path.isfile(path):
            return path
    return None

def main():
    parser = argparse.ArgumentParser(description="Triage open issues")
    parser.add_argument("--repo", required=True, help="GitHub repository")
    parser.add_argument("--limit", type=int, default=50, help="Number of issues to fetch")
    parser.add_argument("--apply", action="store_true", help="Apply suggested labels automatically")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    gh_aw = find_ghaw_bin()
    if not gh_aw:
        print("[ERROR] gh-aw binary not found", file=sys.stderr)
        return 1

    cmd = [gh_aw, "triage", "--repo", args.repo, "--limit", str(args.limit)]
    if args.apply:
        cmd.append("--apply")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if args.output == "json":
            try:
                data = json.loads(result.stdout)
                print(json.dumps(data, indent=2))
            except:
                print(result.stdout)
        else:
            print(result.stdout)
        return result.returncode
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    import json
    sys.exit(main())
