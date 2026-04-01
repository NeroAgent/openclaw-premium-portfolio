# Performance Tips

## Scanning Large Numbers of Repos

Scanning is I/O-heavy. For 100+ repos, consider:

### 1. Limit Depth
Avoid recursing into huge directory trees:

```bash
git-status-summary ~/projects --max-depth 3
```

### 2. Cache Results
Use the `--cache-file` option (not yet implemented, coming soon) to store results for 5-10 minutes. Prevents re-scanning on every heartbeat.

### 3. Parallel Scanning (future)
Future versions may support `--jobs N` to scan repos in parallel. For now, sequential is safe and predictable on mobile.

### 4. Exclude Known Large Repos
Create a `.gitstatusignore` file listing paths to skip:

```
node_modules
vendor
build/dist
*.large
```

## Reducing Git Command Overhead

Each repo results in multiple git invocations:
- `git branch --show-current`
- `git rev-list --left-right --count @{upstream}...HEAD`
- `git log -1`
- `git status --porcelain`
- `git stash list`
- (optional) remote queries

These are lightweight (<50ms each) on local SSDs. On slower storage (Android eMMC), budgets go up to 200ms per repo.

**Tip:** If scanning >50 repos, run during idle time (heartbeat) or with `--max-repos` to cap.

## Network Calls

GitHub PR integration requires API calls (1 per repo with GitHub remote). Rate limits:
- Unauthenticated: 60 requests/hour
- Authenticated: 5000 requests/hour

Use `--github-token` to authenticate.

## Memory Usage

Scanning stores ~1KB per repo in memory. 1000 repos = ~1MB, negligible.

## Benchmark

On a typical developer machine (SSD, 8 cores):
- 10 repos: ~2 seconds
- 50 repos: ~8 seconds
- 200 repos: ~30 seconds

On Termux (eMMC, limited CPU):
- 10 repos: ~5 seconds
- 50 repos: ~25 seconds
- 200 repos: ~90 seconds

Recommendation: Cap at 50 repos for interactive use; batch larger scans overnight.
