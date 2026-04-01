---
name: claude-mem
description: "Persistent memory system that condenses and retrieves cross-session context. Automatically captures tool usage, generates semantic summaries, and makes them available in future sessions. Use to maintain continuity across OpenClaw restarts, compress long conversation history, and perform progressive-disclosure search (index → timeline → details). Enables long-term memory with token-efficient retrieval."
---

# Claude Mem

## Overview

`claude-mem` provides a persistent memory layer for OpenClaw inspired by the Claude-Mem plugin. It runs a background worker service that:

- **Observes** tool calls, prompts, and responses
- **Summarizes** sessions into semantic chunks
- **Indexes** content for search (hybrid full-text + vector)
- **Retrieves** relevant memories on demand with progressive disclosure

**Designed for:** Long-running projects where context loss is a problem. It eliminates cold starts and allows OpenClaw to remember decisions, findings, and patterns across days, weeks, or months.

## Quick Start

```bash
# Install and start the worker (one-time setup)
claude-mem install

# The worker runs automatically on port 37777. Use the search tools:

# 1. Search index (compact, cheap)
claude-mem search "authentication bug" --limit 10

# 2. Get timeline around a result
claude-mem timeline --around <observation_id>

# 3. Fetch full details (expensive) for selected IDs
claude-mem get 123 456 789
```

## Three-Layer Retrieval Pattern

To maximize token efficiency, claude-mem uses a **3-layer progressive disclosure** workflow:

1. **`search`** — Returns compact index with IDs (~50-100 tokens/result)
2. **`timeline`** — Gives chronological context around interesting results
3. **`get_observations`** — Fetches full details ONLY for filtered IDs (~500-1,000 tokens/result)

**~10x token savings** versus blasting entire history each session.

## Capabilities

### 1. Worker Management

```bash
claude-mem install    # Install dependencies and create config
claude-mem start      # Start worker (foreground)
claude-mem start --background  # Daemonize
claude-mem stop       # Stop worker
claude-mem status     # Check if running
```

The worker listens on `http://localhost:37777` and provides a web UI at `http://localhost:37777/ui`.

### 2. Observations

An **observation** is a unit of memory: a tool call, a user prompt, a finding, a decision.

```bash
# Store an observation manually (usually automatic)
claude-mem store --type "finding" --title "Race condition fixed" --content "Added advisory lock to payment_service.rb"

# List recent observations
claude-mem list --limit 20

# Get a specific observation
claude-mem get <observation_id>
```

### 3. Search

```bash
# Full-text search with filters
claude-mem search "authentication bug" --type bugfix --limit 10

# Search by date range
claude-mem search "performance" --after "2026-03-01" --before "2026-03-31"

# JSON output for scripting
claude-mem search "session timeout" --json
```

**Response fields:**
- `id` — observation ID
- `type` — category (finding, decision, task, etc.)
- `title` — short title
- `timestamp` — when it happened
- `snippet` — matching excerpt
- `score` — relevance score

### 4. Timeline

Get chronological context around an observation or a point in time:

```bash
claude-mem timeline --around 123    # 30min window around observation 123
claude-mem timeline --at "2026-04-01T10:00:00Z" --window 1h
```

Useful for understanding the sequence of events leading to a finding.

### 5. Summaries

Auto-generated summaries per session:

```bash
claude-mem summaries --session <session_id>
```

Shows high-level overview of what was accomplished.

## Automatic Capture

When the worker is running and `OPENCLAU_MEM_ENABLED=true` (or default for OpenClaw), the skill hooks into tool calls and automatically stores:

- Tool name and arguments
- Output (truncated to 2k tokens)
- Errors and exceptions
- User prompts and assistant replies (if configured)

This creates a comprehensive audit trail without manual effort.

## Privacy & Tags

You can mark observations as `<private>` to exclude them from storage. Use:

```bash
claude-mem store --content "Sensitive data" --private
```

or in conversation: "Remember this <private>".

Private observations are encrypted at rest (if `ENCRYPTION_KEY` set) and excluded from search results by default.

## Configuration

Settings stored in `~/.claude-mem/settings.json`:

```json
{
  "worker_port": 37777,
  "data_dir": "~/.claude-mem",
  "auto_capture": true,
  "capture_prompts": false,
  "max_output_tokens": 2000,
  "search": {
    "default_limit": 10,
    "timeline_window_minutes": 30
  },
  "ui_enabled": true
}
```

Environment variables:
- `OPENCLAU_MEM_WORKER_URL` — override worker URL
- `OPENCLAU_MEM_ENABLED` — `true`/`false` to toggle auto-capture
- `OPENCLAU_MEM_ENCRYPTION_KEY` — optional encryption for private data

## Installation

The `claude-mem` skill expects the claude-mem worker to be installed. If not present, the `install` script will:

1. Check for Node.js 18+ and Bun
2. Install dependencies via `bun install`
3. Create config and data directories
4. Optionally start the worker

```bash
# Run from within the skill
claude-mem install
# Then start
claude-mem start
```

The worker will keep running in the background until stopped.

**Note:** claude-mem is licensed AGPL-3.0. By using it, you agree to the license terms.

## Use Cases

- **Cross-session memory:** After a week of work on a feature, OpenClaw still remembers the architecture decisions you made.
- **Onboarding:** New project? Search "how we handle auth" to retrieve past discussions.
- **Debugging:** "We fixed a similar bug last month" — search finds the fix.
- **Progress tracking:** Automatic summaries show what was done each day.
- **Token savings:** Instead of re-sending full history, send 3-5 relevant memory snippets (~1k tokens) that capture the essence.

## Web UI

Visit `http://localhost:37777/ui` for:
- Live observation feed
- Search interface
- Session summaries
- Settings adjustments

Real-time view of what claude-mem is seeing.

## Troubleshooting

**Worker not starting**
- Ensure Node.js and Bun installed (`node --version`, `bun --version`)
- Check ports: 37777 must be free
- Look at logs: `~/.claude-mem/logs/`

**Search returns no results**
- Has enough time passed? Auto-capture may be off.
- Check `claude-mem status` — is the worker running?
- Verify `OPENCLAU_MEM_ENABLED` is set to `true`.

**High token usage on retrieval**
- Use the 3-layer pattern; avoid `get` on many IDs at once.
- Limit searches (`--limit 5`) before expanding.

## Advanced: Direct API

The worker exposes REST endpoints:

```
POST /api/observation   — store observation
GET  /api/observation/:id — fetch
GET  /api/search?q=... — search
GET  /api/timeline?around=... — timeline
GET  /api/summaries — session summaries
```

Use these directly if you need tighter integration.

---

**Note:** claude-mem is developed by thedotmack. This skill wraps its worker API. For advanced usage, refer to the upstream documentation at https://github.com/thedotmack/claude-mem.

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
