# OpenBrowser Command Reference

## Core Commands

| Command | Arguments | Purpose |
|---------|-----------|---------|
| `open <url>` | URL | Navigate to a page |
| `click <selector>` | CSS selector | Click an element |
| `type <selector> <text>` | selector, text | Enter text into input |
| `scroll <direction>` | `up`/`down`/`to` | Scroll page |
| `screenshot [path]` | optional file | Capture screenshot (saves to file or returns base64) |
| `extract <goal>` | natural language description | Extract content from page (returns markdown) |
| `eval <js>` | JavaScript snippet | Execute script in page context |
| `state` | — | Show current URL, title, tabs |
| `sessions` | — | List active browser sessions |

## Examples

```
open https://example.com
click button.submit
type input#email "test@example.com"
screenshot form.png
extract "price and product name"
eval "document.title"
```

## Selector Strategies

- Prefer `id` selectors: `#email`
- Class: `.btn-primary`
- Attribute: `[name="q"]`
- Text content: `text=Submit` (openbrowser may support this)

If a selector fails, the agent can try alternatives or report error.

## Output

Commands return structured JSON with:
- `success` (bool)
- `value` (result data, e.g., extracted markdown)
- `error` (if failed)
- `screenshot` (path or base64 if captured)

The `text` output format prints human-readable summaries.

---

For more details, see the upstream repo: https://github.com/ntegrals/openbrowser