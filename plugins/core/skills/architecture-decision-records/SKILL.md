---
name: architecture-decision-records
description: Promotes the few confirmed D-NN decisions that are hard to reverse, surprising and a real trade-off into Architecture Decision Records in the workspace's ADR folder, with status, links back to the work item and supersede-never-delete history. Optional. Planning owns it after Gate 2; Docs Writer may use it when documenting delivered work. Never writes an ADR without the user's confirmation.
---

# Decision Records

`codebase-notes.md` `## 1. Decision Log (D-NN)` is the record of every decision in a work item, and it stays so. An ADR is a second, long-lived home for the rare decision a future reader of the **code** needs to understand without opening that work item. This skill is optional: an item with no ADR is normal and never a gate finding.

## 1. Which D-NN become ADRs

Promote a `D-NN` only when all three hold:

| Test | Question | Reason |
|---|---|---|
| Hard to reverse | Would changing it later cost real work (data migration, rewrite of many callers, a contract with another team)? | An easy-to-reverse choice is simply reversed; a record adds nothing |
| Surprising | Would a reader of the code ask "why was it done this way?" | An obvious choice explains itself |
| Real trade-off | Were there genuine alternatives, rejected for stated reasons (they are in the `D-NN` row's options)? | Without alternatives there is nothing to record |

Usually qualifies: the architecture profile or a deliberate deviation from it, how two modules or front end and back end integrate, who owns a piece of data and how others reference it, a dependency that would take long to replace, a constraint not visible in code (compliance, a partner contract, a device limit), an alternative rejected for a non-obvious reason.

Stays only in `codebase-notes.md`: business rules and UI choices of one item (`BR-NN` level), wording, field order, values that follow the existing convention, anything temporary (a mock until the API is ready).

## 2. Confirm with the user first

1. After Gate 2 is approved (or when Docs Writer closes delivered work), screen the Decision Log and list the candidates with one line per test.
2. Queue one `Q-NN` in `codebase-notes.md` (owner `planning`) and ask it through `grilling`: "Record these as ADRs?" with each candidate selectable, `(Recommended)` on the ones that pass all three tests. Reason: an ADR is a lasting repository file, so it needs the user's choice like any other `D-NN`.
3. Close it as a `D-NN` naming the confirmed ADRs. Write nothing the user did not confirm.

## 3. Where

Detect the workspace's convention before writing:

- Look for an existing folder (`docs/adr/`, `docs/decisions/`, `doc/adr/`, `docs/architecture/decisions/`, `adr/`), an `.adr-dir` file, or ADR rules in the workspace instructions.
- Follow what exists: folder, file extension, numbering and filename pattern, section headings. Continue the sequence; never start a second scheme.
- Two conventions in conflict: ask the user (a `Q-NN`), do not pick.
- None found: use `docs/adr/NNNN-kebab-title.md`, numbering from `0001`. Create the folder only when the first ADR is written.

ADRs are workspace files committed on the item branch with the work they explain; they never go under `.superpowers/work-items/`.

## 4. Format

Use the workspace's headings when it has a convention; otherwise:

```markdown
# ADR-NNNN: <decision as a short statement>

- **Status**: Proposed | Accepted | Superseded by ADR-NNNN | Deprecated
- **Date**: YYYY-MM-DD
- **Work item**: `.superpowers/work-items/<slug>/vN/` - `D-NN` (and the Gate approval reference)

## Context
Forces and constraints that made a decision necessary.

## Decision
What was decided, stated as a rule a reviewer can check.

## Alternatives
Each rejected option and the reason it lost (from the `D-NN` row).

## Consequences
What becomes easier, harder or required because of it.
```

A small ADR may be the header plus one paragraph covering context, decision and why. Status, Date and the work-item link are always present, because supersession depends on them.

## 5. Lifecycle

- Status is `Proposed` while the decision's gate is not yet approved, and `Accepted` once it is.
- Never delete an ADR or rewrite its decision. When a later `D-NN` changes it, write a new ADR that names the old one, and set the old one's Status to `Superseded by ADR-NNNN` - the only edit an accepted ADR receives.
- A decision dropped without replacement becomes `Deprecated`, with one line saying why.
- Note each ADR written or superseded in `codebase-notes.md` `## 6. Change Log` (`D-07 -> ADR-0004`). Do not add columns to the Decision Log.

## 6. Do not

- Write an ADR for every `D-NN`, or copy the Decision Log into ADRs.
- Write an ADR before the user confirms it, or with content that differs from the confirmed `D-NN`.
- Use an ADR to reopen a decision; a change goes through `Q-NN` -> `D-NN` first.

Sources and ideas not adopted: [references/sources.md](references/sources.md).
