# Mode: spec — business dimensions (`spec_writer`, Gate 1)

Use with [SKILL.md](../SKILL.md). The workspace's own question bank, if any, lives in `.agents/skills/requirements-specification/`; read it first and ask in its terms.

## 1. Dimensions to cover

Walk each dimension against the draft and queue a `Q-NN` for every gap the sources leave open. Mark a dimension `N/A` with a reason instead of skipping it silently.

| Dim | Dimension (asked inside the SKILL §2.2 groups) | Settle |
|---|---|---|
| A | Scope and data/API source | In-scope vs out-of-scope; `BE_API_READY` vs `MOCKOON_MOCKED` for an API consumer; endpoint or payload mismatches. |
| B | Happy path and observable states | Primary actor flow; for UI the 4 states (`Default/Content`, `Loading`, `Empty`, `Error`), asked by `designer` when there is UI impact; for a service, the contract responses (stack rules). |
| C | Inferences | Every point inferred from existing flows or a partial prompt. |
| D | Negative, boundary and edge cases | Validation errors, timeouts, duplicate requests or clicks, empty lists, unauthorized states. |
| E | Multi-step, state or transaction lifecycle | Navigation/back and state retention (UI); transaction boundaries and rollback (service); list or cache refresh after a mutation. |

## 2. Clarify groups

| Group | Clarify | Owner |
|---|---|---|
| Data / API | Source (`BE_API_READY` / `MOCKOON_MOCKED`), API count and field gaps against the flow (e.g. the flow needs 4 APIs, the request names 3), payload, nullability, errors. `N/A` with reason when there is no network. | `spec_writer` |
| Business / State | Actor, permission, trigger, transitions, overlapping rules, duplicate actions, unhappy paths. | `spec_writer` |
| UI / Variant | Design-export source, visual tokens, kit candidates and verified APIs (`{{slot:core-package-usage}}`). | `designer` (choice between viable kit matches: `planning`) |
| UX / Quality | Loading, empty, error, disabled, input retention, accessibility, Visual AC. | `designer` when UI, else `spec_writer` |
| Integration | Owner module, changes to the current business flow, DI, router, affected consumers, regression risk. | `planning` (spec_writer consults through the coordinator) |

## 3. Multi-screen or multi-step flows

Resolve each axis or mark it `N/A` with a reason: state ownership, navigation/back, unhappy paths, inter-field dependencies and validation timing, step-up security, post-flow effects (notifications, status changes, refreshed lists).

## 4. Role rules

- Own `requirements.md` (human-facing, about 120 lines, business/UX language, every `BR-NN` cites a `D-NN`, no code, class or node names) and `codebase-notes.md` (agent-facing source of truth).
- Every `Q-NN` names the `G-NN` it serves; a question that serves no goal is out of scope (note it as a non-goal, do not ask it).
- Never invent a codebase fact. A question that needs deep architecture or implementation inspection goes to `planning` or `code_writer` through the coordinator; record their verified answer in `## 3`.
- Unknown external contracts stay `BLOCKED` until a source or the owner answers ([questionnaire](questionnaire.md)).
- Close with `validate_proposal_spec` on both files (REQ-001..006, NOTES-000..005) before the Gate 1 question.
