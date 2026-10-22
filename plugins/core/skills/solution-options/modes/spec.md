# Mode: Spec Writer (behavior and scope options)

Owner: `spec_writer`. Output: one `Q-NN` (`Owner: spec_writer`) → `D-NN` that `requirements.md` cites.

## When

After the goal question is answered (`requirements.md` → `## 0. Goals` is `CONFIRMED`) and the 1B draft exists, before 0 `OPEN` rows remain. Ask it in the `grilling` §2.2 order of its dimension (usually scope, then workflow or rules), so a scope choice is settled before the questions it would remove.

## What counts as an option here

Only what the actor or the business would notice:

| Topic | Example of real options |
|---|---|
| Scope slice | Ship the whole goal now / ship the read-only part first and edit later |
| Rule behavior | Block the action / allow it with a warning / allow it and flag for review |
| Actor and permission | Only the owner / owner and manager / anyone in the team |
| Edge behavior | Keep the draft on failure / discard it and show the error |
| Data source (business view) | Use the existing backend data now / wait for the new API (`BE_API_READY` vs `MOCKOON_MOCKED` stays a separate fact check) |

Not here: storage, libraries, endpoints, payload shapes, state management, folders, components. Those are `planning` options at Gate 2. Workflow step and screen shapes are `designer` options when the item has UI impact; queue them with `Owner: designer`.

## Cost without guessing

When options differ mainly in build cost or risk you cannot judge from the sources, ask the coordinator to consult `planning` (or `code_writer`) before you present them, and record the answer in `codebase-notes.md` → `## 3. Verified Baseline Facts & Cross-Agent Notes`. Never invent effort or risk. Reason: the user picks on the trade-offs you show; a guessed cost turns into a wrong decision.

## Describe in the user's words

Each option says what the actor can do, what they see when it fails, which `G-NN` it meets fully or partly, and what moves out of scope. No class, file or endpoint names (`requirements.md` stays business language).

## After the choice

- `BR-NN`, scope lines and `AC-NN` cite the new `D-NN`. Items the chosen option leaves out go to Non-goals.
- A choice that narrows a goal reopens the goal question.
- Rejected options appear only in `Options Considered`.
