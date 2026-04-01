---
name: git-status-summary
description: "Quick overview of git repositories: changed files, branch status, ahead/behind counts, stashes, and recent commits. Use for daily standups, heartbeat checks, or before starting work to see what needs attention. Scans a directory (or common dev folders) and produces a concise, color-coded summary. Ideal for developers managing multiple repos."
---

# Git Status Summary

## Overview

`git-status-summary` scans directories to find git repositories and produces a concise, at-a-glance report showing:

- Repository location and current branch
- Working tree status (clean, modified, untracked, staged)
- Ahead/behind remote tracking branch
- Recent commit (hash, author, date, message snippet)
- Stash count
- Open pull requests (if GitHub remote detected)

**Designed for:** Developers juggling multiple projects who need a quick "what's the state" without running `git status` in each repo manually.

## Quick Start

```bash
# Scan current directory recursively
git-status-summary .

# Scan common dev directories
git-status-summary ~/projects

# Scan specific paths
git-status-summary ~/code/ ~/work/

# Include all details (full commit messages, file lists)
git-status-summary . --verbose

# Output machine-readable JSON
git-status-summary . --output json
```

## Examples

**User:** "What's the status of my repos?"  
**Nero:** `git-status-summary ~/projects` → produces table:

```
=== Git Summary (12 repos scanned) ===

✅ ~/projects/clawd
   branch: main ↑1 (ahead of origin/main)
   last: abc123 (2h ago) "Fix token parser edge case"
   status: clean

⚠️  ~/projects/webapp
   branch: feature/auth ↑2
   last: def456 (1d ago) "Add OAuth2 flow"
   status: 3 modified, 2 untracked
   stashes: 1

❌ ~/projects/old-api
   branch: develop ↓3 (behind origin/develop)
   last: ghi789 (2w ago) "Refactor DB layer"
   status: 1 modified
   PR: #45 open (needs review)
```

**User:** "Any repos need committing?"  
**Nero:** Scans and filters to show only dirty repos.

**User:** "Morning briefing"  
**Nero:** Includes `git-status-summary` as part of daily digest (heartbeat or morning routine).

## Options

| Flag | Description |
|------|-------------|
| `--path <dir>` | Directory to scan (default: current) |
| `--max-repos <N>` | Limit number of repos shown |
| `--verbose` | Show full commit messages, modified file lists |
| `--output <text\|json>` | Output format (default: text) |
| `--github-token <token>` | Fetch PR info from GitHub API |
| `--depth <N>` | Max commit depth (default: 1) |

## Output Columns

| Column | Meaning |
|--------|---------|
| Status icon | ✅ clean, ⚠️ modified, ❌ detached/conflict |
| Repo path | Shortened path (relative to scanned dir) |
| Branch | Current branch + ahead/behind indicators |
| Last commit | Short hash, time ago, one-line message |
| Dirty count | # modified, # untracked, # staged |
| Stashes | Number of saved work-in-progress |
| PR | Open PR number and status (if available) |

## Integration

- **Heartbeat**: Include in periodic checks to track development activity
- **Pre-commit ritual**: Run before daily coding to remind of unfinished work
- **Project management**: Combine with `skill-health` and `resource-check` for full dev environment health
- **CI/CD triggers**: Use JSON output to gate deployments (e.g., fail if any repo dirty)

## Resources

### scripts/
- `main.py` — Entry point; argument parsing, scanning logic, formatting
- `scanner.py` — Discovers git repos by looking for `.git` directories
- `reporter.py` — Formats output (text table and JSON)
- `git_wrapper.py` — Runs git commands safely, handles errors

### references/
- `output_formats.md` — Details on text table layout and JSON schema
- `performance_tips.md` — How to scan efficiently (caching, parallelization)
- `github_integration.md` — Using GitHub API for PR/issue metadata

## Advanced Usage

### GitHub PR Integration

If you provide a GitHub token (or have `gh` auth configured), `git-status-summary` can fetch:

- Open PRs for the current branch
- Review requests assigned to you
- CI status checks

This requires remote URL to be GitHub (`github.com/owner/repo`).

### Filtering

Only show repos with issues:
```bash
git-status-summary ~/projects --filter dirty,behind,pr-open
```

### Caching

For large repos (100+), scanning can be slow. Use `--cache-file ~/.cache/git-summary.json` to store results for 5 minutes.

---

**Note:** This skill uses standard `git` commands. No external dependencies beyond Python. Works in Termux (install `git` package if not present).


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
