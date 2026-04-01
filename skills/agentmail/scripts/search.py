#!/usr/bin/env python3
"""
agentmail search — Search emails.
"""

import argparse
import json
import os
import sys
from pathlib import Path

def load_config():
    token = os.environ.get("AGENTMAIL_API_TOKEN")
    base_url = os.environ.get("AGENTMAIL_BASE_URL", "https://api.agentmail.io/v1")
    if not token:
        cred_path = Path.home() / ".openclaw" / "credentials" / "agentmail.json"
        if cred_path.exists():
            try:
                with open(cred_path) as f:
                    data = json.load(f)
                    token = data.get("agentmail_api_token") or data.get("token")
                    base_url = data.get("base_url", base_url)
            except:
                pass
    if not token:
        print("[ERROR] AGENTMAIL_API_TOKEN not set", file=sys.stderr)
        return None, None
    return token, base_url

def main():
    parser = argparse.ArgumentParser(description="Search emails")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--since", help="Since date (ISO or relative)")
    parser.add_argument("--from", dest="sender", help="Filter sender")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    token, base_url = load_config()
    if not token:
        return 1

    try:
        import requests
    except ImportError:
        print("[ERROR] Install requests: pip install requests", file=sys.stderr)
        return 1

    params = {"q": args.query, "limit": args.limit}
    if args.since:
        params["since"] = args.since
    if args.sender:
        params["from"] = args.sender

    try:
        resp = requests.get(f"{base_url}/search", headers={"Authorization": f"Bearer {token}"}, params=params, timeout=10)
        if resp.status_code != 200:
            print(f"[ERROR] {resp.status_code}: {resp.text}", file=sys.stderr)
            return 1
        data = resp.json()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

    emails = data.get("messages", [])
    if args.output == "json":
        print(json.dumps(data, indent=2))
        return 0

    print(f"🔍 Search results for '{args.query}': {len(emails)} found\n")
    for e in emails:
        print(f"ID: {e.get('id')}")
        print(f"From: {e.get('sender_name')} <{e.get('sender_email')}>")
        print(f"Subject: {e.get('subject')}")
        print(f"Date: {e.get('date')}")
        snippet = e.get('snippet', '')
        if snippet:
            print(f"Snippet: {snippet[:150]}...")
        print()
    return 0

if __name__ == "__main__":
    sys.exit(main())
