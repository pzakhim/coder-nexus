---
name: bug-hunt
description: Finds real defects in a fixed code revision — each finding names a concrete failure scenario and survives an adversarial verification pass before it is reported. Use as the Reviewer's first pass on every code phase or small item, and as the Code Writer's self-check before READY_FOR_REVIEW. Complements the compliance checks of the stack's review skill; it does not replace them.
---

# Bug Hunt

Answer one question: **with which input or state does this change produce a wrong result, a crash, a leak or a security hole?** Approval-gate, AC-traceability and architecture-profile checks belong to `{{slot:code-review}}`; complexity belongs to `code-simplification`. Do not mix them into this pass.

## 1. Fix the scope

- Record `BASE_REVISION`, `REVIEW_REVISION` and the staged, unstaged and untracked files that belong to the item. Review exactly that tree.
- Read every changed hunk with its whole enclosing function or class, not the hunk alone.
- For each changed public symbol (signature, return type, nullability, thrown/returned errors, state shape, route, JSON key), list its callers with `rg -n "<symbol>" <path>` and read them. A broken caller outside the diff is in scope.

## 2. Cold pass first

Hunt from the code before reading `requirements.md`, `design.md` or the phase plan, so the writer's intent does not hide what the code actually does. Read the documents afterwards only to decide whether a suspicious behavior is intended (`D-NN`) or a defect.

## 3. Generate candidates

Walk the scope once per dimension and write down every suspicion as a candidate (file, line, one-line hypothesis):

1. **Logic and data flow**: wrong condition or operator, off-by-one, inverted flag, wrong variable, lost or overwritten value, unit/timezone/rounding mismatch.
2. **Error and edge paths**: null or missing key, empty collection, first/last page, failure response, timeout, retry, partial success, validation bypass.
3. **State, async and lifecycle**: ordering of awaited calls, stale response overwriting a newer one, double submit, use after dispose/close, unreleased resource, shared mutable state.
4. **Contract and caller breakage**: callers from step 1 that now receive a different type, null, error or state; serialized keys or endpoints that no longer match the other side.
5. **Security and data safety**: missing authorization on the object, injection, secrets or personal data in logs, unsafe parsing that silently substitutes data.
6. **Stack bug patterns**: every applicable item in the bug-pattern reference of `{{slot:code-review}}`. A stack without that reference records dimension 6 as `N/A` with the reason; the other dimensions still run.
7. **Test blind spots**: for each surviving candidate, check whether an existing test would fail if the defect is real. A defect with no failing test is still a defect; also record the missing test.

Cleanups (reuse, simplification, efficiency without a failure) are not candidates here. List them, if worth it, as `NOTE` lines for `code-simplification`; they never block.

## 4. Verify every candidate adversarially

For each candidate, try to **disprove** it before keeping it:

- Trace the real path from an entry point (screen action, endpoint, use case) to the line. Read guards, callers, defaults and framework behavior on the way; do not assume.
- Write the failure scenario as `given <input/state> → when <action> → then <observed wrong result>` with concrete values.
- Where a read-only command can decide it (an existing test, the analyzer, `git show`, a grep of callers), run it and quote the result.
- Classify:
  - `CONFIRMED`: the path is traced end to end and nothing on it prevents the failure, or a command demonstrated it.
  - `PLAUSIBLE`: the failure depends on something you could not see (runtime data, a package internals, a server response). Name exactly what would confirm it.
  - Rejected: a guard, caller contract or framework behavior prevents it. Drop it silently.

Never report a candidate without a failure scenario. "Might be fragile", "consider handling errors" and style remarks are not findings.

## 5. Rank, cap and report

Severity:

- `BLOCKER`: data loss or corruption, security hole, crash or hang on a normal path, approved AC behavior broken.
- `MAJOR`: wrong result or crash on a realistic edge path (empty, failure, retry, last page, rotation, slow network), resource leak.
- `MINOR`: wrong result only in a rare or self-correcting case.

Effort follows the item, not the reviewer's mood:

| Effort | When | Dimensions | Cap |
|---|---|---|---|
| `quick` | Small non-feature item, docs-only, Code Writer self-check | 1–4 on the changed hunks | 5 findings |
| `standard` | Every feature phase (`PHASE-01+`) | 1–7 | 10 findings |
| `deep` | Final phase before close, auth/payment/data-migration code, or a phase that already returned twice | 1–7 plus every caller one level further | No cap |

Report findings most severe first, `CONFIRMED` before `PLAUSIBLE`, using this row:

| ID | Severity | Confidence | File:line | Defect | Failure scenario | Evidence | Fix direction |
|---|---|---|---|---|---|---|---|
| `BH-01` | `MAJOR` | `CONFIRMED` | `path/file:42` | One sentence | given … → when … → then … | Traced path or command output | What must change, not the code itself |

End with `bug-hunt: <n> CONFIRMED, <m> PLAUSIBLE (effort <level>)`, or `bug-hunt: no defect found (effort <level>)` and the dimensions covered.

## 6. Verdict impact

- Any `CONFIRMED` `BLOCKER` or `MAJOR` means `CHANGES_REQUESTED`.
- A `PLAUSIBLE` `BLOCKER` means `BLOCKED` until the named evidence is supplied; other `PLAUSIBLE` findings go to the writer as questions and do not block alone.
- `MINOR` findings are listed and fixed in the same revision when cheap; they do not block alone.
- After 3 review rounds on the same phase (`review-process`) without `APPROVED`, stop the loop and escalate to the coordinator with both positions; neither agent may waive it.

## 7. Roles

- **Reviewer**: run at `standard` (or `deep`) before the stack's compliance checks. Stay read-only; write findings into the review report only, numbered `RV-NN` there (`review-process`).
- **Code Writer (self-check)**: run at `quick` on your own diff after targeted checks pass and before `READY_FOR_REVIEW`. Fix every `CONFIRMED` finding inside the approved scope, add the missing test, rerun checks, and list remaining `PLAUSIBLE` findings in the handoff. A fix that changes behavior, API or design returns to Planning.
