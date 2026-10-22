# Changelog — create-requirements-specification-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.0.0 — 2026-10-22

First version.

- Base rules RS1–RS9 with reasons: source map, question bank per grill-me dimension, mandatory edge cases, observable AC, domain terms only, ready checklist per job type, bug specs, language, fixed process unchanged.
- Generic edge-case catalog (keep only what the workspace has); detection of past specs, ticket and AC style.
- Mandatory: `SKILL.md`, sources and intake, question bank, mandatory edge cases, writing BR/AC/bugs, ready checklist.
- Layout: flat.
- Output path: `<workspace>/.agents/skills/requirements-specification/`.

**Affects:** all generated files.
**Migration:** existing spec guides → run the generator to **adopt** (keeps AC style, IDs and checklists).
