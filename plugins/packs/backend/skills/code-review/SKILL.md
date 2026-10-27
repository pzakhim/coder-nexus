---
name: code-review
description: Backend code review rubric and verification gates for Python 3.12+ / FastAPI / Pydantic v2 / SQLAlchemy 2.x async / Alembic / PostgreSQL services - strictly read-only, runs bug-hunt first, executes deterministic CLI/migration/contract gates independently, grades five review axes against the Backend pack skills, and issues an APPROVED / CHANGES_REQUESTED / BLOCKED verdict with RV-NN findings.
---

# Code Review — Backend (Python / FastAPI)

Reviewer is strictly read-only toward implementation, tests, migrations, and dependencies; write review reports only (`vN/reviews/review_<phase-id>_<REVIEW_REVISION>.md`). Follow `review-workflow` for pass ordering and [handoff-and-status](../work-item-contract/references/handoff-and-status.md) for unified finding rows and status flags.

## 1. CLI & Contract Verification Gates (`PASS` / `FAIL`)

Rerun applicable checks independently on `REVIEW_REVISION` (`R6`). `NOT_RUN`, `BLOCKED`, and `UNVERIFIED` never count as `PASS`:

| Gate | Command | Pass Criteria |
|---|---|---|
| **Static Lint & Import Rules** | `uv run ruff check app tests` | `PASS` (`exit 0`, zero layer/async/bug lint violations) |
| **Strict Typecheck** | `uv run mypy app tests` | `PASS` (`exit 0`, zero `[unused-coroutine]` or type errors) |
| **Security Scanner** | `uv run bandit -r app -ll` | `PASS` (zero medium/high security findings) |
| **Independent Test Suite** | `uv run pytest -q` | `PASS` (all unit & integration tests green) |
| **Offline Migration SQL** | `uv run alembic heads && uv run alembic upgrade <base>:<head> --sql` | `PASS` (single head; non-destructive SQL matching ORM models) |

## 2. Order of Passes

1. **Fix the revision & rerun gates (`R1`, `R2`, `R6`):** Verify `BASE_REVISION..REVIEW_REVISION` and uncommitted scope; check `PHASE-00` (`3RD_PARTY_MOCKOON`) or `PHASE-01+` gates and rerun all CLI checks ([01 — Scope, Gates & Validators](references/01-scope-gates-and-validators.md)).
2. **Cold bug-hunt pass (`R3`):** Run `{{slot:bug-hunt}}` cold at `standard` (or `deep` for migrations, auth, transactions, money, or tenant scoping) before reading specification documents.
3. **Grade the 5 Backend review axes (`R4`, `R5`):** Audit Plan/AC traceability, Clean Architecture & Transactions, Code Quality & Simplicity, Adversarial Tests (`TEST-TAMPER-001`), and Security/API Contract/Migrations ([02 — Review Axes & Rubric](references/02-review-axes-and-rubric.md)).
4. **Write findings & decide verdict (`R7`–`R14`):** Grade findings with unified `BLOCKER` / `MAJOR` / `MINOR` severities, enforce no-waiver rules (`PLAN_CONFLICT` → `change-control`), and write the revision-bound report ([03 — Findings, Verdict & Report](references/03-findings-verdict-and-report.md)).

## 3. Mandatory Rules (`R1`–`R14`)

| ID | Rule Summary | Reference |
|---|---|---|
| **R1–R3, R6, R9** | Fixed revision, strictly read-only, bug-hunt first, rerun CLI gates independently, diff + broken callers scope | [01 — Scope, Gates & Validators](references/01-scope-gates-and-validators.md) |
| **R4–R5** | Grade axes with Backend rubric skills, trace every AC, reject happy-path-only or tampered tests (`TEST-TAMPER-001`) | [02 — Review Axes & Rubric](references/02-review-axes-and-rubric.md) |
| **R7–R8, R10–R14** | No reviewer waivers (`PLAN_CONFLICT`), actionable `RV-NN` rows, verdict criteria, 3-round cap, delta re-review, report | [03 — Findings, Verdict & Report](references/03-findings-verdict-and-report.md) |

## 4. Reference Guides

| Guide | Topic |
|---|---|
| [01 — Scope, Gates & Validators](references/01-scope-gates-and-validators.md) | Fixed revision, read-only rule, Phase/Close/Mockoon gates, CLI checks, and layer boundary validation |
| [02 — Review Axes & Rubric](references/02-review-axes-and-rubric.md) | The 5 Backend review axes, rubric skill links, AC traceability, and anti-happy-path test audit |
| [03 — Findings, Verdict & Report](references/03-findings-verdict-and-report.md) | Unified `BLOCKER`/`MAJOR`/`MINOR` findings, no-waiver rules, verdict thresholds, rounds, and report structure |
