---
name: create-database-migrations-skill
description: Write a workspace's own database-migrations skill from the skill-factory knowledge base - how schema and data changes are designed, verified and delivered safely - the real migration runner and targets, authority to apply, expand/backfill/contract, idempotent ALTERs, defaults and constraints on existing data, locks and volume, scope-aware backfills, verification on a disposable database, backup and recovery, migration states and the DevOps handoff packet - for the backend of any stack (Alembic, Django, Prisma, TypeORM, golang-migrate, raw SQL runners). Use whenever the user wants to set up, standardize or update how the coder agent writes or ships migrations in a workspace, or says things like "tạo skill migration", "quy trình migrate DB", "thay đổi schema an toàn", even if they do not say "skill". Writes .agents/skills/database-migrations/, then trial-runs it on a real schema change.
argument-hint: "[migration tool] [database]"
---

# Create Database Migrations Skill

Goal: produce `<workspace>/.agents/skills/database-migrations/` — how the Code Writer designs, verifies and delivers schema/data changes in this workspace's backend, with its real runner, targets, authority and recovery rules. Backend only: in a fullstack repo the skill covers `<be_dir>`.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: `~/.claude/skill-factory/core/coder-skill-family.md` — clean-architecture decides where migrations live; secure-coding-standards covers sensitive data moved by a migration; this skill covers how a migration is designed, verified and delivered.

## Step 1 — Context Card (+ migration setup)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Runner | Alembic (`alembic.ini`, `versions/`), Django (`migrations/`), Prisma (`schema.prisma`, `migrations/`), TypeORM, golang-migrate, or a custom SQL runner (`schema/manifest.json`, a loader module) — read its code, do not assume |
| Commands | `Makefile` / scripts: migrate, status, validate, backup; which are safe and which reset or clone data |
| Targets | How the destination database is selected (env vars), local/disposable DB, DEV/STG/PROD, read-only sources that are not targets |
| Authority | Who may apply DDL to which target; DevOps ownership; "credentials do not grant authority" rules |
| Data scopes | Tenant/environment/owner columns that backfills must respect |
| Existing skill | `.agents/skills/*migration*` (e.g. `be-database-migration`) |
| Database engine & version | PostgreSQL/MySQL/SQLite version — decides lock behavior and online index support |

## Step 2 — Map the base rules

Read `references/base-rules.md`, `references/patterns.md`, `references/tooling-by-stack.md`. For each rule M1–M14: adopted, adapted, or "not adopted" with a reason. M1, M2, M3, M5, M9, M10 are never "not adopted".

## Step 3 — Propose

- **Runner and targets** on one page: commands with cwd, which are safe, which are forbidden for delivery (reset/sync/seed), how the target is identified without secrets.
- **Design rules** with the engine's real lock behavior and the safe patterns that apply.
- **Verification recipe** on a disposable database.
- **Delivery:** direct apply (who, where) vs handoff packet; states and evidence.

## Step 4 — Gate (user confirms)

One AskUserQuestion round where possible: (1) runner, commands and forbidden commands, (2) targets and authority, (3) verification recipe, (4) delivery path, states and recovery.

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed. Layout: always **flat** (`references/01–05`), scoped to the backend.

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | The never-list and the delivery path on one screen |
| `references/01-runner-and-targets.md` | `templates/01-runner-and-targets.md.tmpl` | **Mandatory** | Wrong runner or wrong target is the most expensive migration mistake |
| `references/02-designing-a-migration.md` | `templates/02-designing-a-migration.md.tmpl` | **Mandatory** | Expand/backfill/contract, locks and existing data decide whether production survives |
| `references/03-verification.md` | `templates/03-verification.md.tmpl` | **Mandatory** | Clean install + upgrade with data + rerun prove it before any shared target |
| `references/04-applying-and-recovery.md` | `templates/04-applying-and-recovery.md.tmpl` | **Mandatory** | Authority, backup, order, postchecks, states |
| `references/05-handoff-packet.md` | `templates/05-handoff-packet.md.tmpl` | Suggested (Mandatory when the coder may not apply to shared targets) | What DevOps needs to apply it safely |

Writing rules: keep each template's purpose, give every rule its reason, real commands with cwd, never a secret value (reference the configuration instead), replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Database migrations
   Schema and data changes follow `.agents/skills/database-migrations/SKILL.md`.
   ```
2. Offer to link it from the coder and reviewer role files (P3).

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Task ideas:

- Add a NOT NULL column to a large, busy table.
- Rename a column used by the API and a worker.
- Add a unique constraint where duplicates may already exist; backfill a column per tenant.
- "Apply it to staging" without authority — does the agent produce a handoff packet instead?

Compare: expand/backfill/contract used, lock impact considered, verification on a disposable DB, forbidden commands avoided, correct state reported.

## Step 8 — Description

Per the authoring guide: workspace name; situations (new table/column/index, constraint, backfill, rename, "migrate the DB", deploy a schema change); team trigger words. Should not trigger for business-content releases or seed data edits.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations, rules adapted/not adopted, trial results.

## Update mode

Existing `.agents/skills/database-migrations/` or a workspace migration skill: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep runner facts, forbidden commands, states and packet format verbatim).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — M1–M14 with reasons
- `references/patterns.md` — safe patterns for common changes
- `references/tooling-by-stack.md` — runners, commands and engine lock notes
- `templates/` — `SKILL.md.tmpl`, `01–05` (suggested shapes)
- `checklist.md` — topic checks
