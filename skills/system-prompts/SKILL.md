---
name: system-prompts
description: "Curated library of system prompts for AI agents: coding, review, testing, DevOps, creative, analytical. Use to quickly find high-quality prompts for your agents, or contribute your own. Supports categories, tags, and versioning. Prompts stored as Markdown with YAML frontmatter. Ideal for building agent frameworks (OpenFang, eliza, tgo) or any LLM-based automation."
---

# System Prompts

## Overview

`system-prompts` is a community-curated collection of battle-tested system prompts for every AI agent use case. It provides:

- **Hundreds of prompts** for coding, code review, testing, DevOps, creative writing, analysis, planning, etc.
- **Structured format** — each prompt is a Markdown file with YAML frontmatter (category, tags, model compatibility, temperature guidelines)
- **Easy discovery** — browse by category, search by tags, or get personalized recommendations
- **Version control** — prompts evolve; track changes and improvements

**Designed for:** AI agent builders who need high-quality, reusable system prompts without reinventing the wheel.

## Quick Start

```bash
# 1. Clone the repository (if not already)
# Already in external/system-prompts-and-models-of-ai-tools/

# 2. Explore prompts
system-prompts list --category coding
system-prompts get code-reviewer
system-prompts search "security audit"

# 3. Use a prompt in your agent
# Example: set as OpenAI system message
{
  "role": "system",
  "content": "$(system-prompts get code-reviewer --format raw)"
}
```

## Capabilities

### 1. List Prompts

```bash
system-prompts list [--category <cat>] [--tag <tag>] [--json]
```

Shows available prompts with short descriptions.

**Categories:**
- `coding` — programming, debugging, refactoring
- `review` — code review, security audit, performance review
- `testing` — test generation, property-based testing
- `devops` — deployment, monitoring, incident response
- `creative` — storytelling, naming, marketing copy
- `analytical` — research, summarization, data analysis
- `planning` — project planning, architecture design
- `teaching` — explanations, tutoring, examples

### 2. Get Prompt

```bash
system-prompts get <name> [--format json|raw]
```

Retrieves full prompt content. `--format raw` outputs just the prompt text (for direct injection).

**Example:**
```bash
prompt=$(system-prompts get senior-engineer --format raw)
openai chat --system "$prompt" --user "Review this PR..."
```

### 3. Search

```bash
system-prompts search "<query>" [--json]
```

Full-text search across prompt titles, descriptions, and content.

### 4. Info

```bash
system-prompts info <name>
```

Shows metadata: category, tags, recommended model (GPT-4, Claude, Llama), temperature, token count.

### 5. Contribute

If you have a great prompt, add it to the `prompts/` directory following the template:

```markdown
---
name: my-prompt
category: coding
tags: [python, testing, pytest]
models: [gpt-4o, claude-sonnet-4]
temperature: 0.2
last_updated: 2026-04-01
---

# My Prompt

You are a...
```

Then submit a PR to the upstream repository.

## Integration with Agent Frameworks

- **OpenFang Hands** can use these prompts as their `system_prompt` directly
- **eliza** characters can load prompts from here
- **tgo** agents can reference them
- **gh-aw** and **gstack** modes are essentially system prompts; this library provides alternatives

## Use Cases

- **Standardize code reviews** across team: use the same "senior-engineer" prompt
- **Onboarding new agents** — pick a prompt that matches the desired persona
- **A/B testing** — try different prompts for the same task and compare results
- **Prompt engineering** — study the curated prompts to learn what works

## Repository Structure

```
system-prompts-and-models-of-ai-tools/
├── prompts/
│   ├── code-reviewer.md
│   ├── security-auditor.md
│   ├── test-writer.md
│   └── ...
├── models/            # (optional) model-specific adjustments
└── README.md
```

## Resources

### scripts/
- `list.py` — List available prompts
- `get.py` — Retrieve a prompt
- `search.py` — Search prompts
- `info.py` — Show metadata
- `validate.py` — Validate prompt file format

### references/
- `prompt_structure.md` — Frontmatter fields and best practices
- `categories.md` — Category definitions and examples
- `temperature_guide.md` — How to choose temperature per task

---

**Note:** This skill wraps the system-prompts-and-models-of-ai-tools repository. For more info: https://github.com/SomeOneUnknown/system-prompts-and-models-of-ai-tools

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
