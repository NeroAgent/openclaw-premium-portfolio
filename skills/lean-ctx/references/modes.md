# Lean File Read Modes

## Full Mode (`full`)
Read the entire file content. Best for:
- Full file review
- Editing
- When you need complete context

**Token cost:** 100% of file tokens first read; subsequent reads from cache cost ~13 tokens (MD5 hash lookup).

**Options:**
- `--fresh` — bypass cache and re-read full content
- `--lines:N-M` — only specific line ranges within full read

## Map Mode (`map`)
Returns a high-level summary of the file:
- Imports/dependencies
- Exported symbols (functions, classes, types)
- File structure (module, mod declarations)

**Best for:** Quick understanding of a file without reading its body.

**Token cost:** ~5-15% of full file tokens.

**Example output (Rust):**
```
stats.rs [284L]
deps: serde::, std::collections::HashMap, std::path::PathBuf
exports: StatsStore, load, save, record, format_gain
API:
  struct StatsStore
  fn load() → StatsStore
  fn save(store: &StatsStore)
  fn record(command: s, input_tokens: n, output_tokens: n)
  fn format_gain() → String
```

## Signatures Mode (`signatures`)
Provides function/class/method signatures with parameter and return types, but no bodies.

**Best for:** Understanding API surface without implementation details.

**Token cost:** ~10-20% of full file.

**Example output (TypeScript):**
```typescript
interface UserService {
  getUser(id: string): Promise<User>
  updateUser(id: string, data: Partial<User>): Promise<void>
  deleteUser(id: string): Promise<boolean>
}
```

## Diff Mode (`diff`)
When re-reading a file that was previously cached, only send the changed hunks (via Myers diff). Assumes you have a previous version in cache.

**Best for:** Incremental updates during active editing.

**Token cost:** proportional to size of changes, typically << 1% of full file.

## Aggressive Mode (`aggressive`)
Strips boilerplate, comments, and verbose sections while preserving syntax structure. Uses language-specific heuristics.

**Best for:** Very large files (1000+ lines) where you need to skim logic.

**Token cost:** ~30-50% of full file.

## Entropy Mode (`entropy`)
Applies Shannon entropy analysis and Jaccard similarity filtering to remove repetitive or low-information content.

**Best for:** Data files, generated code, log-like content.

**Token cost:** ~20-40% of full file.

## Line Range (`lines:10-50,80-90`)
Read only specific line ranges. Useful when you know exactly which part you need.

**Token cost:** proportional to number of lines selected (plus small overhead).

---

## Choosing a Mode

| Scenario | Recommended Mode |
|----------|------------------|
| First time reading a file | `full` (caches for later) |
| Understanding structure | `map` |
| Using an API | `signatures` |
| Re-reading after edit | `diff` (automatic if you use lean-ctx repeatedly) |
| Large generated file | `aggressive` or `entropy` |
| Specific section known | `lines:N-M` |

## Default Behaviors

- `lean-ctx read file.rs` (no mode) → `full` with caching
- Subsequent reads of same file → automatically `diff` if file changed, else cache hit (~13 tokens)
- You can override with explicit `--mode`.

## Cache Management

Cache lives in `~/.lean-ctx/cache/` and auto-expires after 5 minutes of inactivity (configurable). To clear manually:

```bash
lean-ctx cache clear
# or
rm -rf ~/.lean-ctx/cache
```

To bypass cache for a single read:

```bash
lean-ctx read file.rs --fresh
```