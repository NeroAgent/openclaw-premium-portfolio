---
name: openfang
description: "Agent Operating System — run autonomous 'Hands' that work for you 24/7. Use to schedule, monitor, and control OpenFang agents: research, knowledge graphs, social media management, lead generation, reporting. Provides a single binary (~32MB) that compiles to a full agent runtime. Requires Rust toolchain to build, or download prebuilt. OpenFang runs headless with dashboard at localhost:4200."
---

# OpenFang

## Overview

OpenFang is not just another agent framework — it's an **Agent Operating System**. It runs autonomous agents called **Hands** that work on schedules, continuously, without you having to prompt them. Each Hand is a self-contained capability: competitor research, knowledge graph building, social posting, lead gen, etc.

OpenFang compiles to a single ~32MB binary. It's written in Rust, battle-tested (1,767+ tests, zero clippy warnings).

**Designed for:** 24/7 autonomous work — let agents monitor, research, and report while you sleep.

## Quick Start

```bash
# 1. Install openfang binary
# From prebuilt (if available) or build from source
cargo install openfang   # or download from https://openfang.sh

# 2. Initialize configuration
openfang init

# 3. Start the agent system (runs in background by default)
openfang start

# 4. Open dashboard
openfang dashboard  # http://localhost:4200

# 5. List available Hands
openfang hands list

# 6. Enable a Hand (e.g., research-competitors)
openfang hands enable research-competitors
```

## Architecture

- **Core** — Single binary, embedded SQLite for state, Redis for queue (optional)
- **Hands** — Pre-built autonomous modules with system prompts, guardrails, dashboard metrics
- **Dashboard** — Web UI at `http://localhost:4200` to monitor activity, view logs, adjust settings
- **Scheduler** — Cron-like scheduling for Hands
- **Skill interface** — Hands can use MCP tools, browse web, send emails

## Capabilities

### 1. System Control

```bash
openfang init      # Create config directory (~/.openfang)
openfang start     # Start daemon (foreground or background)
openfang stop      # Stop daemon
openfang status    # Check if running
openfang restart   # Restart
openfang dashboard # Open web UI in browser
```

### 2. Hands Management

```bash
openfang hands list                # Show all available Hands
openfang hands enable <name>       # Enable a Hand (starts running on schedule)
openfang hands disable <name>      # Disable
openfang hands config <name>       # Edit Hand configuration (HAND.toml)
openfang hands logs <name>         # View logs for a specific Hand
```

**Built-in Hands:**
- `research-competitors` — Daily competitor intelligence
- `knowledge-graph` — Build semantic knowledge graph from your notes
- `social-manager` — Post to Twitter/LinkedIn on schedule
- `lead-generator` — Scrape and qualify leads
- `daily-briefing` — Morning report aggregating all Hands
- `uptime-monitor` — Monitor services, alert on downtime
- `expense-tracker` — Categorize expenses from emails

### 3. Dashboard

Visit `http://localhost:4200` to:
- See real-time Hand activity
- View execution logs and metrics
- Manually trigger Hands
- Edit configurations
- Manage approvals (for sensitive actions)

### 4. Extending with Custom Hands

You can write your own Hands in TOML + prompt:

```toml
# HAND.toml
name = "my-custom-hand"
schedule = "0 9 * * *"  # daily at 9am
system_prompt = "You are a research agent. Every day, search for news about AI and summarize top 5."
tools = ["web_search", "rss", "email_send"]
approval_required = false
```

Place in `~/.openfang/hands/` and `openfang reload`.

## Integration with OpenClaw

OpenFang runs independently, but OpenClaw can:
- Start/stop OpenFang via `openfang start/stop`
- Trigger a Hand run on demand: `openfang hands trigger <name>`
- Pull logs for analysis: `openfang hands logs <name>`
- Query dashboard metrics via local HTTP API (if enabled)

This allows OpenClaw to schedule heavy autonomous tasks that run in the background, while OpenClaw itself handles interactive tasks.

## Resource Considerations

- **Memory:** ~200MB baseline + per-Hand overhead (50-200MB depending on LLM usage)
- **CPU:** Idle low; spikes during Hand execution
- **Disk:** ~100MB for binary + SQLite DB + logs (rotated)
- **Network:** Depends on Hands (web search, API calls)

**Termux note:** OpenFang is 32MB RAM baseline plus LLM inference; on mobile, use sparingly. Better to run on a small server/VPS.

## Installation on Termux

Building requires Rust (heavy). Recommended: Build on workstation, copy binary to Termux, or run on server.

If you must build on Termux:
```bash
pkg install rust
git clone https://github.com/RightNow-AI/openfang.git
cd openfang
cargo build --release
cp target/release/openfang ~/.local/bin/
```

But expect long compile time and high memory during build.

## Configuration

Main config at `~/.openfang/config.toml`. You can set:

```toml
[general]
dashboard_port = 4200
data_dir = "~/.openfang/data"
log_level = "info"

[database]
sqlite_path = "~/.openfang/data/state.db"

[redis]
url = "redis://localhost:6379"  # optional, for queue

[llm]
provider = "ollama"   # or "openai", "anthropic"
model = "llama3.2:3b"
api_base = "http://localhost:11434"  # for Ollama
```

## Use Cases

- **Lead generation:** Hand scrapesCrunchbase, qualifies, emails you daily
- **Competitor tracking:** Monitors competitors' blogs, pricing pages, job posts
- **Social presence:** Auto-posts curated content daily
- **Uptime monitoring:** Checks your services, pings you if down
- **Knowledge synthesis:** Reads your notes, builds graph, answers questions

## Resources

### scripts/
- `init.py` — Initialize config directory
- `start.py` — Start daemon
- `stop.py` — Stop daemon
- `status.py` — Check status
- `hands_list.py` — List Hands
- `hands_enable.py` / `disable.py` / `config.py` / `logs.py` / `trigger.py`
- `dashboard.py` — Open dashboard URL

### references/
- `hand_manifest.md` — HAND.toml format reference
- `dashboard_api.md` — HTTP API for external control
- `scheduling.md` — Cron expressions and scheduling rules
- `tool_integration.md` — How Hands use MCP tools

---

**Note:** OpenFang is developed by RightNow-AI. This skill wraps its CLI. For detailed Hand development, see https://openfang.sh/docs

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
