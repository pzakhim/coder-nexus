# Checklist — database-migrations

Run this checklist alongside [../../core/checklist-common.md](../../core/checklist-common.md):

- [ ] All mandatory rules **M1–M14** are enforced (zero `"not adopted"` carve-outs)
- [ ] 3-Tier Environment Authority is explicit: (1) **Local / Disposable DB** = autonomous agent verification; (2) **Develop (`develop`)** = agent executes **only when explicitly requested by the user**; (3) **Staging & Production (`staging`, `production`)** = **strictly executed by DevOps** from the handoff packet, never by the agent
- [ ] Runner facts and commands include `cwd`, lockfile prefix, and explicit forbidden commands (`reset`, `db push`, `create_all`, `stamp`)
- [ ] Engine lock notes, `Expand → Backfill → Contract` phases, and batched/tenant-scoped data backfill rules match the workspace's database engine and version
- [ ] Disposable-DB verification gates (`V1`–`V8`) use binary **`PASS` / `FAIL`** flags (`BLOCKED` / `NOT_RUN` never count as `PASS`)
- [ ] DevOps Migration Handoff Packet includes: (1) Summary of Changes & Why (schema + data changes and reasons), and (2) Step-by-step Schema & Data Migration Runbook for `develop`, `staging`, and `production` (with zero secret values)
- [ ] Review findings use the unified **`BLOCKER` / `MAJOR` / `MINOR`** scale (`shared_contracts/flags_and_statuses.md`)
- [ ] Cohesive 3-file `references/` layout (`01-runner-targets-and-workflow.md`, `02-safe-schema-and-backfill-patterns.md`, `03-verification-states-and-handoff.md`)
