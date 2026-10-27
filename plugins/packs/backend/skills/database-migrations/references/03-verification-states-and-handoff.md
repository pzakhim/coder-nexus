# 03 — Disposable-DB Verification (`V1`–`V8`), Migration States, and DevOps Handoff Packet

> Topic: Disposable-DB verification checks (`V1`–`V8` + `pytest-alembic`), 3-tier authority (`develop` on user request vs `staging`/`production` by DevOps), migration states, the DevOps Migration Handoff Packet (`templates/migration-handoff.md.tpl`), and `BLOCKER` / `MAJOR` / `MINOR` review grading.

---

## 1. Disposable-DB Verification Recipe (`V1`–`V8` + `pytest-alembic`)

Execute all 8 checks against a **local/disposable database** (`localhost`, `db-test`, or `app_migration_check` on the same PostgreSQL major version as production) before marking a task done or migrating `develop`. Every check is binary (**`PASS` / `FAIL`**; an unreachable DB is **`BLOCKED`**, never skipped):

| # | Check | Command / Query (`cwd: backend root`) | Pass Criteria (`PASS` / `FAIL`) |
|---|---|---|---|
| **V1** | **Clean Install from Zero** | Fresh empty DB → `uv run alembic upgrade head` | `PASS` when entire chain applies cleanly (`exit 0`, last line names new revision) |
| **V2** | **Single Head & Zero Drift** | `uv run alembic heads && uv run alembic check` | `PASS` when 1 head exists and `No new upgrade operations detected.` |
| **V3** | **Upgrade Over Seeded Data** | `uv run alembic downgrade -1` → seed multi-tenant rows, `NULL`s, & edge values → `uv run alembic upgrade head` | `PASS` when upgrade succeeds on realistic existing rows |
| **V4** | **Data Backfill Invariants (`B7`)** | Run invariant SQL (`SELECT count(*) FROM <table> WHERE <unmigrated> = 0`) & cross-tenant isolation check | `PASS` when unmigrated count is `0` and other tenants' rows are unchanged |
| **V5** | **Reversibility (`downgrade` / `upgrade`)** | `uv run alembic downgrade -1 && uv run alembic upgrade head` | `PASS` when both directions exit `0` |
| **V6** | **Valid Indexes Check** | `SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;` | `PASS` when `0` rows returned (no `INVALID` concurrent index) |
| **V7** | **Offline SQL & Lock Review** | `uv run alembic upgrade <prev>:<new> --sql` | `PASS` when SQL matches safe patterns in [02](02-safe-schema-changes-and-backfills.md) and includes `lock_timeout` |
| **V8** | **Automated Migration & API Tests** | `uv run pytest --test-alembic -q && uv run pytest tests/<affected> -q` | `PASS` when `pytest-alembic` and affected service/API tests exit `0` |

For standalone large backfill scripts: run `--dry-run`, then run the batch backfill, then run it a second time (must report `0` rows updated to prove idempotency), and verify **V4**.

---

## 2. 3-Tier Environment Execution & Canonical Migration States

| Environment | Execution Authority | Mandatory Protocol |
|---|---|---|
| **Local / Disposable DB** | **Backend Agent** | Runs `V1`–`V8` autonomously; sets state to `PENDING` → `READY_FOR_HANDOFF`. |
| **Develop (`develop`)** | **Backend Agent (ONLY when explicitly requested by User)** _or_ **DevOps** | 1. Agent **never** migrates `develop` automatically.<br>2. When the user explicitly requests migrating `develop`, the agent verifies `V1`–`V8` passed on disposable DB first, generates `migration-handoff.md`, runs the upgrade + data backfill + postchecks on `develop`, and records `VERIFIED_IN_TARGET` (or `FAILED` with recovery details). |
| **Staging & Production (`staging`, `production`)** | **Strictly DevOps** (**NEVER the Backend Agent**) | Backend Agent **never** runs commands against `staging` or `production`. The agent generates `migration-handoff.md` (`READY_FOR_HANDOFF`) so the user can hand it over to DevOps. |

### Migration States (Recorded Alongside Core Gate Statuses)
- **`NOT_REQUIRED`**: Task touches no schema or stored data (`alembic check` clean).
- **`PENDING`**: Revision written and `V1`–`V8` verified `PASS` on disposable DB; not applied to shared targets.
- **`READY_FOR_HANDOFF`**: `PENDING` + `migration-handoff.md` is complete with zero placeholders.
- **`APPLIED_UNVERIFIED`**: Applied to a named target (`develop` / `staging` / `production`), postchecks not yet run.
- **`VERIFIED_IN_TARGET`**: Applied + data backfill completed + all postchecks verified `PASS` on the named target.
- **`FAILED`**: Migration or postcheck failed; records the failing step, error output, and recovery action taken.

---

## 3. Mandatory DevOps Migration Handoff Packet (`templates/migration-handoff.md.tpl`)

Whenever a migration is authored (and whenever migrating `develop` or handing off to DevOps for `staging` and `production`), write `evidence/<phase-id>/<REVIEW_REVISION>/migration-handoff.md` from [templates/migration-handoff.md.tpl](../templates/migration-handoff.md.tpl). It **must** contain:

1. **Summary of Changes & Why (Những thay đổi và Lý do thay đổi)**:
   - Every table, column, index, constraint, and data backfill item, linked to `AC-NN` / `D-NN`, and the exact business/technical reason why the change was made.
2. **Order & Application/Worker Deployment Sequencing**:
   - Exact sequence between Alembic schema revisions, API/worker code deployments, and data backfill scripts (`Expand → Deploy Code → Data Backfill → Cutover Code → Contract`).
3. **How to Migrate Schema & Data on `develop`, `staging`, and `production` (Step-by-Step Runbook for DevOps)**:
   - **Step 1 — Pre-Checks & Backup**: Verify `alembic current`, check active locks, and take a database backup/snapshot (`pg_dump` or managed snapshot) before touching `develop`, `staging`, or `production`.
   - **Step 2 — Schema Migration Command**: Exact `uv run alembic upgrade <to_revision>` command + attached `--sql` output (`V7`).
   - **Step 3 — Data Migration / Backfill Command**: How to migrate existing data safely on `develop`, `staging`, and `production`:
     - Run `--dry-run` first to inspect row counts per tenant/scope.
     - Run the batched command (`--batch-size 1000 --sleep-ms 50`) or data revision, and how to resume from the last processed ID if interrupted.
   - **Step 4 — Post-Checks & Invariants**: Exact SQL queries (`alembic current`, `NOT indisvalid` index check, backfill invariant count `= 0`) and API smoke checks to confirm `VERIFIED_IN_TARGET`.
   - **Step 5 — Rollback & Recovery**: What `uv run alembic downgrade <from_revision>` restores vs. what requires restoring from the Step 1 backup snapshot.

---

## 4. Review Severity Rubric (`BLOCKER` / `MAJOR` / `MINOR`)

| Severity | Alembic & PostgreSQL Migration Findings |
|---|---|
| **`BLOCKER`** | • Agent running migrations on `staging` or `production`, or on `develop` without an explicit user command<br>• Using `Base.metadata.create_all()`, `alembic stamp`, or manual SQL outside revisions<br>• Editing an already-applied revision, leaving multiple Alembic heads (`alembic heads > 1`), or importing live `app.models` / `app.services` inside a revision (**A3, A4, A5**)<br>• Violating `Expand → Backfill → Contract` (dropping/renaming/changing column type while running code still reads it) or creating an index without `postgresql_concurrently=True` inside `autocommit_block()` on a populated table<br>• Unscoped or unbatched data backfill, string-interpolated SQL, or secret/PII leaked in revisions or `migration-handoff.md` (**A8, A9, B1–B4**)<br>• Missing disposable-DB verification (`V1`–`V8`) or missing `migration-handoff.md` |
| **`MAJOR`** | • Missing `SET LOCAL lock_timeout` on DDL touching existing tables (**A7**)<br>• Missing or no-op `downgrade()` for a schema change, or missing irreversible-data warning & backup recovery instructions (**A6**)<br>• `migration-handoff.md` missing the **Summary of Changes & Why** table or missing the **Schema & Data Migration Runbook for `develop`, `staging`, and `production`** |
| **`MINOR`** | • Non-imperative revision message slug (**A2**) or minor formatting gap in `migration-handoff.md` |
