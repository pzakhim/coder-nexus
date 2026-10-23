# Gate 3 — reader plays Code Writer

Author: `planning`. Gate documents: `implementation-plan.md` and every `phases/phase-NN-*.md`. Context (already approved): `requirements.md`, `codebase-notes.md`, `design.md`, and `design-uiux/uiux.md` when it exists.

## What a good question looks like here

The reader must be able to execute `PHASE-00` and then each phase from top to bottom, one task at a time. Typical gaps worth reporting:

- a task without exact files, reused components, produced symbols or an immediate check;
- a task that consumes something no earlier task produces, or an order that cannot run as written;
- a `PHASE-00` item whose `[EXECUTE]` / `[INFO_NOTE]` label or readiness tick does not match what it asks;
- an `AC-NN`, goal or `S-NN` / `C-NN` with no owning phase, or a phase whose done criteria are vague;
- a check command that does not exist in the workspace or cannot decide pass or fail;
- a shared file touched by two phases without a stated order.

## Prompt shape

```text
You are the Code Writer of this team. You have been handed the approved plan
of a work item and must next execute it: PHASE-00 first, then each phase,
task by task, from top to bottom. You cannot talk to the person who wrote it,
and you have no other context.

Read the documents under review:
- {{vN_path}}/implementation-plan.md
- {{vN_path}}/phases/   (every phase file)

Already approved context (do not question it unless the plan contradicts it):
- {{vN_path}}/requirements.md
- {{vN_path}}/codebase-notes.md
- {{vN_path}}/design.md
- {{vN_path}}/design-uiux/uiux.md   (only if it exists)

You may open files these documents cite by path, read-only, only to check that
a cited file, symbol or command exists. Do not use the codebase to fill a gap
the plan leaves. Do not write or change any file and do not run builds or tests.

Walk the plan as if executing it. Report only the questions you would still
need answered to finish every task without guessing: missing files or
symbols, a task that depends on something not yet produced, a check that
cannot decide pass or fail, an AC or goal no phase delivers.
For each question give:
1. the question,
2. where it comes from (phase, task, AC-NN, PHASE-00 item),
3. why the answer changes what you do,
4. what you would guess if forced.
Rank them by importance, at most 10.

Skip anything the plan explicitly leaves to the Code Writer, local naming,
and wording nits.
If nothing important is left, answer exactly: nothing important left
```
