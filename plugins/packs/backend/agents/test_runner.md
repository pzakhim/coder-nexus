---
skills:
  - backend-api-contracts
---
## Backend rules

Backend acceptance runs through the real API, following `acceptance-testing` and `{{slot:verification}}`:
- **Source of truth**: `requirements.md` (`BR-NN`, `AC-NN`), `codebase-notes.md` (read-only), and `api_contract.json` & `design.md` (JSON schemas, expected status codes, headers and error shapes), never developer unit test assumptions.
- **Boundary**: `code_writer` owns developer unit tests (`tests/unit/`), graded by `code_reviewer`. `test_runner` owns:
  1. **Contract compliance**: actual HTTP payloads against the agreed schema (types, required keys, nullability).
  2. **Business rule scenarios**: every `AC-NN` through integration tests or API requests with real auth per role.
  3. **Edge and failure paths**: invalid payload → 400, missing auth → 401/403 (including a direct forbidden call), entity not found → 404, server error handling.
  4. **Data integrity**: persisted data read back; transaction atomicity and rollback under failure.
- Map every executed test to an `AC-NN` and report `PASS`, `FAIL`, `BLOCKED` or `NOT_RUN` per case with evidence rows. `NOT_RUN`, `BLOCKED` or `UNVERIFIED` never count as `PASS`.
