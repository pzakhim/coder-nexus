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

## 2. Format (2-Channel Contract)

Every item is a frontier row: its prerequisites are already decided, and its answer does not depend on another item in the same batch. Keep the numbered default list strictly in **Channel 1 (Session chat `content`)** — never stuff the list into `ask_question`:

**Channel 1 — Session chat (`content`):**
```markdown
### Q-11..Q-14 · câu 6/12 · Low-Risk Defaults to Confirm

| # | Queue ID | Proposed Default | Source / Basis |
|---|---|---|---|
| 1 | `Q-11` | Empty list text: `"Chưa có phiếu nào"` | Same as `S-04` list |
| 2 | `Q-12` | Default sort: newest first | PO doc §2 |
| 3 | `Q-13` | Date format: `dd/MM/yyyy` | Codebase convention |
| 4 | `Q-14` | Search clears on leaving the screen | Sibling screens do this |
```

**Channel 2 — `ask_question` tool (1 short confirmation line, unnumbered options, `(Recommended)` prefix on option 1, no manual `"Other"` / `"Change items: …"` — Antigravity's UI adds `"Other"` automatically):**
- **Question**: `"[Q-11..Q-14 · câu 6/12] Confirm the low-risk defaults listed above?"`
- **Options**:
  - `(Recommended) Confirm all defaults`
  - `Review one by one`

## 3. Closing

- `(Recommended) Confirm all defaults` (or `"yes"`) → each item becomes its own `D-NN`, marked `(default accepted)`.
- User picks the UI's automatic `"Other"` option and names specific items to change → changed items record `(user choice)`; the rest close as `(default accepted)`.
- `Review one by one`, or a weak reply (`"ok, maybe"`) → split the batch and ask the items singly in queue order.
- Recount `câu i/N` afterwards.
