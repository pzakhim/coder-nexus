# 03 — Severity, Verdict Impact, and Reporting

> Topic: Effort caps, unified BLOCKER/MAJOR/MINOR calibration, finding table format, verdict impact, and role duties (`H9`–`H14`)

The Code Writer and the Reviewer use one scale and one row format, so a finding can be acted on, copied into the review report, and compared across rounds without re-wording.

## 1. Effort and Cap (`H10`)

Pick the effort and its cap from [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md) → "Bug-hunt effort"; the dimensions each effort covers and the Backend `deep` triggers are in [SKILL.md](../SKILL.md#3-effort--backend-deep-triggers).

When the cap is reached, keep the most severe findings and state in the summary line that the cap truncated the list; do not silently drop findings.

---

## 2. Unified Severity and Confidence (`H9`)

Grade with the unified 3-tier defect scale of [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md): `BLOCKER` / `MAJOR` / `MINOR` with `CONFIRMED` / `PLAUSIBLE`. Do not invent another level or soften one to end a round.

| Severity | Typical Backend Calibration |
|---|---|
| `BLOCKER` | User B reads or edits user A's row; a migration drops or corrupts data; a missing `await` means a write never happens; partial commit across tables; a request hangs the event loop on a normal path |
| `MAJOR` | 500 instead of 404 / 409 on a realistic edge (missing row, duplicate, concurrent edit); last page repeats or skips rows; session or `httpx` client leaked on the error path; naive vs aware datetime crash for a valid input |
| `MINOR` | Wrong result only in a rare or self-correcting case, such as a cache entry that stays stale until its short TTL expires |

A rule violation without wrong runtime behavior is not a `bug-hunt` finding; it belongs to the rubric pass (`{{slot:code-review}}`, `{{slot:clean-code}}`) under the same unified `BLOCKER` / `MAJOR` / `MINOR` scale.

---

## 3. Finding Row Format & Summary Line (`H11`, `H14`)

Order: most severe first, `CONFIRMED` before `PLAUSIBLE`. The columns match the review report's findings table ([handoff-and-status](../../work-item-contract/references/handoff-and-status.md) §5), so the Reviewer copies a row unchanged and only replaces the ID with `RV-NN`:

| ID | Pass | Severity | Confidence | File:line | Problem | Failure scenario / evidence | Fix direction |
|---|---|---|---|---|---|---|---|
| `BH-01` | 2 bug-hunt | `BLOCKER` | `CONFIRMED` | `app/orders/router.py:58` | `get_order` filters by `Order.id` only; no owner check | given order 42 owned by A → when B calls `GET /orders/42` → then 200 with A's order; traced route → `OrderRepository.get` (no `owner_id` filter); no test covers a foreign owner | Load the order scoped to the current user; add a test for a foreign owner expecting 404 |

- **ID:** `BH-NN` in the Code Writer's working notes and hand-off; `RV-NN` in the review report (`review-workflow`).
- **Pass:** `2 bug-hunt`.
- **Problem:** One sentence naming the defect, not the fix.
- **Failure scenario / evidence:** The `given → when → then` line with concrete values, followed by the traced path or read-only command with exit code and key output. For dimension 7, name the missing test.
- **Fix direction:** What must change, not the replacement code itself.

End with the mandatory summary line from [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md):

```text
bug-hunt: 1 CONFIRMED, 1 PLAUSIBLE (effort standard) — dimensions 1-7
bug-hunt: no defect found (effort quick) — dimensions 1-4 on changed hunks
```

"No defect found" is a valid result. Cleanups without a failure go below the table as `NOTE: <path:line> — <cleanup>` for `code-simplification`; they never block and never count toward the cap (`H14`).

---

## 4. Verdict Impact and Role Duties (`H12`, `H13`)

### 4.1 What Findings Do to the Verdict (`H12`)
- **`CONFIRMED` `BLOCKER` or `MAJOR`:** Blocks approval (`REQUEST_CHANGES`), even when every rubric axis of `{{slot:code-review}}` passes.
- **`PLAUSIBLE` `BLOCKER`:** Makes the verdict `BLOCKED` until the named evidence is supplied (e.g., a test against PostgreSQL or verification of production column nullability).
- **Other `PLAUSIBLE` findings:** Go to the Code Writer as questions in the review report; they do not block alone.
- **`MINOR` findings:** Listed and fixed in the same revision when cheap and inside the phase scope; do not block alone.

### 4.2 Reviewer (`H13`)
- Runs this skill as Pass 2 of `review-workflow` at `standard` (or `deep` when Backend triggers apply), cold, before reading the hand-off's Concerns and specification documents.
- Stays strictly read-only toward application code, tests, migrations, and databases; writes findings only into `reviews/review_<phase-id>_<REVIEW_REVISION>.md` as `RV-NN` rows.
- Re-judges a `DISPUTED` finding on the evidence given (`review-resolution`); keeps its ID or withdraws it with the reason.

### 4.3 Code Writer (`H13`)
- Runs this skill at `quick` on its own phase diff after targeted checks pass and before `READY_FOR_REVIEW` (`incremental-implementation`).
- For each `CONFIRMED` finding: writes the reproducing test first (`{{slot:unit-testing}}`), fixes inside the approved Scope / Files at the root (`{{slot:root-cause-debugging}}`), re-runs affected checks, and records evidence rows.
- Lists remaining `PLAUSIBLE` findings as Concerns in `writer-handoff.md` with what would confirm them, and writes the `bug-hunt:` summary line there.
- A fix that changes behavior, an API contract, a migration plan, or the design goes back to Planning as a `PCR-NN` (`change-control`) instead of being made in place.
