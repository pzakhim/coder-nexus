# Pre-flight and hand-off

Working formats for [incremental-implementation](../SKILL.md). Field names and statuses are defined in [plan-and-task contract](../../work-item-contract/references/plan-and-task-contract.md) and [hand-off and status](../../work-item-contract/references/handoff-and-status.md); this file only shows how the Code Writer fills them.

## Pre-flight table

Draft it before Task 1 in your working notes (the `REVIEW_REVISION` that names the hand-off folder does not exist yet) and copy it into `writer-handoff.md` at the end, as the first section of the hand-off. One row per edge where a task consumes something an earlier task or existing code produces. Tasks that share nothing get no row; a phase whose tasks share nothing gets the single line `Pre-flight: no shared interfaces`.

| Consumer task | Consumes (as the plan states it) | Producer (task or existing `path:symbol`) | Produces (real signature) | Finding |
|---|---|---|---|---|
| Task 2.3 | `loadOrders(ownerId) -> list of Order` | existing `orders/repository:loadOrders` | `loadOrders(ownerId, page) -> Page of Order` | Mismatch: extra `page`, different return → `PCR-01` |
| Task 2.4 | `OrderSummary` from Task 2.2 | Task 2.2 | `OrderSummary` (planned) | OK |

Also add one line per task whose own text disagrees with itself (a file it creates and later lists as existing, a check that tests a file outside its Scope / Files), and one line per task that contradicts a `## Global constraints` entry.

Read the real symbol for every "existing" producer (`rg -n "<symbol>" <path>`, then open the file). Reason: the plan was written from a scan that may be older than the branch.

## Tick line

```
- [x] **Task 2.3**: <title> - rev <short-sha>[+dirty] - `<command>` (cwd `<dir>`) - exit 0 - MATCH
```

- `rev` is the revision the check ran on. On an intermediate tick whose change is not committed yet, write `<HEAD short-sha>+dirty`. Before `READY_FOR_REVIEW` the phase is committed and the phase checks are re-run on that commit; the hand-off never cites a `+dirty` revision as `REVIEW_REVISION`.
- The tick is the short form; the same run also gets a full evidence row in `writer-handoff.md` (claim | command (+cwd) | revision | exit code | key output | result).
- Ticking is the only edit the Code Writer makes to plan files.
- Write `MATCH` only. A task that ended `CODE_WRONG` is ticked after the re-run matches; a task that ended `PLAN_WRONG` stays unticked until Planning answers.
- After an `AMENDED` answer, tick against the amended task text and cite the `## Plan change log` entry.

## Hand-off

File: `evidence/<phase-id>/<REVIEW_REVISION>/writer-handoff.md`, where `<REVIEW_REVISION>` is the committed revision handed to review. The common header is the one in [hand-off and status](../../work-item-contract/references/handoff-and-status.md) §1; the Code Writer adds:

```
Status: READY_FOR_REVIEW | BLOCKED | NEEDS_CONTEXT
Phase: PHASE-NN (<phase file>)   Branch: <branch from the git-preflight D-NN>
BASE_REVISION..REVIEW_REVISION: <base sha>..<review sha>
Pre-flight: <table above> | Pre-flight: no shared interfaces
Tasks: ticked <list>; unticked <list with reason>
Evidence: one row per task check and per phase check (claim | command (+cwd) | revision | exit code | key output | result)
Bug-hunt (quick): <CONFIRMED fixed with tests> / <PLAUSIBLE carried as Concerns>
Simplification: <removed or merged> | none (no concrete smell)
PCR raised: <PCR-NN - class - answer (AMENDED / ESCALATED / open)> | none
Concerns: <list> | none                       (READY_FOR_REVIEW only)
Tried / needed: <files read, commands run> / <exact fact or access needed>   (NEEDS_CONTEXT only)
Blocker: <what is missing, who can unblock>   (BLOCKED only)
Noticed but not touching: <path - observation> | none
```

From review round 2 on, add `## Review reply (round N)` with the per-finding reply table from `review-resolution` (reply words in [hand-off and status](../../work-item-contract/references/handoff-and-status.md) §3).

Rules:

- The review revision is the tree the reviewer reads; the Test Runner uses the reviewed revision. A later fix produces a new review revision.
- Concerns are doubts about correctness or design the reviewer should weigh; they never replace a finding fix that is inside scope.
- `NEEDS_CONTEXT` is for a missing fact (a value, an access, a contract owner). A plan defect is a `PCR-NN` with `BLOCKED`, not `NEEDS_CONTEXT`.
