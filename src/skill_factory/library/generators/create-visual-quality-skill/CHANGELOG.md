# Changelog — create-visual-quality-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.1.0 — 2026-10-25

- Standardized all gate flags (`PASS` / `FAIL` / `BLOCKED` / `NOT_RUN` / `UNVERIFIED` / `N/A`) and deviation severities (`BLOCKER` / `MAJOR` / `MINOR` + `ACCEPTED (D-NN)`) to align with `shared_contracts/flags_and_statuses.md`.
- Made `V1`–`V12` mandatory compliance across all UI stacks (mobile, desktop, web, headless golden harnesses), removing `"not adopted"` carve-outs and hardcoded browser/CSS assumptions.
- Consolidated `templates/` into `templates/SKILL.md.tmpl` and 3 cohesive reference templates under `templates/references/01..03-*.md.tmpl`, with optional `profiles/<profile>/` support.

**Affects:** `SKILL.md`, `references/01..03-*.md`.
**Migration:** Re-run `create-visual-quality-skill` in update/sync mode to consolidate `references/` into 3 cohesive files and adopt `BLOCKER` / `MAJOR` / `MINOR` deviation grading.

## 1.0.0 — 2026-10-22

First version.
