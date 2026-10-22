# Changelog — create-implementation-planning-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## Unreleased

- Added: IP10 Global constraints — exact spec values copied once to a new `## Global constraints` section of `implementation-plan.md`, inherited by every task → `references/01-phase-order.md` (`shared/01-…`) "Plan header". (minor)
- Added: IP11 Review focus — up to five uncovered inputs or failure modes, each owned by a task check; missing expected results become `Q-NN` → `01` "Plan header", `02` "Shape". (minor)
- Added: IP12 task sizing XS–XL from repository history with split triggers (XL, 8+ files, "and" in the title, two subsystems) and the reviewer-reject split rule → `02` "Size". (minor)
- Added: IP13 high risk first after PHASE-00 (extends IP9), IP14 prefactor first, IP15 expand → migrate → contract for wide renames → `01` "Unknowns and risk first", "Prefactor and wide renames". (minor)
- Added: IP16 signatures and pinned values, no transcribed function bodies → `02` "Shape". (minor)
- Added: IP17 tests and docs inside each phase, never a final testing phase; IP17 is never "not adopted" → `01` "Tests and docs", `04` checklist items. (minor)
- Changed: generated `SKILL.md` "Always" list gains the plan header, risk/prefactor/expand order, sizing and no-final-testing-phase bullets. (minor)
- Changed: `## Global constraints` and `## Review focus` sit above `## AC coverage` and the empty marker is `None found after checking every AC and BR`, matching the fixed `planning-and-task-breakdown` skill and plan template. (patch)
- Added: generator `references/sources.md` (external sources and ideas not adopted), detection rows for rework history, spec values and review gaps, checklist items, trial-run comparison of review-focus lines. (patch)

**Affects:** `SKILL.md`, `references/01-phase-order.md` (`shared/01-…`), `references/02-task-shape-and-checks.md` (`be/02-…`, `fe/02-…`), `references/04-definition-of-done.md` (`be/04-…`, `fe/04-…`).
**Migration:** look up past approved specs (item-wide values), reviewed commits that landed without rework (size scale) and review/QA defects no check covered. Add "Plan header", "Unknowns and risk first", "Prefactor and wide renames" and "Tests and docs" to 01; add the signature rule and the "Size" table to 02; add the three new Definition of Done items to 04; add the new "Always" bullets to `SKILL.md`. Existing sections keep their names; non-breaking.

## 1.0.0 — 2026-10-22

First version.

- Base rules IP1–IP9 with reasons: order inside a behavior, task shape, paths from clean-architecture, a real check per task, PHASE-00 items, Definition of Done, branch and hotfix tasks, handoffs, unknowns early.
- Detection of layout, past plans, checks, readiness tools and change size.
- Mandatory: `SKILL.md`, phase order, task shape and checks, PHASE-00 readiness, Definition of Done.
- Layout: flat or branched (`shared/` + `be/` + `fe/`).
- Output path: `<workspace>/.agents/skills/implementation-planning/`.

**Affects:** all generated files.
**Migration:** existing planning guides → run the generator to **adopt**.
