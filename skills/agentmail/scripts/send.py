#!/usr/bin/env python3
"""
agentmail send — Send an email.
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

def require_confirmation(to, subject, body_preview):
    """Ask user to confirm sending."""
    print("📨 Prepare to send email:")
    print(f"   To: {to}")
    print(f"   Subject: {subject}")
    print(f"   Body preview: {body_preview[:100]}...")
    response = input("   Send this email? (yes/no): ").strip().lower()
    return response in ("yes", "y")

def main():
    parser = argparse.ArgumentParser(description="Send an email")
    parser.add_argument("--to", required=True, help="Recipient email")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body", required=True, help="Email body text")
    parser.add_argument("--cc", action="append", help="CC recipients")
    parser.add_argument("--bcc", action="append", help="BCC recipients")
    parser.add_argument("--reply-to", help="Email ID to reply to (In-Reply-To)")
    parser.add_argument("--no-confirm", action="store_true", help="Skip confirmation prompt")
    args = parser.parse_args()

    token, base_url = load_config()
    if not token:
        return 1

    try:
        import requests
    except ImportError:
        print("[ERROR] Install requests: pip install requests", file=sys.stderr)
        return 1

    payload = {
        "to": [args.to],
        "subject": args.subject,
        "body": args.body,
        "cc": args.cc or [],
        "bcc": args.bcc or []
    }

    # Confirm unless explicitly disabled
    if not args.no_confirm:
        if not require_confirmation(args.to, args.subject, args.body):
            print("❌ Send cancelled.")
            return 0

    try:
        resp = requests.post(f"{base_url}/messages/send", headers={"Authorization": f"Bearer {token}"}, json=payload, timeout=30)
        if resp.status_code not in (200, 201, 202):
            print(f"[ERROR] {resp.status_code}: {resp.text}", file=sys.stderr)
            return 1
        result = resp.json()
        print(f"✅ Email sent! Message ID: {result.get('id')}")
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
