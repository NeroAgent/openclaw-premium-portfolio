# Filtering & Query Syntax

The Agentmail search endpoint supports basic filters:

## Filter Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `q` | string | Search query (keywords, phrases) |
| `from` | string | Sender email address |
| `since` | string | Date filter: ISO (`2026-04-01`) or relative (`1d`, `2w`, `1m`) |
| `unread` | bool | `"true"` to show only unread |
| `limit` | int | Max results (default 20, max 100) |
| `offset` | int | Pagination offset |

## Examples

```bash
# Emails from Sol in last week
agentmail inbox --from sol@example.com --since 1w

# Search for "deployment" in subject/body
agentmail search "deployment" --limit 20

# Unread only
agentmail inbox --unread-only
```

## Combining Filters

Filters are ANDed together:

```
/from=sol@example.com&since=2026-04-01&unread=true
```

Means: unread emails from Sol since April 1st.

## Date Syntax

- ISO 8601: `2026-04-01T13:00:00Z`
- Relative: `1d` (1 day ago), `2w` (2 weeks), `1m` (1 month), `3M` (3 months)
- Mixed: You can also use `2026-04-01` (interpreted as start of that day)

---

For advanced filters (labels, thread ID), consult the full Agentmail API docs.