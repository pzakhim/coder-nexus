# Changelog — create-code-simplification-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

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
