#!/usr/bin/env python3
"""
agentmail mark-read — Mark email as read.
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
    parser = argparse.ArgumentParser(description="Mark email as read")
    parser.add_argument("email_id", help="Email ID to mark as read")
    args = parser.parse_args()

    token, base_url = load_config()
    if not token:
        return 1

    try:
        import requests
    except ImportError:
        print("[ERROR] Install requests: pip install requests", file=sys.stderr)
        return 1

    try:
        resp = requests.post(f"{base_url}/messages/{args.email_id}/read", headers={"Authorization": f"Bearer {token}"}, timeout=10)
        if resp.status_code not in (200, 204):
            print(f"[ERROR] {resp.status_code}: {resp.text}", file=sys.stderr)
            return 1
        print(f"✅ Marked email {args.email_id} as read")
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
