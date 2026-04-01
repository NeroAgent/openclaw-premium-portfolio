# Agentmail API Reference

## Base

`https://api.agentmail.io/v1`

Authentication: `Authorization: Bearer <AGENTMAIL_API_TOKEN>`

## Endpoints

### GET /messages

List recent messages.

**Query params:**
- `limit` (int, default 20)
- `unread` (bool, `"true"` to filter unread only)
- `since` (date string: ISO 8601 or relative like `1d`, `1w`)
- `from` (sender email)

**Response:**
```json
{
  "messages": [
    {
      "id": "msg_123",
      "sender_email": "sol@example.com",
      "sender_name": "Sol",
      "subject": "Hello",
      "date": "2026-04-01T13:00:00Z",
      "snippet": "Hey, can you...",
      "is_unread": true
    }
  ]
}
```

### GET /messages/:id

Get full email.

**Query params:**
- `include_attachments` (bool)

**Response:**
```json
{
  "id": "msg_123",
  "sender_email": "...",
  "to": ["..."],
  "cc": [],
  "subject": "...",
  "date": "...",
  "body": "Full plaintext body (or HTML if requested)",
  "attachments": [
    {"filename": "file.pdf", "size": 12345, "content_type": "application/pdf"}
  ]
}
```

### GET /search

Full-text search.

**Query params:** same as `/messages` plus `q` (search query).

**Response:** same as `/messages`.

### POST /messages/:id/read

Mark as read. Returns 204 No Content on success.

---

**Note:** This is a provisional API shape. Confirm with actual Agentmail.io docs. Adjust endpoints in skill scripts if different.