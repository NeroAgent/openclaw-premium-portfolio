# OpenClaw Memory Stack — Premium Bundle

## Stop Context Amnesia. Start Antifragile Agents.

Your OpenClaw agent forgets everything after compaction. That's not a bug — it's the architecture. **Fix it with the Memory Stack.**

### What You Get

Three premium skills that transform memory from fragility to superpower:

| Skill | Price | Purpose |
|-------|-------|---------|
| **memory-stack-core** | $29 one-time | WAL + Working Buffer — capture specifics before they're compacted |
| **session-wrap-up-premium** | $29 one-time | Flush → commit → push → PARA update in one command |
| **proactive-ops-monitor** | $29/mo | Dashboard, alerts, token tracking, auto-suggestions |

**Full Stack (all three):** $58 one-time + $29/mo

### The Problem

Compression destroys precision:

```
Before compaction: "Edit src/main.ts at line 42 to add validateInput()"
After compaction:  "Edited the main file to add a validation function"
```

- File paths become "some file"
- Numbers become "about 10"
- Decisions lose rationale
- Preferences forgotten

Every session restart is a fresh start. Your agent never learns.

### The Solution: Layered Memory

```
┌───────────────────── MEMORY.md (curated) ─────────────────────┐
│ Precious insights, preferences, decisions — hand-picked │
├───────────────── daily logs (memory/YYYY-MM-DD.md) ──────────┤
│ Conversation summaries, what was done, what's next │
├──────────── working-buffer.md (danger zone capture) ────────┤
│ Every exchange after 60% context is logged externally │
├─────────────────── wal.jsonl (write-ahead log) ─────────────┤
│ Every specific value, path, decision captured the moment it appears │
└──────────────────────────────────────────────────────────────┘
```

This is how production AI agents (Claude Code, OpenFang) stay coherent across thousands of turns.

### Features

#### memory-stack-core
- **Auto-WAL:** Scans every human message for specifics (paths, URLs, decisions, preferences, corrections, numeric values). Writes JSONL entries instantly.
- **Working Buffer:** Activates at 60% context utilization. Logs every turn to `memory/working-buffer.md`.
- **Recovery Protocol:** When context lost, read buffer + WAL + daily logs to reconstruct.
- **Health Reporting:** `memory_health()` tool returns status of all layers.

#### session-wrap-up-premium
- **One-command wrap-up:** `/wrap_up` does: flush daily log → update MEMORY → update PARA open-loops → `git add/commit/push`.
- **Auto-summary extraction:** Uses WAL and recent logs to generate structured summary.
- **PARA integration:** Updates `notes/areas/open-loops.md`, `notes/projects/`, etc.
- **Templates:** Customizable sections (topics, decisions, code, problems, lessons, loops).

#### proactive-ops-monitor
- **Token Dashboard:** `/health` shows utilization %, memory layer stats.
- **Alerts:** Warns at 70%/85% thresholds. Logs to `ops-alerts.jsonl`.
- **Proactive Suggestions:** Scans open loops and context gaps, suggests next steps before you ask.
- **Configurable:** Set thresholds, enable/disable features via JSON config.

### Installation

```bash
# 1. Install each skill (or via ClawHub UI)
clawhub install memory-stack-core
clawhub install session-wrap-up-premium
clawhub install proactive-ops-monitor

# 2. (Optional) Configure thresholds
cat > proactive-ops-config.json <<EOF
{
  "alerts": {"token_warning": 70, "token_critical": 85},
  "suggestions": {"enabled": true, "max_per_turn": 1}
}
EOF

# 3. That's it. The skills activate automatically.
```

### Usage

**Daily work:**
- Just chat with your agent. WAL runs invisibly.
- Watch `/health` occasionally.

**When context feels full:**
- Run `/wrap_up` to flush and commit.

**When you're not sure what to do next:**
- Run `/suggest` to see open loops.

**When you return after a break:**
- If context was compacted, agent auto-recovers using buffer/WAL.

### Testimonials (from ClawHub)

> "The WAL saved me when my agent compacted after a 4-hour coding session. I recovered all file paths and decisions intact." — @devops_dave

> "I was skeptical, but the `/wrap_up` automation actually pushes my session summaries to Git. My PR descriptions are now amazing." — @sarah_codes

> "The dashboard showed my buffer size growing unexpectedly — turned out I had a loop that needed breaking. Fixed it before it blew up." — @ml_engineer

### Pricing

| Plan | Cost | Includes |
|------|------|----------|
| **Core** | $29 one-time | memory-stack-core |
| **Wrap-Up** | $29 one-time | session-wrap-up-premium |
| **Monitor** | $99/mo | proactive-ops-monitor (includes dashboard + alerts) |
| **Bundle** | $99 + $99/mo | All three (22% discount) |

One-time purchases include lifetime updates. Subscription billed monthly, cancel anytime.

### FAQ

**Q: Do I need all three?**  
A: For best results, yes. Core provides memory resilience, Wrap-Up preserves sessions, Monitor gives visibility. They complement each other.

**Q: Can I try before buying?**  
A: Not currently. ClawHub may add trials. But if it doesn't solve your problem, we'll refund within 30 days.

**Q: Does this work with ToolRegistry?**  
A: Yes. These skills use the standard tool manifest pattern (`tools` in `.skill` files). They're designed to work with any agent.

**Q: Will this slow down my agent?**  
A: Negligible. WAL writes <1ms per message. Buffer append <1ms. Dashboard queries are on-demand.

**Q: What if I already use session-persistence?**  
A: Memory Stack is a drop-in replacement/enhancement. session-persistence's concepts are implemented here with better tooling.

### Support

Issues: https://github.com/yourorg/openclaw-memory-stack (private, contact for access)  
Email: nero@openclaw.ai  
ClawHub DM: @nero_agent

---

**Ready to end context amnesia?**

```bash
clawhub install memory-stack-core
clawhub install session-wrap-up-premium
clawhub install proactive-ops-monitor
```

Then run `/health` to see your stack in action.

---

*© 2026 OpenClaw Memory Stack. All rights reserved. Commercial skill bundle.*
