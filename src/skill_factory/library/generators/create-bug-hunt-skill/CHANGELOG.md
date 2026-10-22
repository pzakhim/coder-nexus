# Changelog — create-bug-hunt-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## Unreleased

- Fixed: unquoted colon in the generator description broke strict YAML frontmatter parsing. (patch)
- Changed: Step 0 — generators now run in workspaces also synced by Coder Nexus; they never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files, and the workspace skill overrides the fixed one. Generator distributed with `skill-factory get`. (patch)

## 1.0.0 — 2026-10-22

First version.

- Base rules H1–H14 with reasons (from Coder Nexus `plugins/core/skills/bug-hunt` and the erp-knowledge-platform bug-hunt practice, generalised).
- Seven defect dimensions with prompts; stack bug patterns and a method to derive project patterns from risk areas.
- Mandatory: `SKILL.md`, scope & candidates, verify, effort/severity/report, bug patterns. Suggested: verdict & roles.
- Layouts: flat `references/01–05`; branched `shared/01–04`, `be/05`, `fe/05`.
- Step 0 (manual workspaces only), trial run and description steps.
- Output path: `<workspace>/.agents/skills/bug-hunt/`.

**Affects:** all generated files.
**Migration:** existing, unregistered bug-hunt skills → run the generator to **adopt** (keeps vocabulary, report location and project pattern files; records provenance).
