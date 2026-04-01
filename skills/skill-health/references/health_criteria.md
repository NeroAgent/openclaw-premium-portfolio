# Health Criteria Reference

This document defines all health checks, their severity, and how to fix them.

## Checks

### Structure

| Code | Severity | Description | Autofixable |
|-------|----------|-------------|-------------|
| FILE_UNREADABLE | critical | SKILL.md cannot be read | No (permissions) |
| MISSING_FRONTMATTER | critical | No `---` at start | Yes |
| INVALID_FRONTMATTER | critical | Unclosed frontmatter | Yes |
| MISSING_NAME | critical | `name:` field absent | Yes (infer from dir) |
| MISSING_DESCRIPTION | critical | `description:` field absent | Yes (placeholder) |

### Content

| Code | Severity | Description |
|-------|----------|-------------|
| NAME_MISMATCH | warning | `name` ≠ directory name |
| SHORT_DESCRIPTION | warning | Description lacks detail |
| NO_TRIGGERS | info | Description missing "use when" |
| BODY_TOO_LARGE | warning | Word count > 5000 |
| DISALLOWED_FILE | warning | Contains README.md, etc. |

### Integrity

| Code | Severity | Description |
|-------|----------|-------------|
| SCRIPT_NOT_EXECUTABLE | info | Script missing +x |
| BROKEN_SYMLINK | critical | Symlink points nowhere |
| MISSING_REFERENCED_ASSET | warning | Asset referenced but missing |

## Severity Guidance

- **Critical**: Skill is broken or non-compliant; will not work
- **Warning**: Suboptimal; may cause confusion or performance issues
- **Info**: Best practice improvement opportunities

## Fix Recommendations

For each check, provide clear remediation steps in the output messages.

## Thresholds

- Word count: 5000 words trigger warning (suggests `references/`)
- Description length: < 20 chars triggers short description warning
- Health score: See algorithm in main specification
