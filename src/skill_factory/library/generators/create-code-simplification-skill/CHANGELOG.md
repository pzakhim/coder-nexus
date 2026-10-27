# Changelog — create-code-simplification-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.2.0 — 2026-10-24

- Consolidated generated `references/` from 5 files into 3 cohesive topic files: `01-scope-and-safety.md` (when & scope, behavior safety, stop criteria), `02-smell-catalog.md` and `03-report-and-review.md`; dropped the branched `be/`/`fe/`/`shared/` layout and `{{branch_suffix}}`.
- Rules renumbered and regrouped as S1–S14; added the four review lenses from Claude Code `/simplify`: **Reuse** (S5), **Simplification** (S8), **Efficiency** (S9, new) and **Altitude** (S10, new). Catalog grouped by lens; findings that would change behavior or reach outside the diff go to Concerns. Rules owned by clean-code (C1, C2, C6) are linked, not repeated.
- Dropped the per-rule severity column; review grading uses `BLOCKER` / `MAJOR` / `MINOR` (`shared_contracts/flags_and_statuses.md`) instead of `P1`/`P2`/`P3`.
- Replaced stack-specific `references/stack-notes.md` with stack-neutral `references/discovery-and-checks.md`.
- Added `<!-- {{profile_references}} -->` marker support for `profiles/<profile>/`.

**Affects:** `SKILL.md`, `references/01-scope-and-safety.md`, `references/02-smell-catalog.md`, `references/03-report-and-review.md`.
**Migration:** merge `01`+`02`+`04` into `01-scope-and-safety.md`, `03` into `02-smell-catalog.md` (regroup rows by lens and add Efficiency and Altitude rows found in the workspace), and `05` into `03-report-and-review.md`; map old rule IDs to S1–S14 (keep workspace IDs if it has its own, P5); replace `P1`/`P2`/`P3` with `BLOCKER`/`MAJOR`/`MINOR`.

## 1.1.0 — 2026-10-23

- Decoupled base input from core `plugins/core/skills/code-simplification`, relying directly on self-contained `references/base-rules.md` and ponytail skills.

**Affects:** generator base input resolution.
**Migration:** none required for existing workspace skills.

## 1.0.0 — 2026-10-22

First version.

- Base rules S1–S13 with reasons and severities (from Coder Nexus `plugins/core/skills/code-simplification`, `plugins/ponytail` and the erp-knowledge-platform simplification standard, generalised).
- Smell → technique catalog (delete, stdlib, native, yagni, shrink, flatten, rename, inline) and stack notes.
- Mandatory: `SKILL.md`, when & scope, behavior safety, smell catalog, stop criteria. Suggested: report.
- Layouts: flat `references/01–05`; branched `shared/01, 02, 04, 05`, `be/03`, `fe/03`.
- Step 0 (never write into Coder Nexus-managed files; workspace skills override fixed ones), trial run and description steps.
- Output path: `<workspace>/.agents/skills/code-simplification/`.
- Fixed: unquoted colon in the generated SKILL.md description broke strict YAML frontmatter parsing.

**Affects:** all generated files.
**Migration:** existing, unregistered simplification skills → run the generator to **adopt** (keeps workspace principles, decision notation, report line; records provenance).
