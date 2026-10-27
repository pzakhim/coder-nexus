# 03 — Severity, Verdict Impact, and Reporting

> Topic: Effort caps, unified BLOCKER/MAJOR/MINOR calibration, finding table format, verdict impact, and role duties (`H9`–`H14`)

The Code Writer and the Reviewer use one scale and one row format, so a finding can be acted on, copied into the review report, and compared across rounds without re-wording.

## 1. Effort and Cap (`H10`)

Pick the effort and its cap from [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md) → "Bug-hunt effort"; the dimensions each effort covers and the Flutter `deep` triggers are in [SKILL.md](../SKILL.md#3-effort--flutter-deep-triggers).

When the cap is reached, keep the most severe findings and state in the summary line that the cap truncated the list; do not silently drop findings.

---

## 2. Unified Severity and Confidence (`H9`)

Grade with the unified 3-tier defect scale of [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md): `BLOCKER` / `MAJOR` / `MINOR` with `CONFIRMED` / `PLAUSIBLE`. Do not invent another level or soften one to end a round.

| Severity | Typical Flutter Calibration |
|---|---|
| `BLOCKER` | Runtime crash (`NullCheckError`, `_TypeError` in `fromJson`, `FlutterError: setState() called after dispose()`, unbounded viewport crash) on a normal or realistic edge path; silent failure where a failed save/payment appears to succeed; stale user/tenant cache served after logout; auth token or secret leaked in plaintext storage/logs; broken approved AC behavior |
| `MAJOR` | UI stuck in infinite loading spinner when an API call fails; `Cubit` emitting mutated state reference so UI fails to rebuild; undisposed `Controller` / `StreamSubscription` / `Timer` memory leak; duplicate mutation on rapid taps; `RenderFlex` layout overflow clipping action buttons or data on target phone/tablet viewports |
| `MINOR` | Rare edge-case visual glitch or stale state that self-corrects on the next frame/refresh without data loss or crash |

A rule violation without wrong runtime behavior is not a `bug-hunt` finding; it belongs to the rubric pass (`{{slot:code-review}}`, `{{slot:clean-code}}`) under the same unified `BLOCKER` / `MAJOR` / `MINOR` scale.

---

## 3. Finding Row Format & Summary Line (`H11`, `H14`)

Order: most severe first, `CONFIRMED` before `PLAUSIBLE`. The columns match the review report's findings table ([handoff-and-status](../../work-item-contract/references/handoff-and-status.md) §5), so the Reviewer copies a row unchanged and only replaces the ID with `RV-NN`:

| ID | Pass | Severity | Confidence | File:line | Problem | Failure scenario / evidence | Fix direction |
|---|---|---|---|---|---|---|---|
| `BH-01` | 2 bug-hunt | `BLOCKER` | `CONFIRMED` | `lib/modules/orders/data/models/order_model.dart:28` | `OrderModel.fromJson` casts `json['total'] as double`, crashing when backend sends an integer amount | given payload `{"id": "1", "total": 100}` → when `OrderModel.fromJson` parses the response → then throws `_TypeError: type 'int' is not a subtype of type 'double'`; no unit test covers integer JSON numbers | Parse numeric JSON fields safely via `num` or the workspace's safe double parser; add a `fromJson` unit test with integer `total` |

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

"No defect found" is a valid result. Cleanups without a failure (e.g., missing `const` or helper extraction) go below the table as `NOTE: <path:line> — <cleanup>` for `code-simplification`; they never block and never count toward the cap (`H14`).

---

## 4. Verdict Impact and Role Duties (`H12`, `H13`)

### 4.1 What Findings Do to the Verdict (`H12`)
- **`CONFIRMED` `BLOCKER` or `MAJOR`:** Blocks approval (`REQUEST_CHANGES`), even when every rubric axis of `{{slot:code-review}}` passes.
- **`PLAUSIBLE` `BLOCKER`:** Makes the verdict `BLOCKED` until the named evidence is supplied (e.g., verifying the backend's actual JSON field nullability or running a widget test at the target viewport).
- **Other `PLAUSIBLE` findings:** Go to the Code Writer as questions in the review report; they do not block alone.
- **`MINOR` findings:** Listed and fixed in the same revision when cheap and inside the phase scope; do not block alone.

### 4.2 Reviewer (`H13`)
- Runs this skill as Pass 2 of `review-workflow` at `standard` (or `deep` when Flutter triggers apply), cold, before reading the hand-off's Concerns and specification documents.
- Stays strictly read-only toward application code, generated files, and tests; writes findings only into `reviews/review_<phase-id>_<REVIEW_REVISION>.md` as `RV-NN` rows.
- Re-judges a `DISPUTED` finding on the evidence given (`review-resolution`); keeps its ID or withdraws it with the reason.

### 4.3 Code Writer (`H13`)
- Runs this skill at `quick` on its own phase diff after targeted checks pass and before `READY_FOR_REVIEW` (`incremental-implementation`).
- For each `CONFIRMED` finding: writes the reproducing unit/cubit/widget test first (`{{slot:unit-testing}}`), fixes inside the approved Scope / Files at the root (`{{slot:root-cause-debugging}}`), re-runs affected checks, and records evidence rows.
- Lists remaining `PLAUSIBLE` findings as Concerns in `writer-handoff.md` with what would confirm them, and writes the `bug-hunt:` summary line there.
- A fix that changes behavior, an API contract, or the approved UI/architecture design goes back to Planning as a `PCR-NN` (`change-control`) instead of being made in place.
