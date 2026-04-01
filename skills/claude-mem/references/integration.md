# Integration Patterns

## Auto-Capture Setup

To automatically capture OpenClaw tool calls:

1. Set environment variable: `OPENCLAU_MEM_ENABLED=true`
2. Run the worker: `claude-mem start`
3. Ensure OpenClaw's tool execution goes through a wrapper that:
   - Before tool call: store intent
   - After tool call: store result

We can create a middleware skill that intercepts tool calls and posts to the worker. For now, manual capture is via `claude-mem store`.

## Progressive Disclosure in Conversations

When a user asks a question that might benefit from past context:

1. Search index with `claude-mem search` (cheap)
2. Present 3-5 most relevant IDs to the user/LLM
3. Use `claude-mem get` to fetch full details for the chosen ones
4. Inject those snippets into the conversation

This avoids sending the entire memory log (expensive) while still leveraging long-term recall.

## Session Continuity

At the beginning of a new session, you can warm the context:

```bash
# Get recent observations from last session
claude-mem list --limit 10
# Or search for ongoing project keywords
claude-mem search "project-name" --limit 5
```

Then feed those summaries into the initial prompt.

## Privacy Enforcement

Private observations are:
- Encrypted at rest if `ENCRYPTION_KEY` is set
- Excluded from search by default unless `--private` flag used
- Not shown in timelines unless explicitly requested

Use `<private>` tags in content to auto-mark.

---

**Note:** This is a basic integration guide. A more seamless integration could be built as an OpenClaw plugin that hooks into the tool lifecycle.