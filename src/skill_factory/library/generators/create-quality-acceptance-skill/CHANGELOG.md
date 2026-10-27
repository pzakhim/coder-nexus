# Changelog — create-quality-acceptance-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see [../../core/sync-protocol.md](../../core/sync-protocol.md)). Bump rules: [../../core/versioning.md](../../core/versioning.md).

## 1.1.0 — 2026-10-25

### Changed
- Standardized defect severities on **`BLOCKER` / `MAJOR` / `MINOR`**, case outcomes on **`PASS` / `FAIL` / `BLOCKED` / `NOT_RUN`**, and deterministic CLI execution gates on **`PASS` / `FAIL`** (`shared_contracts/flags_and_statuses.md`).
- Removed branched `templates/shared/` + `templates/branch/03-execution.md.tmpl` (`be/03`, `fe/03`) layout, organizing runtime verification by stack-agnostic **UI/Client Surface (`A5`)** and **API/Service Surface (`A6`)** in a flat 3-reference layout.
- Enforced **mandatory compliance** for `A1`–`A14` (removed optional rule carve-outs).
- Explicitly connected `A6` with `security-review` (`SR14`) for live runtime verification of the `Role × Environment × Action × Object` authorization matrix (`401`/`403`/`404` anti-IDOR) and runtime-dependent `PLAUSIBLE` checks handed over by Security Review.
- Consolidated `templates/` into `templates/SKILL.md.tmpl` (< 115 lines) and 3 cohesive reference templates under `templates/references/` (`01-preconditions-safety-and-case-loop.md.tmpl`, `02-ui-and-api-execution-checks.md.tmpl`, `03-failures-retest-and-gates.md.tmpl`).

## 1.0.0 — 2026-10-22

First version.

- Base rules `A1`–`A14` with reasons: approved plan on the reviewed revision, read-only boundary, cases executed as written, real data paths and persistence read-back, real UI/client states and console/network health, real API/service execution with auth per role and forbidden-call verification, `BLOCKED` when a tool is unreachable, evidence per case, result vocabulary, failure details, out-of-scope and regression cases, re-test scope, safety, and flakiness classification.
- UI/client and API/service tools detected in the workspace and confirmed at the gate, with an operations map per tool.
- Output path: `<workspace>/.agents/skills/quality-acceptance/`.
