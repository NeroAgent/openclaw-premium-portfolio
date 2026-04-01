# Output Formats Reference

## Text Format (default)

```
=== Git Summary (N repos scanned) ===

✅ /path/to/repo1
   branch: main ↑1
   last: abc123 (2h ago) "Fix bug in parser"
   status: 2 modified, 1 untracked

⚠️  /path/to/repo2
   branch: feature/new-ui ↑2 ↓1
   last: def456 (1d ago) "Add responsive layout"
   stashes: 1
```

**Legend:**
- ✅ clean repository
- ⚠️ has uncommitted changes
- ❓ detached HEAD
- ↑ ahead count
- ↓ behind count

**Columns shown:**
- Path (relative or absolute)
- Branch + ahead/behind
- Last commit (hash, time, message)
- Status counts (modified, untracked, staged)
- Stash count
- PR info (if enabled)

### Verbose Mode (`--verbose`)

Adds file listings:

```
⚠️  /path/to/repo
   branch: main
   last: abc123 (2h ago) "WIP"
   status: 3 modified, 2 untracked
   Modified files:
     - src/app.py
     - tests/test_api.py
     - README.md
   Untracked files:
     - .env.local
     - docs/draft.txt
```

## JSON Format (`--output json`)

```json
{
  "generated_at": "2026-04-01T11:10:00Z",
  "repos": [
    {
      "path": "/home/user/project",
      "branch": "main",
      "ahead_count": 1,
      "behind_count": 0,
      "last_commit": {
        "hash": "abc123",
        "author": "Nero",
        "date": "2 hours ago",
        "message": "Fix bug"
      },
      "dirty": false,
      "staged_count": 0,
      "modified_count": 0,
      "untracked_count": 0,
      "stash_count": 0,
      "open_prs": 0,
      "pr_list": []
    }
  ]
}
```

**Fields:**

| Field | Type | Meaning |
|-------|------|---------|
| `path` | string | Absolute path to repository |
| `branch` | string | Current branch or `DETACHED:<hash>` |
| `ahead_count` | int | Commits ahead of upstream |
| `behind_count` | int | Commits behind upstream |
| `last_commit` | object or null | Hash, author, date, message |
| `dirty` | bool | Working tree has changes |
| `staged_count` | int | Number of staged files |
| `modified_count` | int | Modified but unstaged files |
| `untracked_count` | int | Untracked files |
| `stash_count` | int | Number of stashes |
| `open_prs` | int | Number of open PRs (if GitHub integration enabled) |
| `pr_list` | array | Details of recent PRs (number, title, user) |
| `error` | string | If scan failed, error message |

## Filtering Output

The `--filter` flag limits visible repos:

```bash
# Only dirty repos
git-status-summary ~/projects --filter dirty

# Only repos behind upstream
git-status-summary ~/projects --filter behind

# Repos with open PRs
git-status-summary ~/projects --filter pr-open
```

Combine with commas:

```bash
git-status-summary ~/projects --filter dirty,behind
```

(Shows repos that are dirty AND/OR behind — union of filters.)

## Machine Integration

Use JSON output for scripts:

```bash
result=$(git-status-summary ~/projects --output json)
dirty_count=$(echo "$result" | jq '[.repos[] | select(.dirty)] | length')
```

Check if any repo needs attention:

```bash
if git-status-summary ~/projects --filter dirty,behind | grep -q .; then
  echo "Some repos need attention"
else
  echo "All clean"
fi
```
