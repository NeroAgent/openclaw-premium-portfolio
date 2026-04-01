# @openclaw/tool-registry

Unified tool manifest and registry system for OpenClaw agents, based on the architecture from the Claude Code leak.

## Overview

This library provides a TypeScript implementation of the tool system pattern used in modern AI coding agents. It defines:

- **ToolSpec**: A JSON Schema-based manifest for each tool (name, description, input schema, required permission)
- **PermissionMode**: Three-tier permission model (`read_only`, `workspace_write`, `danger_full_access`)
- **GlobalToolRegistry**: Combines built-in tools and plugin tools with conflict detection, alias normalization, and execution dispatch

## Motivation

The leak of Claude Code revealed a production-grade tool architecture that has been adopted by many AI agent projects. This library ports the best patterns to OpenClaw:

- Clear separation between tool specification and execution
- Permission gating for safety
- Plugin tool registration with name conflict detection
- Normalized tool name aliases (`read` → `read_file`, `grep` → `grep_search`)
- Schema-based input validation (via Zod or similar)

## Installation

```bash
npm install @openclaw/tool-registry
```

## Quick Start

```typescript
import { GlobalToolRegistry, PermissionMode, mvpToolSpecs } from '@openclaw/tool-registry';

// Create a registry with built-in tools
const registry = new GlobalToolRegistry([]);

// Add a plugin tool
registry.withPluginTools([{
  definition: {
    name: 'echo',
    description: 'Echo back a message',
    inputSchema: {
      type: 'object',
      properties: {
        message: { type: 'string' },
        times: { type: 'number' }
      },
      required: ['message']
    }
  },
  requiredPermission: () => PermissionMode.ReadOnly,
  execute: async (input) => {
    return `${input.message}`.repeat(input.times || 1);
  }
}]);

// Execute a tool
const result = await registry.execute('echo', { message: 'Hello', times: 3 });
console.log(result); // { success: true, output: 'HelloHelloHello' }
```

## Concepts

### ToolSpec

```typescript
interface ToolSpec {
  name: string;           // canonical name (underscores)
  description: string;
  inputSchema: JsonSchema; // JSON Schema draft 4/6/7
  requiredPermission: PermissionMode;
}
```

### PermissionMode

| Mode | Access |
|------|--------|
| `read_only` | Can read files, no writes or command execution |
| `workspace_write` | Can read/write files, but no arbitrary commands |
| `danger_full_access` | Can execute any command, delete files, etc. |

### GlobalToolRegistry

- `definitions(allowedTools?)` → list of `ToolSpec` (filtered if provided)
- `execute(name, input)` → `ToolResult`
- `normalizeAllowedTools(tokens)` → `Set<string>` of canonical names (with alias support)

### MVP Tools

The library includes a set of built-in tools mirroring claw-code's MVP:

- `bash` — Execute shell command (`DangerFullAccess`)
- `read_file` — Read file (`ReadOnly`)
- `write_file` — Write file (`WorkspaceWrite`)
- `edit_file` — Replace text (`WorkspaceWrite`)
- `glob_search` — Find files by pattern (`ReadOnly`)
- `grep_search` — Search file contents (`ReadOnly`)

## Integration Guide

### Step 1: Update Skill Manifest

Skills that expose tools should declare them in `.skill` file:

```json
{
  "name": "file-reader",
  "tools": [
    {
      "name": "read_file",
      "description": "Read a text file",
      "input_schema": { "type": "object", "properties": { "path": { "type": "string" } }, "required": ["path"] },
      "permission": "read_only"
    }
  ]
}
```

### Step 2: Implement `tool-call` Entrypoint

Each skill's `scripts/run.py` should handle:

```bash
python run.py tool-call <tool_name> <json_input>
```

It should validate input, perform the operation, and print JSON result to stdout.

### Step 3: Agent Uses Registry

OpenClaw agent:

```typescript
import { GlobalToolRegistry } from '@openclaw/tool-registry';

// Discover plugin tools from skill_registry.json
const plugins = await discoverPluginTools(); // see agent.ts demo
const registry = new GlobalToolRegistry([]).withPluginTools(plugins).unwrap();

// Decide tool (via LLM or hardcoded)
const decision = { tool: 'read_file', input: { path: 'README.md' } };

// Check permission (prompt user if needed)
const spec = registry.definitions().find(d => d.name === decision.tool);
if (!spec) throw new Error('Unknown tool');
if (!await userApproves(spec.requiredPermission)) throw new Error('Denied');

// Execute
const result = await registry.execute(decision.tool, decision.input);
```

### Step 4: Add Input Validation

For stronger safety, wrap `execute` with Zod validation based on `inputSchema`.

## Demo

- `agent.ts` — Discovers tools from skill registry, runs a demo call
- `file-reader` skill — Example skill using the manifest pattern
- `claw-code` skill — Demonstrates how to wrap an existing CLI with `list_tools` and `run_tool`

## Development

```bash
npm install
npm run build   # tsc
npm test        # vitest
```

## Status

Early prototype. APIs may change.

## License

MIT
