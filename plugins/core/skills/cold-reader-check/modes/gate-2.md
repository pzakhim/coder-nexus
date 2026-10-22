# Gate 2 — reader plays Code Writer

Author: `planning`. Gate document: `design.md`. Context (already approved at Gate 1): `requirements.md`, `codebase-notes.md`, and `design-uiux/uiux.md` when it exists.

## What a good question looks like here

The reader must be able to build from the design without inventing a contract or a structure. Typical gaps worth reporting:

- a contract (signature, payload, status or error mapping) referenced but not defined;
- a folder, class or component named in one section and missing or different in another;
- a state, transition or data flow step the design leaves open;
- an `S-NN` or `C-NN` in `uiux.md` with no entry in `## UI/UX mapping`, or a mapping that cannot be built as drawn;
- a goal in `## Goal alignment` with no design element that delivers it;
- test data (Pass / Default, Fail, Empty) the design relies on but does not state;
- an error or storage policy that two developers would implement differently.

## Prompt shape

```text
You are the Code Writer of this team. You have been handed the approved
technical design of a work item and must next build it, phase by phase.
You cannot talk to the person who wrote it, and you have no other context.

Read the document under review:
- {{vN_path}}/design.md

Already approved context (do not question it unless design.md contradicts it):
- {{vN_path}}/requirements.md
- {{vN_path}}/codebase-notes.md
- {{vN_path}}/design-uiux/uiux.md   (only if it exists)

You may open files these documents cite by path, read-only, only to check that
a cited path, class or component exists. Do not use the codebase to fill a gap
the design leaves. Do not write or change any file.

Report only the questions you would still need answered before you could
build this without guessing: places where you would have to invent a
contract, a structure, a state, an error mapping or test data, and a wrong
guess would matter.
For each question give:
1. the question,
2. where it comes from (design.md section, D-NN, AC-NN, S-NN / C-NN),
3. why the answer changes what you build,
4. what you would guess if forced.
Rank them by importance, at most 10.

Skip anything the design explicitly leaves to the Code Writer, naming and
formatting choices you can make yourself, and wording nits.
If nothing important is left, answer exactly: nothing important left
```
