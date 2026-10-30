---
skills:
  - backend-api-contract-design
  - backend-postgres
  - backend-realtime
---
## Backend rules (Python + FastAPI + PostgreSQL)

Backend acceptance executes `vN/test-plan.md` (`E2E-01..E2E-N`) sequentially with **Fail-Fast** and **zero test-case tampering** through the real API and test database, following `quality-acceptance` and `{{slot:verification}}`:
- **Sequential Backend E2E Verification Ladder (`E2E-01..E2E-N` — Fail-Fast)**:
  1. **Rung 1 — Environment & Alembic Migration Gate**: Run the reviewed revision against the test database (`DATABASE_URI` from the workspace `.env`, never production) with `alembic upgrade head` applied; record the Alembic head revision in the environment record. When testing against mocked outbound 3rd-party services (`3RD_PARTY_MOCKOON`), ensure `mockoon-cli` (`mocks/<provider>_mockoon.json`) is running in the background.
  2. **Rung 2 — Live HTTP/REST API & Role/Tenant Authorization (`backend-api-contract-design`)**: Execute each `E2E-i` scenario through the real API with real tokens per role (an HTTP client or `httpx`), verifying status codes, response bodies against `api_contract.json`, validation error codes, and direct calls with another actor's or tenant's id refused (`403`) per the contract.
  3. **Rung 3 — Persisted Data & Transaction Rollback (`backend-postgres`)**: Read rows back with the pack's Postgres MCP in restricted (read-only) mode or a `SELECT` against the test database; verify that failed multi-table writes rolled back cleanly and left no partial records behind.
  4. **Rung 4 — Realtime WebSocket / SSE Delivery (`backend-realtime`)**: When realtime channels are in scope, connect a WebSocket / SSE client per role, trigger the event through the API, and verify that only in-scope clients receive it, including after a reconnect when `design.md` names one.
- **Fail-Fast & Handoff (`test_runner` ↔ `bug_fixer` ↔ `planning`)**:
  - Developer unit tests are owned by `code_writer` / `bug_fixer` and were graded in review; never count them as acceptance evidence.
  - Tick `- [x] **E2E-i**` in `vN/test-plan.md` with fresh HTTP/DB/WS evidence as each scenario passes.
  - If any `E2E-i` fails, **stop immediately (`FAIL-FAST`)**, never alter `test-plan.md`, record the exact HTTP request/response, SQL state, traceback, and `FAILED_AT: E2E-i` in `vN/evidence/final_qa/<revision>/acceptance-report.md`, and return `CHANGES_REQUESTED` so the coordinator invokes **`bug_fixer`** (`L1`/`L2` service/repo fix or `L3` `PCR-NN.md` escalation to **`planning`**).
  - Once fixed, re-run `E2E-01` through `E2E-N` from start to finish until 100% pass.
