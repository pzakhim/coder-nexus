# 03 — Effort, severity and report

The Code Writer and the Reviewer use one scale and one row format, so a finding can be acted on, copied into the review report and compared across rounds without re-wording.

## Effort and cap

Pick the effort and its cap from [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md) → "Bug-hunt effort"; the dimensions each effort covers and the Backend `deep` triggers are in [SKILL.md](../SKILL.md#effort). Reason: effort matched to risk keeps a small item fast and a migration or auth change thorough.

When the cap is reached, keep the most severe findings and say in the summary line that the cap cut the list; do not silently drop findings.

## Severity and confidence

Grade with the defect scale of [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md): `BLOCKER` / `MAJOR` / `MINOR` with `CONFIRMED` / `PLAUSIBLE`. Do not invent another level or soften one to end a round. Backend readings of that scale, as calibration only:

| §9 severity | Typical Backend case |
|---|---|
| `BLOCKER` | User B reads or edits user A's row; a migration drops or rewrites data; a missing `await` means the write never happens; partial commit across tables; a request hangs the event loop on a normal path |
| `MAJOR` | 500 instead of 404 / 409 on a realistic edge (missing row, duplicate, concurrent edit); last page repeats or skips rows; session or `httpx` client leaked on the error path; naive vs aware datetime crash for a valid input |
| `MINOR` | Wrong result only in a rare or self-correcting case, for example a cache entry that is stale until its short TTL expires |

A rule violation without wrong behavior is not this skill's finding; it is graded `P1`–`P3` by the rubric pass (`{{slot:code-review}}`, `clean-code`).

## Finding row

Order: most severe first, `CONFIRMED` before `PLAUSIBLE`. The columns are the review report's findings table ([handoff-and-status](../../work-item-contract/references/handoff-and-status.md) §5), so the Reviewer copies a row unchanged and only replaces the ID with `RV-NN`:

| ID | Pass | Severity | Confidence | File:line | Problem | Failure scenario / evidence | Fix direction |
|---|---|---|---|---|---|---|---|
| `BH-01` | 2 bug-hunt | `BLOCKER` | `CONFIRMED` | `app/orders/router.py:58` | `get_order` filters by `Order.id` only; no owner check | given order 42 owned by A → when B calls `GET /orders/42` → then 200 with A's order; traced route → `OrderRepository.get` (no `owner_id` filter); no test covers a foreign owner | Load the order scoped to the current user; add a test for a foreign owner expecting 404 |

- **ID** — `BH-NN` in the Code Writer's working notes and hand-off; `RV-NN` once in the review report (`review-workflow`).
- **Pass** — `2 bug-hunt`, the review pass that produced it.
- **Problem** — one sentence naming the defect, not the fix.
- **Failure scenario / evidence** — the `given → when → then` line with concrete values, then the traced path or the command with exit code and key output. For dimension 7, add the missing test ("no test covers …").
- **Fix direction** — what must change, not the code itself. Reason: the Code Writer owns the fix and may find a better one inside the scope.
- **File:line** — the line on `REVIEW_REVISION`; `app/…` paths above are conventions.

## Summary line

End with the line from [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md) → "Rows", followed by the dimensions covered, so a reader sees how far the hunt went:

```
bug-hunt: 1 CONFIRMED, 1 PLAUSIBLE (effort standard) — dimensions 1-7
bug-hunt: no defect found (effort quick) — dimensions 1-4 on changed hunks
```

"No defect found" is a valid result. Reason: padding the list with style remarks to look thorough hides the next real defect.

## Notes

Cleanups without a failure go below the table as `NOTE: <path:line> — <cleanup>` for `code-simplification`. They never block and never count toward the cap.
