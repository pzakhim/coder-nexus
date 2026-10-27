# Changelog — create-code-review-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.1.0 — 2026-10-24

- Replaced stack-specific `references/axes.md` and 5 branched templates (`shared/01, 03, 04, 05` + `branch/02`) with stack-agnostic `references/deriving-the-model.md` and 3 cohesive reference templates (`01-scope-gates-and-validators.md`, `02-review-axes-and-rubric.md`, `03-findings-verdict-and-report.md`).
- Standardized on mandatory `R1`–`R14` compliance, binary `PASS` / `FAIL` gate execution, and unified `BLOCKER` / `MAJOR` / `MINOR` finding severities.

**Affects:** generator templates and reference guides.
**Migration:** existing workspace skills can consolidate `01` → `01-scope-gates-and-validators.md`, `02` → `02-review-axes-and-rubric.md`, and `03`+`04`+`05` → `03-findings-verdict-and-report.md`.

## 1.0.0 — 2026-10-22

First version.
