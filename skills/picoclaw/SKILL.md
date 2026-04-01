---
name: picoclaw
description: "An ultra-lightweight AI agent (~10MB RAM) written in Go. Use for simple task automation, command execution, and file operations on resource-constrained devices. Ideal for Termux/Android where memory is scarce. Provides a small, fast agent that can interpret goals and execute shell commands safely. Think of it as a tiny 'assistant' that lives in your terminal."
---

# Picoclaw

## Overview

`picoclaw` is a minimalist AI agent that runs on very limited hardware. It uses a small local model (or remote API) to parse natural language goals into shell commands, then executes them with safety checks.

**Key characteristics:**
- **Tiny footprint:** ~10MB RAM, ~2MB binary
- **Fast startup:** <1 second
- **Offline-capable:** Can use local LLM (GGUF) or remote API
- **Safety guardrails:** Confirms destructive commands before running

**Designed for:** Resource-constrained environments (Termux/Android, Raspberry Pi) where full LLM agents like Claude or GPT-4 are overkill or unavailable.

## Quick Start

```bash
# 1. Build or download picoclaw binary
cd /root/.openclaw/workspace/external/picoclaw
go build -o picoclaw ./cmd/picoclaw
mv picoclaw ~/.local/bin/

# 2. Configure model (optional)
export PICOCLAW_MODEL="qwen2.5:3b"    # if using local LLM via ollama
# or
export PICOCLAW_OPENAI_API_KEY="sk-..."  # if using OpenAI

# 3. Run a task
picoclaw "list files larger than 10MB"
picoclaw "find all Python files containing 'TODO'"
picoclaw "compress old log files in ~/logs"
```

## Capabilities

### 1. Goal → Command

You provide a plain-English description; picoclaw decides which shell command(s) to run.

**Examples:**
- "Count lines of code in this project"
- "Show disk usage sorted by size"
- "Kill processes using port 8080"
- "Backup my dotfiles to /storage/emulated/0/backup"

### 2. Safety Confirmation

For potentially destructive commands (rm, mv, kill, dd), picoclaw prompts for confirmation:
```
? This will delete 15 files. Continue? [y/N]
```

This can be disabled with `--force`, but not recommended.

### 3. Multi-step Plans

Complex goals can be broken into sequential commands:
```
$ picoclaw "Set up a new Node.js project, install express, and create server.js"
# Steps:
# 1. mkdir myapp && cd myapp && npm init -y
# 2. npm install express
# 3. echo "const express = require('express')..." > server.js
# ...
```

### 4. File Operations

Can read/write files, search content, move/rename, etc.

## Configuration

Environment variables:

| Variable | Purpose |
|----------|---------|
| `PICOCLAW_MODEL` | Local model name (if using Ollama) |
| `PICOCLAW_OPENAI_API_KEY` | OpenAI API key (if using cloud) |
| `PICOCLAW_ANTHROPIC_API_KEY` | Anthropic key |
| `PICOCLAW_MAX_STEPS` | Max commands per goal (default: 5) |
| `PICOCLAW_WORKDIR` | Default working directory |
| `PICOCLAW_CONFIRM_DESTRUCTIVE` | `true`/`false` (default: true) |

## Integration with OpenClaw

The `picoclaw` skill provides a simple wrapper:

```bash
tool("picoclaw", "run", goal="Show largest files in current directory")
```

This is useful when you need a quick agent but don't want to spawn a heavy LLM.

## Use Cases

- **Quick file ops:** "Find duplicate files" → runs `fdupes` or custom script
- **System maintenance:** "Clean package cache" → `apt clean`
- **Code tasks:** "List all functions in this file" → `grep -E '^func '` or similar
- **Mobile file management:** On Termux, "move photos to DCIM" → mv commands

## Limitations

- Not a general-purpose LLM; it's a command generator with limited reasoning
- Requires well-defined shell environment (coreutils, find, grep, etc.)
- May fail on highly complex multi-step tasks
- Quality depends on the underlying model (use qwen2.5:3b or GPT-4o)

## Installation

On Termux:
```bash
# Ensure Go is installed
pkg install go

# Build
cd /root/.openclaw/workspace/external/picoclaw
go build -o picoclaw ./cmd/picoclaw
chmod +x picoclaw
mv picoclaw ~/.local/bin/
```

## Resources

### scripts/
- `run.py` — Execute a goal
- `shell.py` — Interactive REPL (like chat but for shell)
- `config.py` — Print effective configuration

### references/
- `safety.md` — Destructive command patterns and confirmation rules
- `prompt_templates.md` — How goals are turned into LLM prompts
- `model_choices.md` — Which models work best (qwen2.5:3B recommended)

---

**Note:** picoclaw is developed by the OpenClaw community. For upstream issues, see https://github.com/openclaw/picoclaw

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
