#!/usr/bin/env python3
"""
claude-mem list — List recent observations.
"""

import argparse
import json
import sys
import os
import requests

def main():
    parser = argparse.ArgumentParser(description="List recent observations")
    parser.add_argument("--limit", type=int, default=20, help="Number to show")
    parser.add_argument("--type", help="Filter by type")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    worker_url = os.environ.get("OPENCLAU_MEM_WORKER_URL", "http://localhost:37777")
    endpoint = f"{worker_url}/api/observations/recent"

    params = {"limit": args.limit}
    if args.type:
        params["type"] = args.type

    try:
        resp = requests.get(endpoint, params=params, timeout=10)
        if resp.status_code != 200:
            print(f"[ERROR] {resp.status_code}: {resp.text}", file=sys.stderr)
            return 1
        data = resp.json()

        if args.json:
            print(json.dumps(data, indent=2))
        else:
            for obs in data.get("observations", []):
                print(f"{obs['id']} — {obs['type']} — {obs['timestamp']}")
                print(f"   {obs['title']}")
            print(f"\nTotal: {len(data.get('observations', []))} observations")
        return 0
    except requests.ConnectionError:
        print("[ERROR] Worker not running", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    main()
