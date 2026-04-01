# OpenBrowser Architecture

## Components

1. **Agent** — The AI brain that decides actions based on page state and task.
2. **Viewport** — Playwright browser instance controlling Chromium.
3. **Commands** — Discrete actions: `goto`, `click`, `type`, `scroll`, `screenshot`, `extract`, etc.
4. **Model** — LLM integration (OpenAI, Anthropic, Google).
5. **Metering** — Token usage, cost tracking, step counting.
6. **Sandbox** (optional) — Resource-limited execution with timeouts.

## Flow

```
Task → Agent → Select Command → Viewport execute → Observe → next step...
```

The agent maintains a conversation with the LLM, providing:
- Current URL and page title
- Actionable elements (clickable, typeable) with selectors
- Screenshots (optional)
- Previous steps and outcomes

The LLM responds with a command to execute. The loop continues until:
- Task completion signal
- Max steps reached
- Error threshold exceeded
- User interrupt

## Stalls and Recovery

If the page seems stuck (network slow, spinner), the agent detects lack of progress and may:
- Refresh the page
- Scroll to trigger lazy loading
- Retry failed actions

## Cost

Each step sends page context (~1-2k tokens) + LLM response (~500 tokens). With 25 steps, expect ~60k tokens per task. Choose models wisely.

## Recording & Debugging

Set `OPEN_BROWSER_TRACE_PATH` to capture traces viewable in Chrome DevTools. Set `OPEN_BROWSER_SAVE_RECORDING_PATH` to save a video of the session.

---

For full UPSTREAM documentation see: https://github.com/ntegrals/openbrowser