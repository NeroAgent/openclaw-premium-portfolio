#!/usr/bin/env python3
"""
agentmail extract-codes — Extract verification codes from emails.
"""

import argparse
import json
import os
import re
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

def fetch_emails(token, base_url, email_id=None, unread=False, limit=20):
    """Fetch emails either by ID or by unread list."""
    try:
        import requests
    except ImportError:
        print("[ERROR] Install requests: pip install requests", file=sys.stderr)
        return None

    emails = []
    try:
        if email_id:
            resp = requests.get(f"{base_url}/messages/{email_id}", headers={"Authorization": f"Bearer {token}"}, timeout=10)
            if resp.status_code == 200:
                emails = [resp.json()]
        elif unread:
            resp = requests.get(f"{base_url}/messages", headers={"Authorization": f"Bearer {token}"}, params={"unread": "true", "limit": limit}, timeout=10)
            if resp.status_code == 200:
                emails = resp.json().get("messages", [])
        else:
            # Default to recent
            resp = requests.get(f"{base_url}/messages", headers={"Authorization": f"Bearer {token}"}, params={"limit": limit}, timeout=10)
            if resp.status_code == 200:
                emails = resp.json().get("messages", [])
    except Exception as e:
        print(f"[ERROR] Failed to fetch emails: {e}", file=sys.stderr)
        return None

    return emails

def extract_codes_from_text(text):
    """Find verification codes in text."""
    codes = []
    # Common patterns
    # 6-digit codes
    for match in re.finditer(r"\b(?:code|pin|number|verification)[\s:]*([0-9]{4,8})\b", text, re.IGNORECASE):
        codes.append(match.group(1))
    # Standalone 6-digit that might be code
    for match in re.finditer(r"\b([0-9]{6})\b", text):
        # Avoid false positives: check context
        start = max(0, match.start() - 50)
        window = text[start:match.end() + 50].lower()
        if "code" in window or "verify" in window or "enter" in window or "pin" in window or "otp" in window:
            codes.append(match.group(1))
    # Deduplicate
    return list(set(codes))

def extract_verification_links(text):
    """Find URLs that look like verification links."""
    urls = []
    url_pattern = r"https?://[^\s<>\"']+"
    for match in re.finditer(url_pattern, text):
        url = match.group(0)
        if "verify" in url or "confirm" in url or "activation" in url or "token=" in url or "auth" in url:
            urls.append(url)
    return urls

def main():
    parser = argparse.ArgumentParser(description="Extract verification codes from emails")
    parser.add_argument("--email-id", help="Specific email ID to scan")
    parser.add_argument("--unread", action="store_true", help="Scan unread emails")
    parser.add_argument("--limit", type=int, default=20, help="Number of emails to scan")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    if not args.email_id and not args.unread:
        # Default to unread
        args.unread = True

    token, base_url = load_config()
    if not token:
        return 1

    emails = fetch_emails(token, base_url, email_id=args.email_id, unread=args.unread, limit=args.limit)
    if emails is None:
        return 1

    results = []
    for email in emails:
        email_id = email.get("id")
        subject = email.get("subject", "")
        sender = email.get("sender_name", "") or email.get("sender_email", "")
        body = email.get("body", "")
        codes = extract_codes_from_text(body)
        links = extract_verification_links(body)
        if codes or links:
            results.append({
                "email_id": email_id,
                "sender": sender,
                "subject": subject,
                "codes": codes,
                "verification_links": links
            })

    if args.output == "json":
        print(json.dumps({"results": results, "total": len(results)}, indent=2))
        return 0

    # Text output
    if not results:
        print("🔍 No verification codes or links found.")
        return 0

    print(f"🔍 Found {len(results)} email(s) with verification data:\n")
    for r in results:
        print(f"📧 From: {r['sender']}")
        print(f"   Subject: {r['subject']}")
        if r['codes']:
            print(f"   Codes: {', '.join(r['codes'])}")
        if r['verification_links']:
            for link in r['verification_links'][:3]:  # limit links shown
                print(f"   Link: {link}")
        print()
    return 0

if __name__ == "__main__":
    sys.exit(main())
