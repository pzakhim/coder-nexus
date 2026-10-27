# 01 — Scope, Verification Gates, and Boundary Validators

> Topic: Fixed revision scope, read-only discipline, Phase/Close/Mockoon gates, and independent CLI verification (`R1`–`R3`, `R6`, `R9`)

## 1. Fixed Revision & Read-Only Discipline (`R1`, `R2`, `R9`)

- **Fixed Revision (`R1`):** Record `BASE_REVISION` and `REVIEW_REVISION` from the hand-off header, plus staged, unstaged, and untracked files (`git status --short`, `git diff --stat <BASE_REVISION>..<REVIEW_REVISION>`). Review exactly that tree. A moving tree or unresolvable revision is `BLOCKED`.
- **Strictly Read-Only (`R2`):** Never edit application code (`app/`), tests (`tests/`), migrations (`alembic/`), contracts, or `pyproject.toml`. Write only the review report under `vN/reviews/`.
- **Diff & Caller Scope (`R9`):** Inspect changed files and any callers, routes, schemas, or migrations broken by the diff (`rg -n -w "<symbol>" app tests`). Pre-existing legacy debt outside the diff is recorded only as a non-blocking note.

---

## 2. Two-Gate Protocol (`PHASE-00` vs `PHASE-01+` vs Close Gate)

### 2.1 `PHASE-00` Gate (`3RD_PARTY_MOCKOON` Preparation Phase)
When reviewing a `PHASE-00` that prepares third-party provider mocks (`mocks/<provider>_mockoon.json`):
1. Audit `mocks/<provider>_mockoon.json` against the **Mockoon Trigger & Test Data Table** in `design.md` (Pass/Default `200/201`, Empty `[]`, and Fail `400/401/403/429/500` conditional rules).
2. Verify responses via `mockoon-cli` / `curl` where applicable.
3. Confirm `phases/phase-00-prepare.md` is ticked `[x] PREPARED / COMPLETED` and `app/` contains only the real `httpx.AsyncClient` adapter (zero fake provider classes in production code).

### 2.2 `PHASE-01+` Phase Gate & Close Gate (`R3`, `R6`)
1. **Rerun CLI Gates Independently (`R6`):** Treat the Code Writer's hand-off rows as claims, not proof. Run the checks on `REVIEW_REVISION` and record each exit code (`PASS` / `FAIL`):
   - `uv run ruff check app tests`
   - `uv run mypy app tests`
   - `uv run bandit -r app -ll`
   - `uv run pytest -q` (focused phase tests + full suite at Close Gate)
   - `uv run alembic heads` and `uv run alembic upgrade <base>:<head> --sql` (when models or migrations change)
2. **Cold Bug-Hunt Pass (`R3`):** Run `{{slot:bug-hunt}}` cold on `BASE_REVISION..REVIEW_REVISION` before reading `requirements.md`, `design.md`, or `api_contract.json`. Copy surviving findings into the report as `RV-NN` rows.

---

## 3. Backend Layer & Cross-Module Boundary Checks

| Rule ID | Boundary Requirement | Verification Command / Check | Severity |
|---|---|---|---|
| `DOM-001` | Domain entities, value objects, and repository protocols have zero imports of FastAPI, SQLAlchemy, Pydantic HTTP schemas, or `httpx` | `rg -n "from (fastapi|sqlalchemy|httpx)" app/**/domain` | `BLOCKER` |
| `APP-001` | Application use cases own transaction boundaries (`UnitOfWork` / `session.begin()`); repositories never call `session.commit()` | `rg -n "\.commit\(" app/**/infrastructure app/**/repositories` | `BLOCKER` |
| `API-001` | FastAPI routers contain only transport wiring (`Depends`, status codes, `response_model`) and delegate business logic to use cases | Inspect changed router modules | `MAJOR` |
| `CRX-001` | Cross-module communication uses public application/domain interfaces rather than importing another module's internal ORM models or repositories | Inspect cross-module imports in diff | `BLOCKER` |
