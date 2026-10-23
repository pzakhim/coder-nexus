---
name: verification
description: Independent backend verification — integration, contract compliance, business-rule scenarios, failure paths and database integrity, mapped to AC-NN.
---

# Backend Verification

Executes and verifies backend integration and system tests independently of `code_writer`.

## 1. Upstream Authority & Source of Truth

Connect directly to upstream artifacts rather than relying on developer unit test assumptions:
1. **`codebase-notes.md` (read-only)**: Decision Log (`D-NN`) for business rationale, Glossary for entity mapping, and Extended Rule Details for boundary conditions and formulas.
2. **`requirements.md`**: Behavioral scenarios, Business Rules (`BR-NN`), and Acceptance Criteria (`AC-NN`).
3. **`api_contract.json` & `design.md`**: JSON schemas, expected HTTP status codes, headers, and error shapes.

## 2. Independent Verification Boundary

- `code_writer` owns Developer Unit Tests (`tests/unit/`) verified by `code_reviewer`.
- `test_runner` owns **Independent Integration, Contract Compliance, and Live API Verification**:
  1. **Contract Compliance**: Validates actual HTTP response payloads against the agreed JSON schema in `api_contract.json` (validating property types, required keys, and nullability).
  2. **Business Rule Scenarios**: Verifies all Acceptance Criteria (`AC-NN`) through integration tests or API requests.
  3. **Edge & Failure Paths**: Actively asserts negative scenarios (invalid payload -> 400, missing auth -> 401/403, entity not found -> 404, server error recovery -> 500).
  4. **Database Integrity & Rollback**: Verifies transaction atomicity and rollback under failure conditions.

## 3. Execution & Reporting

- Run integration test suites or API test commands via `run_command`.
- Map every executed test to an `AC-NN` ID from `requirements.md`.
- Report verdict (`PASS`, `FAIL`, `BLOCKED`) with execution logs and evidence to the coordinator and `docs_writer` for `as-built.md`.
- `NOT_RUN`, `BLOCKED`, or `UNVERIFIED` can NEVER be counted as `PASS`.
