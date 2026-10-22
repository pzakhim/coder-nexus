# Changelog — create-implementation-planning-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.0.0 — 2026-10-22

First version.

- Base rules IP1–IP9 with reasons: order inside a behavior, task shape, paths from clean-architecture, a real check per task, PHASE-00 items, Definition of Done, branch and hotfix tasks, handoffs, unknowns early.
- Detection of layout, past plans, checks, readiness tools and change size.
- Mandatory: `SKILL.md`, phase order, task shape and checks, PHASE-00 readiness, Definition of Done.
- Layout: flat or branched (`shared/` + `be/` + `fe/`).
- Output path: `<workspace>/.agents/skills/implementation-planning/`.

**Affects:** all generated files.
**Migration:** existing planning guides → run the generator to **adopt**.
