# Shell Command Patterns

lean-ctx recognizes 90+ commands across 34 categories and applies custom compression filters. This document lists the supported commands and the typical savings achieved.

## Git (19 commands)

| Command | Typical Savings | Notes |
|---------|----------------|-------|
| `git status` | -70% | Removes branch info noise, groups changes |
| `git log` | -80% | Condenses commit lines, drops author/date if not needed |
| `git diff` | -85% | Strips whitespace, groups hunks by file |
| `git show` | -80% | Similar to diff |
| `git branch` | -60% | Lists only branch names |
| `git checkout` / `switch` | -50% | Minimal output |
| `git merge` | -70% | Conflict summaries only |
| `git stash` | -60% | Lists stashes compactly |
| `git tag` | -60% | Simple list |
| `git remote -v` | -50% | Table compacted |
| `git fetch` | -90% | Progress bar stripped, only errors shown |
| `git pull` | -75% | Combines fetch + merge output |
| `git push` | -70% | Progress stripped |
| `git clone` | -80% | Progress removed |
| `git reset` | -50% | Minimal |
| `git blame` | -85% | Removes author/date if not needed |
| `git cherry-pick` | -70% | Conflict summaries |
| `git reflog` | -80% | Condensed |
| `git add --interactive` | -60% | Short prompts |

## npm / pnpm / yarn (6)

| Command | Savings |
|---------|---------|
| `npm install` | -85% |
| `npm test` | -80% |
| `npm run` | -70% |
| `npm list` | -75% |
| `npm outdated` | -70% |
| `npm audit` | -65% |

## Cargo (3)

| Command | Savings |
|---------|---------|
| `cargo build` | -85% |
| `cargo test` | -90% |
| `cargo clippy` | -70% |

## Docker (10)

| Command | Savings |
|---------|---------|
| `docker build` | -85% |
| `docker ps` | -60% |
| `docker images` | -60% |
| `docker logs` | -80% |
| `docker compose ps` | -65% |
| `docker compose up` | -80% |
| `docker compose down` | -50% |
| `docker exec` | -70% |
| `docker network ls` | -60% |
| `docker volume ls` | -60% |

## GitHub CLI (gh) (9)

| Command | Savings |
|---------|---------|
| `gh pr list` | -75% |
| `gh pr view` | -65% |
| `gh pr create` | -50% |
| `gh pr merge` | -60% |
| `gh issue list` | -75% |
| `gh issue view` | -65% |
| `gh issue create` | -50% |
| `gh run list` | -70% |
| `gh run view` | -60% |

## Others

- **Kubernetes (kubectl)** — 8 commands: -60% to -85%
- **Python (pip / ruff)** — -60% to -80%
- **Ruby (bundle / rake / rspec)** — -60% to -85%
- **Build tools (tsc, next build, vite build)** — -60% to -80%
- **Test runners (jest, vitest, pytest, go test, etc.)** — -90%
- **Terraform** — -60% to -85%
- **Make** — -60% to -80%
- **AWS CLI** — -60% to -80%
- ** Databases (psql, mysql)** — -50% to -80%
- **Prisma** — -70% to -85%
- **Helm** — -60% to -80%
- **Utilities (ls, find, grep, curl, wget)** — -50% to -89%

## Unrecognized Commands

If a command doesn't match a known pattern, lean-ctx applies generic compression:
- Remove ANSI escape codes
- Collapse multiple empty lines
- Strip trailing whitespace
- Truncate very long output (last 1000 lines by default)
Result: typically -30% to -50% depending on output type.

## Custom Patterns

You can add custom patterns via `~/.lean-ctx/config.toml`:

```toml
[patterns.mycmd]
regex = "mycmd --verbose(.+)"
replace = "mycmd $1"
strip = ["^\\s+[0-9]+: "]
```

See `references/patterns.md` for pattern syntax.

---

These patterns are part of lean-ctx's Shell Hook. When you run `lean-ctx init --global`, your shell aliases (`git='lean-ctx -c git'`, etc.) automatically invoke compression for all these commands.