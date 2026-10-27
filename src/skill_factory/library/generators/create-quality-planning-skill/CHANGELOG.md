# Changelog — create-quality-planning-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see [../../core/sync-protocol.md](../../core/sync-protocol.md)). Bump rules: [../../core/versioning.md](../../core/versioning.md).

## 1.1.0 — 2026-10-25

### Changed
- Unified test case risk tiers and plan-review finding severities on **`BLOCKER` / `MAJOR` / `MINOR`** and deterministic CLI verification gates on **`PASS` / `FAIL`** (`shared_contracts/flags_and_statuses.md`), removing legacy numbered priority labels.
- Removed branched `templates/shared/` + `templates/branch/04-test-levels.md.tmpl` (`be/04`, `fe/04`) layout and hardcoded tool/framework names in `references/test-levels.md`, organizing test levels by stack-neutral verification boundaries (API/Service Acceptance, UI/Client End-to-End, Visual Fidelity, Integration, Unit).
- Enforced mandatory compliance for `Q1`–`Q14` across `references/base-rules.md`, `SKILL.md`, and `checklist.md` (removed `"not adopted"` carve-outs).
- Explicitly connected `Q4` with `security-review` (`SR14`): test plans include `Role × Environment × Action × Object` permission matrix cases and runtime-dependent `PLAUSIBLE` items handed over from `security-review`.
- Consolidated `templates/` into `templates/SKILL.md.tmpl` (< 115 lines) and 3 cohesive reference templates under `templates/references/` (`01-sources-testability-and-traceability.md.tmpl`, `02-case-design-and-test-levels.md.tmpl`, `03-data-environments-and-plan-gates.md.tmpl`).

## 1.0.0 — 2026-10-22

First version.

- Base rules Q1–Q14 with reasons: specs as source of truth, early testability review, two-way traceability, coverage categories, cheapest proving level, safe test data, environments, risk priority, out-of-scope guards, regression set, concrete expected results, case IDs, plan approval, independence from the implementation.
- Case-design techniques and test-level selection with owners (integration-test owner chosen per workspace).
- First generator of the Quality Assurance Pack ([../../core/quality-skill-family.md](../../core/quality-skill-family.md)).
- Output path: `<workspace>/.agents/skills/quality-planning/`.
