# Mode: batch-confirm — several low-risk inferences in one question

Use with [SKILL.md](../SKILL.md). This is the only exception to "one question per `ask_question` call". Use it at most once per round, after the higher-risk rows are closed, so it never hides a real decision.

## 1. What may be batched

| Allowed | Never batched |
|---|---|
| Wording, labels, messages already used by sibling screens | Business rules |
| A default the sources strongly imply (one reading only) | Permissions and data scopes |
| A convention already used in the codebase (verified fact behind it) | Money, prices, quantities that drive money |
| Test data rows that only restate the requirements (planning) | Data loss, deletion, irreversible actions |
| Display order, formatting, empty-state text | API contracts (request, response, error codes) |

If any item in the batch touches the right-hand column, take it out and ask it alone. Reason: a "yes" to a list is skimmed; risky items need their own attention.

## 2. Format

Every item is a frontier row: its prerequisites are already decided, and its answer does not depend on another item in the same batch. Word each item so "yes" accepts the recommendation.

```text
Q-11..Q-14 · câu 6/12 · Confirm low-risk defaults
Reply "yes" to accept all recommendations, or name the items to change.
  1. Q-11 Empty list text: "Chưa có phiếu nào"        (same as S04 list)
  2. Q-12 Default sort: newest first                     (source: PO doc §2)
  3. Q-13 Date format: dd/MM/yyyy                        (codebase convention)
  4. Q-14 Search clears on leaving the screen            (sibling screens do this)
Options: Confirm all (Recommended) / Review one by one / Change items: …
```

## 3. Closing

- "yes" or `Confirm all` → each item becomes its own `D-NN`, marked `(default accepted)`.
- Items the user changes → that item's answer is recorded as `(user choice)`; the rest close as above.
- `Review one by one`, or a weak reply ("ok, maybe") → split the batch and ask the items singly in queue order.
- Recount `câu i/N` afterwards.
