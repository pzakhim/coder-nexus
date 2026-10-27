# Changelog — create-git-workflow-skill

## 1.1.0 — 2026-10-25

### Changed
- Added mandatory rule `M10` and expanded `G2`/`G3` for **Parent-Ticket Branch Naming + Sub-Ticket / Accepted-Phase Commit Traceability & Checkpoint Discipline** (no arbitrary WIP commits; every commit must bind to a verified Huly sub-ticket and/or accepted `PHASE-NN` checkpoint).
- Replaced hardcoded `be-v…` / `fe-v…` tag examples with stack-neutral `<component>-v…` (`V7`).
- Enforced mandatory compliance across `M1`–`M10`, `G1`–`G6`, `V1`–`V7`, `R1`–`R2` (removed `"not adopted"` carve-outs).
- Consolidated `templates/` from 5 micro-files into `templates/SKILL.md.tmpl` and 3 cohesive reference templates under `templates/references/` (`01-branch-model-and-preflight.md.tmpl`, `02-naming-commits-and-merge-strategy.md.tmpl`, `03-versioning-release-and-gates.md.tmpl`) with binary `PASS`/`FAIL` CLI gates and `BLOCKER`/`MAJOR`/`MINOR` review grading.

## [1.0.0] - 2026-04-12

- Initial release of `create-git-workflow-skill`.
