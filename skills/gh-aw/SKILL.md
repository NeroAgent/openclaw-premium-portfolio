---
name: gh-aw
description: "GitHub Agentic Workflows — AI-powered GitHub automation: auto-review PRs, generate issue descriptions, triage, create changelogs, and more. Uses LLM to assist with GitHub interactions. Wraps the 'gh-aw' CLI for OpenClaw. Requires GitHub CLI (gh) and an LLM (OpenAI/Anthropic/Ollama)."
---

# gh-aw

## Overview

`gh-aw` (GitHub Agentic Workflows) is an AI assistant for GitHub. It can:

- **Review PRs** — generate detailed reviews with code suggestions
- **Write PR descriptions** — auto-generate from diff
- **Write issue descriptions** — flesh out ideas
- **Triage issues** — categorize, suggest labels, detect duplicates
- **Generate changelogs** — from merged PRs since last release

**Designed for:** speeding up GitHub collaboration with AI that knows your codebase.

## Quick Start

```bash
# 1. Install gh-aw (from source or download)
go install github.com/rightnow-ai/gh-aw@latest

# 2. Authenticate GitHub (requires gh CLI)
gh auth login

# 3. Configure LLM (OpenAI, Anthropic, or Ollama)
export OPENAI_API_KEY="sk-..."
# or
export ANTHROPIC_API_KEY="sk-..."
# or use local Ollama
export GH_AW_LLM="ollama"
export GH_AW_LLM_MODEL="llama3.2:3b"

# 4. Review a PR
gh-aw review 123 --repo owner/repo

# 5. Generate PR description from branch
gh-aw pr-description --repo owner/repo --branch feature/foo
```

## Capabilities

### 1. PR Review

```bash
gh-aw review <pr_number> [--repo <owner/repo>]
```

The AI reads the diff, codebase context (via GitHub API), and produces:
- Overall assessment
- Line-by-line comments (specific suggestions)
- Identified risks/edge cases
- Test coverage gaps

Options:
- `--level < thorough|quick >` — depth of review (default: thorough)
- `--output <json|markdown>` — format of review

### 2. PR Description Generation

```bash
gh-aw pr-description --repo owner/repo --branch my-branch
```

Creates a conventional commit-style description summarizing changes. Useful when you haven't written one yet.

### 3. Issue Description

```bash
gh-aw issue-description --create --repo owner/repo --title "Bug: login fails"
```

Takes a rough issue title and expands into a full description with:
- Problem statement
- Steps to reproduce
- Expected vs actual
- Environment details

### 4. Triage

```bash
gh-aw triage --repo owner/repo --limit 20
```

Analyzes open issues:
- Suggests labels (`bug`, `enhancement`, `question`)
- Detects duplicates (by similarity)
- Assigns priority (P0-P3)
- Recommends assignment (if CODEOWNERS)

Output can be applied automatically with `--apply`.

### 5. Changelog

```bash
gh-aw changelog --since v1.2.0 --to v1.3.0 --repo owner/repo
```

Generates release notes grouped by type (features, fixes, breaking changes). Uses conventional commit messages.

## Integration with OpenClaw

The `gh-aw` skill provides simple wrappers:

```bash
tool("gh-aw", "review", pr=123, repo="owner/repo", level="quick")
tool("gh-aw", "pr-description", repo="owner/repo", branch="feature/xyz")
tool("gh-aw", "triage", repo="owner/repo", limit=50, apply=False)
tool("gh-aw", "changelog", since="v1.0.0", to="v1.1.0", repo="owner/repo")
```

This allows OpenClaw to automate GitHub maintenance tasks autonomously.

## Configuration

- `GH_AW_LLM` — `openai`, `anthropic`, or `ollama` (default: `openai`)
- `GH_AW_LLM_MODEL` — Model name (e.g., `gpt-4o`, `claude-sonnet-4`, `llama3.2:3b`)
- `GH_AW_REPO` — Default repo (can override per command)
- `GH_AW_CONTEXT_LINES` — Number of source lines to include for each changed file (default: 5)

For Ollama integration:
```bash
export GH_AW_LLM="ollama"
export GH_AW_LLM_BASE_URL="http://localhost:11434"
export GH_AW_LLM_MODEL="llama3.2:3b"
```

## Use Cases

- **Every PR gets a review:** Run `gh-aw review` automatically on new PRs via GitHub Actions or OpenFang Hand
- **Triage incoming issues:** Daily batch triage to keep backlog organized
- **Generate changelog:** Before release, run `gh-aw changelog` to draft notes
- **Help contributors:** Use `gh-aw issue-description` to improve issue quality

## Dependencies

- `gh` CLI installed and authenticated
- LLM provider (OpenAI, Anthropic, or Ollama)
- Go toolchain if building from source

## Installation on Termux

```bash
pkg install go
go install github.com/rightnow-ai/gh-aw@latest
# Binary to ~/.local/bin/gh-aw
```

Or download prebuilt for ARM64 if available.

## Limitations

- LLM token limits can restrict review of very large PRs (>500 lines). Consider splitting.
- Accuracy depends on model quality; use GPT-4o or Claude Sonnet for best results.
- Requires network access to GitHub API and LLM.

---

**Note:** gh-aw is developed by RightNow-AI. This skill wraps its CLI. https://openfang.sh/docs/gh-aw

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
