# Changelog — create-clean-code-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`).

## 1.0.0 — 2026-10-22

First version.

- Base rules C1–C14 with reasons and default severities (from Coder Nexus `plugins/core/skills/clean-code` and the erp-knowledge-platform clean-code standard, generalised).
- Naming and self-check references per stack (Python, TypeScript/React/Next.js, NestJS, Flutter/Dart, Go).
- Mandatory: `SKILL.md`, naming, size & structure, **splitting (02b, clean-code's half of `core/splitting-protocol.md`, with a fallback when the workspace has no clean-architecture skill)**, errors & logging, self-check. Suggested: types/constants/comments, review severity.
- Thresholds are owned here (02); clean-architecture links to them.
- Layouts: flat `references/01–06`; branched `be/01–05`, `fe/01–05`, `shared/06`.
- Includes Step 0 (manual workspaces only), trial run and description steps.
- Output path: `<workspace>/.agents/skills/clean-code/`.

**Affects:** all generated files.
**Migration:** existing, unregistered `clean-code` skills → run the generator to **adopt** (keeps workspace rule IDs, severities and checks; records provenance).
