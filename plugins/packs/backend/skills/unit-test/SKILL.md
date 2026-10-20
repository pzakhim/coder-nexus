---
name: unit-test
description: Backend developer unit and repository tests — every UseCase, service and repository method covers the Happy Path and the Negative / Edge cases, including database rollback.
---

# Backend Unit Tests

Owned by `code_writer`, graded by `code_reviewer`. Integration, contract and live API verification belong to `test_runner` (see `{{slot:verification}}`).

## Scope and location

- For every UseCase, service, and repository method, create corresponding unit tests under `tests/unit/`.

## Mandatory cases (no Happy-Path-only suites)

Test both:
- **Happy Path**: 200/201, valid payload.
- **Negative / Edge Cases**:
  - Validation failures (400 Bad Request on invalid payload types/missing fields).
  - Auth failures (401 Unauthorized / 403 Forbidden).
  - Resource missing (404 Not Found).
  - Server error (500).
  - Database transaction failure & rollback.

Never write only Happy-Path tests.

## Running

- Run the task's test command via `run_command` (e.g., `pytest tests/unit/...` or the service's test runner). Must achieve 100% pass before proceeding to the next task.
