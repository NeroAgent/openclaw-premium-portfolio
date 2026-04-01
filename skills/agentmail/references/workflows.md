# Example Workflows

## Auto-Signup for a Service

```bash
# 1. Navigate to signup page (send to openbrowser)
openbrowser run "Go to https://example.com/register, fill username 'testuser' and password 'securePass123', submit"

# 2. Wait for verification email (from no-reply@example.com)
code=$(agentmail wait-for-code --sender no-reply@example.com --timeout 600)

# 3. Enter code in browser (if not auto-submitted)
if [ -n "$code" ]; then
  openbrowser command type "input[name='verification_code']" "$code"
  openbrowser click "button[type='submit']"
else
  echo "No code received; check email manually"
fi
```

## Pulling Tracking Numbers from Shipment Emails

```bash
# Search for recent shipment notifications
agentmail search "tracking number" --since 1d --output json > /tmp/emails.json

# Extract tracking IDs (might need custom parsing; could use LLM)
# Then use in conversation: "Your package is tracked by XYZ123456"
```

## Daily Digest of Important Emails

```bash
# In HEARTBEAT or morning script:
unread=$(agentmail inbox --unread-only --output json | jq '.messages | length')
if [ "$unread" -gt 0 ]; then
  agentmail summarize-unread --output text | say  # if TTS available
  # Or send notification to Telegram/Signal
fi
```

## Auto-Reply to Common Queries

```bash
# If you receive many "how are you?" emails, auto-reply with a template
agentmail search "how are you" --unread --output json | jq -r '.messages[].id' | while read id; do
  agentmail send --to "$(agentmail get $id --output json | jq -r '.sender_email')" \
    --subject "Re: How are you?" \
    --body "I'm doing well, thanks! (Auto-reply)" \
    --no-confirm
  agentmail mark-read $id
done
```

---

These patterns can be baked into custom scripts or skills. Be cautious with auto-reply to avoid spam.