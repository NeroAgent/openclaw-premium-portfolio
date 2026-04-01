#!/usr/bin/env python3
"""
Skill Health Auditor - validates, scores, and reports on installed skills.

Usage:
    audit.py [--all] [--level LEVEL] [--output FORMAT]

Examples:
    python audit.py                    # Run full audit
    python audit.py --level critical   # Only show critical issues
    python audit.py --output json     # Machine-readable output
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime

# Configuration
OPENCLAW_SKILLS_DIR = Path("/usr/local/lib/node_modules/openclaw/skills")
WORKSPACE_SKILLS_DIR = Path("/root/.openclaw/workspace/skills")

# Severity levels
SEVERITY_CRITICAL = "critical"
SEVERITY_WARNING = "warning"
SEVERITY_INFO = "info"

# Health status
STATUS_HEALTHY = "healthy"
STATUS_WARNING = "warning"
STATUS_ERROR = "error"


def discover_skills():
    """Find all installed skill directories."""
    skills = []

    for base_dir in [OPENCLAW_SKILLS_DIR, WORKSPACE_SKILLS_DIR]:
        if not base_dir.exists():
            continue
        for item in base_dir.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                skill_md = item / "SKILL.md"
                if skill_md.exists():
                    skills.append({
                        "name": item.name,
                        "path": item,
                        "source": "system" if base_dir == OPENCLAW_SKILLS_DIR else "workspace"
                    })

    return skills


def validate_skill_md(skill):
    """Validate a skill's SKILL.md file. Returns list of issues."""
    issues = []
    skill_md = skill["path"] / "SKILL.md"

    try:
        content = skill_md.read_text()
    except Exception as e:
        issues.append({
            "severity": SEVERITY_CRITICAL,
            "code": "FILE_UNREADABLE",
            "message": f"Could not read SKILL.md: {e}"
        })
        return issues

    # Check for YAML frontmatter
    if not content.startswith("---"):
        issues.append({
            "severity": SEVERITY_CRITICAL,
            "code": "MISSING_FRONTMATTER",
            "message": "SKILL.md missing YAML frontmatter (must start with ---)"
        })
        return issues

    # Extract frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        issues.append({
            "severity": SEVERITY_CRITICAL,
            "code": "INVALID_FRONTMATTER",
            "message": "Frontmatter not properly terminated with ---"
        })
        return issues

    frontmatter = parts[1]
    body = parts[2].strip()

    # Parse YAML (simple check, not full YAML parser)
    name_match = re.search(r"name:\s*(.+)", frontmatter)
    desc_match = re.search(r"description:\s*(.+)", frontmatter)

    if not name_match:
        issues.append({
            "severity": SEVERITY_CRITICAL,
            "code": "MISSING_NAME",
            "message": "Frontmatter missing 'name' field"
        })
    else:
        name = name_match.group(1).strip()
        if name != skill["name"]:
            issues.append({
                "severity": SEVERITY_WARNING,
                "code": "NAME_MISMATCH",
                "message": f"Skill name '{skill['name']}' does not match SKILL.md name '{name}'"
            })

    if not desc_match:
        issues.append({
            "severity": SEVERITY_CRITICAL,
            "code": "MISSING_DESCRIPTION",
            "message": "Frontmatter missing 'description' field"
        })
    else:
        description = desc_match.group(1).strip()
        if len(description) < 20:
            issues.append({
                "severity": SEVERITY_WARNING,
                "code": "SHORT_DESCRIPTION",
                "message": "Description is very short; should include specific use cases and triggers"
            })
        # Check for trigger keywords
        trigger_keywords = ["use when", "use if", "trigger", "when to use"]
        if not any(kw in description.lower() for kw in trigger_keywords):
            issues.append({
                "severity": SEVERITY_INFO,
                "code": "NO_TRIGGERS",
                "message": "Description could be improved by adding specific trigger scenarios"
            })

    # Check body size
    body_word_count = len(body.split())
    if body_word_count > 5000:
        issues.append({
            "severity": SEVERITY_WARNING,
            "code": "BODY_TOO_LARGE",
            "message": f"SKILL.md body is {body_word_count} words (>5k). Consider moving content to references/"
        })

    # Check for disallowed files
    disallowed = ["README.md", "INSTALL.md", "QUICKSTART.md", "CHANGELOG.md"]
    for filename in disallowed:
        if (skill["path"] / filename).exists():
            issues.append({
                "severity": SEVERITY_WARNING,
                "code": "DISALLOWED_FILE",
                "message": f"Found '{filename}' - skills should not include auxiliary documentation"
            })

    # Check script permissions if scripts/ exists
    scripts_dir = skill["path"] / "scripts"
    if scripts_dir.exists():
        for script in scripts_dir.iterdir():
            if script.is_file() and not script.name.endswith(".py") and not script.name.endswith(".sh"):
                continue
            # Check if executable
            import os
            if not os.access(script, os.X_OK):
                issues.append({
                    "severity": SEVERITY_INFO,
                    "code": "SCRIPT_NOT_EXECUTABLE",
                    "message": f"Script '{script.name}' is not executable (chmod +x recommended)"
                })

    return issues


def compute_health_score(issues):
    """Compute health score (0-100) and status based on issues."""
    score = 100
    has_critical = False
    has_warning = False

    for issue in issues:
        if issue["severity"] == SEVERITY_CRITICAL:
            score -= 30
            has_critical = True
        elif issue["severity"] == SEVERITY_WARNING:
            score -= 5
            has_warning = True
        else:
            score -= 1

    if has_critical:
        status = STATUS_ERROR
    elif has_warning:
        status = STATUS_WARNING
    else:
        status = STATUS_HEALTHY

    return max(0, score), status


def audit_all_skills(level_filter=None):
    """Run full audit on all skills."""
    skills = discover_skills()
    results = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_skills": len(skills),
        "skills": [],
        "summary": {
            STATUS_HEALTHY: 0,
            STATUS_WARNING: 0,
            STATUS_ERROR: 0
        }
    }

    for skill in skills:
        issues = validate_skill_md(skill)
        score, status = compute_health_score(issues)

        # Filter by level if specified
        if level_filter == SEVERITY_CRITICAL:
            issues = [i for i in issues if i["severity"] == SEVERITY_CRITICAL]
        elif level_filter == SEVERITY_WARNING:
            issues = [i for i in issues if i["severity"] in (SEVERITY_CRITICAL, SEVERITY_WARNING)]

        skill_result = {
            "name": skill["name"],
            "source": skill["source"],
            "status": status,
            "score": score,
            "issues": issues
        }
        results["skills"].append(skill_result)
        results["summary"][status] += 1

    return results


def print_human_report(results):
    """Print human-readable health report."""
    print(f"=== Skill Health Report ===")
    print(f"Generated: {results['generated_at']}")
    print(f"Total skills: {results['total_skills']}")
    print(f"Healthy: {results['summary']['healthy']}")
    print(f"Warnings: {results['summary']['warning']}")
    print(f"Errors: {results['summary']['error']}")
    print()

    # Sort by status (errors first, then warnings, then healthy)
    def sort_key(s):
        order = {"error": 0, "warning": 1, "healthy": 2}
        return order[s["status"]]
    sorted_skills = sorted(results["skills"], key=sort_key)

    for skill in sorted_skills:
        status_icon = {"healthy": "✅", "warning": "⚠️ ", "error": "❌"}[skill["status"]]
        print(f"{status_icon} {skill['name']} (score: {skill['score']})")
        for issue in skill["issues"][:2]:  # Show first 2 issues max
            print(f"   • {issue['message']}")
        if len(skill["issues"]) > 2:
            print(f"   • ...and {len(skill['issues']) - 2} more")
        print()


def main():
    parser = argparse.ArgumentParser(description="Audit skill health")
    parser.add_argument("--level", choices=["critical", "warning", "all"],
                        default="all", help="Minimum severity level to include")
    parser.add_argument("--output", choices=["text", "json"],
                        default="text", help="Output format")
    args = parser.parse_args()

    level_map = {"critical": SEVERITY_CRITICAL, "warning": SEVERITY_WARNING, "all": None}
    level_filter = level_map[args.level]

    results = audit_all_skills(level_filter)

    if args.output == "json":
        print(json.dumps(results, indent=2))
    else:
        print_human_report(results)


if __name__ == "__main__":
    main()
