# Changelog — create-clean-architecture-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace. Sync agents apply entries newer than the version recorded for a workspace (see `~/.claude/skill-factory/core/sync-protocol.md`).

## 1.1.0 — 2026-10-24

- Consolidated generated `references/` from 7–10 fragmented files into 3 cohesive topic files: `01-layout-and-layer-roles.md`, `02-dependencies-di-and-contracts.md`, and `03-adding-splitting-and-review.md`.
- Standardized `SKILL.md` into (1) Deterministic Tool & Boundary Gates (`PASS` / `FAIL`) and (2) Mandatory Core Architecture Principles (`A1`–`A10`), with unified `BLOCKER` / `MAJOR` / `MINOR` review severities (`shared_contracts/flags_and_statuses.md`).
- Replaced stack-specific generator files (`backend-rules.md`, `frontend-rules.md`, `principles.md`, `stacks/*`, `templates/be/*`, `templates/fe/*`) with stack-agnostic `references/base-rules.md`, `references/discovery-and-structure.md`, and `templates/references/01..03.md.tmpl`.
- Added `<!-- {{profile_references}} -->` marker support for `profiles/{imespro,external-structured,external-standard}/`.

**Affects:** `SKILL.md`, `references/01-layout-and-layer-roles.md`, `references/02-dependencies-di-and-contracts.md`, `references/03-adding-splitting-and-review.md`.
**Migration:** merge `01`+`02` into `01-layout-and-layer-roles.md`, `05`+`08..10` into `02-dependencies-di-and-contracts.md`, and `03`+`04`+`06`+`07` into `03-adding-splitting-and-review.md`; update `SKILL.md` to use `PASS`/`FAIL` gates and `BLOCKER`/`MAJOR`/`MINOR` review severities.

## 1.0.0 — 2026-10-22

First version inside the skill factory.

- Layouts: flat (single stack) and branched `shared/ + be/ + fe/` (fullstack).
- Knowledge: principles, backend rules B1–B13, frontend rules F1–F14, splitting protocol, presets for FastAPI, NestJS, Next.js, Flutter.
- Existing-project lessons P1–P5 (now in `core/existing-project.md`).
- Output path: `<workspace>/.agents/skills/clean-architecture/`.
- Step 0: never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name. Distributed with `skill-factory get`.
- Templates are **suggested shapes**; only the four slices 01–04 (per branch) and `SKILL.md` are **Mandatory**. Output table gains Kind + Why columns.
- Every template starts with a `<!-- GEN: Why … -->` note; rules are written with their reason, hard "never/always" only for absolute rules (`core/authoring-guide.md`).
- New Step 7 **Trial run**: 2–3 real workspace tasks planned with vs without the skill by read-only subagents; improve until the skill helps (`core/trial-run.md`).
- New Step 8 **Description**: workspace name, concrete situations, team trigger words; checked against the trial prompts.
- Step 9 now records provenance and reports deviations from the suggested shape.
- Generator description rewritten to trigger on more phrasings (incl. Vietnamese).
- Moved: `splitting-protocol.md` to `core/` (shared with create-clean-code-skill); it now states which skill owns each step, forbids re-export shims when moving code, and adds a fallback for workspaces without clean-architecture.
- Changed: template 04 no longer repeats thresholds; it links the workspace's clean-code skill (defaults only when none exists).

**Affects:** all generated files.
**Migration:** workspaces generated before the factory existed are not registered → run the generator in the workspace to **adopt** (records provenance, refreshes to this frame, keeps project rules and custom blocks).
