# Changelog — create-root-cause-debugging-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.1.0 — 2026-10-23

- Decoupled verify step from core bug-hunt, referencing self-contained `references/base-rules.md` and `work-item-contract` §9.

**Affects:** generator base input resolution.
**Migration:** none required for existing workspace skills.

## 1.0.0 — 2026-10-22

First version.

- Base rules D1–D14 with reasons (reproduce first, read the real error, isolate, one falsifiable hypothesis at a time, root cause at the right layer, regression test, never green-wash, environment vs code, temporary instrumentation removed, time-box and escalation, workspace tracing tools, report).
- Symptom → approach techniques and focused/verbose/rerun/bisect commands per stack.
- Mandatory: `SKILL.md`, reproduce & read, isolate & hypothesize, fix & prevent, stop & escalate, tools & commands. Suggested: report.
- Layouts: flat `references/01–06`; branched `shared/01–04, 06`, `be/05`, `fe/05`.
- Output path: `<workspace>/.agents/skills/root-cause-debugging/`.

**Affects:** all generated files.
**Migration:** existing debugging skills → run the generator to **adopt** (keeps tool rules such as mandatory impact analysis).
