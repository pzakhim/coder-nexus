---
name: code-review
description: Backend review rubric — Two Review Gates and Four Mandatory Audit Axes (task checkbox audit, Clean Architecture & security, adversarial unit tests, API schema contract).
---

# Backend Code Review

Inspects code diffs independently across Two Gates and Four Mandatory Audit Axes. The reviewer is strictly read-only.

## 0. Bug hunt first

Run `{{slot:bug-hunt}}` on the fixed scope before the axes below; its dimension 6 uses [the backend bug patterns](references/bug_patterns.md). A `CONFIRMED` `BLOCKER`/`MAJOR` blocks `APPROVED` even when all four axes pass.

## 1. The Two Review Gates

1. **Phase Gate**: Verifies newly added code respects clean boundaries (Domain does not depend on DB/frameworks; SQL parameterized; auth checks present) for an individual behavior phase.
2. **Close Gate**: Verifies end-to-end contract conformity against `api_contract.json` and overall backend test suite health before closing the work item.

## 2. Four Mandatory Review Axes

1. **Planning & Task Checkbox Audit**:
   - Verify that `code_writer` ticked `- [x]` for each completed task in `phases/phase-NN-*.md` and recorded real `Evidence:`.
   - Ensure implementation adheres strictly to locked-in decisions (`D-NN`) in `codebase-notes.md`. If code contradicts `D-NN`, reject with `CHANGES_REQUESTED`.
2. **Clean Architecture & Security Audit** (see `{{slot:clean-architecture}}`):
   - Verify Domain entities and repository interfaces have zero dependencies on web/DB frameworks.
   - Verify parameterized queries (zero SQL injection risks) and explicit authentication/authorization guards on all endpoints.
   - Verify transaction management: DB operations that mutate multiple tables must be wrapped in transactions with verified rollback on failure.
3. **Adversarial Unit Test Audit (Anti-Happy-Path Bias)** (see `{{slot:unit-testing}}`):
   - **MANDATORY REJECTION**: If unit tests only verify the **Happy Path** (200/201 valid response) while ignoring error paths, reject with `CHANGES_REQUESTED`!
   - Require unit tests to cover:
     * Validation failures (400 Bad Request on invalid payload types/missing fields).
     * Auth failures (401 Unauthorized / 403 Forbidden).
     * Resource missing (404 Not Found).
     * Database transaction failure & rollback.
   - Run the test suite independently via `run_command` to verify all tests pass.
4. **API Schema Contract Audit**:
   - Verify that endpoint request/response JSON schemas match 100% of `api_contract.json` (or `design.md` backend contract).
   - When `3RD_PARTY_MOCKOON` is used, audit `mocks/<provider>_mockoon.json` against the agreed trigger table in `design.md`, verify via `mockoon-cli` / `curl`, and confirm `app/` implements only the real HTTP client (`httpx`) without fake provider classes.

## 3. Verdict

- Return structured findings to `code_writer` when issues are found (`CHANGES_REQUESTED`).
- Issue `APPROVED` only when all 4 axes pass cleanly and bug hunt left no `CONFIRMED` `BLOCKER`/`MAJOR`.
