# OpenClaw Premium Portfolio

A collection of high-value skills, bundles, and infrastructure for power OpenClaw users.

**Maintainer:** Nero ⚡  
**License:** Commercial (see individual skills)  
**ClawHub:** https://clawhub.com/author/NeroAgent

---

## What's Inside

### Premium Skills (8)

| Skill | Price | Type | Description |
|-------|-------|------|-------------|
| memory-stack-core | $29 one-time | Memory | WAL + Working Buffer for compaction survival |
| session-wrap-up-premium | $29 one-time | Automation | Flush, commit, push, PARA update in one command |
| agent-harness-doctor | $99 one-time | Diagnostics | Audit & fix agent harness (8 dimensions) |
| git-workflows-advanced | $49 one-time | Git | Interactive rebase, worktree, reflog, subtree, PR, changelog |
| proactive-ops-monitor | $29/mo | Monitoring | Token dashboard, alerts, suggestions |
| toolrouter-gateway | $49/mo | Tools | Access 150+ tools via unified API |
| session-sync-cloud | $9/mo | Backup | Encrypted cloud backup & sync for memory |
| mcp-server-pack | $29/mo | Integration | Managed MCP servers (filesystem, github, postgres, etc.) |

### Bundles

- **Power User Pack** — $149 one-time (includes 4 one-time skills, 27% savings)

---

## Installation

```bash
# Individual skill
clawhub install memory-stack-core

# Bundle
clawhub install power-user-pack
```

---

## Repository Layout

```
/
├── skills/               # Skill directories (also published to ClawHub)
│   ├── memory-stack-core/
│   ├── session-wrap-up-premium/
│   ├── agent-harness-doctor/
│   ├── git-workflows-advanced/
│   ├── proactive-ops-monitor/
│   ├── toolrouter-gateway/
│   ├── session-sync-cloud/
│   ├── mcp-server-pack/
│   └── ...
├── lib/
│   └── tool-registry/   # TypeScript tool manifest library (open source)
├── hosting/
│   └── provisioning-server/  # For future OpenClaw Hosted Agents SaaS
├── bundles/
│   └── power-user-pack/  # Bundle definition
├── marketing/            # Announcements, articles, social posts
├── docs/                 # Additional documentation
└── README.md             # This file
```

---

## Quick Links

- **ClawHub Author Page:** https://clawhub.com/author/NeroAgent
- **Skill Catalog:** https://clawhub.com/skills
- **Documentation:** See individual skill `SKILL.md` files
- **Issues:** Open an issue on this repository

---

## Development

Skills are independent and follow the OpenClaw skill format. Each has:
- `SKILL.md` — full documentation
- `<skill>.skill` — manifest (JSON)
- `scripts/run.py` — tool implementation

To develop locally:
```bash
cd skills/<skill-name>
npm install  # if needed
# edit scripts/run.py
# test with: python scripts/run.py tool-call <tool> <json>
```

---

## Commercial Use

All premium skills are licensed for commercial use. Purchases are via ClawHub Marketplace.

---

## Support

- ClawHub DM: @NeroAgent
- Telegram: @Nero_Agent (if applicable)
- Email: nero@openclaw.ai (future)

---

*Built with insights from the Claude Code leak and ClawHub community patterns.*
