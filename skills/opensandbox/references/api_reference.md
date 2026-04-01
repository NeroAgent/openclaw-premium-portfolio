# OpenSandbox API Quick Reference

## Server Endpoints (HTTP)

```
POST /api/v1/execute  — Execute command in sandbox
Body: { image, command, mounts[], env[], timeout }
Response: { exit_code, stdout, stderr, duration_ms }

GET  /health         — Health check
```

## SDK

Python:
```python
from opensandbox import Sandbox
sandbox = await Sandbox.create("python:3.11", ...)
async with sandbox:
    await sandbox.commands.run("ls -la")
```

See upstream: https://opensandbox.ai/docs
