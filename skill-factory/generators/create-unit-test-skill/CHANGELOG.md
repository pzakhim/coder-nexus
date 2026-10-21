# Changelog — create-unit-test-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.0.0 — 2026-10-22

First version.

- Base rules U1–U14 with reasons and default severities (from Coder Nexus `plugins/packs/{backend,flutter}/skills/unit-test` and the erp-knowledge-platform unit-test practice, generalised).
- Required cases per layer (domain, use case, repository/mapper, data source, controller/router, FE utils/hooks/components, Flutter cubit) and tooling per stack.
- Mandatory: `SKILL.md`, what to test, location & naming, doubles & fixtures, running & evidence. Suggested: test quality, test boundaries.
- Layouts: flat `references/01–06`; branched `be/01–05`, `fe/01–05`, `shared/06`.
- Step 0 (manual workspaces only), trial run and description steps.
- Output path: `<workspace>/.agents/skills/unit-test/`.

**Affects:** all generated files.
**Migration:** existing, unregistered test skills → run the generator to **adopt** (keeps fixtures conventions, evidence locations and check ownership; records provenance).
