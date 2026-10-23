---
name: code-simplification
description: Simplifies code changed in the current task or phase so a newcomer reads, understands and maintains it on the first read, while behavior stays exactly the same - after the task's checks pass, one named smell at a time, delete before writing, small steps with checks, never weakening tests, validation or authorization, with stop rules and a one-line report. Use after implementation checks are green and before the self-check for READY_FOR_REVIEW, or when a review finding names unnecessary complexity. Not for red code, code outside the diff, or behavior changes.
---

# Code Simplification

Goal: code a newcomer reads, understands and maintains on the first read. Not the fewest lines: a change is a simplification only when a reader holds **fewer concepts** afterwards. Moving the same complexity somewhere else is not simpler.

## When

| Situation | Simplify? |
|---|---|
| The task's checks pass and the diff has a named smell | Yes, inside the changed code only |
| A review finding names a smell in the phase's code | Yes, as the fix revision for that finding |
| Checks are red | No: fix with `root-cause-debugging` first |
| The smell is outside the diff | No: record it in the handoff's Concerns as a separate item |
| The code is already clear, or a later task in the plan rewrites it | No |

A simplification made after READY_FOR_REVIEW is a new revision: rerun the affected checks, and the earlier review and test evidence for that code no longer counts.

## Rules

| # | Rule | Why |
|---|---|---|
| SM1 | **Behavior identical.** Same inputs, outputs, errors and messages, side effects, ordering, state transitions, accessibility and performance limits. Existing tests pass unchanged (fixing an import path after a move is the only edit allowed). | A "simplification" that changes behavior is an unreviewed feature change. |
| SM2 | **Understand first.** Read the callers, side effects, error paths, lifecycle and tests of the code before editing it. | Code that looks redundant often guards an edge case. |
| SM3 | **A named smell is required.** Pick a row from [references/smell-catalog.md](references/smell-catalog.md) or from `{{slot:clean-code}}`; "I had to read it twice" counts only when you can say what forced the second read. | Simplifying clear code is churn that costs a review round. |
| SM4 | **Delete before writing.** Ask in order: is it needed at all? does the repository already have it? does the standard library, framework or platform ship it? Only then write the minimum. | The cheapest code to maintain is code that does not exist. |
| SM5 | **One way of doing things.** Reuse the patterns and libraries already in the repository; no new dependency for what a few lines do. | Two ways of doing one thing double the learning and the bugs. |
| SM6 | **Small steps with checks.** One simplification at a time; run the formatter, analyzer and affected tests after each and keep the evidence. | A failing check after one small step points straight at the cause. |
| SM7 | **Never weaken protection.** Never edit a test to make a simplification pass; never remove validation, error mapping, authorization or data-scope checks, dependency boundaries or package contracts; never leave a wrapper, alias or shim after moving code (`clean-code` CC1, CC2). | These remove safety, not complexity. |
| SM8 | **Stop** when behavior or a public contract would change, when a `D-NN` or `{{slot:clean-architecture}}` keeps the abstraction, when the gain is cosmetic, or when a hot path would change without a measurement. | Past these points it is no longer simplification: it is a design change that needs `plan-change-request`. |

## Steps

1. Take the diff of the task or phase (or the code a review finding names) and list candidate smells with `path:line`.
2. For each candidate, apply SM2 and SM8; drop it if a stop rule applies or no catalog row fits.
3. Apply the catalog technique for one smell, then run the checks of SM6.
4. Repeat for the next smell. Stop when no named smell remains or a stop rule applies.
5. Report.

## Report

One line in the handoff, per task or phase:

`simplify: <smell> -> <technique> at <path:line>[; ...]; net <+/-n> lines; checks: <command> exit <code>`

or `simplify: nothing worth changing (looked at: <files>)`. Deliberate shortcuts kept on purpose are named with their limit and upgrade path so they do not silently become permanent.

## Review severity

Unnecessary complexity in the phase's diff is `P2` (`P3` when small) on the `clean-code` scale and does not block alone. It is `P1` only when it breaks `clean-code` CC1/CC2, SM7 or a `D-NN`. Only code changed in the phase is graded.

## Sources

[references/sources.md](references/sources.md)
