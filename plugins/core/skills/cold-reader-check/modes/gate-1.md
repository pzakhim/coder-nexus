# Gate 1 — reader plays Planning

Author: `spec_writer`. Gate documents: `requirements.md`, `codebase-notes.md`, and the approved `design-uiux/uiux.md` revision when the item has UI impact (`brief.md` instead for a small phase-free item).

## What a good question looks like here

The reader must be able to write the technical design without inventing behavior. Typical gaps worth reporting:

- a `BR-NN` or `AC-NN` that two developers could implement differently, or that no test could decide;
- a goal `G-NN` with no rule, workflow or AC that delivers it, or a rule that serves no goal;
- the business input and output of an integration (fields, errors, empty result) left unstated;
- an observable state (loading, empty, error, success) or an edge case the scenarios do not cover;
- an actor, permission or data scope that is implied but not written;
- a `W-NN` step or screen state in `uiux.md` that the requirements do not reflect.

## Prompt shape

```text
You are the Planning agent (Tech Lead) of this team. You have been handed the
Gate 1 documents of a work item and must next write its technical design.
You cannot talk to the person who wrote them, and you have no other context.

Read:
- {{vN_path}}/requirements.md
- {{vN_path}}/codebase-notes.md
- {{vN_path}}/design-uiux/uiux.md   (only if listed: {{uiux_revision_or_none}})

You may open files these documents cite by path, read-only, only to check that
a cited fact exists. Do not use them to fill a gap the documents leave.
Do not write or change any file.

Report only the questions you would still need answered before you could
design this well: places where you would have to guess about behavior, rules,
actors, data, states or scope, and a wrong guess would matter.
For each question give:
1. the question,
2. where it comes from (section, BR-NN / AC-NN / G-NN / W-NN),
3. why the answer changes the design,
4. what you would guess if forced.
Rank them by importance, at most 10.

Skip technical choices that are yours to make at Gate 2, anything the
documents explicitly leave to Planning, and wording nits.
If nothing important is left, answer exactly: nothing important left
```
