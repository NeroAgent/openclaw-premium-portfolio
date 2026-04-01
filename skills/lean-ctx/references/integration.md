# OpenClaw Integration Guide

This guide explains how to integrate lean-ctx with OpenClaw for maximum token efficiency.

## Installation Steps

1. **Build or install lean-ctx binary**
   ```bash
   cargo install lean-ctx
   # or build from source in external/lean-ctx
   ```

2. **Ensure binary is in PATH**
   ```bash
   export PATH="$HOME/.cargo/bin:$PATH"
   # Add to ~/.zshrc or ~/.bashrc
   ```

3. **Install OpenClaw skill**
   The `lean-ctx` skill should be installed in `~/.openclaw/skills/`.

## Usage Patterns

### Pattern 1: Explicit Compression

Use the skill's commands directly:

```bash
# In OpenClaw, execute a shell command with compression
exec("lean-ctx run 'git status'")
```

This calls the `run.py` script, which invokes `lean-ctx -c "git status"`.

### Pattern 2: Shell Hook (Transparent)

If you have run `lean-ctx init --global` and your shell profile is sourced, then OpenClaw's `exec` calls that use common commands (git, npm, cargo, etc.) will be automatically compressed because the aliases are active.

However, OpenClaw typically runs commands via `/bin/sh -c "command"` which doesn't load interactive shell configs. To make the hook work:

- Ensure your shell profile is sourced for non-interactive shells, or
- Use the explicit `lean-ctx run` pattern, or
- Configure OpenClaw to use a login shell: `exec(..., shell="bash -lc 'git status'")`.

### Pattern 3: File Reads

Instead of `read_file(path)`, use:

```python
result = tool("lean-ctx", "read", file=path, mode="signatures")
```

This reads the file with compression, dramatically reducing token usage for large files.

### Pattern 4: Analytics

Periodically check token savings:

```bash
tool("lean-ctx", "gain", json=True)  # get stats as JSON
```

You can use this to adapt behavior: if savings are high, lean-ctx is working; if low, maybe the commands aren't recognized.

## Configuration

Environment variables:

- `LEAN_CTX_BIN` — override path to binary
- `LEAN_CTX_CACHE_TTL` — cache expiration in seconds (default 300)
- `LEAN_CTX_CACHE_SIZE` — max cache entries (default 1000)

These can be set in the OpenClaw environment before running tools.

## MCP Server (Optional)

If you also use an MCP-capable editor (Cursor, Copilot, etc.), you can start the MCP server:

```bash
# Start in background
tool("lean-ctx", "mcp-server", daemon=True, port=3333)
```

The server will stay running and provide tools to the editor. OpenClaw does not use the MCP server directly; it uses the CLI tools.

## Performance Tips

- Cache is per-session. After 5 minutes of inactivity, cache clears. For long-running sessions, cache stays warm.
- Use `diff` mode for iterative editing; it sends only line changes.
- For large repositories, consider excluding node_modules, target, .git from scans (lean-ctx ignores by default).

## Troubleshooting

**No compression happening:**
- Verify binary: `which lean-ctx`
- Check version: `lean-ctx --version`
- Run manually: `lean-ctx -c "git status"` to see if compression occurs (it prints stats to stderr).

**Cache misses:**
- Ensure you're using the same `~/.lean-ctx` directory across sessions (default). If OpenClaw runs under a different user or HOME, cache won't persist.

**High token usage despite lean-ctx:**
- Some commands may not have patterns. Use `lean-ctx discover` to analyze shell history and suggest new patterns.
- Encourage use of `read` with `--mode` instead of raw `file` tool.

## Advanced: Custom Tool Definitions

If you want to expose lean-ctx capabilities as native OpenClaw tools, you can add entries to your AGENTS.md or create a skill that directly calls the binary. The `lean-ctx` skill already does this via scripts.

---

For lean-ctx documentation, see https://leanctx.com and the upstream repository.