# Migration Handoff Packet — {{WORK_ITEM}} ({{PHASE_ID}})

> **Migration state:** `{{MIGRATION_STATE}}` <!-- PENDING | READY_FOR_HANDOFF | VERIFIED_IN_TARGET -->
> **Git revision:** `{{REVIEW_REVISION}}`
> **Alembic revisions:** `{{FROM_REVISION}}` → `{{TO_REVISION}}`
> **Rollout step type:** `{{STEP_TYPE}}` <!-- expand | backfill | contract | additive-only -->
> **Execution authority:** `develop` = User-authorized Agent or DevOps · `staging` & `production` = **Strictly DevOps (never Backend Agent)**
> **Prepared by / at:** Code Writer, `{{PREPARED_AT}}`

*Zero secret values appear in this document. Database credentials are referenced strictly via `DATABASE_URL` in the target environment.*

---

## 1. Summary of Changes & Why (Những thay đổi và Lý do thay đổi)

| # | Change Type (`Schema DDL` \| `Index/Constraint` \| `Data Backfill`) | Object / Table & Column | Revision / Script | Linked Spec (`AC-NN` / `D-NN`) | Why This Change Is Required (Lý do nghiệp vụ & kỹ thuật) |
|---|---|---|---|---|---|
| 1 | `{{CHANGE_TYPE}}` | `{{TABLE_AND_COLUMN}}` | `{{REVISION_OR_SCRIPT}}` | `{{SPEC_REF}}` | `{{CHANGE_REASON}}` |
{{CHANGE_SUMMARY_ROWS}}

---

## 2. Target Environments & Authority Matrix

| Environment | Host / Target Label (no secrets) | Who Executes? | Current Revision Before Run | Target Revision |
|---|---|---|---|---|
| **Develop (`develop`)** | `{{DEVELOP_HOST_LABEL}}` | DevOps (or Backend Agent **only when explicitly requested by User**) | `{{FROM_REVISION}}` | `{{TO_REVISION}}` |
| **Staging (`staging`)** | `{{STAGING_HOST_LABEL}}` | **DevOps only** | *(Operator checks via `alembic current`)* | `{{TO_REVISION}}` |
| **Production (`production`)** | `{{PRODUCTION_HOST_LABEL}}` | **DevOps only** | *(Operator checks via `alembic current`)* | `{{TO_REVISION}}` |

---

## 3. Rollout Sequencing with Application & Workers (`Expand → Backfill → Contract`)

| Step # | Action (`Schema` \| `Deploy Code` \| `Data Backfill` \| `Postcheck`) | Executed By | Timing / Dependency |
|---|---|---|---|
| 1 | {{SEQUENCE_STEP_1}} | DevOps | Before / after deploying API & workers at `{{REVIEW_REVISION}}` |
{{SEQUENCE_ROWS}}

---

## 4. Environment Execution Runbook for DevOps (`develop` / `staging` / `production`)

Run all commands from working directory `{{BACKEND_ROOT}}` with `DATABASE_URL` exported for the target environment (`develop`, `staging`, or `production`):

### Step 4.1 — Pre-Checks & Backup (Mandatory Before Touching Target DB)
```bash
# 1. Verify current Alembic head and check for active long-running locks:
{{PRECHECK_COMMANDS}}
# e.g. uv run alembic current

# 2. Take backup / snapshot before applying schema or data changes:
{{BACKUP_STEP}}
# e.g. pg_dump --format=custom --no-owner --no-acl "$DATABASE_URL" -f backup_{{TO_REVISION}}_$(date +%Y%m%d_%H%M%S).dump
```

### Step 4.2 — How to Migrate Schema (DDL Upgrade)
```bash
# Review offline SQL first: {{SQL_FILE}} (generated via: uv run alembic upgrade {{FROM_REVISION}}:{{TO_REVISION}} --sql)
# Apply schema revision(s):
{{SCHEMA_MIGRATION_COMMANDS}}
# e.g. uv run alembic upgrade {{TO_REVISION}}
```

### Step 4.3 — How to Migrate Data (Batched & Scoped Backfill)
> If this change is schema-only with no data migration, record `N/A — No data backfill required`.
```bash
# 1. Dry-run to inspect exact row count to be migrated per tenant/scope:
{{DATA_BACKFILL_DRY_RUN_COMMAND}}
# e.g. uv run python -m app.scripts.backfill_<name> --dry-run

# 2. Execute batched, idempotent data migration (safe to re-run or resume if interrupted):
{{DATA_BACKFILL_APPLY_COMMAND}}
# e.g. uv run python -m app.scripts.backfill_<name> --batch-size 1000 --sleep-ms 50
```

### Step 4.4 — Post-Checks & Data Invariants (Verify `VERIFIED_IN_TARGET`)
| Check | Command / SQL Query | Expected Result |
|---|---|---|
| **Alembic Head Reached** | `uv run alembic current` | `{{TO_REVISION}} (head)` |
| **Zero Invalid Indexes** | `SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;` | `0 rows` |
| **Data Backfill Invariant (`B7`)** | `{{INVARIANT_SQL_QUERY}}` | `0 rows remaining` |
{{POSTCHECK_ROWS}}

### Step 4.5 — Rollback & Recovery Plan (If Any Step Fails)
- **Schema Rollback Command**: `{{DOWNGRADE_COMMAND}}` (e.g., `uv run alembic downgrade {{FROM_REVISION}}`)
- **What `downgrade` restores**: {{DOWNGRADE_RESTORES}}
- **Irreversible Data / Requires Backup Restore**: {{IRREVERSIBLE_PARTS}}
- *Note: Rolling back application/worker containers does not automatically roll back database schema or backfilled data.*

---

## 5. Lock & Volume Impact Assessment

| Revision / Backfill | SQL Statement Summary | PostgreSQL Lock Level | Estimated Rows | Expected Duration | Safe During Live Traffic? |
|---|---|---|---|---|---|
{{IMPACT_ROWS}}

- **`lock_timeout` enforced**: `{{LOCK_TIMEOUT}}`
- **Sensitive / Personal Data (`SC11`)**: {{SENSITIVE_DATA_NOTE}}

---

## 6. Disposable-DB Verification Evidence (Completed by Backend Agent)

| Verification Gate (`V1`–`V8`) | Command (`cwd: {{BACKEND_ROOT}}`) | Revision | Exit Code | Key Output | Result (`PASS` / `FAIL`) |
|---|---|---|---|---|---|
{{EVIDENCE_ROWS}}

---

## 7. Operator Execution Log (Filled by DevOps / User After Running)

| Environment (`develop` \| `staging` \| `production`) | Executed By | Timestamp (UTC) | Final State (`APPLIED_UNVERIFIED` \| `VERIFIED_IN_TARGET` \| `FAILED`) | Post-Check & Invariant Output |
|---|---|---|---|---|
| `develop` | | | | |
| `staging` | | | | |
| `production` | | | | |
