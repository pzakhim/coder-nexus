# Base rules (generic, every workspace)

Generalised from a real workspace's migration practice. Each rule goes into the generated skill with the workspace's runner, commands and targets **and its reason**, or is marked "not adopted" with a reason.

| # | Rule | Why | Goes into |
|---|---|---|---|
| M1 | **Use the real runner; know the target.** Read the runner's code/config before choosing commands; never invent a new migration framework. Record the target's identity (host/database, environment) without secrets before touching it. | Wrong runner or wrong database is the most expensive migration mistake. | 01 |
| M2 | **Authority is explicit.** Credentials or app roles do not grant DDL authority. Apply only to targets the user authorised; otherwise hand off. | Having access is not having permission. | 04 |
| M3 | **Never deliver through reset/sync/seed tools.** Commands that recreate, clone or reset data are not migrations. | They can wipe or overwrite real business data. | 01, SKILL |
| M4 | **Expand → backfill → contract.** Add compatible structure first, move data, switch code, remove old structure in a later step; order the rollout with the API and workers. | Old and new code run side by side during deploys. | 02 |
| M5 | **Idempotent and immutable.** Existing tables need `ALTER`, not just `CREATE IF NOT EXISTS`; guard statements so a rerun is safe; never edit a migration that has been deployed — add a new one. | Runners replay or partially fail; edited history diverges between environments. | 02 |
| M6 | **Respect existing data.** Defaults/nullability for rows that already exist; check data before adding unique/FK/check constraints (add as not-validated, fix, then validate where the engine supports it). | A constraint that existing rows violate fails the deploy or locks the table. | 02 |
| M7 | **Mind locks and volume.** Estimate rows; avoid long exclusive locks on hot tables; online/concurrent index builds (outside transactions); batch large backfills. | A 30-second lock on a busy table is an outage. | 02 |
| M8 | **Scope-aware, parameterised data changes.** Backfills respect tenant/environment/owner scopes; values are bind parameters, not string-built SQL. | A backfill without its scope rewrites everyone's data. | 02 |
| M9 | **Verify on a disposable database.** Clean install, upgrade from the previous schema **with data**, rerun, index validity, and the affected API/worker behavior — before any shared target. "Validate" commands that roll back are not complete dry runs. | Only a real upgrade with data shows what production will do. | 03 |
| M10 | **Backup and recovery before applying.** Define recovery explicitly; a backup listing is not a restore rehearsal; rolling back code does not roll back data. | When it fails, the recovery plan is the only thing that matters. | 04 |
| M11 | **States and evidence.** Report `NOT_REQUIRED` (reason), `PENDING`, `READY_FOR_HANDOFF`, `APPLIED_UNVERIFIED`, `VERIFIED_IN_TARGET`, `FAILED` with commands, target and revision. Startup auto-migration or a migrations table row alone is not proof. | "Migrated" without evidence hides partial failures. | 04 |
| M12 | **Handoff packet when not authorised.** Owner, target identity, revision, exact files/order/hashes, commands with cwd, secret *references* (never values), prerequisites, backup/recovery, lock/backfill impact, app/worker sequencing, postchecks. Preparing it is not sending it; send only with the user's authorisation. | DevOps can apply safely only what is fully described. | 05 |
| M13 | **Schema migrations are infrastructure**, separate from business-content releases or seed data edits. | Mixing them couples deploys with content approvals. | 01 |
| M14 | **Sensitive data.** No secrets in migration files; migrations that copy, transform or expose personal data follow secure-coding-standards and are flagged for review. | Migrations run with wide privileges and are easy to overlook. | 02, SKILL |

**Never "not adopted":** M1, M2, M3, M5, M9, M10.
