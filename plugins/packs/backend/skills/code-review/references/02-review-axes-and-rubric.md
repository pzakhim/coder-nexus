# 02 — Backend Review Axes and Rubric Mapping

> Topic: Grading the 5 Backend review axes against pack rubric skills, AC traceability, and adversarial test requirements (`R4`, `R5`)

## 1. The Five Backend Review Axes (`R4`)

Grade changed code and broken callers against the Backend pack's rubric skills:

| Axis | What to Audit | Rubric Skill | Typical `BLOCKER` / `MAJOR` Findings |
|---|---|---|---|
| **1. Plan, Scope & AC Traceability** | Tasks in `phases/phase-NN-*.md` ticked `- [x]` with real `Evidence:`; locked decisions (`D-NN`) in `codebase-notes.md` honored; every phase AC mapped to code + test; no out-of-scope edits | `incremental-implementation`, `work-item-contract` | Contradicted `D-NN` decision (`BLOCKER`); untraced AC (`BLOCKER`); fake provider class inside `app/` (`BLOCKER`) |
| **2. Clean Architecture & Transaction Integrity** | Domain purity (`DOM-001`); use case transaction ownership (`APP-001`); rollback verified on multi-table write failure; ORM entities never returned directly as HTTP responses | `{{slot:clean-architecture}}`, `postgres` | Domain importing SQLAlchemy/FastAPI (`BLOCKER`); `commit()` inside repository (`BLOCKER`); partial write without rollback (`BLOCKER`) |
| **3. Code Quality, Async & Simplicity** | Explicit async/await discipline (no blocking I/O in `async def`, no unawaited coroutines); explicit error mapping (no bare `except Exception: return []`); `Decimal` for money; `datetime.now(UTC)` for timestamps; no redundant pass-through wrappers | `{{slot:clean-code}}`, `{{slot:code-simplification}}`, `fastapi` | Swallowed exception returning fake 200/empty list (`BLOCKER`); blocking sync call in `async def` (`MAJOR`); float arithmetic on currency (`BLOCKER`) |
| **4. Adversarial Unit & Integration Tests (`TEST-TAMPER-001`)** | Happy + negative + edge/boundary coverage; doubles only at architectural seams (`FakeRepository`, `ASGITransport`, `httpx.MockTransport`); no weakened/deleted assertions | `{{slot:unit-testing}}` | Happy-path-only tests (`BLOCKER`); mocking the use case under test (`MAJOR`); weakened/deleted assertion `TEST-TAMPER-001` (`BLOCKER`) |
| **5. Security, API Contract & Migrations** | Object-level auth & tenant/owner query scoping; parameterized SQL; `SecretStr` / zero leaked secrets; 100% schema/status parity with `api_contract.json`; expand/contract Alembic migrations | `{{slot:secure-coding-standards}}`, `api-contract-design`, `database-migrations` | Missing owner/tenant filter IDOR (`BLOCKER`); SQL injection (`BLOCKER`); response/status drift from `api_contract.json` (`BLOCKER`); destructive/un-expandable migration (`BLOCKER`) |

---

## 2. Adversarial Test Audit (Anti-Happy-Path Rule — `R5`)

**Mandatory Rejection (`CHANGES_REQUESTED`):** If the test suite for a changed endpoint or use case only tests the **Happy Path** (`200 OK` / `201 Created`) while omitting error paths, raise a `BLOCKER` finding. Require tests covering all applicable failure modes:
1. **Validation failure (`400` / `422`):** Missing required fields, invalid types, out-of-range values, or domain invariant violations.
2. **Authentication & Authorization (`401` / `403` / `404` foreign owner):** Unauthenticated call, insufficient role/capability, and cross-tenant / foreign-owner access attempt.
3. **Resource / State conflict (`404` / `409`):** Missing target record or duplicate/idempotency conflict.
4. **Transaction rollback / upstream failure:** Verify that when a secondary write or external provider fails, earlier writes in the unit of work roll back cleanly.
5. **Anti-Tamper (`TEST-TAMPER-001`):** Inspect `git diff` on `tests/`. Deleting, skipping (`@pytest.mark.skip`), or loosening an existing assertion to make a broken change pass is an immediate `BLOCKER`.
