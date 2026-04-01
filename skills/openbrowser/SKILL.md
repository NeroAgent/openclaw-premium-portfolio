---
name: openbrowser
description: "Autonomous web browsing and search using openbrowser (Playwright + AI). Use when you need to interact with websites, fill forms, extract data, or perform multi-step web tasks that regular search APIs can't handle. Acts as a fallback to DuckDuckGo when search results are insufficient or require interaction. Supports OpenAI, Anthropic, and Google models. Provides both one-shot tasks and interactive REPL mode."
---

# OpenBrowser

## Overview

`openbrowser` wraps the [openbrowser](https://github.com/ntegrals/openbrowser) framework to give AI agents a real browser: they can navigate, click, type, scroll, extract data, and complete complex web workflows autonomously.

**Designed for:** Tasks that go beyond simple search — logging in, filling multi-page forms, scraping dynamic content, testing web apps, automating repetitive web interactions.

## Quick Start

```bash
# One-shot task (non-interactive)
openbrowser run "Find the price of the MacBook Pro on apple.com"

# Interactive REPL (drop into browser session)
openbrowser interactive

# Direct commands
openbrowser open https://example.com
openbrowser click "button.submit"
openbrowser type "input#email" "test@example.com"
openbrowser screenshot page.png
openbrowser extract "main headline"
```

## Capabilities

### 1. Run Agent Tasks (`run`)

Give a natural language description; the AI figures out the steps.

```bash
openbrowser run "Search for 'openclaw github' and star the repository"
openbrowser run "Log into the dashboard, navigate to settings, and export data"
```

**Options:**
- `--model` — Model to use (`gpt-4o`, `claude-sonnet-4`, `gemini-2.0-flash`, etc.)
- `--provider` — `openai`, `anthropic`, or `google`
- `--headless` / `--no-headless` — Show or hide browser window
- `--max-steps` — Limit agent iterations (default: 25)
- `--verbose` — Detailed step-by-step logging

**Example:**
```bash
openbrowser run "Check the weather in Tokyo" --provider anthropic
```

The agent will:
1. Open search engine (DuckDuckGo by default)
2. Enter query
3. Click first result
4. Extract temperature
5. Return answer

### 2. Interactive REPL (`interactive`)

Drop into a live `browser>` prompt:

```
$ openbrowser interactive
browser> open https://news.ycombinator.com
browser> extract "top 5 stories with titles and points"
browser> click .morelink
browser> screenshot page.png
browser> state
```

Great for exploration, debugging, and prototyping.

### 3. Direct Commands

| Command | Purpose |
|---------|---------|
| `open <url>` | Navigate to URL |
| `click <selector>` | Click element (CSS selector) |
| `type <selector> <text>` | Enter text |
| `screenshot [file]` | Capture screenshot |
| `extract <goal>` | Extract content as markdown |
| `eval <js>` | Run JavaScript on page |
| `state` | Show current URL, title, tabs |
| `sessions` | List active browser sessions |

These map to the underlying openbrowser CLI tools.

## Use Cases

- **Research:** "Find recent papers on transformer attention" and extract links/abstracts.
- **Data extraction:** "Get the top 10 products from Amazon bestsellers" with prices and ratings.
- **Form automation:** "Sign up for the newsletter on example.com with email test@example.com."
- **Testing:** "Verify the login flow works on staging.example.com."
- **Fallback search:** When a standard search API (DuckDuckGo) returns no results, use openbrowser to interactively explore.

## Installation

If `open-browser` binary is not in PATH:

```bash
# Clone the repo (already done)
cd /root/.openclaw/workspace/external/openbrowser

# Install dependencies
bun install

# Build the CLI
bun run build

# Optionally symlink to a bin directory
ln -sf /root/.openclaw/workspace/external/openbrowser/packages/cli/dist/index.js /usr/local/bin/open-browser
```

**Requirements:**
- Node.js (already present)
- Bun runtime (install with `curl -fsSL https://bun.sh/install | bash`)
- Playwright browsers (installed automatically on first run)

**Verify:**
```bash
open-browser --help
```

## Environment Variables

- `OPENAI_API_KEY` — for OpenAI provider
- `ANTHROPIC_API_KEY` — for Anthropic
- `GOOGLE_GENERATIVE_AI_API_KEY` — for Google
- `BROWSER_HEADLESS` — `true`/`false` (default: `true`)
- `OPEN_BROWSER_TRACE_PATH` — directory for traces
- `OPEN_BROWSER_SAVE_RECORDING_PATH` — directory for video recordings

Set these before running skills.

## OpenClaw Integration

The `openbrowser` skill provides wrappers:

- `run.py` — executes `open-browser run "<task>"`
- `interactive.py` — starts REPL (foreground)
- `command.py` — runs direct commands like `open`, `click`, `type`, etc.

Example usage within OpenClaw:

```python
# Natural language task
tool("openbrowser", "run", task="Find the latest release of openbrowser on GitHub")

# Direct control
tool("openbrowser", "command", cmd="open", url="https://github.com")
tool("openbrowser", "command", cmd="click", selector=".repo")
```

## Safety & Ethics

- openbrowser runs a real browser; it can click buttons, submit forms, and consume resources.
- Use only on sites you own or have permission to automate.
- Be mindful of rate limits and Terms of Service.
- The `--headless` mode can run invisibly; still respects network traffic.

## Troubleshooting

**"Bun not found"**
- Install Bun: `curl -fsSL https://bun.sh/install | bash`
- Ensure `~/.bun/bin` is in PATH.

**"Playwright browsers not found"**
- First run will auto-install Chromium. This takes a few minutes.
- If it fails, run manually: `bunx playwright install chromium`

**"API key missing"**
- Set the appropriate environment variable for your provider.

**Browser hangs**
- Use `--max-steps` to limit iterations.
- Check `OPEN_BROWSER_TRACE_PATH` for diagnostics.

## References

### scripts/
- `run.py` — Agent task execution
- `interactive.py` — REPL mode
- `command.py` — Direct commands wrapper

### references/
- `architecture.md` — How openbrowser works (agent, viewport, commands)
- `commands.md` — Full reference of available commands
- `configuration.md` — Advanced options and environment variables

---

**Note:** openbrowser is developed by ntegrals. This skill provides a thin OpenClaw wrapper. Refer to upstream docs for detailed API and examples.

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
