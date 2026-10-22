# Changelog — create-database-migrations-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.0.0 — 2026-10-22

First version.

- Base rules M1–M14 with reasons (from the erp-knowledge-platform `be-database-migration` practice, generalised): real runner and targets, authority, forbidden delivery commands, expand/backfill/contract, idempotent ALTERs, defaults and constraints on existing data, locks and volume, scope-aware backfills, disposable-DB verification, backup and recovery, states, handoff packet, schema vs business releases, sensitive data.
- Safe patterns for common changes; runners, commands and engine lock notes per stack.
- Mandatory: `SKILL.md`, runner & targets, designing, verification, applying & recovery. Suggested: handoff packet (mandatory without apply authority).
- Layout: always flat, backend only.
- Output path: `<workspace>/.agents/skills/database-migrations/`.

**Affects:** all generated files.
**Migration:** existing migration skills → run the generator to **adopt** (keeps runner facts, forbidden commands, states and packet format).
