---
name: lean-ctx
description: "Token optimizer that compresses CLI output, file reads, and project context to reduce LLM token consumption by up to 99%. Use when running resource-intensive tasks, processing large files, or when token budget is tight. Integrates via shell hook for transparent compression or via direct API calls. Provides analytics to track savings. Essential for Termux/Android and other resource-constrained environments."
---

# Lean Ctx

## Overview

`lean-ctx` wraps the [lean-ctx](https://github.com/yvgude/lean-ctx) binary to provide token-efficient command execution, file reading, and analytics within OpenClaw. It reduces the number of tokens sent to and from the LLM by:

- Compressing CLI output (git, cargo, npm, docker, etc.)
- Caching file reads with smart modes (`map`, `signatures`, `diff`, `aggressive`)
- Maintaining cross-session memory (CCP) to avoid cold starts
- Applying Token Dense Dialect (TDD) for compact communication

**Designed for:** Developers on limited token budgets or slow connections, and for CI/CD pipelines where token efficiency matters.

## Quick Start

```bash
# Initialize shell hook (compresses all supported commands automatically)
lean-ctx init

# Run a command with compression
lean-ctx run "git status"

# Read a file with optimal mode
lean-ctx read src/main.py --mode signatures

# Show token savings statistics
lean-ctx gain

# Start the MCP server for editor integration (optional)
lean-ctx mcp-server
```

## Capabilities

### 1. Command Compression (`run`)

Execute shell commands with output compression. Uses 90+ built-in patterns for git, npm, cargo, docker, kubectl, etc.

```bash
lean-ctx run "git log --oneline -10"
lean-ctx run "cargo test -- --nocapture"
lean-ctx run "npm ls --depth=0"
```

**Options:**
- `--show-original` — Display raw output alongside compressed
- `--json` — Output machine-readable stats (tokens saved, compression ratio)

**Example output:**
```
$ lean-ctx run "git status"
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  modified:   src/lib.rs
  deleted:    tests/test_api.rs

→ [compressed: 245→73 tokens, -70%]
```

### 2. Smart File Reading (`read`)

Read files with different optimization modes:

| Mode | Use Case | Token Cost |
|------|----------|------------|
| `full` | Editing (cached after first read) | 100% first, ~0% subsequent |
| `map` | Quick overview (deps + exports) | ~5-15% |
| `signatures` | API surface, no bodies | ~10-20% |
| `diff` | Re-reading changed files | only changed lines |
| `aggressive` | Large boilerplate files | ~30-50% |
| `entropy` | Repetitive patterns | ~20-40% |
| `lines:10-50,80-90` | Specific line ranges | proportional |

```bash
lean-ctx read Cargo.toml --mode map
lean-ctx read src/lib.rs --mode signatures
lean-ctx read src/main.rs --mode "lines:1-100"
```

### 3. Token Analytics (`gain`)

Show persistent token savings statistics across sessions:

```bash
lean-ctx gain              # Visual dashboard with bars and sparklines
lean-ctx gain --graph      # 30-day savings chart
lean-ctx gain --daily      # Day-by-day breakdown with USD estimates
lean-ctx gain --json       # Raw JSON export
```

Output includes:
- Total tokens saved
- Compression percentage
- Commands run
- USD saved ($2.50 per 1M tokens)
- Top commands by savings

### 4. Shell Hook Integration (`init`)

Install shell aliases to automatically compress common commands:

```bash
# Add to ~/.zshrc or ~/.bashrc
lean-ctx init --global
```

This creates aliases for: `git`, `npm`, `pnpm`, `yarn`, `cargo`, `docker`, `docker-compose`, `kubectl`, `gh`, `pip`, `ruff`, `go`, `golangci-lint`, `eslint`, `prettier`, `tsc`, `ls`, `find`, `grep`, `curl`, `wget`, etc.

After installing, any command run through OpenClaw's `exec` that uses these aliases will be automatically compressed if the shell profile is sourced.

### 5. MCP Server (`mcp-server`)

(Optional) Start the MCP server for editor integrations. Not needed for OpenClaw skill usage, but useful if you also use Cursor, Copilot, or Windsurf:

```bash
lean-ctx mcp-server &
```

## Examples

**Before:** Running `git status` on a large repo might produce 800 tokens of output. The LLM sees all of it.

**After:** `lean-ctx run "git status"` compresses to ~150 tokens, preserving only relevant information (file names, statuses) in a structured format.

**File reads:** Reading a 2000-line file (~8000 tokens) in `map` mode reduces to ~400 tokens (dependency graph + exports).

**Analytics:** After a week of use, `lean-ctx gain` might show:

```
  150k tokens saved  78% compression  412 commands   $0.38 USD saved
```

## Installation

If `lean-ctx` binary is not in PATH, you need to install it first.

**Option A: Cargo (recommended on Termux)**
```bash
cargo install lean-ctx
# Binary installed to ~/.cargo/bin/lean-ctx
```

**Option B: Homebrew**
```bash
brew tap yvgude/lean-ctx
brew install lean-ctx
```

**Option B: Build from source**
```bash
git clone https://github.com/yvgude/lean-ctx.git
cd lean-ctx/rust
cargo build --release
cp target/release/lean-ctx ~/.local/bin/
```

**Verify:**
```bash
lean-ctx --version   # should print version
```

## Notes for OpenClaw

- The `run` and `read` scripts invoke the `lean-ctx` binary. Ensure it's in PATH or set `LEAN_CTX_BIN` environment variable.
- The `init` command modifies shell configuration files. Use with care.
- Statistics are stored in `~/.lean-ctx/stats.json`. The `gain` command reads this file.
- Compression is lossy but preserves functional information. For legal/contractual text, review compressed output.

## Troubleshooting

**"lean-ctx: command not found"**
- Install lean-ctx (see Installation)
- Or set `LEAN_CTX_BIN` to the full path: `export LEAN_CTX_BIN=/path/to/lean-ctx`

**"Shell hook not active"**
- After `lean-ctx init --global`, restart your shell or `source ~/.zshrc` (or `~/.bashrc`).
- In OpenClaw, if you use `exec` with a non-login shell, ensure the alias definitions are sourced. You may need to wrap commands with `bash -c "git status"` after init to pick up aliases.

**Poor compression**
- Not all commands have patterns. Unrecognized commands get generic filtering (ANSI removal, whitespace collapse). Use `lean-ctx discover` to analyze shell history and find missed opportunities.

**Memory usage**
- lean-ctx caches file reads in memory. For very large projects, cache can grow; adjust `LEAN_CTX_CACHE_SIZE` or use `ctx_cache(action: "clear")`.

## Resources

### scripts/
- `run.py` — Executes `lean-ctx -c "<command>"` and formats output
- `read.py` — Calls `lean-ctx read <path> --mode <mode>`
- `gain.py` — Runs `lean-ctx gain` with optional format flags
- `init.py` — Runs `lean-ctx init --global` (shell hook installation)
- `mcp_server.py` — Starts the MCP server (background)

### references/
- `modes.md` — Detailed file read modes and when to use each
- `shell_patterns.md` — List of 90+ compressed commands and their patterns
- `integration.md` — How to integrate lean-ctx with OpenClaw, Cursor, Copilot, etc.

## Advanced

### Custom Compression Patterns

If you have custom commands not covered, create a TOML config at `~/.lean-ctx/config.toml`:

```toml
[patterns.mycmd]
regex = "mycmd --verbose .+"
replace = "mycmd $1"  # keep only first argument
```

See `references/shell_patterns.md` for pattern examples.

### CCP Cross-Session Memory

Enable CCP (Context Continuity Protocol) to persist task context across OpenClaw sessions:

```bash
lean-ctx config set ccp.enabled true
```

Then, use the `ctx_session` MCP tool (exposed via lean-ctx MCP server) to store and retrieve context. OpenClaw can integrate via HTTP API if needed.

---

**Note:** lean-ctx is developed by yvgude. This skill simply wraps its CLI. Refer to the upstream documentation for detailed technical deep-dives.

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
