---
name: claw-code
description: "Claude Code clean-room Rust rewrite (instructkr/claw-code). A terminal-based AI coding agent with tool system, multi-agent orchestration, slash commands, and persistent memory. Built on Rust for safety and speed. Requires building from source via cargo."
---

# Claw Code

## Overview

`claw` (from the community clean-room rewrite of Claude Code) is a terminal AI coding agent written in Rust. It implements the same core concepts as Anthropic's Claude Code but as an independent, MIT-licensed implementation.

**Features:**

- Tool-based architecture (~40 tools)
- Multi-agent orchestration (swarms)
- Slash commands (`/commit`, `/review`, etc.)
- Persistent memory
- Provider abstraction (OpenAI, Anthropic, Qwen, Ollama)
- IDE bridge (JWTAuthenticated)
- Compaction for long sessions

This skill wraps the Rust binary built from `instructkr/claw-code`.

## Prerequisites

- Rust toolchain (rustc, cargo) — installed ✓
- Build dependencies (standard library + TLS)
- LLM provider API key or Ollama running

## Installation (Build from Source)

```bash
cd /root/.openclaw/workspace/external/claude-code/rust
cargo build --release -p claw-cli
# Binary will be at: target/release/claw
```

## Quick Start

```bash
# 1. Build binary (once)
cargo build --release -p claw-cli

# 2. Configure provider (e.g., OpenAI)
export OPENAI_API_KEY="sk-..."

# 3. Use via OpenClaw
tool("claw-code", "ask", "Explain the project structure")

# Or run interactive
tool("claw-code", "interactive")
```

## Capabilities

### 1. Ask (non-interactive)

Pass a prompt and get a response:

```python
tool("claw-code", "ask", "Explain the project structure")
```

Options:
- `--json` → return structured output (tool calls, steps)

### 2. Run Tool (direct invocation)

Call a specific built-in tool directly without LLM parsing:

```python
tool("claw-code", "run_tool", "read_file", json.dumps({"path": "README.md"}))
```

Supported tools (whitelisted for safety):
- `read_file` — Read a workspace file
- `write_file` — Write a file (requires workspace-write permission)
- `edit_file` — Replace text in a file
- `glob_search` — Find files by pattern
- `grep_search` — Search file contents
- `bash` — Execute shell command (danger-full-access)

All tools accept JSON input matching their schema. Returns JSON with tool result.

### 3. Interactive

```python
tool("claw-code", "interactive")
```

Launch interactive REPL with full slash commands.

### 4. List Tools

```python
tool("claw-code", "list_tools")
```

Returns JSON array of available tools with descriptions and input schemas.

### 5. Auth & Models

```python
tool("claw-code", "auth")  # configure provider
tool("claw-code", "models") # list configured models
```

## Configuration

Settings JSON at `~/.claw/settings.json` (format similar to qwen-code).

## Use Cases

- Autonomous coding tasks
- Codebase navigation
- Automated PR reviews
- Test generation

## Status

Binary build may be in progress. Skill will be activated after successful build.

## Resources

### scripts/
- `run.py` — Wrapper calling the built binary

### references/
- (to be added)

## Note

This is a community rewrite, not an official Anthropic product. It is MIT-licensed and safe to use.
