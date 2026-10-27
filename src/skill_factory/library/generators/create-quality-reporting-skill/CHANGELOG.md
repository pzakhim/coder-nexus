# Changelog — create-quality-reporting-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see [../../core/sync-protocol.md](../../core/sync-protocol.md)). Bump rules: [../../core/versioning.md](../../core/versioning.md).

## 1.1.0 — 2026-10-25

### Changed
- Unified defect and report review severities on **`BLOCKER` / `MAJOR` / `MINOR`**, per-case statuses on **`PASS` / `FAIL` / `BLOCKED` / `NOT_RUN`** (`UNVERIFIED` never counts as `PASS`), feature verdicts on **`ACCEPTED` / `CHANGES_REQUESTED` / `BLOCKED`**, and deterministic CLI report gates on **`PASS` / `FAIL`** (`shared_contracts/flags_and_statuses.md`).
- Replaced stack-specific table headings with stack-agnostic surface tables (`API / Service Surface` and `UI / Client Surface`, or a single unified results table).
- Enforced **mandatory compliance** for all base rules `RP1`–`RP12`.
- Consolidated `templates/` into `templates/SKILL.md.tmpl` (< 115 lines) and 3 cohesive reference templates under `templates/references/` (`01-report-structure-and-verdict.md.tmpl`, `02-defects-and-retest-history.md.tmpl`, `03-evidence-hygiene-and-gates.md.tmpl`).

## 1.0.0 — 2026-10-22

First version.

- Base rules `RP1`–`RP12` with reasons: revision-bound report with environment record, per-case results with evidence, AC coverage derived from cases, feature verdict criteria, defect list and lifecycle, limitations, honest counting, evidence hygiene, destination and authorisation, re-test history, verdict-first summary, no edited expectations.
- Full report template.
- Output path: `<workspace>/.agents/skills/quality-reporting/`.
