---
name: create-database-migrations-skill
description: "Generate a workspace's `database-migrations` skill from the skill-factory knowledge base — enforcing the 3-tier environment authority model (Local/Disposable = autonomous; Develop = only on explicit user request; Staging & Production = strictly DevOps via handoff packet), expand/backfill/contract rollout, lock-aware DDL, scoped/batched data backfills, disposable-DB verification (`PASS` / `FAIL`), and the DevOps Migration Handoff Packet (changes + reasons + `develop`/`staging`/`production` schema & data runbook) across any migration runner (Alembic, Django, Prisma, TypeORM, golang-migrate, Drift, SQL runners)."
argument-hint: "[migration tool] [database]"
---

# Create Database Migrations Skill

Goal: produce `<workspace>/.agents/skills/database-migrations/` — governing how the Code Writer, Reviewer, and Test Runner design, verify, and hand off schema and data migrations in this workspace (`{{target_dir}}`).

User input: `$ARGUMENTS`

Follow [../../core/workflow.md](../../core/workflow.md), starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed pack skill of the same name). Ownership: [../../core/coder-skill-family.md](../../core/coder-skill-family.md) — `clean-architecture` decides where migrations live; `secure-coding-standards` covers sensitive data moved by a migration; this skill covers how a migration is designed, verified, and handed off to DevOps.

## Step 1 — Context Card (+ Migration Setup)

Run the core Context Card ([../../core/detect-stack.md](../../core/detect-stack.md)) and P1–P2 ([../../core/existing-project.md](../../core/existing-project.md)). Additionally collect:

| Field | Where to Inspect |
|---|---|
| **Runner** | Alembic (`alembic.ini`, `versions/`), Django (`migrations/`), Prisma (`schema.prisma`, `migrations/`), TypeORM, golang-migrate, Drift, or custom SQL runner — read its config/code, never assume |
| **Commands** | `Makefile` / `pyproject.toml` / `package.json`: create, upgrade, downgrade, status/check, offline `--sql`, backup; which commands are safe vs. forbidden (`reset`, `db push`, `create_all`, `seed`) |
| **Targets & 3-Tier Authority** | (1) **Local / Disposable DB**: agent runs autonomously for verification; (2) **Develop (`develop`)**: agent runs **only when the user explicitly requests/approves it**; (3) **Staging & Production (`staging`, `production`)**: **strictly executed by DevOps** from the handoff packet, never by the agent |
| **Data Scopes** | Tenant/environment/organization/owner columns that data backfills must filter by |
| **Database Engine & Version** | PostgreSQL / MySQL / SQLite version — determines lock behavior, `CONCURRENTLY` index builds, and `NOT VALID` constraints |

## Step 2 — Enforce Base Rules (`M1`–`M14`)

Read [references/base-rules.md](references/base-rules.md), [references/patterns.md](references/patterns.md), and [references/tooling-by-stack.md](references/tooling-by-stack.md). All rules **M1–M14** are **mandatory compliance** — translate each rule into the workspace's exact migration runner syntax, commands, and target environments.

## Step 3 — Propose

Present on one screen:
- **Runner, Commands & 3-Tier Target Authority**: exact commands with `cwd`, forbidden commands, and the 3-tier authority boundary (`Local/Disposable` vs `Develop on explicit user request` vs `Staging/Production by DevOps`).
- **Safe Schema & Data Backfill Rules**: engine lock behavior, `Expand → Backfill → Contract`, and batched/scoped backfill patterns.
- **Disposable-DB Verification Gates (`PASS` / `FAIL`)**: clean install, upgrade with seeded data, backfill invariants, downgrade/upgrade reversibility, and automated migration tests.
- **DevOps Migration Handoff Packet**: mandatory summary of changes + reasons + step-by-step schema & data migration runbook for `develop`, `staging`, and `production`.

## Step 4 — Gate (User Confirms)

Confirm in one round: (1) runner, commands, and forbidden commands, (2) 3-tier target authority (`develop` on user request vs `staging`/`production` via DevOps handoff), (3) disposable-DB verification recipe, and (4) DevOps handoff packet structure.

## Step 5 — Author (Cohesive 3-File `references/` Layout)

Read [../../core/authoring-guide.md](../../core/authoring-guide.md). Generate a concise `SKILL.md` (< 120 lines) and 3 cohesive reference files under `references/`:

| Output File | Template | Kind | Purpose |
|---|---|---|---|
| `SKILL.md` | [templates/SKILL.md.tmpl](templates/SKILL.md.tmpl) | **Mandatory** | 3-tier environment authority table, Never-list, 5-step workflow, `M1`–`M14` index, `PASS` / `FAIL` CLI gates, and `<!-- {{profile_references}} -->` |
| `references/01-runner-targets-and-workflow.md` | [templates/references/01-runner-targets-and-workflow.md.tmpl](templates/references/01-runner-targets-and-workflow.md.tmpl) | **Mandatory** | Runner setup, autogenerate hand-review, 3-tier target authority (`Local/Disposable`, `Develop` on user request, `Staging/Production` by DevOps), and revision rules (`M1`–`M3`, `M5`, `M13`) |
| `references/02-safe-schema-and-backfill-patterns.md` | [templates/references/02-safe-schema-and-backfill-patterns.md.tmpl](templates/references/02-safe-schema-and-backfill-patterns.md.tmpl) | **Mandatory** | `Expand → Backfill → Contract` lifecycle, lock-aware DDL, online index/constraint patterns, and batched/scoped data backfills (`M4`, `M6`–`M8`, `M14`) |
| `references/03-verification-states-and-handoff.md` | [templates/references/03-verification-states-and-handoff.md.tmpl](templates/references/03-verification-states-and-handoff.md.tmpl) | **Mandatory** | Disposable-DB verification (`PASS` / `FAIL`), migration states, DevOps Handoff Packet (Changes & Reasons + `develop`/`staging`/`production` schema & data runbook), and `BLOCKER` / `MAJOR` / `MINOR` review rubric (`M9`–`M12`) |

## Step 6 — Wire

Add a pointer in `CLAUDE.md` / `AGENTS.md` (unless already present):
```markdown
## Database migrations
Schema and data changes follow `.agents/skills/database-migrations/SKILL.md`.
```

## Step 7 — Trial Run

Follow [../../core/trial-run.md](../../core/trial-run.md). Test prompts:
- Add a `NOT NULL` column to a populated multi-tenant table and backfill existing rows.
- User asks: *"Migrate this schema and data change to `develop`, and prepare the handoff for `staging` and `production`"* — verify that the agent checks explicit user authorization for `develop`, never runs against `staging`/`production`, and produces the complete DevOps handoff packet with changes, reasons, and per-environment commands.

## Step 8 — Description & Step 9 — Verify, Record & Report

Verify against [checklist.md](checklist.md) and [../../core/checklist-common.md](../../core/checklist-common.md), then record provenance ([../../core/provenance.md](../../core/provenance.md)).

## Resources

- [references/base-rules.md](references/base-rules.md) — Mandatory rules `M1`–`M14`
- [references/patterns.md](references/patterns.md) — Safe patterns for common schema & data changes
- [references/tooling-by-stack.md](references/tooling-by-stack.md) — Runners, commands, and engine lock notes
- [templates/SKILL.md.tmpl](templates/SKILL.md.tmpl) & `templates/references/01..03.md.tmpl`
- [checklist.md](checklist.md) — Topic verification checklist
