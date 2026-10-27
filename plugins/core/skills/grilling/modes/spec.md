# Mode: Spec Writer — Business Dimensions & Scope/Behavior Options (`spec_writer`, Gate 1)

Use with [`SKILL.md`](../SKILL.md) and [`01 — Solution Options & Divergent Pass`](../references/01-solution-options-and-divergent-pass.md). If the workspace defines `.agents/skills/requirements-specification/`, read its domain question bank first and ask in its vocabulary.

## 1. Business Dimensions to Cover (`A`–`E`)

Walk each dimension against the `DRAFT` `requirements.md` and queue a `Q-NN` (`Owner: spec_writer`) for every gap the sources leave open. Mark a dimension `N/A` with a reason instead of skipping it silently.

| Dim | Dimension (ordered per `SKILL.md` §2.2) | What to Settle |
|---|---|---|
| **A** | Scope and data / API source | In-scope vs out-of-scope; `BE_API_READY` vs `MOCKOON_MOCKED` for an API consumer; endpoint or payload mismatches against the user flow. |
| **B** | Happy path and observable states | Primary actor flow; for UI items the 4 visual states (`Default/Content`, `Loading`, `Empty`, `Error`), queued as `Owner: spec_writer` via `figma-intake`; for a backend service, contract responses per stack rules. |
| **C** | Inferences | Every business rule or behavior inferred from existing flows or a partial prompt. |
| **D** | Negative, boundary, and edge cases | Validation errors, timeouts, duplicate requests/clicks, empty lists, unauthorized states. |
| **E** | Multi-step, state, or transaction lifecycle | Navigation/back and state retention (UI); transaction boundaries and rollback (service); list or cache refresh after a mutation. |

## 2. Clarify Groups & Ownership Routing

| Group | What to Clarify | Owner in Queue |
|---|---|---|
| **Data / API** | Source (`BE_API_READY` / `MOCKOON_MOCKED`), API count and field gaps against the flow (e.g., flow needs 4 APIs, ticket names 3), payload, nullability, error codes. `N/A` with reason when no network is involved. | `spec_writer` |
| **Business / State** | Actor, permission, trigger, state transitions, overlapping rules, duplicate actions, unhappy paths. | `spec_writer` |
| **UI / Workflow** | Workflow steps (`W-NN`), screen transitions (`S-NN`), 4 visual states, viewports (`figma-intake`). | `spec_writer` |
| **UI Kit / Component Choice** | Multiple viable Kit components matching one need (`{{slot:architecture-design}}`). | `planning` (Gate 2) |
| **Integration & Architecture** | Owner module, changes to current architecture, DI, routing, affected consumers, regression risk. | `planning` (`spec_writer` consults via coordinator when needed) |

For multi-screen or multi-step flows, resolve each axis or mark `N/A` with a reason: state ownership, navigation/back behavior, unhappy paths, inter-field dependencies and validation timing, step-up security, and post-flow effects (notifications, status changes, refreshed lists).

## 3. Behavior & Scope Options (`spec_writer` Solution Options)

When more than one materially different business behavior or scope slice can satisfy the confirmed `G-NN` goals, apply [`01 — Solution Options & Divergent Pass`](../references/01-solution-options-and-divergent-pass.md):

| Option Topic | Examples of Materially Different Business Options |
|---|---|
| **Scope slice** | Ship the full goal now vs. ship the read-only/core flow first and defer editing to a linked item |
| **Rule behavior** | Hard-block the action vs. allow with a confirmation warning vs. allow and flag for supervisor review |
| **Actor & permission** | Only the record owner vs. owner and line manager vs. any member of the site team |
| **Failure / Edge behavior** | Retain local draft on failure vs. discard draft and show retry banner |
| **Business data source** | Use existing backend data now vs. wait for the new API (`BE_API_READY` vs `MOCKOON_MOCKED` stays a separate fact check) |

- **Strictly business/UX language**: Describe what the actor can do, what they see when it fails, which `G-NN` it meets, and what moves out of scope. Never include class, file, database table, or endpoint names in `requirements.md`.
- **Cost without guessing**: When options differ in build effort or technical risk that `spec_writer` cannot verify from sources, ask the coordinator to consult `planning` (or `code_writer`) and record the verified fact in `codebase-notes.md` → `## 3`. Never guess technical effort.
- **After the user picks**: Cite the new `D-NN` in `BR-NN`, scope lines, and `AC-NN`; move deferred items to **Non-goals**; keep rejected options only in `Options Considered`.

## 4. Role Rules

- Own `requirements.md` (human-facing, $\le \sim 120$ lines, pure business/UX language, every `BR-NN` cites a `D-NN`, zero code/class names) and `codebase-notes.md` (permanent agent-facing SSOT).
- Every `Q-NN` names the `G-NN` it serves; any question serving no confirmed goal is out of scope.
- Close with `validate_proposal_spec` (`PASS`: `REQ-001..006`, `NOTES-000..005`, `0 OPEN Q-NN`) before presenting Gate 1.
