# Changelog — create-clean-code-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## Unreleased

- Added: C15 no meaningless module-level or global variables — only shared constants read by two or more functions and the settings object; no mutable global state; a one-function constant lives in that function. Default P1 when mutable global state is added, else P2 → `references/02-size-and-structure.md` (`be/02-…`, `fe/02-…`) "Module-level and global variables". (minor)
- Added: C16 helper locality — private in its file until a second file needs it, then moved to the owning module and named for what it does; no `utils`/`helpers`/`common`/`misc`. Default P1 when internals get exposed, else P2 → `02` "Helper locality". (minor)
- Added: C17 export surface — entry files export only symbols other modules import; no wildcard export; no internals. Default P1 when internals are exposed, else P2 → `02` "Export surface". (minor)
- Changed: C15–C17 join the never-"not adopted" set; generated `SKILL.md` rule table gains three rows. (minor)
- Added: `05-self-check` "Structure greps" row and C15–C17 rows in `references/self-check-by-stack.md`; Step 1 detection row for module-level state, generic helper files and entry files; checklist items. (patch)
- Added: generator `references/sources.md` (external sources and ideas not adopted). (patch)

**Affects:** `SKILL.md`, `references/02-size-and-structure.md` (`be/02-…`, `fe/02-…`), `references/05-self-check.md` (`be/05-…`, `fe/05-…`).
**Migration:** find the workspace's private convention, package entry files, wildcard exports, mutable module-level state and generic `utils`/`helpers` files. Add rows C15–C17 to the `SKILL.md` rule table, add the three sections to 02 with the workspace's real conventions, add the structure-grep row to 05. List existing violations as drift; fix them only inside tasks that touch those files. Existing rule IDs and sections keep their names; non-breaking.

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
