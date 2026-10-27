# Checklist — code-review

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule `R1`–`R14` is adopted and adapted to the workspace's stack, validators, commands, and report location (zero `"not adopted"` waivers)
- [ ] Generated skill uses the cohesive 3-reference layout (`01-scope-gates-and-validators.md`, `02-review-axes-and-rubric.md`, `03-findings-verdict-and-report.md`)
- [ ] Each review axis links its rubric skill, or carries the fallback checklist when a skill is not installed
- [ ] Gate commands and validators are real and rerun independently by the reviewer (`PASS` / `FAIL`; `NOT_RUN`, `BLOCKED`, `UNVERIFIED` never count as `PASS`)
- [ ] Finding severities use the single unified scale (`BLOCKER` / `MAJOR` / `MINOR` — zero `P1`–`P3` remnants)
- [ ] Verdict words (`APPROVED`, `CHANGES_REQUESTED`, `BLOCKED`), finding IDs (`RV-NN`), and report location match the workspace's contract
- [ ] Bug-hunt effort levels match the `bug-hunt` skill
- [ ] Reviewer stays strictly read-only; no reviewer waiver path exists (`PLAN_CONFLICT` routes to planning/user)
