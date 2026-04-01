---
name: gstack
description: "Collection of specialist cognitive modes for Claude Code: plan-ceo-review, plan-eng-review, review, ship, browse, qa, setup-browser-cookies, retro. Use these to switch AI mental gears on demand. This skill provides quick-reference and usage patterns. To actually use them, install gstack in Claude Code first (see Installation)."
---

# Gstack

## Overview

`gstack` is not an OpenClaw skill per se; it's a suite of **specialist modes for Claude Code** created by Garry Tan. Each mode gives the AI a different cognitive style:

- `/plan-ceo-review` → Founder/CEO mindset (10-star product thinking)
- `/plan-eng-review` → Engineering manager (architecture, diagrams, edge cases)
- `/review` → Paranoid staff engineer (find bugs that pass CI)
- `/ship` → Release engineer (sync, test, PR)
- `/browse` → QA engineer (browser automation, screenshots)
- `/qa` → QA lead (systematic testing of affected routes)
- `/setup-browser-cookies` → Session manager (import real browser cookies)
- `/retro` → Engineering manager (retrospective analysis)

## When to Use Which Mode

| Situation | Mode |
|-----------|------|
| "I want to build X" → Is X the right thing? | `/plan-ceo-review` |
| "How do we implement X?" | `/plan-eng-review` |
| "Review my PR" | `/review` |
| "Branch ready to land" | `/ship` |
| "Check staging UI manually" | `/browse` |
| "Verify my changes work" | `/qa` |
| "Test authenticated pages" | `/setup-browser-cookies` then `/qa` |
| "Weekend retro" | `/retro` |

## Installation

**If you haven't installed gstack yet:**

Open Claude Code and run:

```
/plugin marketplace add garrytan/gstack
/plugin install gstack
```

That installs the skills into `~/.claude/skills/gstack` and symlinks them.

**Project-specific install:**

```bash
git clone https://github.com/garrytan/gstack.git .claude/skills/gstack
cd .claude/skills/gstack && ./setup
```

Add a `gstack` section to your project's `CLAUDE.md` describing the skills.

## Example Workflow

```
1. Describe feature in plain language
2. /plan-ceo-review → "What's the 10-star version?"
3. /plan-eng-review → Architecture diagram, state machine, edge cases
4. Implement
5. /review → Paranoid pass
6. /ship → Land it
7. /qa → Verify on staging
```

## Integration with OpenClaw

While gstack is designed for Claude Code, you can still:
- Keep it installed for Claude Code sessions
- Use OpenClaw for background tasks and automation
- Reference gstack's prompts to shape OpenClaw's behavior (copy the ideas)

## References

### references/
- `modes.md` — Detailed explanation of each mode with examples
- `installation.md` — Step-by-step install and troubleshooting
- `usage.md` — Common workflows and tips

---

**Note:** This skill is a *reference wrapper*; it does not execute gstack commands. To actually use `/plan-ceo-review` etc., you need the gstack plugin installed in Claude Code. This skill merely documents them for quick lookup within OpenClaw.

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
