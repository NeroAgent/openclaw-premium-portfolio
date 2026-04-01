#!/usr/bin/env python3
"""
agentmail wait-for-code — Block until a verification code arrives.
"""

import argparse
import json
import os
import re
import sys
import time
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

def extract_codes(text):
    codes = []
    for match in re.finditer(r"\b([0-9]{4,8})\b", text):
        start = max(0, match.start() - 50)
        window = text[start:match.end() + 50].lower()
        if "code" in window or "verify" in window or "enter" in window or "pin" in window or "otp" in window:
            codes.append(match.group(1))
    return list(set(codes))

def main():
    parser = argparse.ArgumentParser(description="Wait for a verification code to arrive")
    parser.add_argument("--sender", help="Filter by sender email")
    parser.add_argument("--subject-contains", help="Filter by subject keyword")
    parser.add_argument("--timeout", type=int, default=300, help="Seconds to wait (default 300)")
    parser.add_argument("--poll-interval", type=int, default=10, help="Polling interval in seconds")
    args = parser.parse_args()

    token, base_url = load_config()
    if not token:
        return 1

    try:
        import requests
    except ImportError:
        print("[ERROR] Install requests: pip install requests", file=sys.stderr)
        return 1

    print(f"[INFO] Waiting for verification email (timeout {args.timeout}s)...")
    start_time = time.time()
    seen_email_ids = set()

    while time.time() - start_time < args.timeout:
        # Fetch recent unread (or recent) emails
        params = {"limit": 20}
        if args.sender:
            params["from"] = args.sender
        try:
            resp = requests.get(f"{base_url}/messages", headers={"Authorization": f"Bearer {token}"}, params=params, timeout=10)
            if resp.status_code != 200:
                time.sleep(args.poll_interval)
                continue
            emails = resp.json().get("messages", [])
        except:
            time.sleep(args.poll_interval)
            continue

        # Check each email we haven't processed yet
        for email in emails:
            email_id = email.get("id")
            if email_id in seen_email_ids:
                continue
            seen_email_ids.add(email_id)

            # Apply subject filter if provided
            if args.subject_contains and args.subject_contains.lower() not in email.get("subject", "").lower():
                continue

            # Fetch full email body (if snippet insufficient, we need full)
            try:
                full_resp = requests.get(f"{base_url}/messages/{email_id}", headers={"Authorization": f"Bearer {token}"}, timeout=10)
                if full_resp.status_code != 200:
                    continue
                full_email = full_resp.json()
                body = full_email.get("body", "")
            except:
                continue

            codes = extract_codes(body)
            if codes:
                print(f"\n✅ Received verification code!")
                print(f"   From: {email.get('sender_email')}")
                print(f"   Subject: {email.get('subject')}")
                print(f"   Code: {codes[0]}")
                print(f"   Email ID: {email_id}")
                return 0

        time.sleep(args.poll_interval)

    print(f"\n❌ Timeout after {args.timeout}s: no verification code found.")
    return 1

if __name__ == "__main__":
    sys.exit(main())
