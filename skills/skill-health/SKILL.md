---
name: skill-health
description: "Audit, validate, and monitor the health of installed skills. Use for: verifying skill integrity after installs, checking for outdated or broken skills, diagnosing issues, generating inventory, and ensuring specification compliance. Provides health scoring, validation reports, and actionable recommendations."
---

# Skill Health

## Overview

`skill-health` audits the entire skill ecosystem to ensure reliability, catch issues early, and maintain a healthy, performant skill base. It validates structure, checks for common problems, and provides a clear health dashboard.

## When to Use This Skill

- After installing new skills (verify they're properly structured)
- Periodically (proactive health monitoring)
- When a skill misbehaves or fails to trigger
- Before upgrading OpenClaw (check compatibility)
- When managing many skills (inventory and cleanup)

## Health Checks Performed

### 1. Structure Validation
- SKILL.md exists and is parseable
- YAML frontmatter contains required fields (`name`, `description`)
- Description is non-empty and informative
- Skill name matches directory name
- No disallowed files (README.md, INSTALL.md, etc.)

### 2. Content Quality
- Description triggers appropriately (includes specific use cases)
- SKILL.md body outlines clear workflows
- Resources are organized correctly (scripts/, references/, assets/)
- No excessive context bloat warnings (>5k words in SKILL.md body)

### 3. Integrity & Compatibility
- Scripts are executable (scripts/ with proper shebang + chmod)
- No broken symlinks
- Asset files referenced are present
- Skill name uses lowercase hyphen-case (no spaces, capitals)

### 4. Dependency & Ecosystem
- Detects skill-to-skill dependencies (mentioned in description or content)
- Identifies potential conflicts (duplicate capabilities, name overlaps)
- Checks for deprecated skills (marked with "deprecated" in description)

## Quick Start

```bash
# Run full health audit
skill-health audit --all

# Check only critical issues
skill-health audit --level critical

# Generate JSON report for external tools
skill-health audit --output json

# Check a specific skill
skill-health check skill-name

# List all installed skills with health scores
skill-health list
```

## Sample Output

```
=== Skill Health Report ===
Total skills: 53
Healthy: 48 (90%)
Warnings: 4 (7%)
Errors: 1 (2%)

✅ github (v1.2.0) - Healthy
✅ gh-issues (v1.0.3) - Healthy
⚠️  pdf-tools - Warning: description lacks specific triggers
⚠️  image-edit - Warning: SKILL.md body exceeds 6k words
❌ old-skill - Error: SKILL.md missing required frontmatter
```

## Resources

### scripts/
Holds the executable audit and validation logic.

**Key scripts:**
- `audit.py` - Main auditor, runs all checks and aggregates results
- `validator.py` - Low-level validation of SKILL.md structure
- `inventory.py` - Builds skill inventory with metadata
- `scorer.py` - Computes health scores based on check results

### references/
Detailed documentation on the AgentSkills specification, validation rules, and health scoring algorithm.

**Key references:**
- `specification.md` - The AgentSkills spec (frontmatter rules, directory structure)
- `health_criteria.md` - Complete checklist of health checks with severity levels
- `troubleshooting.md` - Common issues and fixes

## Advanced Usage

### Continuous Integration

Integrate `skill-health` into CI pipelines to catch skill regressions:

```yaml
# .github/workflows/skill-health.yml
- name: Audit skills
  run: skill-health audit --all --output json > health-report.json
- name: Fail on errors
  run: |
    jq -e '.errors | length == 0' health-report.json
```

### Pre-commit Hook

Run light validation before committing skill changes:

```bash
skill-health check changed-skill --level critical
```

### Monitoring & Alerts

Set up periodic health checks (cron or heartbeat):

```
0 */6 * * * skill-health audit --all --output json | jq .
```

Threshold alerts: if error count > 0 or warning count > 10, notify.

---

**Note:** This skill is self-referential — it can audit itself. Run `skill-health check skill-health` to verify its own health.
