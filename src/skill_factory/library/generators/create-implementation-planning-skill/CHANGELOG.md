# Changelog — create-implementation-planning-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see [../../core/sync-protocol.md](../../core/sync-protocol.md)). Bump rules: [../../core/versioning.md](../../core/versioning.md).

## 1.1.0 — 2026-10-25

- Standardized all rules `IP1`–`IP17` as mandatory compliance across every generated `implementation-planning` skill. (minor)
- Updated `IP7` to align with `git-workflow` (`G2`, `G3`, `M3`, `M10`): work branches are named after the parent/umbrella ticket (`<type>/<PARENT-TICKET>-<short-description>`, or `<type>/<short-description>` only when no tracker ticket exists), and each phase or sub-ticket boundary maps to an explicit verified commit checkpoint carrying the sub-ticket ID (`<type>(<SUB-TICKET>): <summary> [parent: <PARENT-TICKET>, PHASE-NN]`) or accepted phase ID (`<type>(<PARENT-TICKET>): [PHASE-NN] <summary>` / `<type>(phase-NN): <summary>`) rather than arbitrary WIP commits. (minor)
- Consolidated generated reference templates into 3 cohesive topic files under `templates/references/`: `01-phase-order-and-slicing-strategy.md.tmpl`, `02-task-shape-sizing-and-checks.md.tmpl`, and `03-phase-00-readiness-and-dod.md.tmpl`, and added `<!-- {{profile_references}} -->` to `templates/SKILL.md.tmpl`. (minor)
- Aligned CLI verification gates (`validate_plan_slices`, task checks, `PHASE-00` readiness probes) to binary `PASS` / `FAIL` and plan review findings to `BLOCKER` / `MAJOR` / `MINOR` per `shared_contracts/flags_and_statuses.md`. (minor)
- Removed legacy multi-directory branching assumptions and replaced global core paths with repository-relative `../../core/` links. (patch)

**Affects:** `SKILL.md`, `references/01-phase-order-and-slicing-strategy.md`, `references/02-task-shape-sizing-and-checks.md`, `references/03-phase-00-readiness-and-dod.md`.
**Migration:** re-run `create-implementation-planning-skill` in update/sync mode to consolidate `01`–`04` into `01`–`03`, add `IP7` parent-ticket branch and sub-ticket/phase commit checkpoint rules, and apply `PASS`/`FAIL` gates and `BLOCKER`/`MAJOR`/`MINOR` review severities.

## 1.0.0 — 2026-10-22

First version.

- Base rules `IP1`–`IP17` with reasons: order inside a behavior, task shape, paths from `clean-architecture`, a real check per task, `PHASE-00` items, Definition of Done, branch and hotfix tasks, handoffs, unknowns early, global constraints, review focus, task sizing, high risk first, prefactor first, expand-migrate-contract, signatures-not-bodies, and tests/docs inside each phase.
- Detection of layout, past plans, checks, readiness tools, and change size.
- Output path: `<workspace>/.agents/skills/implementation-planning/`.

**Affects:** all generated files.
**Migration:** existing planning guides → run the generator to **adopt**.
