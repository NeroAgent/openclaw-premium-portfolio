# Local HTTP API (Optional)

If you enable "Developer Options → Enable Local API" in the app, it starts an HTTP server on port 8080 (configurable). This allows programmatic control without ADB.

## Endpoints

### POST /chat

Send a text generation request.

```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3-4b","prompt":"Hello"}'
```

Response:
```json
{
  "response": "Hello! How can I help?",
  "tokens_per_second": 12.5,
  "total_tokens": 15
}
```

### POST /vision

Send an image + prompt.

```bash
curl -X POST http://localhost:8080/vision \
  -F "image=@photo.jpg" \
  -F "prompt=What is in this image?"
```

### POST /generate-image

Generate an image from text.

```bash
curl -X POST http://localhost:8080/generate-image \
  -d '{"prompt":"a cat on a sofa","steps":20}'
```

### GET /status

Get app status, loaded model, etc.

## Using from OpenClaw

Instead of ADB, if the local API is enabled, you can call these endpoints directly:

```python
import requests
resp = requests.post("http://localhost:8080/chat", json={"model":"qwen3-4b","prompt":"..."})
```

This is faster and more reliable than ADB UI automation.

## Security

The local API binds to 127.0.0.1 only by default. If you need remote access, set up SSH tunnel or consider security implications.

---

**Note:** This API is provided by Off Grid Mobile, not part of OpenClaw. For API changes, consult the app's documentation.