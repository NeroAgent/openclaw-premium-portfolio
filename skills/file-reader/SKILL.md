---
name: file-reader
description: "Read file contents with optional line limiting. Demonstrates ToolRegistry manifest pattern."
tools:
  - name: read_file
    description: "Read a text file from the workspace"
    input_schema:
      type: object
      properties:
        path:
          type: string
        offset:
          type: integer
          minimum: 0
        limit:
          type: integer
          minimum: 1
      required: [path]
    permission: read_only
---

# File Reader Skill

This is a simple skill that provides file reading capability following the ToolRegistry manifest pattern.

## Implementation

The skill exposes a `read_file` tool. Under the hood, it uses OpenClaw's `read` tool but presents a clean manifest.

When invoked via the registry-based agent, the tool's input is validated against the JSON schema and then executed with the specified permission level.

## Example

```json
{
  "path": "/root/.openclaw/workspace/README.md",
  "limit": 10
}
```

## Status

Ready for registry integration. Add this skill's directory to the pluginTools list in the agent.
