# gh-aw Quick Reference

## Commands

| Skill script | gh-aw command | Purpose |
|--------------|---------------|---------|
| `review.py` | `gh-aw review <pr>` | AI review of pull request |
| `pr_description.py` | `gh-aw pr-description` | Generate PR description from diff |
| `issue_description.py` | `gh-aw issue-description` | Expand issue title into full description |
| `triage.py` | `gh-aw triage` | Auto-triage issues (labels, duplicates) |
| `changelog.py` | `gh-aw changelog` | Generate release notes from PRs |

## Environment Variables

- `GHAW_BIN` — override path to `gh-aw` binary
- `GH_AW_LLM` — `openai` (default), `anthropic`, or `ollama`
- `GH_AW_LLM_MODEL` — e.g., `gpt-4o`, `claude-sonnet-4`, `llama3.2:3b`
- `GH_AW_LLM_BASE_URL` — for Ollama: `http://localhost:11434`
- `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` — API keys

## Example Workflows

### Auto-review every new PR (via OpenFang Hand)

```toml
# HAND.toml
name = "gh-pr-reviewer"
schedule = "*/5 * * * *"  # every 5 minutes
system_prompt = "You are a senior code reviewer."
tools = ["gh-aw-review"]
[config]
review_level = "quick"
min_labels = ["needs-review"]
```

### Daily triage

```bash
tool("gh-aw", "triage", repo="owner/repo", limit=100, apply=False)
# Review suggestions, then apply with --apply if satisfied
```

### Changelog before release

```bash
tool("gh-aw", "changelog", repo="owner/repo", since="v1.2.0", to="v1.3.0")
```

---

For full documentation: https://openfang.sh/docs/gh-aw