# Migration hand-off — {{WORK_ITEM}} {{PHASE_ID}}

> **Migration state:** `{{MIGRATION_STATE}}` <!-- PENDING | READY_FOR_HANDOFF -->
> **Revision (git):** `{{REVIEW_REVISION}}`
> **Alembic:** `{{FROM_REVISION}}` → `{{TO_REVISION}}`
> **Step type:** {{STEP_TYPE}} <!-- expand | backfill | contract | additive only -->
> **Owner who applies it:** {{OWNER_ROLE}} <!-- user / DevOps; never the agent -->
> **Prepared by / at:** Code Writer, {{PREPARED_AT}}

No secret values anywhere in this file. Connection strings are referenced as `DATABASE_URL` from the operator's environment.

## Targets

| Environment | Host label (no credentials) | Current Alembic revision (operator fills) |
|---|---|---|
{{TARGET_ROWS}}

## Order and sequencing

| # | Action | Who | Before / after |
|---|---|---|---|
{{SEQUENCE_ROWS}}
<!-- e.g. 1 | alembic upgrade <expand rev> | DevOps | before deploying API {{REVIEW_REVISION}} -->

## Commands (cwd: `{{BACKEND_ROOT}}`)

```bash
{{COMMANDS}}
# e.g. uv run alembic current
#      uv run alembic upgrade {{TO_REVISION}}
#      uv run python -m <backfill module> --dry-run && uv run python -m <backfill module> --batch-size 1000
```

Generated SQL for review: `{{SQL_FILE}}` (from `uv run alembic upgrade {{FROM_REVISION}}:{{TO_REVISION}} --sql`).

## Impact

| Revision | Statement | Lock | Rows (estimate) | Expected duration | Safe during traffic |
|---|---|---|---|---|---|
{{IMPACT_ROWS}}

`lock_timeout` used: {{LOCK_TIMEOUT}}. Concurrent index revisions run outside a transaction.

## Backup and recovery

- Backup before applying: {{BACKUP_STEP}}
- `downgrade` restores: {{DOWNGRADE_RESTORES}}
- Not restorable by downgrade: {{IRREVERSIBLE_PARTS}} <!-- "none" or the data lost -->
- Rolling back application code does not roll back data.

## Postchecks

| Check | Query / request | Expected |
|---|---|---|
| Revision applied | `uv run alembic current` | `{{TO_REVISION}} (head)` |
| No invalid index | `SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;` | no rows |
{{POSTCHECK_ROWS}}

## Verification already done (disposable database)

| Claim | Command (+cwd) | Revision | Exit code | Key output | Result |
|---|---|---|---|---|---|
{{EVIDENCE_ROWS}}

## Sensitive data

{{SENSITIVE_DATA_NOTE}} <!-- "No personal data copied or exposed" or what is moved and the guard -->

## Operator report (filled by whoever applies it)

| Environment | Applied by | At | Result state | Postcheck output |
|---|---|---|---|---|
| | | | `APPLIED_UNVERIFIED` / `VERIFIED_IN_TARGET` / `FAILED` | |
