---
skills:
  - backend-api-contracts
---
## Backend rules

Within the `review-process` passes, `{{slot:code-review}}` adds these backend checks; each failure is a finding graded on the bug-hunt scale:
1. **Layers and security**: domain entities and repository interfaces have no web or database framework dependency; queries are parameterized (no SQL injection); every endpoint has explicit authentication and object-level authorization guards; multi-table writes run in one transaction with verified rollback on failure.
2. **Negative-path tests**: tests that only verify 200/201 leave the phase's AC unprotected. Require 400 validation, 401/403 authorization, 404 not found and transaction-failure rollback where the design names them; run the suite yourself via `run_command`.
3. **API contract**: request/response schemas, status codes and error shapes match `api_contract.json` (or the `design.md` backend contract) exactly. At the closing phase, check end-to-end contract conformity and backend suite health.
