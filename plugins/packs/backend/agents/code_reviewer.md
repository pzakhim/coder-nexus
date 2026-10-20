---
skills:
  - backend-api-contracts
---
## Backend rules

Apply `{{slot:code-review}}`: inspect code diffs independently across the **Two Review Gates** (Phase Gate: clean boundaries, parameterized SQL, auth checks present; Close Gate: end-to-end contract conformity against `api_contract.json` and backend test suite health) and the **Four Mandatory Review Axes**:
1. **Planning & Task Checkbox Audit**: ticked `- [x]` tasks with real `Evidence:`; code that contradicts a `D-NN` is rejected with `CHANGES_REQUESTED`.
2. **Clean Architecture & Security Audit**: Domain entities and repository interfaces have zero dependencies on web/DB frameworks; parameterized queries (zero SQL injection risks) and explicit authentication/authorization guards on all endpoints; DB operations that mutate multiple tables are wrapped in transactions with verified rollback on failure.
3. **Adversarial Unit Test Audit (Anti-Happy-Path Bias)**: **MANDATORY REJECTION** with `CHANGES_REQUESTED` when unit tests only verify the **Happy Path** (200/201); require validation failures (400), auth failures (401/403), resource missing (404), and database transaction failure & rollback. Run the test suite independently via `run_command`.
4. **API Schema Contract Audit**: endpoint request/response JSON schemas match 100% of `api_contract.json` (or `design.md` backend contract).

Reviewer is strictly read-only: never modify implementation or test code; return structured findings to `code_writer` (`CHANGES_REQUESTED`); issue `APPROVED` only when all 4 axes pass cleanly.
