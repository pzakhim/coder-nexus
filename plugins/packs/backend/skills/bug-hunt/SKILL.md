---
name: bug-hunt
description: Finds real defects in a fixed revision of a Backend (Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2.x async, Alembic, PostgreSQL) service - fixes the scope and reads callers, makes a cold pass through seven defect dimensions, tries to disprove every candidate, and keeps only findings with a concrete given/when/then failure scenario using Python/FastAPI/SQLAlchemy/async bug patterns. Use for the Code Writer's quick self-check before READY_FOR_REVIEW and for the Reviewer's bug-hunt pass on every phase or small item, or whenever someone asks to "find bugs in this diff", "self-check before handoff", "what breaks here", "tìm bug", "review tìm lỗi", even if they only say "review this endpoint" or "check this migration". Not for style, architecture compliance, or complexity review.
---

# Bug Hunt — Backend (Python / FastAPI)

**One question:** with which input or state does this change produce a wrong result, a crash, a hang, a leak, a data-scope breach (another user's or tenant's rows), or a security hole?

Out of scope for this skill (because mixing them in buries real defects under noise):
- Approval gates, AC traceability, layer boundaries, and review rubric axes → `{{slot:code-review}}` and `review-workflow`.
- Rule compliance (naming, structure, Clean Architecture) → `{{slot:clean-code}}`, `{{slot:clean-architecture}}`.
- Complexity and cleanups → `{{slot:code-simplification}}` (recorded only as `NOTE` lines).
- How to write secure code → `{{slot:secure-coding-standards}}`; this skill only *hunts* the breach.
- Fixing a confirmed defect at its root → `{{slot:root-cause-debugging}}`.

Severity (`BLOCKER` / `MAJOR` / `MINOR`), confidence (`CONFIRMED` / `PLAUSIBLE`), verdict impact, effort caps, and the `bug-hunt:` summary line follow [handoff-and-status §9](../work-item-contract/references/handoff-and-status.md).

## 1. Read-Only CLI Verification Gates (`PASS` / `FAIL` / `NOT_RUN`)

| Check | Command | Gate |
|---|---|---|
| **Caller & Symbol Search** | `rg -n -w "<symbol>" app tests` | Read-only trace |
| **Type & Coroutine Check** | `uv run mypy <path>` | `PASS` / `FAIL` (`[unused-coroutine]`) |
| **Async / Bug Lint** | `uv run ruff check <path>` | `PASS` / `FAIL` (`ASYNC`, `B006`, `BLE001`, `DTZ`, `RUF006`, `S608`) |
| **Focused Test Execution** | `uv run pytest <path> -q` | `PASS` / `FAIL` |
| **Offline Migration SQL** | `uv run alembic upgrade <base>:<head> --sql` | Read-only SQL inspection |

During the hunt, never modify application code, tests, or migrations; an unrun command is `NOT_RUN`, never evidence (`evidence-standard`).

## 2. The Hunt Loop

1. **Fix the revision & read callers:** Record `BASE_REVISION..REVIEW_REVISION`, read each changed hunk whole, and find/read all callers of changed public symbols ([01 — Scope, Dimensions & Patterns](references/01-scope-dimensions-and-patterns.md)).
2. **Cold pass through 7 dimensions:** Walk the code before reading specs/designs; write candidates as `file:line — hypothesis` ([01 — Scope, Dimensions & Patterns](references/01-scope-dimensions-and-patterns.md)).
3. **Adversarial disproof:** Trace the real path from entry point to line; keep only candidates with a `given → when → then` scenario and evidence ([02 — Verify & Disprove](references/02-verify-and-disprove.md)).
4. **Rank, cap & report:** Order by severity (`BLOCKER` / `MAJOR` / `MINOR`) and confidence (`CONFIRMED` / `PLAUSIBLE`); end with the `bug-hunt:` line ([03 — Severity, Verdict & Report](references/03-severity-verdict-and-report.md)).
5. **Apply verdict & role duties:** Enforce verdict impact and Reviewer vs Code Writer responsibilities ([03 — Severity, Verdict & Report](references/03-severity-verdict-and-report.md)).

## 3. Effort & Backend `deep` Triggers

| Effort | Dimensions | Scope | Cap |
|---|---|---|---|
| `quick` | 1–4 | Changed hunks only | 5 |
| `standard` | 1–7 | Changed code plus direct callers | 10 |
| `deep` | 1–7 | Plus every caller one level further | No cap |

**Backend `deep` triggers:** any file under `alembic/versions/`; authentication or authorization dependencies (`Depends(get_current_user)` guards, permission checks); session / transaction / unit-of-work management; money, quantity, or balance arithmetic; tenant or owner scoping of queries.

## 4. Mandatory Rules (`H1`–`H14`)

| ID | Rule Summary | Reference |
|---|---|---|
| **H1–H5** | Single defect question, fixed revision, whole context & callers, cold pass first, 7 dimensions | [01 — Scope, Dimensions & Patterns](references/01-scope-dimensions-and-patterns.md) |
| **H6–H8** | Disprove every candidate (read-only), concrete `given → when → then` scenario, `CONFIRMED`/`PLAUSIBLE` | [02 — Verify & Disprove](references/02-verify-and-disprove.md) |
| **H9–H14** | Unified `BLOCKER`/`MAJOR`/`MINOR`, effort caps, report row & `bug-hunt:` line, verdict impact, roles, `NOTE` cleanups | [03 — Severity, Verdict & Report](references/03-severity-verdict-and-report.md) |

## 5. Reference Guides

| Guide | Topic |
|---|---|
| [01 — Scope, Dimensions & Patterns](references/01-scope-dimensions-and-patterns.md) | Fixed revision, caller tracing, cold pass, 7 defect dimensions, and Python/FastAPI/SQLAlchemy/Alembic bug patterns |
| [02 — Verify & Disprove](references/02-verify-and-disprove.md) | Adversarial disproof steps, `given → when → then` scenarios, read-only CLI checks, and typical disproofs |
| [03 — Severity, Verdict & Report](references/03-severity-verdict-and-report.md) | Effort caps, `BLOCKER`/`MAJOR`/`MINOR` calibration, finding row format, verdict impact, and role duties |
