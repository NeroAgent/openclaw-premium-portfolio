#!/usr/bin/env python3
"""
agentmail get — Retrieve full email content.
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
    parser = argparse.ArgumentParser(description="Get email by ID")
    parser.add_argument("email_id", help="Email ID (from inbox or search)")
    parser.add_argument("--include-attachments", action="store_true", help="Include attachment info")
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

    params = {}
    if args.include_attachments:
        params["include_attachments"] = "true"

    try:
        resp = requests.get(f"{base_url}/messages/{args.email_id}", headers={"Authorization": f"Bearer {token}"}, params=params, timeout=10)
        if resp.status_code != 200:
            print(f"[ERROR] {resp.status_code}: {resp.text}", file=sys.stderr)
            return 1
        email = resp.json()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

    if args.output == "json":
        print(json.dumps(email, indent=2))
        return 0

    # Text format
    print(f"📧 Email ID: {email.get('id')}")
    print(f"From: {email.get('sender_name')} <{email.get('sender_email')}>")
    print(f"To: {', '.join(email.get('to', []))}")
    print(f"Date: {email.get('date')}")
    print(f"Subject: {email.get('subject')}")
    print("\nBody:\n")
    print(email.get('body', ''))
    if email.get('attachments'):
        print("\nAttachments:")
        for att in email['attachments']:
            print(f"  - {att['filename']} ({att['size']} bytes)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
