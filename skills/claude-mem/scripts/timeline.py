#!/usr/bin/env python3
"""
claude-mem timeline — Get timeline around an observation.
"""

import argparse
import json
import sys
import os
import requests

def main():
    parser = argparse.ArgumentParser(description="Get timeline context")
    parser.add_argument("--around", type=int, help="Observation ID to center on")
    parser.add_argument("--at", help="ISO timestamp to center on")
    parser.add_argument("--window", default="30m", help="Time window (e.g., 30m, 1h)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if not args.around and not args.at:
        parser.error("Either --around or --at required")

    worker_url = os.environ.get("OPENCLAU_MEM_WORKER_URL", "http://localhost:37777")
    endpoint = f"{worker_url}/api/timeline"

    params = {}
    if args.around:
        params["around_id"] = args.around
    if args.at:
        params["at"] = args.at
    params["window"] = args.window

    try:
        resp = requests.get(endpoint, params=params, timeout=10)
        if resp.status_code != 200:
            print(f"[ERROR] {resp.status_code}: {resp.text}", file=sys.stderr)
            return 1
        data = resp.json()

        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print(f"Timeline around {args.around or args.at} (window: {args.window})\n")
            for obs in data.get("observations", []):
                print(f"{obs['timestamp']} — {obs['type']}: {obs['title']}")
                print(f"   {obs.get('content', '')[:100]}...")
                print()
        return 0
    except requests.ConnectionError:
        print("[ERROR] Worker not running", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    main()
