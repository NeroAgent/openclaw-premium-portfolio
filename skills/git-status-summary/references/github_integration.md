# GitHub Integration

## Fetching Pull Request Information

`git-status-summary` can optionally query the GitHub API to display open PRs for repositories that have a GitHub remote.

### Prerequisites

1. GitHub remote configured in the repo (`origin` or upstream points to `github.com/...`)
2. Either:
   - `gh` CLI authenticated (`gh auth login`) — token is read from `~/.config/gh/hosts.yml`
   - Or provide `--github-token` flag

### What Gets Fetched

For each repo with a GitHub remote:
- Number of open PRs
- For the first 3 PRs (if any): PR number, title, author

This information is displayed in the summary line:

```
   PR: 2 open (#45, #46)
```

### Rate Limits

- Unauthenticated: 60 requests/hour from same IP
- Personal token: 5000 requests/hour

If you hit rate limits, the PR count will be omitted silently (no error).

### Setting Up GitHub Token

Preferred: Use `gh` CLI:

```bash
gh auth login
# Follow prompts to authenticate with browser
```

`git-status-summary` will automatically read token from `~/.config/gh/hosts.yml` under `github.com:oauth_token`.

Alternative: Generate a classic personal access token (PAT) with `repo` scope, then:

```bash
git-status-summary . --github-token ghp_xxxxx
```

**Tip:** Store token in environment variable `GITHUB_TOKEN` and omit flag for convenience.

### Multiple Remotes

The skill scans remotes and picks the first that matches `github.com`. If you have both `origin` (GitHub) and `upstream` (self-hosted), PR info comes from GitHub.

### Privacy Note

PR titles and author usernames are printed to stdout. Ensure you're in a secure environment if using shared terminals.

### Troubleshooting

**No PR info appearing:**
- Check remote URL: `git remote -v` should show `github.com`
- Verify token: `gh auth status` or test token with `curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user`
- Repo may have no open PRs

**Rate limit errors:**
- Switch to authenticated token
- Reduce number of repos scanned (`--max-repos`)
- Cache results
