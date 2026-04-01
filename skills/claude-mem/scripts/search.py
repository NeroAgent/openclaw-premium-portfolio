#!/usr/bin/env python3
"""
claude-mem search — Search observations.
"""

import argparse
import json
import sys
import os
import requests

def main():
    parser = argparse.ArgumentParser(description="Search observations")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=10, help="Max results")
    parser.add_argument("--type", help="Filter by type")
    parser.add_argument("--after", help="Filter after date (ISO)")
    parser.add_argument("--before", help="Filter before date (ISO)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--private", action="store_true", help="Include private observations")
    args = parser.parse_args()

    worker_url = os.environ.get("OPENCLAU_MEM_WORKER_URL", "http://localhost:37777")
    endpoint = f"{worker_url}/api/search"

    params = {
        "q": args.query,
        "limit": args.limit,
        "type": args.type,
        "after": args.after,
        "before": args.before,
        "include_private": args.private
    }

    try:
        resp = requests.get(endpoint, params=params, timeout=10)
        if resp.status_code != 200:
            print(f"[ERROR] {resp.status_code}: {resp.text}", file=sys.stderr)
            return 1
        data = resp.json()

        if args.json:
            print(json.dumps(data, indent=2))
        else:
            # Human readable
            print(f"Search results for '{args.query}': {len(data.get('results', []))} found\n")
            for r in data.get("results", []):
                print(f"ID {r['id']} [{r['type']}] {r['title']} ({r['timestamp']})")
                print(f"   {r['snippet']}")
                print()
        return 0
    except requests.ConnectionError:
        print("[ERROR] Worker not running. Start it with 'claude-mem start'.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    main()
