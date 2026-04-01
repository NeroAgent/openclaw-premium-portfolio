---
name: demo-tool
description: "Demo skill showing how to use the new ToolRegistry pattern. Exposes a simple 'echo' tool that returns its input."
---

# Demo Tool

This demonstrates Phase 2: Tool Spec manifest pattern.

## Tool: echo

Simple pass-through tool that echoes back input.

**Input schema:**
```json
{
  "type": "object",
  "properties": {
    "message": { "type": "string" },
    "times": { "type": "integer", "minimum": 1 }
  },
  "required": ["message"]
}
```

**Example call:**
```json
{ "message": "Hello", "times": 3 }
```

**Result:**
```
Hello
Hello
Hello
```

## Implementation Notes

This skill uses the `@openclaw/tool-registry` library to declare its tool spec and registers itself with the global registry at startup.

## Status

Library created at `/root/.openclaw/workspace/lib/tool-registry`. Demo skill scaffold ready for implementation.
