---
name: code-simplification
description: Simplification standard for a Backend (Python 3.12+ / FastAPI / Pydantic v2 / SQLAlchemy 2.x async) service - reduces the code changed in the current task or phase to the simplest form a newcomer understands on first read while behavior stays exactly the same - only after ruff, mypy and pytest are green, one named smell at a time (needless class, single-implementation Protocol, generic repository, `**kwargs` pass-through, dict as record, hand-rolled stdlib), delete before writing, stdlib and framework first, YAGNI, rule of three, small steps with checks, never weakening tests, Pydantic validation, authorization or dependency boundaries, with stop rules and the one-line `simplify:` report. Use after implementation checks pass and before the self-check for READY_FOR_REVIEW, when asked to "clean this up", "simplify", "this is too complex" or "over-engineered", or when a review finding names unnecessary complexity in the diff, even if the word "simplify" is not used. Not for red code, code outside the diff, new features, bug fixes or any behavior change.
---

# Code Simplification — Backend (Python / FastAPI)

Goal: code a newcomer reads, understands and maintains on the first read. Not the fewest lines: a change is a simplification only when a reader holds **fewer concepts** afterwards (names, branches, modes, layers). Moving the same complexity somewhere else is not simpler.

## The loop

1. `ruff check`, `mypy` and the affected `pytest` tests are green; take only the phase's diff ([01 — when and scope](references/01-when-and-scope.md)).
2. Read callers, side effects, error paths, transactions and tests of the code ([02 — behavior safety](references/02-behavior-safety.md)).
3. Name the smell from the catalog; skip code that is already clear ([03 — smell catalog](references/03-smell-catalog.md)).
4. One small simplification → rerun `ruff format`, `ruff check`, `mypy` and the affected tests.
5. Stop at the stop criteria ([04 — stop criteria](references/04-stop-criteria.md)).
6. Report one `simplify:` line ([05 — report and review](references/05-report.md)).

A simplification made after READY_FOR_REVIEW is a new revision: rerun the affected checks; earlier review and test evidence for that code no longer counts (`evidence-standard`).

## Rules

| # | Rule | Why | Severity | Enforced by |
|---|---|---|---|---|
| SM1 | **Behavior identical.** Same inputs, outputs, HTTP status codes and response bodies, raised exceptions and messages, side effects, query count and ordering, transaction boundaries, state transitions and performance limits. Existing tests pass unchanged (an import path after a move is the only allowed edit). | A "simplification" that changes behavior is an unreviewed feature change. | P1 | `pytest` on the affected tests; review |
| SM2 | **Understand first.** Read the callers (`git grep -n`), FastAPI dependencies, side effects, error paths, session/transaction lifecycle and tests before editing. | Code that looks redundant often guards an edge case (a retry, a rollback, a tenant filter). | P2 | Review |
| SM3 | **A named smell is required.** Pick a row from [03](references/03-smell-catalog.md) or a rule from `{{slot:clean-code}}`; "I had to read it twice" counts only when you can say what forced the second read. | Simplifying clear code is churn that costs a review round. | P3 | Review |
| SM4 | **Delete before writing.** Ask in order: needed at all? already in the repository? shipped by the stdlib, FastAPI, Pydantic or SQLAlchemy? Only then write the minimum. | The cheapest code to maintain is code that does not exist. | P2 | Review; ruff `F401`, `F841`, `ARG`, `ERA001` where enabled |
| SM5 | **One way of doing things.** Reuse the patterns and libraries already in the repository; no new dependency in `pyproject.toml` for what a few lines do (if one is added, the reason goes into the hand-off). | Two ways of doing one thing double the learning and the bugs. | P2 | Review of `pyproject.toml` diff |
| SM6 | **Small steps with checks.** One simplification at a time; run the formatter, linter, type checker and affected tests after each and keep the evidence. | A failing check after one small step points straight at the cause. | P2 | Evidence rows in the hand-off |
| SM7 | **Never weaken protection.** Never edit a test to make a simplification pass; never remove Pydantic validation, error mapping, authorization or data-scope checks, `Depends` boundaries, transactions or the API contract; never leave a wrapper, alias or re-export after moving code (`{{slot:clean-code}}` wrapper and alias rules). | These remove safety, not complexity. | P1 | Review; `pytest` |
| SM8 | **Stop** when behavior or a public contract would change, when a `D-NN` or `{{slot:clean-architecture}}` keeps the abstraction, when the gain is cosmetic, or when a hot path would change without a measurement ([04](references/04-stop-criteria.md)). | Past these points it is a design change that needs `change-control`, not simplification. | P1 | Review |
| SM9 | **Only after checks pass, only the changed code.** Simplify the phase's diff once it is green; anything outside goes into the hand-off's Concerns. | Simplifying red code or code outside the diff mixes refactoring with behavior change and bloats review. | P1 | `git diff --name-only`; review |
| SM10 | **YAGNI.** No `Protocol`, ABC, factory, settings field or layer with one implementation, a constant value or one caller, unless a `D-NN` or a `{{slot:clean-architecture}}` port requires it. | Speculative flexibility costs every reader and is rarely used as imagined. | P2 | Review |
| SM11 | **Rule of three for logic.** Extract shared logic on the third repetition; two may stay. Definitions (Pydantic models, ORM models, enums, SQL) are never duplicated. | Early extraction couples code that later diverges; duplicated definitions drift. | P2 | Review |
| SM12 | **Flat and plain.** Guard clauses over nesting (limits from `{{slot:clean-code}}`); no nested comprehensions, `reduce` chains, metaclasses, `getattr` dispatch or dynamic imports where plain code reads at once; composition over inheritance for reuse. | Clever code saves the writer seconds and costs every reader minutes. | P2 | ruff `C901`, `PLR09xx`, `SIM`, `RET` where enabled; review |
| SM13 | **Report one line.** The `simplify:` line of [handoff-and-status §9](../work-item-contract/references/handoff-and-status.md); deliberate shortcuts are named with their limit and upgrade path. | Reviewers see the intent; shortcuts do not silently become permanent. | P3 | Review of the hand-off |

Severity uses the `P1`/`P2`/`P3` rule-violation scale of [handoff-and-status §9](../work-item-contract/references/handoff-and-status.md); a "simplification" that produced a wrong result is graded there as a defect instead.

## Relationship with other skills

- Thresholds (function length, parameters, nesting), naming, wrapper/alias, dead-code and duplicated-definition rules: `{{slot:clean-code}}` — linked, not repeated here.
- Placement, ports and who may import whom: `{{slot:clean-architecture}}`; decisions (`D-NN`) keep the abstractions they require.
- Guards from `{{slot:secure-coding-standards}}` are never simplified away.
- Called from the simplicity pass of `incremental-implementation`, before the `bug-hunt` self-check hand-off; findings are graded by `{{slot:code-review}}` with the §9 scale.
- Red checks: fix with `{{slot:root-cause-debugging}}` first.

## Not adopted

- "Fewer lines" as the target: the goal is first-read understanding; net lines are reported, never targeted.
- Splitting a large file before adding to it: file splitting and placement are planned work (`{{slot:clean-architecture}}`, the plan's file list), not an in-task simplification.
- Replacing repeated `if`/`match` with class polymorphism: it adds hierarchies to small tasks; a lookup dict or a single `match` is the simpler form.

## Sources

[references/sources.md](references/sources.md)
