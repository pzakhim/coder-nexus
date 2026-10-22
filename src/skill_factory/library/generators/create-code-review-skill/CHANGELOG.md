# Changelog — create-code-review-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.0.0 — 2026-10-22

First version.

- Base rules R1–R14 with reasons (from Coder Nexus `plugins/core/agents/code_reviewer.md` and `plugins/packs/<stack>/skills/code-review`, generalised): fixed revision, read-only, bug-hunt first, axes graded by the workspace's own skills, traceability, gates rerun, no reviewer waivers, finding format, diff-only scope, verdicts, rounds and escalation, no cosmetic demands, revision-bound report, delta re-review.
- Review axes for backend and frontend with rubric skills, gates and typical blocking findings.
- Mandatory: `SKILL.md`, scope & order, review axes, findings & severity, verdicts & rounds. Suggested: report.
- Layouts: flat `references/01–05`; branched `shared/01, 03, 04, 05`, `be/02`, `fe/02`.
- First generator of the Code Review Pack (`core/reviewer-skill-family.md`).
- Output path: `<workspace>/.agents/skills/code-review/`.

**Affects:** all generated files.
**Migration:** existing review skills → run the generator to **adopt** (keeps axes, finding IDs, verdict words and report location).
