#!/usr/bin/env python3
"""
claude-mem summaries — Show session summaries.
"""

import argparse
import json
import sys
import os
import requests

def main():
    parser = argparse.ArgumentParser(description="Show session summaries")
    parser.add_argument("--session", help="Filter by session ID")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    worker_url = os.environ.get("OPENCLAU_MEM_WORKER_URL", "http://localhost:37777")
    endpoint = f"{worker_url}/api/summaries"

    params = {}
    if args.session:
        params["session"] = args.session

    try:
        resp = requests.get(endpoint, params=params, timeout=10)
        if resp.status_code != 200:
            print(f"[ERROR] {resp.status_code}: {resp.text}", file=sys.stderr)
            return 1
        data = resp.json()

        if args.json:
            print(json.dumps(data, indent=2))
        else:
            for summary in data.get("summaries", []):
                print(f"Session: {summary['session_id']}")
                print(f"Started: {summary['started_at']}")
                print(f"Duration: {summary.get('duration_minutes', '?')} minutes")
                print(f"Observations: {summary.get('observation_count', 0)}")
                print(f"Summary: {summary.get('summary', 'N/A')}")
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
