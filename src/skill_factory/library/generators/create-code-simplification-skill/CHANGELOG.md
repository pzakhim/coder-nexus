# Changelog — create-code-simplification-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## Unreleased

- Fixed: unquoted colon in the generated SKILL.md description broke strict YAML frontmatter parsing. (patch)
- Changed: Step 0 — generators now run in workspaces also synced by Coder Nexus; they never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files, and the workspace skill overrides the fixed one. Generator distributed with `skill-factory get`. (patch)

## 1.0.0 — 2026-10-22

First version.

- Base rules S1–S13 with reasons and severities (from Coder Nexus `plugins/core/skills/code-simplification`, `plugins/ponytail` and the erp-knowledge-platform simplification standard, generalised).
- Smell → technique catalog (delete, stdlib, native, yagni, shrink, flatten, rename, inline) and stack notes.
- Mandatory: `SKILL.md`, when & scope, behavior safety, smell catalog, stop criteria. Suggested: report.
- Layouts: flat `references/01–05`; branched `shared/01, 02, 04, 05`, `be/03`, `fe/03`.
- Step 0 (manual workspaces only), trial run and description steps.
- Output path: `<workspace>/.agents/skills/code-simplification/`.

**Affects:** all generated files.
**Migration:** existing, unregistered simplification skills → run the generator to **adopt** (keeps workspace principles, decision notation, report line; records provenance).
