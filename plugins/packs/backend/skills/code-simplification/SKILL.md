---
name: code-simplification
description: Simplification standard for a Backend (Python 3.12+ / FastAPI / Pydantic v2 / SQLAlchemy 2.x async) service - reduces the code changed in the current task or phase to the simplest form a newcomer understands on first read while behavior stays exactly the same - only after ruff, mypy and pytest are green, through four lenses (reuse, simplification, efficiency, altitude) with one named smell at a time (needless class, single-implementation Protocol, generic repository, `**kwargs` pass-through, N+1 query, special case in a shared dependency, hand-rolled stdlib), small steps with checks, never weakening tests, Pydantic validation, authorization or dependency boundaries, with stop rules and the one-line `simplify:` report. Use after implementation checks pass and before the self-check for READY_FOR_REVIEW, when asked to "clean this up", "simplify", "this is too complex" or "over-engineered", or when a review finding names unnecessary complexity in the diff, even if the word "simplify" is not used. Not for red code, code outside the diff, new features, bug fixes or any behavior change.
---

# Code Simplification — Backend (Python / FastAPI)

Goal: code a newcomer reads, understands and maintains on the first read. Not the fewest lines: a change is a simplification only when a reader holds **fewer concepts** afterwards (names, branches, modes, layers). Moving the same complexity somewhere else is not simpler.

All check flags (`PASS` / `FAIL`) and review severities (`BLOCKER` / `MAJOR` / `MINOR`) follow `shared_contracts/flags_and_statuses.md` and `work-item-contract` (`references/handoff-and-status.md` §9).

## 1. The loop

1. `ruff check`, `mypy` and the affected `pytest` tests are green; take only the phase's diff ([01](references/01-scope-and-safety.md)).
2. Read callers, FastAPI dependencies, side effects, error paths, transactions and tests of the code ([01](references/01-scope-and-safety.md)).
3. Pass the diff through the four lenses — **Reuse, Simplification, Efficiency, Altitude** — and name each smell from the catalog; skip code that is already clear ([02](references/02-smell-catalog.md)).
4. One small simplification → rerun `ruff format --check`, `ruff check`, `mypy` and the affected tests (`PASS` / `FAIL`).
5. Stop at the stop criteria; findings that would change behavior or reach outside the diff go to Concerns ([01](references/01-scope-and-safety.md) §7).
6. Report one `simplify:` line ([03](references/03-report-and-review.md)).

A simplification made after READY_FOR_REVIEW is a new revision: rerun the affected checks; earlier review and test evidence for that code no longer counts (`evidence-standard`).

## 2. Rules (Mandatory Compliance)

| Rule | Principle | Why | Reference |
|---|---|---|---|
| **S1** | **Only after checks pass, only the changed code.** Anything outside the phase's diff goes into the hand-off's Concerns. | Simplifying red code or code outside the diff mixes refactoring with behavior change. | [01](references/01-scope-and-safety.md) |
| **S2** | **Behavior identical.** Same outputs, HTTP status codes and bodies, exceptions and messages, side effects, query count and order, transaction boundaries, state transitions. Existing tests pass unchanged (an import path after a move is the only allowed edit). | A "simplification" that changes behavior is an unreviewed feature change. | [01](references/01-scope-and-safety.md) |
| **S3** | **Understand first.** Read callers (`rg -n`, plus string/dynamic use), `Depends` chains, side effects, error paths, session lifecycle and tests. | Code that looks redundant often guards an edge case (a retry, a rollback, a tenant filter). | [01](references/01-scope-and-safety.md) |
| **S4** | **A named smell is required.** One catalog row under one of the four lenses, or a `{{slot:clean-code}}` rule. | Simplifying clear code is churn that costs a review round. | [02](references/02-smell-catalog.md) |
| **S5** | **Reuse before writing** *(Reuse)*. Needed? → in the repo? → stdlib, FastAPI, Pydantic or SQLAlchemy? → only then the minimum. No new `pyproject.toml` dependency for a few lines. | The cheapest code to maintain is code that does not exist. | [02](references/02-smell-catalog.md) |
| **S6** | **YAGNI.** No `Protocol`, ABC, factory, settings field or layer with one implementation, a constant value or one caller, unless a `D-NN` or a `{{slot:clean-architecture}}` port requires it. | Speculative flexibility costs every reader. | [02](references/02-smell-catalog.md) |
| **S7** | **Rule of three for logic.** Extract on the third repetition. Definitions (Pydantic/ORM models, enums, SQL) are never duplicated (`{{slot:clean-code}}` C1). | Early extraction couples code that later diverges. | [02](references/02-smell-catalog.md) |
| **S8** | **Flat and plain** *(Simplification)*. No derivable state, copy-paste variants, deep nesting (C6 limit) or clever code (nested comprehensions, `reduce`, metaclasses, `getattr` dispatch). | Clever code costs every reader minutes. | [02](references/02-smell-catalog.md) |
| **S9** | **No wasted work** *(Efficiency)*. No N+1 queries, repeated reads in one request, needlessly sequential independent awaits, blocking work at import or in async paths. Hot-path changes need a measurement. | Wasted work in new code is paid on every request. | [02](references/02-smell-catalog.md) |
| **S10** | **Fix at the right depth** *(Altitude)*. No special cases for one endpoint inside shared dependencies or middleware; fix the cause, not the symptom. Outside the diff → Concerns. | A patched symptom leaves special cases every reader must remember. | [02](references/02-smell-catalog.md) |
| **S11** | **Small steps with checks.** One simplification at a time; checks after each, with evidence. | A failing check after one small step points straight at the cause. | [01](references/01-scope-and-safety.md) |
| **S12** | **Never weaken protection.** No edited tests, no removed Pydantic validation, error mapping, authorization/data-scope checks, `Depends` boundaries or transactions, no leftover wrapper/alias (C1), no `# type: ignore` / `# noqa` to pass. | These remove safety, not complexity. | [01](references/01-scope-and-safety.md) |
| **S13** | **Stop** when behavior or a contract would change, a `D-NN` keeps the abstraction, the gain is cosmetic, a hot path changes unmeasured, or the next step leaves the diff. | Past these points it needs `change-control`, not simplification. | [01](references/01-scope-and-safety.md) |
| **S14** | **Report one line.** The §9 `simplify:` line; skipped findings in Concerns; shortcuts with their limit and upgrade path. | Reviewers see intent; nothing is silently dropped or made permanent. | [03](references/03-report-and-review.md) |

## 3. Reference Guides

| Topic | Reference |
|---|---|
| When and scope, behavior safety and Python traps, per-step checks, never-rules and stop criteria | [01 — Scope & Safety](references/01-scope-and-safety.md) |
| Smell → technique catalog by lens (Reuse, Simplification, Efficiency, Altitude), rule of three, what to leave alone | [02 — Smell Catalog](references/02-smell-catalog.md) |
| `simplify:` report line, skipped findings, shortcuts and review grading (`BLOCKER` / `MAJOR` / `MINOR`) | [03 — Report & Review](references/03-report-and-review.md) |

## 4. Relationship with Other Skills

- Thresholds (function length, parameters, nesting), naming, wrappers/aliases, dead code and duplicated definitions: `{{slot:clean-code}}` — linked, not repeated here.
- Placement, ports and who may import whom: `{{slot:clean-architecture}}`; decisions (`D-NN`) keep the abstractions they require.
- Guards from `{{slot:secure-coding-standards}}` are never simplified away.
- Called from the simplicity pass of `incremental-implementation`, before the `bug-hunt` self-check hand-off; findings are graded by `{{slot:code-review}}`.
- Red checks: fix with `{{slot:root-cause-debugging}}` first.
