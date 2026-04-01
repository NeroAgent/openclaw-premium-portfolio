---
name: agentmail
description: "Full email agent: fetch, search, send, and autonomously handle verification flows. Use to monitor inbox, extract verification codes, auto-apply for services, send replies, and bring email context into conversations. Supports filtering, batch operations, and safe mode with approvals. Requires AGENTMAIL_API_TOKEN."
---

# Agentmail

## Overview

`agentmail` is your autonomous email agent. It integrates with Agentmail.io to:

- **Read & monitor** inbox, search history
- **Extract verification codes** (2FA, sign-up confirmations)
- **Send emails** (draft, reply, forward)
- **Auto-handle verification flows** — combine with `openbrowser` to fill forms and click email links
- **Bring email context** into OpenClaw conversations

**Designed for:** Delegating email-based tasks: signing up for services, verifying accounts, managing notifications, and retrieving information while you're busy.

## Safety & Ethics

- **Send approvals:** By default, sending emails requires explicit confirmation. Can be relaxed with config.
- **Link safety:** Verification links are extracted but not auto-clicked unless you enable `--auto-confirm`.
- **Privacy:** Emails are fetched on-demand, not stored long-term. Summaries can be kept in memory only.
- **Scope:** Use only for tasks you explicitly delegate. Avoid impersonation or spam.

## Quick Start

```bash
# 1. Set API token (already done)
export AGENTMAIL_API_TOKEN="am_us_..."

# 2. Check inbox
agentmail inbox --limit 5

# 3. Extract verification codes from unread
agentmail extract-codes --unread

# 4. Send an email
agentmail send --to support@example.com --subject "Question" --body "Hello"

# 5. Auto-apply flow: browse to signup page, then verify email when code arrives
agentmail wait-for-code --timeout 300  # blocks up to 5min for code
```

## Capabilities

### 1. Inbox & Search (as before)

```bash
agentmail inbox [--unread-only] [--limit N]
agentmail search "<query>" [--from <sender>] [--since <date>]
agentmail get <email_id> [--include-attachments]
```

### 2. Extract Verification Codes

Scans email bodies for common verification patterns:

```bash
# From unread emails
agentmail extract-codes --unread

# From specific email
agentmail extract-codes --email-id msg_123

# Output JSON for automation
agentmail extract-codes --unread --output json
```

**Detects:**
- 6-digit codes (common 2FA)
- 4-8 digit PINs
- "Your code is: XXXX"
- "Enter: XXXXX"
- "Verification link" URLs

**Output:**
```
📧 Found code in email from GitHub:
   Code: 123456
   Context: "Enter this code to verify your device"
   Email ID: msg_456
   Received: 2 min ago
```

### 3. Send Emails

```bash
agentmail send \
  --to "recipient@example.com" \
  --subject "Hello" \
  --body "Message body" \
  [--cc <cc>] [--bcc <bcc>] [--reply-to <email_id>]
```

**Safety:** By default, `send` requires user confirmation. Can be disabled with `--no-confirm` (dangerous).

### 4. Wait for Code (blocking)

Useful for automated sign-up flows:

```bash
# Wait up to 5 minutes for a verification email from "service@example.com"
agentmail wait-for-code --sender service@example.com --timeout 300
```

This blocks until a code is found or timeout. Returns the code and email ID.

**Integration with openbrowser:**
```bash
# 1. Fill signup form
openbrowser run "Sign up at example.com with username test123"

# 2. Wait for verification email
code=$(agentmail wait-for-code --sender welcome@example.com --timeout 300)

# 3. Enter code in browser (could use openbrowser again)
openbrowser command type "input#code" "$code"
```

### 5. Summarize Unread (as before)

```bash
agentmail summarize-unread [--important-only]
```

Now includes code extraction automatically: "You have 3 unread emails, 2 contain verification codes."

### 6. Mark as Read (as before)

```bash
agentmail mark-read <email_id>
```

## Advanced: Auto-Apply Workflow

A complete workflow script (conceptual):

```bash
#!/bin/bash
# apply-for-service.sh
service_name="NewsletterX"
signup_url="https://newsletterx.com/signup"
email_used="sol@example.com"

# 1. Open signup page
openbrowser run "Go to $signup_url and sign up with $email_used" --headless

# 2. Wait for verification email
echo "Waiting for verification email..."
code=$(agentmail wait-for-code --sender "no-reply@newsletterx.com" --timeout 600)

if [ -n "$code" ]; then
  echo "Got code: $code"
  # 3. Enter code (could be manual or automated)
  openbrowser command type "input.verification" "$code"
  openbrowser click "button.submit"
  echo "✅ Verification submitted"
else
  echo "❌ No code arrived within timeout"
fi
```

## Configuration

Environment:
- `AGENTMAIL_API_TOKEN` (required)
- `AGENTMAIL_BASE_URL` (optional, default: `https://api.agentmail.io/v1`)
- `AGENTMAIL_SEND_CONFIRM` (default: `true`) — require confirmation before sending
- `AGENTMAIL_AUTO_CLICK_LINKS` (default: `false`) — auto-open verification links

Credential file: `~/.openclaw/credentials/agentmail.json` (mode 600) stores token.

## Safety Controls

- **Send confirmation:** Unless `AGENTMAIL_SEND_CONFIRM=false`, `agentmail send` prompts for approval.
- **Link safety:** Verification URLs are printed but not visited automatically. Use `openbrowser` to visit if you trust it.
- **Code extraction:** Only reads emails you specify or unread ones. No permanent storage.

## Use Cases

- **Sign up for free tiers** of cloud services (requires email verification)
- **2FA code retrieval** when logging in via browser automation
- ** pulling tracking numbers** from shipment emails
- ** pulling OTP codes** from authenticator emails (less secure, but works)
- **Auto-respond** to common queries (e.g., "I'm away, will reply later")

## Resources

### scripts/
- `inbox.py` — List recent emails
- `search.py` — Full-text search
- `get.py` — Fetch full email
- `send.py` — Send email (new)
- `extract_codes.py` — Find verification codes (new)
- `wait_for_code.py` — Blocking wait for code (new)
- `summarize.py` — LLM summarization
- `mark_read.py` — Mark as read

### references/
- `api.md` — Agentmail.io API reference
- `verification_patterns.md` — How code extraction works
- `workflows.md` — Example automation workflows

---

**Note:** This skill wraps the Agentmail.io HTTP API. Ensure your API token has the necessary scopes (read, send). Use responsibly.

## Quick Start

```bash
# 1. Set your Agentmail.io API token
export AGENTMAIL_API_TOKEN="am_us_..."

# 2. Check recent inbox
agentmail inbox --limit 10

# 3. Search for specific topic
agentmail search "project update" --from sol@example.com

# 4. Get full email content
agentmail get <email_id>

# 5. Summarize unread important emails
agentmail summarize-unread
```

## Capabilities

### 1. Inbox Overview

```bash
agentmail inbox [--limit N] [--unread-only] [--output json|text]
```

Shows recent emails with:
- Sender, subject, date
- Preview snippet
- Unread status
- Labels/tags (if available)

**Example output:**
```
📬 Inbox (5 unread, 50 total)
────────────────────────────────────────
From: Sol <sol@example.com>
Subject: Quick question about the API
Date: 10:30 AM
Preview: Hey, can you check the token consumption on the...

From: GitHub <noreply@github.com>
Subject: [NeroAgent/clawd] New PR #42
Date: Yesterday
Preview: someone opened a pull request...
```

### 2. Search

```bash
agentmail search "<query>" [--from <email>] [--since <date>] [--limit N]
```

Full-text search across emails. Supports:
- Keywords
- Phrases
- Date ranges
- Sender filtering

**Example:**
```bash
agentmail search "lean-ctx deployment" --since "2026-04-01" --limit 5
```

### 3. Get Email

```bash
agentmail get <email_id> [--include-attachments] [--output json|text]
```

Retrieves full email body, headers, and optionally attachments. Output can be parsed for action items.

### 4. Summarize Unread

```bash
agentmail summarize-unread [--important-only] [--output text]
```

Uses LLM to generate concise summaries of unread emails, highlighting:
- Key questions needing response
- Action items with deadlines
- Important updates

This is the most useful for proactive awareness.

### 5. Mark as Read

```bash
agentmail mark-read <email_id>
```

Mark an email as read after processing.

## Configuration

Set environment variables:

```bash
export AGENTMAIL_API_TOKEN="am_us_your_token_here"
export AGENTMAIL_BASE_URL="https://api.agentmail.io/v1"  # optional, default
```

The token you provided: `am_us_e756fed917df12eef55d5ed9387ee41a7e389fe3d23e7e1c4a2effcf9543a20f` should be stored securely. I'll store it in `~/.openclaw/credentials/agentmail.json` with mode 600.

## Auto-Digest Integration

You can use `agentmail` in heartbeat checks:

```
# In HEARTBEAT.md
- Run: agentmail summarize-unread --output text
- If urgent emails found, notify immediately
- Otherwise, just log findings
```

## Use Cases

- **Morning triage:** "What's in my inbox that needs my attention?"
- **Context recall:** "What did we discuss about project X last week?" → search emails
- **Follow-up detection:** "Are there any emails I should reply to?" → summarize-unread
- **External event awareness:** "Any emails about the server outage?" → search

## Security

- API token is stored locally with restricted permissions
- Email content is fetched on-demand, not stored persistently unless you choose to
- Summaries can be kept in memory only

## Setup

1. Ensure you have an Agentmail.io account and API token
2. Store the token securely (I'll help set this up)
3. Test connectivity: `agentmail inbox --limit 1`
4. Integrate into your workflow

## References

### scripts/
- `inbox.py` — List recent emails
- `search.py` — Full-text search
- `get.py` — Fetch full email
- `summarize.py` — LLM summarization
- `mark_read.py` — Mark as read

### references/
- `api.md` — Agentmail.io API reference
- `filtering.md` — Advanced query syntax
- `summarization_prompts.md` — How summarization works

---

**Note:** This skill wraps the Agentmail.io HTTP API. For alternatives (IMAP, other providers), we could create additional mail skills.

## Structuring This Skill

[TODO: Choose the structure that best fits this skill's purpose. Common patterns:

**1. Workflow-Based** (best for sequential processes)
- Works well when there are clear step-by-step procedures
- Example: DOCX skill with "Workflow Decision Tree" -> "Reading" -> "Creating" -> "Editing"
- Structure: ## Overview -> ## Workflow Decision Tree -> ## Step 1 -> ## Step 2...

**2. Task-Based** (best for tool collections)
- Works well when the skill offers different operations/capabilities
- Example: PDF skill with "Quick Start" -> "Merge PDFs" -> "Split PDFs" -> "Extract Text"
- Structure: ## Overview -> ## Quick Start -> ## Task Category 1 -> ## Task Category 2...

**3. Reference/Guidelines** (best for standards or specifications)
- Works well for brand guidelines, coding standards, or requirements
- Example: Brand styling with "Brand Guidelines" -> "Colors" -> "Typography" -> "Features"
- Structure: ## Overview -> ## Guidelines -> ## Specifications -> ## Usage...

**4. Capabilities-Based** (best for integrated systems)
- Works well when the skill provides multiple interrelated features
- Example: Product Management with "Core Capabilities" -> numbered capability list
- Structure: ## Overview -> ## Core Capabilities -> ### 1. Feature -> ### 2. Feature...

Patterns can be mixed and matched as needed. Most skills combine patterns (e.g., start with task-based, add workflow for complex operations).

Delete this entire "Structuring This Skill" section when done - it's just guidance.]

## [TODO: Replace with the first main section based on chosen structure]

[TODO: Add content here. See examples in existing skills:
- Code samples for technical skills
- Decision trees for complex workflows
- Concrete examples with realistic user requests
- References to scripts/templates/references as needed]

## Resources (optional)

Create only the resource directories this skill actually needs. Delete this section if no resources are required.

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Codex for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Codex's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Codex should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Codex produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
