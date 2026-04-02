# Chaos Engineering Skill

Adversarial training & auto-healing system for OpenClaw agents. Induce controlled failures to test resilience, then watch shadow skills auto-recover. Includes thermal dashboard for system status.

## Overview

The Chaos Engineering skill implements a Chaos Monkey pattern specifically for OpenClaw environments:

- **Induce failures**: Break dependencies, hijack ports, corrupt permissions, wipe git history, corrupt WAL, flood buffer
- **Auto-healing**: Each breakage automatically spawns a shadow skill that detects and repairs itself
- **Thermal dashboard**: Terminal-based vision showing system health
- **Battle log**: JSONL journal of all chaos events for post-mortems

## Why Use This?

- **Test your memory stack**: Will WAL/buffer survive? Can you recover?
- **Prove agent resilience**: Show customers your agent handles failures gracefully
- **Auto-healing demos**: Impress prospects with self-repair capabilities
- **Stress test limits**: Find thresholds before customers do

## Quick Start

```bash
# Induce a random failure at the system
tool("chaos-engineering", "chaos_induce", {})

# Induce a specific type
tool("chaos-engineering", "chaos_induce", {"type": "memory_wal_corruption"})

# Auto-heal all breakages (shadow skills execute)
tool("chaos-engineering", "chaos_heal", {})

# Check status (journal + shadow skills count)
tool("chaos-engineering", "chaos_status", {})

# Thermal dashboard (terminal UI)
tool("chaos-engineering", "thermal_dashboard", {"format": "ansi"})
```

Or run scripts directly:

```bash
python3 skills/chaos-engineering/scripts/chaos.py induce random
python3 skills/chaos-engineering/scripts/chaos.py heal
python3 skills/chaos-engineering/scripts/chaos.py status
bash skills/chaos-engineering/thermal_dashboard/render.sh
```

## Chaos Types

| Type | What It Breaks | Fix |
|------|----------------|-----|
| `dependency_hell` | Moves a skill manifest, corrupting skill registry | Restores file |
| `port_hijack` | Kills process on port 9004 | Restarts service |
| `permission_entropy` | Sets all skill dirs to 000 | Restores 755 |
| `git_amnesia` | Deletes .git, reinitializes | Checks out original |
| `memory_wal_corruption` | Truncates WAL to zero | Creates new entry |
| `buffer_flood` | Fills buffer with 10MB zeros | Clears buffer |

Each break creates a **shadow skill** (JSON manifest) that knows how to heal itself. Shadow skills are stored in `~/.neroclaw/surprise/shadow_skills/` and can be reused.

## Recovery Protocol

When chaos is induced:

1. Chaos Monkey executes break command
2. Logs event to `~/.neroclaw/surprise/chaos_engine/battle_log.jsonl`
3. Generates shadow skill with healing command
4. Shadow skill can be triggered manually via `chaos_heal` or automatically by monitoring (future)

The `chaos_heal` tool scans all shadow skills and executes their `healing_command`.

## Dashboard

`thermal_dashboard` shows:

- Vision service status
- CAD server status
- Shadow skill count
- Recent chaos events
- OpenClaw WAL entry count
- Working buffer size
- Skill registry health
- Thermal gradient (cool → hot based on WAL activity)

Run it with `format="ansi"` for colored terminal output, or `format="text"` for plain.

## Integration with Memory Stack

Use chaos to test your memory recovery:

```bash
# 1. Have a conversation, let memory stack capture data
# 2. Induce memory corruption
tool("chaos-engineering", "chaos_induce", {"type": "memory_wal_corruption"})

# 3. Check WAL is gone
tool("memory-stack-core", "wal_read", {"limit": 5})  # should be empty or partial

# 4. Heal
tool("chaos-engineering", "chaos_heal", {})

# 5. Recover from buffer?
tool("memory-stack-core", "buffer_read", {"tail": 1000})

# 6. If both corrupted, session wrap-up couldn't run properly — test your backups!
```

## Safety Notes

- **Use in controlled environments only** — some breaks affect real services
- **Do not run on production agents** — only on test/dev instances
- **Shadow skills require execute permissions** on healing commands
- **Git amnesia** rewrites history; healing uses `git checkout -- .` which may not restore untracked files

## Files Created

- `~/.neroclaw/surprise/chaos_engine/battle_log.jsonl` — event log
- `~/.neroclaw/surprise/shadow_skills/*.json` — auto-generated healing skills
- `memory/` — may be corrupted during testing (that's the point)

## Pricing

$49 one-time. Includes chaos engine, thermal dashboard, and 6 built-in break types. Shadow skills are unlimited and auto-generated.

---

*"What doesn't kill you makes you stronger. Break to rebuild."*