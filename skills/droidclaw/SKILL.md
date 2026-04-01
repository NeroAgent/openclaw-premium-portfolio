---
name: droidclaw
description: "AI agent that controls your Android phone via ADB and accessibility. Give it a plain-English goal; it reads the screen, decides taps/swipes/types, and executes until done. Can delegate requests to ChatGPT/Gemini/Google Search on the device and return results. Requires 'adb' and Bun runtime. Use for automating phone workflows, testing, or remote assistance."
---

# Droidclaw

## Overview

`droidclaw` is an AI agent that automates your Android phone. It uses:

- **ADB** (Android Debug Bridge) to send touch/type/swipe events
- **AccessibilityTree** to read screen content
- **LLM** (configurable) to decide next action
- **Bun** runtime (TypeScript)

You describe a goal in plain English, and droidclaw figures out the steps: open apps, tap buttons, enter text, scroll, etc. It's like having a robot finger that thinks.

**Designed for:** Automating repetitive phone tasks, testing mobile UIs, delegating queries to on-device AI (ChatGPT/Gemini apps), and building phone-based agents.

## Quick Start

```bash
# 1. Prerequisites
# - ADB installed and device connected with USB debugging
# - Bun installed (curl -fsSL https://bun.sh/install | bash)
# - Device authorized for debugging

# 2. Install droidclaw
cd /root/.openclaw/workspace/external/droidclaw
bun install

# 3. Run an agent task
bun run src/kernel.ts "Open YouTube and search for 'lofi hip hop'"

# 4. Watch it work (screen mirror optional)
# The agent will output steps and actions.
```

## Capabilities

### 1. Goal-Driven Automation

```bash
bun run src/kernel.ts "<goal>"
```

Examples:
- "Send a WhatsApp message to Alice: 'Running late'"
- "Open Chrome and search for 'weather in Tokyo'"
- "Take a screenshot and save to Downloads"
- "Turn on WiFi and connect to 'MyNetwork'"

The agent observes the screen, thinks, acts, and repeats until the goal is completed or max steps reached.

### 2. Delegate to On-Device AI

Droidclaw can use the device's own AI apps (ChatGPT, Gemini, Google) as "reasoning engines":

```bash
# Configure which app to use for thinking
export DROIDCLAW_DELEGATE="chatgpt"  # or "gemini", "google"
bun run src/kernel.ts "What's the capital of France?"
```

The agent will:
1. Open the designated app
2. Type the question
3. Submit
4. Read the answer from the screen
5. Return the result

### 3. Custom Workflows

Beyond one-off goals, you can encode workflows in Markdown (YAML frontmatter) and run them. See `workflows/` directory.

Example:
```yaml
---
name: daily-check
steps:
  - open: "com.android.settings"
  - tap: "Battery"
  - read: "Battery level"
  - report: "Battery is {battery_level}%"
```

## Configuration

Environment variables:

| Variable | Purpose |
|----------|---------|
| `DROIDCLAW_ADB_PATH` | Path to adb binary (default: `adb`) |
| `DROIDCLAW_LLM` | LLM to use for decisions (`local`, `openai`, `anthropic`) |
| `DROIDCLAW_DELEGATE` | On-device app for delegation (`chatgpt`, `gemini`, `google`) |
| `DROIDCLAW_MAX_STEPS` | Max actions before timeout (default: 30) |
| `DROIDCLAW_SCREENSHOT_DIR` | Where to save screenshots |

## Use Cases

- **Phone automation:** "Every morning at 8am, check notifications and summarize"
- **Testing:** Validate UI flows automatically
- **Data extraction:** "Read latest 5 SMS messages and list senders"
- **Delegated reasoning:** Ask complex questions using on-device ChatGPT without installing separate API

## Installation on Termux

Termux can control an Android device via ADB over TCP/Wi-Fi:

```bash
# Enable ADB over network on device (Developer options)
adb tcpip 5555
adb connect 192.168.1.100:5555

# Then run droidclaw from Termux; it will control the remote device.
```

Alternatively, run droidclaw *on* the Android device itself using Termux (install adb via pkg).

## Limitations

- Requires ADB connection (USB or TCP)
- Screen reading via accessibility may fail on some apps (security restrictions)
- LLM decisions can be slow if using cloud API; local delegates faster
- Not all UI elements are tappable (games with custom rendering may be impossible)

## Resources

### scripts/
- `run.py` — Execute a goal: `bun run src/kernel.ts "<goal>"`
- `workflow.py` — Run a predefined workflow file
- `delegate.py` — Delegate a query to on-device AI
- `adb_helper.py` — Low-level ADB commands (tap, swipe, type)

### references/
- `adb_commands.md` — ADB shell commands for screen interaction
- `accessibility_tree.md` — How screen content is parsed
- `workflows.md` — YAML workflow format
- `delegates.md` — Configuring ChatGPT/Gemini/Google delegates

---

**Note:** droidclaw is experimental. Use with caution; ensure your device is secured. Developed by UnitedByAI. For more details: https://github.com/unitedbyai/droidclaw

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
