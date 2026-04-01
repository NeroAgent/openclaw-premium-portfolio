#!/usr/bin/env python3
"""
claude-mem store — Manually store an observation.
"""

import argparse
import json
import sys
import os
import requests

def main():
    parser = argparse.ArgumentParser(description="Store an observation")
    parser.add_argument("--type", default="note", help="Observation type (finding, decision, task, note)")
    parser.add_argument("--title", required=True, help="Short title")
    parser.add_argument("--content", required=True, help="Content text")
    parser.add_argument("--tags", default="", help="Comma-separated tags")
    parser.add_argument("--private", action="store_true", help="Mark as private")
    parser.add_argument("--session", default="default", help="Session ID")
    args = parser.parse_args()

    worker_url = os.environ.get("OPENCLAU_MEM_WORKER_URL", "http://localhost:37777")
    endpoint = f"{worker_url}/api/observation"

    payload = {
        "type": args.type,
        "title": args.title,
        "content": args.content,
        "tags": args.tags.split(",") if args.tags else [],
        "private": args.private,
        "session": args.session
    }

    try:
        resp = requests.post(endpoint, json=payload, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            print(f"Stored observation ID: {data.get('id')}")
            return 0
        else:
            print(f"[ERROR] {resp.status_code}: {resp.text}", file=sys.stderr)
            return 1
    except requests.ConnectionError:
        print("[ERROR] Could not connect to claude-mem worker. Is it running?", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    main()
