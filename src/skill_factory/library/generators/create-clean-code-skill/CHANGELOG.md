# Changelog — create-clean-code-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.2.0 — 2026-10-24

- Consolidated generated `references/` from 6+ fragmented files into 3 cohesive topic files: `01-structure-naming-and-types.md`, `02-errors-lifecycle-and-logging.md`, and `03-self-check-and-review.md`.
- Split `SKILL.md` into (1) Deterministic Tool Gates (`PASS` / `FAIL`) and (2) Mandatory Core Design Principles (dropping per-rule severity column).
- Unified review severities to `BLOCKER` / `MAJOR` / `MINOR` (`shared_contracts/flags_and_statuses.md`) and replaced stack-specific generator references with stack-neutral `base-rules.md` and `discovery-and-checks.md`.
- Added `<!-- {{profile_references}} -->` marker support for `profiles/{imespro,external-structured,external-standard}/`.

**Affects:** `SKILL.md`, `references/01-structure-naming-and-types.md`, `references/02-errors-lifecycle-and-logging.md`, `references/03-self-check-and-review.md`.
**Migration:** merge `01`+`02`+`02b`+`04` into `01-structure-naming-and-types.md`, `03` into `02-errors-lifecycle-and-logging.md`, and `05`+`06` into `03-self-check-and-review.md`; update `SKILL.md` to use `PASS`/`FAIL` tool gates and `BLOCKER`/`MAJOR`/`MINOR` review severities.

## 1.1.0 — 2026-10-23

- Decoupled base input from core `plugins/core/skills/clean-code`, relying directly on self-contained `references/base-rules.md`.

**Affects:** generator base input resolution.
**Migration:** none required for existing workspace skills.

## 1.0.0 — 2026-10-22

First version.

- Base rules C1–C14 with reasons and default severities (from Coder Nexus `plugins/core/skills/clean-code` and the erp-knowledge-platform clean-code standard, generalised).
- Naming and self-check references per stack (Python, TypeScript/React/Next.js, NestJS, Flutter/Dart, Go).
- Mandatory: `SKILL.md`, naming, size & structure, **splitting (02b, clean-code's half of `core/splitting-protocol.md`, with a fallback when the workspace has no clean-architecture skill)**, errors & logging, self-check. Suggested: types/constants/comments, review severity.
- Thresholds are owned here (02); clean-architecture links to them.
- Layouts: flat `references/01–06`; branched `be/01–05`, `fe/01–05`, `shared/06`.
- Includes Step 0 (never write into Coder Nexus-managed files; workspace skills override fixed ones), trial run and description steps.
- Output path: `<workspace>/.agents/skills/clean-code/`.

**Affects:** all generated files.
**Migration:** existing, unregistered `clean-code` skills → run the generator to **adopt** (keeps workspace rule IDs, severities and checks; records provenance).
