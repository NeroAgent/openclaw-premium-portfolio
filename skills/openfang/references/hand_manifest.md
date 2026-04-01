# Hand Manifest (HAND.toml)

Every Hand is defined by a `HAND.toml` file in `~/.openfang/hands/`.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique identifier (lowercase, hyphens) |
| `schedule` | string | Cron expression (e.g., `0 9 * * *` daily at 9am) |
| `system_prompt` | string | LLM system prompt describing the Hand's mission |
| `tools` | array of strings | MCP tools the Hand can use (e.g., `web_search`, `email_send`) |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `description` | string | `""` | Human-readable description |
| `timeout_seconds` | int | 300 | Max execution time |
| `max_iterations` | int | 50 | Max LLM calls |
| `approval_required` | bool | false | If true, requires manual approval before each run |
| `retention_days` | int | 7 | How long to keep logs |
| `environment` | map | `{}` | Environment variables for the Hand |
| `config` | map | `{}` | Tool-specific configuration (e.g., RSS feed URL) |

## Example

```toml
name = "research-competitors"
schedule = "0 8 * * *"   # daily 8am
description = "Daily competitor intelligence report"
system_prompt = """
You are a competitive intelligence analyst. Each day:
1. Search news for competitor names: AcmeCorp, XYZInc
2. Summarize key developments (new products, funding, layoffs)
3. Send a digest email to team@example.com
4. Update the knowledge graph with findings
"""
tools = ["web_search", "rss", "email_send", "knowledge_graph_update"]
approval_required = false
timeout_seconds = 600

[config]
email_recipient = "team@example.com"
competitor_names = ["AcmeCorp", "XYZInc"]
rss_feeds = ["https://feeds.feedburner.com/techcrunch"]
```

## Writing Your Own Hands

1. Create `~/.openfang/hands/my-hand/HAND.toml`
2. Reload: `openfang reload`
3. Enable: `openfang hands enable my-hand`
4. Check dashboard for activity

Hands can use any MCP tool available to OpenClaw. They have full file system access within allowed dirs.

---

For advanced Hand development (custom tool invocations, error handling), see the full docs: https://openfang.sh/docs/hands