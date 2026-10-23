---
name: bug-hunt
description: Finds real defects in a fixed revision of a Backend (Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2.x async, Alembic, PostgreSQL) service - fixes the scope and reads callers, makes a cold pass through seven defect dimensions, tries to disprove every candidate and keeps only findings with a concrete given/when/then failure scenario, using Python/FastAPI/SQLAlchemy/async bug patterns. Use for the Code Writer's quick self-check before READY_FOR_REVIEW and for the Reviewer's bug-hunt pass on every phase or small item, or whenever someone asks to "find bugs in this diff", "self-check before handoff", "what breaks here", "tìm bug", "review tìm lỗi", even if they only say "review this endpoint" or "check this migration". Not for style, architecture compliance or complexity review.
---

# Bug Hunt — Backend (Python / FastAPI)

**One question:** with which input or state does this change produce a wrong result, a crash, a hang, a leak, a data-scope breach (another user's or tenant's rows) or a security hole?

Not here, because mixing them in buries real defects under noise:

- Approval gates, AC traceability, layer boundaries and the review axes → `{{slot:code-review}}` and `review-workflow`.
- Rule compliance (naming, structure, Clean Architecture) → `clean-code` / `{{slot:clean-code}}`, `{{slot:clean-architecture}}`.
- Complexity and cleanups → `code-simplification` / `{{slot:code-simplification}}` (as `NOTE` lines).
- How to write secure code → `{{slot:secure-coding-standards}}`; this skill only *finds* the breach.
- Fixing a confirmed defect at its root → `{{slot:root-cause-debugging}}`.

Severity (`BLOCKER` / `MAJOR` / `MINOR`), confidence (`CONFIRMED` / `PLAUSIBLE`), verdict impact, effort caps and the `bug-hunt:` summary line are defined once in [handoff-and-status §9](../work-item-contract/references/handoff-and-status.md). This skill uses them and never re-grades them, so the writer and the reviewer read a finding the same way.

## The loop

1. Fix the revision, read each changed hunk whole, find and read callers ([01](references/01-scope-and-candidates.md)).
2. Cold pass through the seven dimensions before reading the documents; write candidates as `file:line — hypothesis` ([01](references/01-scope-and-candidates.md)).
3. Try to disprove each candidate; keep only those with a `given → when → then` scenario and evidence ([02](references/02-verify.md)).
4. Rank, cap and write the rows; end with the `bug-hunt:` line ([03](references/03-effort-severity-report.md)).
5. Apply the verdict impact and your role's duties ([04](references/04-verdict-and-roles.md)).

During the hunt nobody edits application code, tests or migrations: a hunt that changes the tree no longer describes the revision under review.

## Effort

Which effort applies and its finding cap come from [handoff-and-status §9](../work-item-contract/references/handoff-and-status.md) → "Bug-hunt effort". What each effort covers here:

| Effort | Dimensions | Scope |
|---|---|---|
| `quick` | 1–4 | Changed hunks only |
| `standard` | 1–7 | Changed code plus direct callers |
| `deep` | 1–7 | Plus every caller one level further |

Backend changes that count as §9's "auth / payment / data-migration" trigger, so they run `deep`: anything under `alembic/versions/`; authentication or authorization dependencies (`Depends(get_current_user)`-style guards, permission checks); session / transaction / unit-of-work management; money, quantity or balance arithmetic; tenant or owner scoping of queries. Reason: these are the defects that corrupt data or leak it, and they rarely show in a happy-path test.

## Which file to read

| Doing | Read |
|---|---|
| Fixing the scope, callers, cold pass, seven dimensions | [01-scope-and-candidates.md](references/01-scope-and-candidates.md) |
| Verifying or rejecting a candidate | [02-verify.md](references/02-verify.md) |
| Ranking, cap, finding row, summary line | [03-effort-severity-report.md](references/03-effort-severity-report.md) |
| What findings do to the verdict; Reviewer vs Code Writer | [04-verdict-and-roles.md](references/04-verdict-and-roles.md) |
| Python / FastAPI / SQLAlchemy / async / Alembic patterns (dimension 6) | [05-bug-patterns.md](references/05-bug-patterns.md) |

## Relationship with other skills

- `incremental-implementation` runs this at `quick` as the Code Writer's phase-end self-check and puts the `bug-hunt:` line in the hand-off.
- `review-workflow` runs this as pass 2 at `standard` or `deep`; the Reviewer copies the rows as `RV-NN`.
- A confirmed defect gets a reproducing test first per `{{slot:unit-testing}}`; the fix follows `{{slot:root-cause-debugging}}` inside the phase scope (`incremental-implementation`).
- A fix that would change behavior, an API contract (`api-contract-design`) or the design goes to Planning via `change-control`.
- Claims about checks follow `evidence-standard`; a command you did not run is `NOT_RUN`, never evidence.
