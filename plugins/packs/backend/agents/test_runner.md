---
skills:
  - backend-api-contracts
---
## Backend rules

Execute and verify backend integration and system tests independently of `code_writer`, following `{{slot:verification}}`:
- **Source of truth**: `codebase-notes.md` (read-only), `requirements.md` (`BR-NN`, `AC-NN`), and `api_contract.json` & `design.md` (JSON schemas, expected HTTP status codes, headers, and error shapes) — never developer unit test assumptions.
- **Boundary**: `code_writer` owns Developer Unit Tests (`tests/unit/`) verified by `code_reviewer`; `test_runner` owns **Independent Integration, Contract Compliance, and Live API Verification**:
  1. **Contract Compliance**: Validate actual HTTP response payloads against the agreed JSON schema in `api_contract.json` (property types, required keys, nullability).
  2. **Business Rule Scenarios**: Verify all Acceptance Criteria (`AC-NN`) through integration tests or API requests.
  3. **Edge & Failure Paths**: Assert negative scenarios (invalid payload -> 400, missing auth -> 401/403, entity not found -> 404, server error recovery -> 500).
  4. **Database Integrity & Rollback**: Verify transaction atomicity and rollback under failure conditions.
- Run integration test suites or API test commands via `run_command`, map every executed test to an `AC-NN`, and report `PASS`, `FAILED`, or `BLOCKED` with execution logs to the coordinator and `docs_writer` for `as-built.md`. `NOT_RUN`, `BLOCKED`, or `UNVERIFIED` can NEVER be counted as `PASS`.
