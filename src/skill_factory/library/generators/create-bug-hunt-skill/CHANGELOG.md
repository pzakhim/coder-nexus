# Changelog — create-bug-hunt-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.1.0 — 2026-10-23

- Decoupled base inputs from core `plugins/core/skills/bug-hunt`, relying directly on self-contained `references/base-rules.md`.

**Affects:** generator base input resolution.
**Migration:** none required for existing workspace skills.

## 1.0.0 — 2026-10-22

First version.

- Base rules H1–H14 with reasons (from Coder Nexus `plugins/core/skills/bug-hunt` and the erp-knowledge-platform bug-hunt practice, generalised).
- Seven defect dimensions with prompts; stack bug patterns and a method to derive project patterns from risk areas.
- Mandatory: `SKILL.md`, scope & candidates, verify, effort/severity/report, bug patterns. Suggested: verdict & roles.
- Layouts: flat `references/01–05`; branched `shared/01–04`, `be/05`, `fe/05`.
- Step 0 (never write into Coder Nexus-managed files; workspace skills override fixed ones), trial run and description steps.
- Output path: `<workspace>/.agents/skills/bug-hunt/`.
- Fixed: unquoted colon in the generator description broke strict YAML frontmatter parsing.

**Affects:** all generated files.
**Migration:** existing, unregistered bug-hunt skills → run the generator to **adopt** (keeps vocabulary, report location and project pattern files; records provenance).
