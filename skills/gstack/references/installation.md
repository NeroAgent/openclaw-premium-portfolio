# Installation Guide

## Global Install (Recommended)

1. Open **Claude Code** (not OpenClaw).
2. Run these commands:

```
/plugin marketplace add garrytan/gstack
/plugin install gstack
```

3. Restart Claude Code.

The skills will appear in `~/.claude/skills/` with symlinks.

## Project-Specific Install

If you want teammates to get the skills automatically:

```bash
# In your project root:
git clone https://github.com/garrytan/gstack.git .claude/skills/gstack
cd .claude/skills/gstack && ./setup
```

This builds the browser binary and registers the skills. Add a `gstack` section to your project's `CLAUDE.md` to document the available modes.

## Verifying Install

```
/help
```

You should see the gstack modes listed: `/plan-ceo-review`, `/plan-eng-review`, etc.

## Dependencies

- **Bun** v1.0+ — required for `/browse` (compiles native browser binary)
- **Git** — for cloning and version checks

If Bun is missing, `./setup` will attempt to install it automatically.

## Troubleshooting

**Skill not showing up?**
- Run `cd ~/.claude/skills/gstack && ./setup`
- Check that symlinks exist in `~/.claude/skills/` pointing into gstack dir
- Restart Claude Code

**`/browse` fails with "binary not found"?**
- The binary is built on first use. Run `/browse` and it will compile (~1 minute).
- Ensure Bun is in PATH.

**Want to uninstall?**
```bash
for s in browse plan-ceo-review plan-eng-review review ship retro qa setup-browser-cookies; do
  rm -f ~/.claude/skills/$s
done
rm -rf ~/.claude/skills/gstack
# Remove gstack section from CLAUDE.md
```

---

For more help, see the upstream repo: https://github.com/garrytan/gstack