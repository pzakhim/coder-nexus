# 04 — Stop criteria

Rule SM8. Reason: knowing when not to simplify protects behavior and approved decisions as much as the techniques do; past these points the change is design work that needs `change-control`.

Stop simplifying when:

| Situation | Do instead |
|---|---|
| Behavior, an endpoint's request/response schema, a status code, an exception type or a DB schema would change | Stop; it is a contract change: `change-control` and the approval gate. API shape belongs to `api-contract-design` |
| A `D-NN` or a `{{slot:clean-architecture}}` port requires the abstraction | Leave it; mention it in the hand-off's Concerns if it looks unnecessary |
| The gain is cosmetic (renaming taste, reordering imports ruff already sorts, quote style) | Leave it |
| A hot path (query count, eager vs lazy loading, `await` points, batching) would change without a measurement | Measure first (query log, timing in an integration test) or leave it |
| The next step needs code outside the diff | Record a separate item in Concerns |
| An Alembic revision that already ran outside a local database would be edited | Leave it; a new revision is planned work |
| A guard from `{{slot:secure-coding-standards}}` would be removed or merged away | Leave it |
| Checks turn red and the cause is not obvious | Revert the last step; do not debug a refactor |
| No named smell remains | Stop and report |
