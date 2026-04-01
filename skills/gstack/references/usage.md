# Usage Patterns

## Single-Threaded Workflow

```
Describe feature → /plan-ceo-review → /plan-eng-review → Code → /review → /ship → /qa
```

## Parallel with Conductor

If you use [Conductor](https://conductor.build) to run multiple Claude Code sessions in parallel, you can have:

- Session 1: `/browse` checking staging
- Session 2: `/review` on a PR
- Session 3: Implementing a new feature
- Session 4: `/qa` on another branch

All isolated with separate browser instances.

## Greptile Integration

If you have Greptile reviewing your PRs, `/review` and `/ship` automatically triage Greptile comments:
- Valid issues → fixed before ship
- Already fixed → auto-reply
- False positives → user confirms, then reply explaining

## Cookie Import for Authenticated Testing

1. `/setup-browser-cookies` → pick domains from your real browser
2. `/browse https://staging.example.com` or `/qa` will now be logged in

## Retrospective Cadence

Run `/retro` weekly. It analyzes commit history, PRs, and code changes to produce an engineering retro with per-person feedback.

Saved snapshots allow comparison week-over-week.

## Tips

- Don't use `/ship` until `/review` is clean.
- Use `/qa` on every feature branch before merging.
- Use `/plan-ceo-review` early to avoid building the wrong thing.
- Keep the browser window visible while `/browse` runs; it's fascinating to watch.

---

For detailed mode explanations, see `modes.md`.