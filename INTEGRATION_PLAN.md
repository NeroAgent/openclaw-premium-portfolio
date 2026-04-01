# Integration Plan — Adopting ClawHub Patterns

Based on ClawHub search and inspection, here are the specific patterns to adopt into OpenClaw core.

## Tier 1 — Must Adopt (Immediate)

### 1. Compaction Survival (from `compaction-survival`)

**Problem:** Compaction loses specifics (paths, numbers, decisions).

**Solution:** Three mechanisms:

- **WAL (Write-Ahead Log)**: On every human message, scan for specifics and write to `SESSION-STATE.md` BEFORE responding.
  - Trigger patterns: corrections, proper nouns, preferences, decisions, draft changes, specific values (numbers, dates, IDs, URLs, paths)
  - File: `memory/session-state.md`

- **Working Buffer**: At 60% context utilization, start appending exchanges to `memory/working-buffer.md`.
  - This file survives compaction because it's external.
  - Use as emergency restore source.

- **Compaction Recovery**: When context missing or user says "continue", read in order:
  1. `memory/working-buffer.md`
  2. `SESSION-STATE.md`
  3. Today's + yesterday's `memory/YYYY-MM-DD.md`
  4. `memory_search` if needed
  5. Extract important context → update SESSION-STATE.md

**Implementation:**
- Add middleware to agent runtime that checks human input for WAL triggers
- Create/append to `memory/session-state.md` with structured sections
- Track token utilization (from `usage` crate port) and at 60% create working buffer
- On session startup with `<summary>`, automatically run recovery

### 2. Session Wrap-Up (from `session-wrap-up`)

**Protocol for ending sessions:**

1. Flush to daily log (`memory/YYYY-MM-DD.md`)
2. Update `MEMORY.md` with significant learnings
3. Update PARA notes (`notes/areas/open-loops.md`, etc.)
4. `git add -A && git commit -m "wrap-up: YYYY-MM-DD session summary" && git push`
5. Report summary to user

**Implementation:**
- Add `/wrap_up` slash command to agent
- Agent generates structured summary, performs steps automatically
- Use `git-status-summary` skill to detect changes and commit

### 3. Session Persistence Architecture (from `session-persistence`)

Three-layer memory system:

| Layer | Purpose | Format |
|-------|---------|--------|
| **WAL/Buffer** | Critical details & danger zone | `SESSION-STATE.md`, `working-buffer.md` |
| **Daily Logs** | Conversation summaries | `memory/YYYY-MM-DD.md` |
| **Long-term** | Curated wisdom | `MEMORY.md` |

**Implementation:**
- Ensure agent reads yesterday's + today's logs at startup (already in AGENTS.md)
- Add WAL and buffer layers on top
- Use `session-logs` pattern for searchable archives (JSONL)

## Tier 2 — Should Adopt (Short-term)

### 4. Tool Discovery & MCP Integration

**Skills:**
- `mcp-server-discovery` — catalog, search, generate configs
- `toolrouter` — single gateway to 150+ tools (could wrap as one skill)

**Implementation:**
- Add `mcp` tool to registry that lists available MCP servers
- Generate `~/.openclaw/mcp/config.json` automatically based on user needs
- Consider `toolrouter-mcp` as a fallback for rare tools

### 5. Agent Harness Diagnostics

**Skill:** `agent-harness-architect`

**8 dimensions to periodically self-assess:**

| Dimension | Check |
|-----------|-------|
| Session Bridge | Is there a structured state file? |
| Fixed startup sequence | Are the first N steps fixed and mandatory? |
| Smoke test | Do we verify environment before tasks? |
| Atomic checkpoint | Do we commit/save after each task? |
| Output self-verification | Do we validate before reporting "done"? |
| State file format | JSON not Markdown? |
| Multi-agent protocol | Clear message passing? |
| Fallback plan | What if dependency fails? |

**Implementation:**
- Add self-diagnostic command `/harness-check` that audits current setup
- Generate improvement plan (P0/P1/P2) automatically

### 6. Proactive Capabilities

**Skill:** `proactive-agent-lite`

Patterns:
- Pre-compaction flush (before context fills)
- Reverse prompting (suggest before asked)
- Self-healing (detect and fix inconsistencies)
- Alignment/mission focus

**Implementation:**
- Add proactive suggestion module that triggers on certain keywords or periodically
- Before any user message, check SESSION-STATE for open loops and suggest progress

## Tier 3 — Nice to Have (Medium-term)

### 7. Rust-Based Patterns

**Skill:** `rust` — ownership/borrowing insights apply to TypeScript design too:
- Move semantics → Immutability, spread operator
- Borrow checker → Effect systems (Zod, typed validation)
- Lifetimes → Resource management (disposables, finalizers)
- Error handling → `Result`-like `Either<Error,T>` patterns

**Implementation:**
- Use TypeScript's type system to enforce immutability where possible
- Adopt `Either` pattern for error handling in tool execution

### 8. Performance Analysis

**Skill:** `performance` — profiles code, identifies bottlenecks

**Implementation:**
- Add `profile` tool to registry that wraps Python cProfile or Node --prof
- Use in automated code optimization tasks

### 9. Git Workflows

**Skills:** `git-workflows`, `pr-commit-workflow`

Patterns:
- Interactive rebase with autosquash
- Worktrees for parallel development
- Reflog recovery
- PR body structure (human-written intent required)

**Implementation:**
- Wrap advanced git operations as tools (`git_rebase_interactive`, `git_worktree_add`, `git_reflog_recover`)
- Enforce PR workflow: always include human-written intent, use templates

## Concrete Next Steps (Ordered)

1. **Integrate ToolRegistry into OpenClaw agent**
   - Modify agent startup to load `.skill` files, build `GlobalToolRegistry`
   - Route all tool calls through registry
   - Add `tool-call` entrypoint requirement to skills (with backward compatibility shim for existing skills)

2. **Implement WAL + Working Buffer**
   - Create `memory/session-state.md` and `memory/working-buffer.md` schemas
   - Add WAL scanner: regex for dates, paths, URLs, decisions; LLM extraction fallback
   - Update agent to write WAL entries on human input
   - Add token counter; at 60% threshold switch to buffer mode

3. **Add `/wrap_up` command**
   - Implement session wrap-up script (shell/agent step)
   - Integrate with git-status-summary to detect changes
   - Format commit message and push automatically

4. **Add `/harness_check` command**
   - Implement 8-dimension audit using current agent state
   - Output P0/P1/P2 prioritized list

5. **Install and configure MCP**
   - Install `mcporter` skill
   - Use `mcp-server-discovery` to generate config for filesystem + memory + GitHub
   - Add MCP tool to registry

6. **Build external binaries** (on external machine, then copy in)
   - ollama (if not prebuilt)
   - llmfit (Rust)
   - gh-aw, picoclaw (Go)
   - openfang (Rust)
   - Document build process in TOOLS.md

7. **Publish progress to ClawHub** (optional)
   - Consider publishing `tool-registry` as a ClawHub skill for others
   - Publish `compaction-survival-patch` that adds WAL/buffer to vanilla OpenClaw

---

*End of integration plan.*
