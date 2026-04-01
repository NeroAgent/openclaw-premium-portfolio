#!/usr/bin/env python3
"""
agentmail inbox — List recent emails.
"""

import argparse
import json
import os
import sys
from pathlib import Path

def load_config():
    """Load API token and base URL from credentials or env."""
    token = os.environ.get("AGENTMAIL_API_TOKEN")
    base_url = os.environ.get("AGENTMAIL_BASE_URL", "https://api.agentmail.io/v1")

    if not token:
        # Try credentials file
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
        print("[ERROR] AGENTMAIL_API_TOKEN not set and no credentials file found.", file=sys.stderr)
        print("  Set environment variable or create ~/.openclaw/credentials/agentmail.json", file=sys.stderr)
        return None, None

    return token, base_url

def main():
    parser = argparse.ArgumentParser(description="List recent emails")
    parser.add_argument("--limit", type=int, default=10, help="Max emails to show")
    parser.add_argument("--unread-only", action="store_true", help="Only unread")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--since", help="Filter by date (ISO or relative like '1d', '1w')")
    parser.add_argument("--from", dest="sender", help="Filter by sender email")
    args = parser.parse_args()

    token, base_url = load_config()
    if not token:
        return 1

    # Build query params
    params = {"limit": args.limit}
    if args.unread_only:
        params["unread"] = "true"
    if args.since:
        params["since"] = args.since
    if args.sender:
        params["from"] = args.sender

    # Make HTTP request
    try:
        import requests
    except ImportError:
        print("[ERROR] 'requests' library required. Install: pip install requests", file=sys.stderr)
        return 1

    try:
        resp = requests.get(f"{base_url}/messages", headers={"Authorization": f"Bearer {token}"}, params=params, timeout=10)
        if resp.status_code != 200:
            print(f"[ERROR] {resp.status_code}: {resp.text}", file=sys.stderr)
            return 1
        data = resp.json()
    except requests.ConnectionError:
        print("[ERROR] Could not connect to Agentmail.io. Check network.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

    # Format output
    emails = data.get("messages", [])
    if args.output == "json":
        print(json.dumps(data, indent=2))
        return 0

    # Text format
    unread_count = sum(1 for e in emails if e.get("is_unread"))
    print(f"📬 Inbox ({unread_count} unread, {len(emails)} shown)\n")
    for e in emails:
        prefix = "🆕" if e.get("is_unread") else "  "
        sender_name = e.get("sender_name", "unknown")
        sender_email = e.get("sender_email", "")
        subject = e.get("subject", "(no subject)")
        date = e.get("date", "")
        snippet = e.get("snippet", "")
        email_id = e.get("id", "")

        print(f"{prefix} From: {sender_name} <{sender_email}>")
        print(f"    Subject: {subject}")
        print(f"    Date: {date}")
        print(f"    ID: {email_id}")
        if snippet:
            print(f"    Preview: {snippet[:100]}...")
        print()

    return 0

if __name__ == "__main__":
    sys.exit(main())
