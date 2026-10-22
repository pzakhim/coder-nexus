# Changelog — create-domain-knowledge-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.0.0 — 2026-10-22

First version.

- Base rules DK1–DK8 with reasons: one term one meaning, entity cards with lifecycles, roles × scopes × actions, business-rule catalog with locations, labelled facts, linked volatile facts, upkeep, no personal data.
- Domain-neutral detection of entities, statuses, transitions, roles, data scopes, user-facing labels and documents; tracker history optional.
- Mandatory: `SKILL.md`, glossary, entities and lifecycles, roles and scopes, business rules, sources and upkeep.
- Layout: flat; large domains split per module.
- Output path: `<workspace>/.agents/skills/domain-knowledge/`.

**Affects:** all generated files.
**Migration:** existing glossary or domain docs → run the generator to **adopt** (keeps terms, IDs and confirmed rules).
