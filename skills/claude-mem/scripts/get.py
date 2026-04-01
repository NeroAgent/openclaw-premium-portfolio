#!/usr/bin/env python3
"""
claude-mem get — Fetch full observation details by IDs.
"""

import argparse
import json
import sys
import os
import requests

def main():
    parser = argparse.ArgumentParser(description="Get observations by ID")
    parser.add_argument("ids", type=int, nargs="+", help="Observation IDs")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    worker_url = os.environ.get("OPENCLAU_MEM_WORKER_URL", "http://localhost:37777")
    endpoint = f"{worker_url}/api/observations"

    try:
        resp = requests.get(endpoint, params={"ids": ",".join(str(i) for i in args.ids)}, timeout=10)
        if resp.status_code != 200:
            print(f"[ERROR] {resp.status_code}: {resp.text}", file=sys.stderr)
            return 1
        data = resp.json()

        if args.json:
            print(json.dumps(data, indent=2))
        else:
            for obs in data.get("observations", []):
                print(f"ID {obs['id']} — {obs['type']} — {obs['timestamp']}")
                print(f"Title: {obs['title']}")
                print(f"Content:\n{obs['content']}")
                print("-" * 40)
        return 0
    except requests.ConnectionError:
        print("[ERROR] Worker not running", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    main()
