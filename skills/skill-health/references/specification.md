# AgentSkills Specification (for skill-health reference)

This document summarizes the key requirements of the AgentSkills specification as they relate to health validation.

## Directory Structure

```
skill-name/
├── SKILL.md (required)
├── scripts/ (optional)
├── references/ (optional)
└── assets/ (optional)
```

**Valid:**
- Skill directories may contain scripts/, references/, assets/
- Additional files are allowed if they support the skill's functionality

**Invalid:**
- README.md, INSTALL.md, CHANGELOG.md (auxiliary docs not part of spec)
- .git directories are allowed but not required

## SKILL.md Requirements

### 1. YAML Frontmatter

Must include exactly two fields:
- `name` (string): skill name
- `description` (string): comprehensive explanation of what the skill does and when to use it

Example:
```yaml
---
name: pdf-editor
description: Comprehensive PDF manipulation including merging, splitting, text extraction, and form filling. Use when working with PDF files for document processing, archival, or data extraction tasks.
---
```

### 2. Body

Markdown documentation. Should include:
- Overview of capabilities
- Workflows or task-based guidance
- Examples of user requests that trigger this skill
- References to bundled resources as needed

### 3. Naming Conventions

- Skill name: lowercase, hyphen-separated (e.g., `git-commit`, `frontend-builder`)
- Directory name must match the `name` field (normalized)
- Length: 1-64 characters (letters, digits, hyphens only)

## Common Validation Failures

| Code | Severity | Description | Fix |
|------|----------|-------------|-----|
| MISSING_FRONTMATTER | critical | SKILL.md doesn't start with `---` | Add YAML frontmatter |
| MISSING_NAME | critical | Frontmatter lacks `name` field | Add `name:` |
| MISSING_DESCRIPTION | critical | Frontmatter lacks `description` field | Add `description:` |
| NAME_MISMATCH | warning | Directory name ≠ SKILL.md name | Align names |
| SHORT_DESCRIPTION | warning | Description < 20 chars | Expand with triggers |
| BODY_TOO_LARGE | warning | Body > 5000 words | Move content to `references/` |
| DISALLOWED_FILE | warning | Contains README.md, etc. | Remove auxiliary docs |
| SCRIPT_NOT_EXECUTABLE | info | Script missing +x flag | Run `chmod +x` |

## Health Scoring Algorithm

Start at 100 points. Deductions:
- Critical issue: -30 points each
- Warning: -5 points each
- Info: -1 point each

Status thresholds:
- Healthy: score ≥ 90, no critical issues
- Warning: score 70-89, or critical=0 but warnings present
- Error: score < 70 or any critical issues

## Progressive Disclosure

Keep SKILL.md body lean (<500 lines). Move detailed content to:
- `references/` — API docs, schemas, long guides
- `scripts/` — reusable code
- `assets/` — templates, boilerplate, media

## Self-Validation

Skills may include a reference to `specification.md` to stay compliant. Use `skill-health` to validate.
