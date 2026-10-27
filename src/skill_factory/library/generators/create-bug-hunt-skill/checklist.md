# Checklist — bug-hunt

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule `H1`–`H14` is adopted and adapted to the workspace's stack, commands, and report location (zero `"not adopted"` waivers)
- [ ] Generated skill uses the cohesive 3-reference layout (`01-scope-dimensions-and-patterns.md`, `02-verify-and-disprove.md`, `03-severity-verdict-and-report.md`)
- [ ] Project and stack patterns are derived from the workspace's architecture and risk areas, each naming real paths and checks
- [ ] Effort triggers name the workspace's high-risk areas for `deep`
- [ ] Severity uses the unified `BLOCKER` / `MAJOR` / `MINOR` scale with `CONFIRMED` / `PLAUSIBLE` confidence (zero `P0`–`P3` remnants)
- [ ] Read-only verification commands and caller search (`rg`, analyzer, focused test runner) are real, report binary `PASS` / `FAIL` (or `NOT_RUN`), and never modify code
- [ ] Reviewer is strictly read-only; Code Writer self-check runs at `quick` and fixes `CONFIRMED` findings with a regression test first
- [ ] The self bug-hunt step of `incremental-implementation` (if present) links here at `quick`
