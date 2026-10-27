# Changelog — create-database-migrations-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `../../core/sync-protocol.md`). Bump rules: `../../core/versioning.md`.

## 1.1.0 — 2026-10-25

- Standardized on the 3-tier Environment Authority model (`Local/Disposable` = autonomous agent verification; `Develop` = agent execution allowed **only on explicit user request**; `Staging & Production` = strictly executed by DevOps via the Migration Handoff Packet).
- Upgraded the mandatory Migration Handoff Packet (`M12`) to require: (1) a table of all schema/data changes and their business/technical reasons, and (2) a step-by-step DevOps execution runbook for migrating both schema and data across `develop`, `staging`, and `production`.
- Consolidated `templates/` into `templates/SKILL.md.tmpl` and 3 cohesive templates under `templates/references/` (`01-runner-targets-and-workflow.md.tmpl`, `02-safe-schema-and-backfill-patterns.md.tmpl`, `03-verification-states-and-handoff.md.tmpl`) with binary `PASS` / `FAIL` CLI gates, unified `BLOCKER` / `MAJOR` / `MINOR` review grading, and `<!-- {{profile_references}} -->`.
- Enforced mandatory compliance for all `M1`–`M14` rules (removing `"not adopted"` carve-outs and replacing `{{be_dir}}` with stack-agnostic `{{target_dir}}`).

**Affects:** `SKILL.md`, `references/01..03.md`.

## 1.0.0 — 2026-10-22

First version.

- Base rules M1–M14 with reasons: real runner and targets, authority, forbidden delivery commands, expand/backfill/contract, idempotent ALTERs, defaults and constraints on existing data, locks and volume, scope-aware backfills, disposable-DB verification, backup and recovery, states, handoff packet, schema vs business releases, sensitive data.
- Safe patterns for common changes; runners, commands and engine lock notes per stack.
- Output path: `<workspace>/.agents/skills/database-migrations/`.
