# Changelog — create-security-review-skill

## 1.1.0 — 2026-10-25

### Changed
- Unified security finding severities on **`BLOCKER` / `MAJOR` / `MINOR`** and CLI scanner gates on **`PASS` / `FAIL`** (`shared_contracts/flags_and_statuses.md`), removing `CRITICAL` / `HIGH` / `MEDIUM` / `LOW`.
- Removed branched `templates/shared/` + `templates/branch/04-checks.md.tmpl` (`be/04`, `fe/04`) layout and hardcoded stack headings (`FastAPI`, `React`, `Flutter`), organizing security checks by stack-agnostic architectural boundaries.
- Enforced mandatory compliance for `SR1`–`SR14` (removed `"not adopted"` carve-outs).
- Consolidated `templates/` into `templates/SKILL.md.tmpl` and 3 cohesive reference templates under `templates/references/` (`01-triggers-threat-model-and-auth-matrix.md.tmpl`, `02-security-checks-and-cli-gates.md.tmpl`, `03-findings-verdict-and-report.md.tmpl`).

## [1.0.0] - 2026-04-12

- Initial release of `create-security-review-skill`.
