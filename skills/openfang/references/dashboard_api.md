# Dashboard API

OpenFang's web dashboard (http://localhost:4200) also exposes a local HTTP API for programmatic control.

## Endpoints

### GET /api/health

Health check.

```json
{"status": "ok", "version": "0.19.0"}
```

### GET /api/hands

List all Hands with status.

```json
{
  "hands": [
    {
      "name": "research-competitors",
      "enabled": true,
      "last_run": "2026-04-01T08:00:00Z",
      "next_run": "2026-04-02T08:00:00Z",
      "status": "success"
    }
  ]
}
```

### POST /api/hands/:name/trigger

Trigger a Hand immediately.

```bash
curl -X POST http://localhost:4200/api/hands/research-competitors/trigger
```

Response:

```json
{
  "triggered": true,
  "run_id": "run_12345"
}
```

### GET /api/runs/:id

Get details of a specific execution.

```json
{
  "id": "run_12345",
  "hand": "research-competitors",
  "started_at": "...",
  "finished_at": "...",
  "status": "success",
  "logs": "...",
  "output": "Report generated..."
}
```

### GET /api/logs/:hand

Stream logs for a Hand (SSE or plain text).

```bash
curl http://localhost:4200/api/logs/research-competitors?lines=100
```

---

**Note:** This API is localhost-only by default. Do not expose to the internet without authentication.

For more endpoints, see the OpenFang API spec: https://openfang.sh/docs/api