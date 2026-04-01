# API Reference

## Base URL

`http://localhost:37777` (configurable via `PORT`)

## Endpoints

### POST /api/observation

Store an observation.

**Body:**
```json
{
  "type": "finding" | "decision" | "task" | "note",
  "title": "string",
  "content": "string",
  "tags": ["array"],
  "private": false,
  "session": "session-id"
}
```

**Response:**
```json
{ "id": 123, "status": "stored" }
```

### GET /api/observances/:id

Fetch a single observation.

### GET /api/observations/recent?limit=N&type=...

List recent observations.

### GET /api/search?q=...&limit=N&type=...&after=...&before=...&include_private=bool

Full-text search. Returns index entries (id, type, title, timestamp, snippet, score).

### GET /api/timeline?around_id=...|at=...&window=30m

Get chronological window around a point.

### GET /api/summaries?session=...

Get session summaries.

### GET /api/health

Health check.

---

For more details, see the upstream API spec: https://github.com/thedotmack/claude-mem/blob/main/docs/API.md