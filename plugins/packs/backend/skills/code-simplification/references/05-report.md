# 05 — Report and review

Rule SM13 and the review severity. Reason: one line of what was cut lets reviewers see intent, and named shortcuts do not silently become permanent.

## Report line (in the Code Writer hand-off)

Use the `simplify:` line defined in [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md) exactly; it is not redefined here. Illustrative filled example:

```
simplify: needless indirection -> inline at app/orders/service.py:42; dict as record -> frozen dataclass at app/orders/pricing.py:18; net -31 lines; checks: pytest tests/unit/orders -q exit 0
```

When nothing qualified, use the §9 "nothing worth changing" form and list the files looked at. One line per task or phase, next to the `bug-hunt:` line.

## Deliberate shortcuts

A shortcut kept on purpose (a simple implementation with a known limit) is named in the hand-off with its limit and upgrade path, for example "in-memory filter, fine below ~1k rows; move to a `WHERE` clause when the list is paginated". Reason: without the limit it silently becomes permanent. The workspace may add a code-comment marker convention; none is imposed here.

## Review severity

Graded on the rule-violation scale of [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md), with verdict impact from the same section:

| Finding | Severity |
|---|---|
| Unnecessary complexity in the diff (catalog row present) | `P2` (`P3` if small); does not block alone |
| Wrapper, alias or re-export left after a move (`{{slot:clean-code}}` wrapper and alias rules), SM7 violated, or a `D-NN` ignored | `P1` |
| A "simplification" that changed a result, status code, transaction or error path | A defect (`BLOCKER` / `MAJOR` / `MINOR` + confidence), not a `P` finding |

Only code changed in the phase is graded; complexity outside the diff is a note, never a finding.
