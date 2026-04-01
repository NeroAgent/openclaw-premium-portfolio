#!/usr/bin/env python3
"""
gh-aw review — AI review of a PR.
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
    parser = argparse.ArgumentParser(description="AI review of a PR")
    parser.add_argument("pr", type=int, help="Pull request number")
    parser.add_argument("--repo", required=True, help="GitHub repository (owner/repo)")
    parser.add_argument("--level", choices=["quick", "thorough"], default="thorough", help="Review depth")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    gh_aw = find_ghaw_bin()
    if not gh_aw:
        print("[ERROR] gh-aw binary not found. Install: go install github.com/rightnow-ai/gh-aw@latest", file=sys.stderr)
        return 1

    cmd = [gh_aw, "review", str(args.pr), "--repo", args.repo, "--level", args.level]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if args.output == "json":
            # gh-aw might have --json flag; we can try adding
            try:
                parsed = json.loads(result.stdout)
                print(json.dumps(parsed, indent=2))
            except:
                print(result.stdout)
        else:
            print(result.stdout)
        if result.returncode != 0:
            print(f"[ERROR] {result.stderr}", file=sys.stderr)
            return 1
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    import json
    sys.exit(main())
