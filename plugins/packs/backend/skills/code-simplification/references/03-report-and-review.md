# 03 — Report & Review Severity

Rule S14 and the review severity. Reason: one line of what was cut lets reviewers see intent, skipped findings stay visible, and named shortcuts do not silently become permanent.

## 1. Report line (in the Code Writer hand-off)

Use the `simplify:` line defined in [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md) exactly; it is not redefined here. Illustrative filled example:

```
simplify: needless indirection -> inline at app/orders/service.py:42; N+1 query -> batched select at app/orders/repository.py:88; net -31 lines; checks: pytest tests/unit/orders -q exit 0
```

When nothing qualified, use the §9 "nothing worth changing" form and list the files looked at. One line per task or phase, next to the `bug-hunt:` line.

## 2. Skipped findings

A finding whose fix would change behavior or needs code outside the diff is **not applied**. List it in the hand-off's Concerns:

```
<lens>/<tag> at <path:line>: <why skipped>
```

Example: `altitude/generalize at app/api/deps.py:30: special case for /orders/export belongs in the shared dependency, outside this phase's diff`.

## 3. Deliberate shortcuts

A shortcut kept on purpose (a simple implementation with a known limit) is named in the hand-off with its limit and upgrade path, for example "in-memory filter, fine below ~1k rows; move to a `WHERE` clause when the list is paginated". Reason: without the limit it silently becomes permanent. The workspace may add a code-comment marker convention; none is imposed here.

## 4. Review severity (`BLOCKER` / `MAJOR` / `MINOR`)

Graded on the unified scale of `shared_contracts/flags_and_statuses.md` §2, with verdict impact from [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md):

| Severity | Finding | Review Verdict Impact |
|---|---|---|
| `BLOCKER` | A check `FAIL`s after simplification; wrapper, alias or re-export left after a move (`{{slot:clean-code}}` C1); S12 violated; a `D-NN` ignored | `CHANGES_REQUESTED` |
| `MAJOR` | Unnecessary complexity in the diff with a named catalog row (any lens) | Fixed in the same revision when inside the phase's scope |
| `MINOR` | Small, local simplification opportunity | Optional; never blocks |

A "simplification" that changed a result, status code, transaction or error path is a **defect** (severity + `CONFIRMED`/`PLAUSIBLE` + failure scenario), not a simplification finding.

Only code changed in the phase is graded; complexity outside the diff is a note in Concerns, never a finding.
