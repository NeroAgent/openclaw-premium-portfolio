# HTTP API Reference

Ollama exposes a REST API on `http://localhost:11434`.

## Generate

`POST /api/generate`

Body:
```json
{
  "model": "llama3.2:3b",
  "prompt": "Why is the sky blue?",
  "system": "You are a helpful assistant.",
  "format": "json",
  "stream": false
}
```

Response:
```json
{
  "model": "llama3.2:3b",
  "created_at": "2024-01-01T00:00:00Z",
  "response": "Because of Rayleigh scattering...",
  "done": true
}
```

## Chat

`POST /api/chat`

Body:
```json
{
  "model": "llama3.2:3b",
  "messages": [
    {"role": "system", "content": "You are helpful."},
    {"role": "user", "content": "Hello!"}
  ],
  "stream": false
}
```

## Embed

`POST /api/embed`

Body:
```json
{
  "model": "nomic-embed-text",
  "prompt": "The sky is blue because..."
}
```

Response:
```json
{"embedding": [0.0123, -0.0456, ...]}
```

## Models

`GET /api/tags` — List models (same as `ollama list`)

## Show

`POST /api/show` — Show model details

---

All endpoints also support `stream: true` for streaming responses (SSE). The skill scripts use the CLI for simplicity; for tighter integration, call the API directly.

Full API docs: https://github.com/ollama/ollama/blob/main/docs/api.md