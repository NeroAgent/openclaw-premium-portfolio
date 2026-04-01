# Session: 2026-04-01 15:06:17 UTC

- **Session Key**: agent:main:telegram:direct:7792473438
- **Session ID**: a08e0972-2809-490a-a2f6-2185d7c50713
- **Source**: telegram

## Conversation Summary

assistant: Package openfang:
assistant: Now `gh-aw` — GitHub Agentic Workflows (Go binary). Let's wrap:
assistant: gh-aw is a GitHub Actions/CLI tool. Let's create a skill that wraps its commands:
assistant: Create gh-aw scripts:
assistant: Fix syntax error:
assistant: Now add reference docs and package gh-aw:
assistant: Package gh-aw:
assistant: Now update the tracking files with progress:
assistant: Let's verify the new skills are installed and get final count:
assistant: ---

## ✅ Wrapping Complete: droidclaw, off-grid-mobile, picoclaw, openfang, gh-aw

All five skills have been created, documented, and installed to the system skill directory.

### Summary of New Skills

| Skill | Purpose | Status |
|-------|---------|--------|
| **droidclaw** | AI agent that controls Android device via ADB; reads screen, taps, types, delegates to on-device ChatGPT/Gemini | ✅ Installed (scripts: run, workflow, delegate, check_adb) |
| **off-grid-mobile** | Full offline AI suite for mobile (text, image, vision, voice, docs) | ✅ Installed (scripts: start, status, push_model, send_prompt) |
| **picoclaw** | Ultra-lightweight agent (~10MB RAM) for simple shell-based tasks | ✅ Installed (scripts: run, shell, config) |
| **openfang** | Agent Operating System — runs autonomous 24/7 "Hands" for research, knowledge graphs, social media, etc. | ✅ Installed (scripts: init, start, stop, status, dashboard, hands list/enable/disable/trigger/logs/config) |
| **gh-aw** | GitHub Agentic Workflows — AI PR reviews, issue triage, changelog generation | ✅ Installed (scripts: review, pr_description, issue_description, triage, changelog) |

---

### Current Skill Ecosystem

**Total skills in system:** ~70 (53 system + 17 custom)

**Custom skills installed (17):**
1. skill-health
2. resource-check
3. git-status-summary
4. lean-ctx
5. openbrowser
6. claude-mem
7. opensandbox
8. gstack
9. chatterbox-tts
10. agentmail
11. ollama
12. llmfit
13. droidclaw
14. off-grid-mobile
15. picoclaw
16. openfang
17. gh-aw

**External repos cloned (22):** See `/root/.openclaw/workspace/setup_queue.json`

---

### What's Ready to Use Now (on this Termux)

- `resource-check` — monitor system
- `git-status-summary` — repo overview
- `lean-ctx` — token compression (functional)
- `skill-health` — audit ecosystem

**Others need external setup:**
- `agentmail` — needs Python `requests` (installable)
- `ollama` — binary not installed; requires ARM64 build or use on server
- `llmfit` — binary needs `cargo install`
- `droidclaw` — needs Bun + ADB connection to Android device
- `off-grid-mobile` — needs Android app installed; ADB control only
- `picoclaw` — needs Go build
- `openfang` — needs Rust build; runs as daemon
- `gh-aw` — needs Go build; requires `gh` CLI and API keys
- `openbrowser` — needs Bun + Playwright browsers
- `claude-mem` — OOM on Termux; external server
- `opensandbox` — needs Docker
- `chatterbox-tts` — needs PyTorch (x86_64)

---

### Next Options

**A. Install binaries for the lightweight tools:**
- Build `llmfit` (Rust, already cloned)
- Build `picoclaw` (Go)
- Build `droidclaw` (Bun, already installed)
- Build `openfang` (Rust) — heavier but doable

**B. Set up external server** (VPS/laptop) for heavy services:
- Deploy claude-mem worker
- Deploy ollama + models
- Deploy OpenSandbox (Docker)
- Deploy off-grid-mobile on Android device (app install)

**C. Continue wrapping remaining repos** (tgo, langflow, n8n, eliza, etc.)

**D. Integrate and test** existing skills in actual workflows

What's your priority, Sol?
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "351",
  "sender_id": "7792473438",
  "sender": "ይወስኑ 🐋",
  "timestamp": "Wed 2026-04-01 14:45 UTC"
}
```

Sender (untrusted metadata):
```json
{
  "label": "ይወስኑ 🐋 (7792473438)",
  "id": "7792473438",
  "name": "ይወስኑ 🐋",
  "username": "MrDrHeman"
}
```

C.
assistant: Excellent. Let's wrap the next batch: system-prompts, tgo, and eliza.

I'll create skills for them in parallel:
assistant: Now build out these skills content. I'll start with system-prompts (simplest — just a library):
assistant: Now scripts for system-prompts:
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "355",
  "sender_id": "7792473438",
  "sender": "ይወስኑ 🐋",
  "timestamp": "Wed 2026-04-01 15:05 UTC"
}
```

Sender (untrusted metadata):
```json
{
  "label": "ይወስኑ 🐋 (7792473438)",
  "id": "7792473438",
  "name": "ይወስኑ 🐋",
  "username": "MrDrHeman"
}
```

Enable reasoning
