# Changelog — create-unit-testing-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## Unreleased

- Changed: Step 0 — generators now run in workspaces also synced by Coder Nexus; they never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files, and the workspace skill overrides the fixed one. Generator distributed with `skill-factory get`. (patch)

## 2.0.0 — 2026-10-22

- Renamed: generator `create-unit-test-skill` → `create-unit-testing-skill`; generated skill `unit-test` → `unit-testing` (output `<workspace>/.agents/skills/unit-testing/`). (major)

**Affects:** the skill folder name and its `SKILL.md` `name`.
**Migration:** `git mv .agents/skills/unit-test .agents/skills/unit-testing`, set `name: unit-testing`, then update inbound links (P3: list them, ask, edit only link lines). No rule change. No workspace was registered with 1.0.0.

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
