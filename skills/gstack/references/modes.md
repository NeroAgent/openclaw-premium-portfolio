# Gstack Modes Deep Dive

## /plan-ceo-review

**Mental模型:** Founder / CEO (Brian Chesky style). Ask: "What is the 10-star product hiding inside this request?"

**Focus:** Product taste, user empathy, long-term vision.

**Output:** Rethought problem statement, premium experience, delight factors, maybe a entirely different direction than the original ask.

**Example:**

User: "Add photo upload to listings."
`/plan-ceo-review` → Might suggest: auto-identify product from photo, import specs & comps, generate title/description, pick hero image. Not just a file input.

## /plan-eng-review

**Mental模型:** Engineering manager / tech lead.

**Focus:** Architecture, data flow, state machines, failure modes, trust boundaries, test coverage, diagrams.

**Output:** Architecture diagram, sequence diagrams, list of risks, test matrix.

**Example:** After CEO plan, this mode fleshes out the technical spine.

## /review

**Mental模型:** Paranoid staff engineer.

**Focus:** Bugs that survive CI. N+1 queries, race conditions, stale reads, missing indexes, trust boundary violations, orphan cleanup, retry logic, invariant violations.

**Output:** Structured list of issues with severity and code locations.

## /ship

**Mental Model:** Release engineer.

**Focus:** Execution. Not ideation — shipping.

**Actions:** Sync main, run tests, resolve Greptile reviews (if present), update changelog, push branch, open or update PR.

**Outcome:** Branch lands with proper hygiene.

## /browse

**Mental Model:** QA engineer.

**Focus:** Give the agent eyes. It controls a real browser (Chromium via Playwright).

**Capabilities:**
- Navigate, click, type, scroll
- Take screenshots, read console
- Multi-step workflows
- Persistent session (cookies carry over)

**Use:** Smoketest, authenticated page checks, visual verification.

## /qa

**Mental Model:** QA lead.

**Focus:** Systematic testing. Two modes:
- **Diff-aware** (default on branches): Analyzes `git diff main` to identify affected routes/pages and tests them.
- **Full** / **Quick** / **Regression** modes.

**Output:** Health score, top issues with screenshots.

## /setup-browser-cookies

**Mental Model:** Session manager.

**Focus:** Import cookies from your real browser (Chrome, Arc, Brave, Edge) into the headless session. Allows testing authenticated pages without manual login.

**Process:** Interactive picker UI, then cookies loaded into Playwright session.

## /retro

**Mental Model:** Engineering manager.

**Focus:** Data-driven team retro.

**Output:** Week summary, per-contributor breakdown (praise + growth opportunities), metrics (commits, LOC, test ratio, PR sizes), top wins, habits.

**Saves:** JSON snapshot to `.context/retros/` for trend tracking.

---

## Choosing the Right Mode

| Goal | Mode |
|------|------|
| Validate problem space | `/plan-ceo-review` |
| Design technical solution | `/plan-eng-review` |
| Ensure code quality | `/review` |
| Land a branch | `/ship` |
| See it in browser | `/browse` |
| Verify changes | `/qa` |
| Test logged-in areas | `/setup-browser-cookies` then `/qa` |
| Reflect on team progress | `/retro` |

Mix-and-match. A typical feature: CEO → Eng → Implement → Review → Ship → QA.