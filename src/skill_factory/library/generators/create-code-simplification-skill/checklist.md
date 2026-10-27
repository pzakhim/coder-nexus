# Checklist — code-simplification

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule S1–S14 is adopted, adapted, cited as enforced by a gate, or "not adopted" with a reason; S1, S2, S12, S13 are adopted
- [ ] The catalog covers the four lenses (Reuse, Simplification, Efficiency, Altitude); each kept row has a real example or is marked illustrative
- [ ] Thresholds, naming, dead code and wrapper rules are linked to clean-code, not repeated
- [ ] Abstractions required by decisions or clean-architecture ports are listed under "Leave these alone"
- [ ] Per-step check commands exist in the workspace and are reported as `PASS` / `FAIL`
- [ ] Findings that would change behavior or reach outside the diff go to Concerns, not into the code
- [ ] Report line uses the workspace's `simplify:` hand-off notation; review grading uses `BLOCKER` / `MAJOR` / `MINOR` (`shared_contracts/flags_and_statuses.md` §2), never `P1`/`P2`/`P3`
- [ ] `references/01-scope-and-safety.md`, `02-smell-catalog.md` and `03-report-and-review.md` are present
- [ ] The simplicity pass of incremental-implementation (if present) links here
