---
name: qwen-code
description: "An open-source AI coding agent for the terminal, optimized for Qwen3-Coder. Provides code understanding, automated refactoring, test generation, and agentic workflows. Integrates with OpenAI, Anthropic, and Qwen OAuth. Install via npm i -g @qwen-code/qwen-code."
---

# Qwen Code

## Overview

`qwen-code` (package: `@qwen-code/qwen-code`) is a terminal-based AI coding agent developed by Alibaba/Qwen. It helps you:

- Understand large codebases
- Automate repetitive coding tasks
- Refactor, document, and generate tests
- Execute shell commands with AI supervision
- Run multi-agent workflows with sub-agents

**Key features:**

- Multi-protocol auth: Qwen OAuth (free tier), OpenAI, Anthropic, Gemini, ModelStudio
- ~40 built-in tools (Read, Write, Edit, Bash, Grep, LSP, MCP)
- Slash commands (`/commit`, `/review-pr`, etc.)
- Persistent memory across sessions
- IDE integrations (VS Code, JetBrains, Zed)
- Undercover Mode for stealth OSS contributions

This skill provides a thin OpenClaw wrapper around the `qwen` CLI.

## Prerequisites

- Node.js 20+ (already installed: v20.19.4)
- `qwen` binary (install: `npm i -g @qwen-code/qwen-code`)

One-time auth required before use: `qwen /auth`

## Quick Start

```bash
# Install globally (already done in this session)
npm install -g @qwen-code/qwen-code

# Authenticate (once)
qwen /auth
# Choose Qwen OAuth (recommended) or API-KEY

# Use via OpenClaw tool
tool("qwen-code", "ask", "Explain the architecture of this project")

# Or run interactive session
tool("qwen-code", "interactive", "--help")
```

## Capabilities

### 1. Ask (non-interactive)

Pass a prompt and get a response:

```python
tool("qwen-code", "ask", prompt="Generate unit tests for src/main.py")
```

Options:
- `--json` → return structured output (tool calls, steps)
- `--stream` → stream output in real-time (future)

### 2. Interactive

Launch the full interactive REPL:

```python
tool("qwen-code", "interactive")
```

Within interactive mode, use slash commands:
- `/help` - Show commands
- `/auth` - Switch auth method
- `/commit` - Generate commit message
- `/review-pr` - Review a PR
- `/memory` - View persistent memory
- `/settings` - Toggle configuration

### 3. Authentication Management

```python
tool("qwen-code", "auth")  # Re-run auth flow
```

### 4. Model Discovery

List configured models and providers:

```python
tool("qwen-code", "list-models")
```

Outputs JSON with providers and model names.

## Configuration

Qwen Code stores config in `~/.qwen/settings.json`. Example:

```json
{
  "modelProviders": {
    "openai": [
      {
        "provider": "openai",
        "apiKey": "sk-...",
        "models": ["gpt-4o", "gpt-4-turbo"]
      }
    ],
    "qwen": [
      {
        "provider": "qwen",
        "auth": {"type": "oauth"},
        "models": ["qwen3-5-plus", "qwen3-coder-32b"]
      }
    ]
  },
  "defaultProvider": "qwen",
  "defaultModel": "qwen3-5-plus",
  "telemetry": false,
  "sandbox": {"enabled": true}
}
```

## Use Cases

- **Codebase onboarding**: "What does this project do and how is it structured?"
- **Refactoring**: "Extract this logic into a separate module"
- **Testing**: "Write pytest tests for this function with edge cases"
- **Debugging**: "Why is this function returning null? Investigate"
- **Documentation**: "Generate a README for this package"
- **Git workflows**: "Stage changes, commit with a good message, push"

## Integration with OpenClaw

This skill is designed to be part of an autonomous coding workflow:

```bash
# Use openbrowser to triage GitHub issues, then delegate to qwen-code
openbrowser run "Check latest issues in myrepo"
# Parse issues, then:
tool("qwen-code", "ask", prompt="Fix issue #42: <description>")
```

Combine with `git-status-summary` and `lean-ctx` for efficient development.

## Resources

### scripts/
- `run.py` — Main wrapper script invoked by OpenClaw tool calls

### references/
- `settings_schema.json` — Full settings schema (auto-generated)
- `tools.md` — List of built-in tools and permissions
- `slash_commands.md` — Slash command reference

## Architecture Notes

Qwen Code's internal architecture (from leaked source analysis):

- Runtime: Bun (TypeScript)
- Terminal UI: React + Ink (component-based)
- Tool system: plugin architecture with permission gates
- Query Engine: LLM orchestration, streaming, caching (~46K LOC)
- Multi-agent: sub-agents/swarms for parallel tasks
- IDE bridge: JWT-authenticated channels to extensions
- Persistent memory: file-based, cross-session
- Compaction: context management for long sessions
- Anti-distillation: fake tool definitions injected to poison training data

These patterns inform OpenClaw's own harness design.

## Performance

- Startup: ~1-2s (Bun runtime)
- Token throughput: depends on model (Qwen OAuth free: 1K req/day)
- Local models via Ollama supported (experimental)

## License

Apache 2.0 (upstream). This wrapper: MIT.
