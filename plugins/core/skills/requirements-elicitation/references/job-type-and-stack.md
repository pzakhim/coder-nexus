# Job type, stack and size (Stage 1A-0)

## Job type

The 8 work-item Types are canonical: `feature`, `bugfix`, `refactor`, `optimization`, `migration`, `maintenance`, `investigation`, `documentation`. The job-type question uses everyday words and maps each answer onto a Type. Read `status` and `status_category` of the ticket (and of each in-scope child).

| Ticket state | Example statuses | Ask | Answer → Type and path |
|---|---|---|---|
| Not started | Backlog, Todo | No question. Classify the Type from the sources and state it in the goal question so the user can correct it. | The classified Type, new work item |
| In progress | DEV IN PROGRESS | Continue the existing work, or restart? | **continue** → same Type, the existing `vN` goes on. **restart** → same Type, `vN+1` from Gate 1 (see `work-item-contract`); what happens to the unfinished code is a `Q-NN`. |
| Built or later | Dev Done, QA/QC ..., Prod ..., RESOLVED, Done | Is this a change, a bug fix, a verification, or documentation? | **change** → `feature` (observable behavior changes) or `refactor` (behavior stays), as a new `vN` with `change-impact.md` against the built code. **bug fix** → `bugfix` sequence. **verification** → `investigation` that writes findings only to `verification.md`, no code. **documentation** → `documentation`, handed to Docs Writer. |
| Closed | Canceled / LOST category | Confirm the user really wants to work on a canceled ticket. | Then as above |

The answer is the first `D-NN` of the work item; it selects the sequence in `work-item-contract` → type sequences. Ask it on its own, before the goal question, because the goals of a verification and of a change are different goals.

## Stack check

Compare the stack each part needs with the packs in `.agents/stack.json`. Clues: ticket text, title, documents, comments, diagrams (a named runtime, platform or service kind). A part whose stack has no installed pack is `BLOCKED — out of plugin scope`:

- Tell the user which part is blocked and why (ticket ID, the stack it needs, "no pack installed").
- Write no requirements, design or plan for it, and do not guess its code. List it under Non-goals with the reason.
- Supported parts continue. If only blocked parts remain, stop with `BLOCKED`.

## Size the work

Say how big the work is in plain words inside the goal question; the user can override it with Edit.

| Size | Signal | Artifacts |
|---|---|---|
| Small | Not a `feature`; one checked result, no phase depends on another, no new behavior contract to approve | `brief.md` (phase-free path of `work-item-contract`), with its goal line confirmed by the same `D-NN` |
| Work item | Any `feature`, or several dependent results | `requirements.md` + `codebase-notes.md`, Gates 1/2/3 as the Type requires |
| Several work items | AC split into groups that ship and are checked on their own | Propose linked work items ([split check](goal-candidates.md#split-check)) |

If the work grows later (a second dependent result, a new behavior contract), say so, record a `D-NN` and move up a size; never stretch `brief.md` past its purpose.
