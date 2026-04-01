# Troubleshooting Guide

## Common Issues

### "SKILL.md missing required frontmatter"
**Cause:** The file doesn't start with `---` or the YAML block is missing.
**Fix:** Add proper frontmatter:
```yaml
---
name: my-skill
description: What the skill does and when to use it.
---
```

### "Description is very short"
**Cause:** Description is < 20 characters or doesn't explain triggers.
**Fix:** Expand description to include specific scenarios:
> "Use when you need to merge PDF files, extract text from scanned documents, or fill form fields."

### "SKILL.md body exceeds 5k words"
**Cause:** Too much content in one file; violates progressive disclosure.
**Fix:** Move detailed guides, API references, or examples to `references/` directory and link to them.

### "Script is not executable"
**Cause:** Script file lacks +x permission.
**Fix:** Run `chmod +x scripts/your_script.py`.

### "Found README.md"
**Cause:** Auxiliary documentation file violates skill spec.
**Fix:** Move that content into SKILL.md body or `references/`, then delete README.md.

### "Skill name mismatch"
**Cause:** Directory name differs from `name` field in SKILL.md.
**Fix:** Rename either the directory or update `name:` to match (use lowercase hyphen-case).

## Self-Help

Run `skill-health check skill-name` to get issues specific to that skill.

## When All Else Fails

1. Re-run with `--output json` and inspect the `code` field
2. Consult the AgentSkills specification in `references/specification.md`
3. Use `skill-creator` to reinitialize and migrate content
