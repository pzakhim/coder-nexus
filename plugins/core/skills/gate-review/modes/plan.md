# Mode: plan (before Gate 3)

Reviews `implementation-plan.md` and every linked `phases/*.md` against the approved `requirements.md`, `design.md` and `codebase-notes.md`. Pass 1 is clean before this file starts. Findings use the prefix `GR-P-NN`.

`PLAN-V-006` and `PLAN-V-010` already check that every AC and goal is mapped to a phase, and `PLAN-V-009` that phases do not depend forward. This mode checks that the mapped tasks really deliver and fit together.

The spec is the binding authority; the plan is its argument. When they disagree, the plan is wrong unless the spec owner confirms otherwise through a `Q-NN`.

## P1. Interface pre-flight table

The table is the output; "no conflicts" without rows is not a review.

One row for every pair of tasks (in one phase or across phases) that share a file or a symbol:

| Task A | Task B | Shared file / symbol | A produces | B consumes | Match | Finding |
|---|---|---|---|---|---|---|
| 1.2 | 2.1 | `OrderRepository.fetchPage` | `(page, size) -> Page<Order>` | `fetchPage(cursor)` | no: name/parameters differ | `GR-P-02` |

- "Produces" comes from the task's **Produces** field; "consumes" from the other task's files, code direction and acceptance check.
- Names, parameter and return types, nullability, error results, JSON keys and routes must match. A mismatch is `HIGH`.
- A consumer ordered before its producer (inside a phase, or in an earlier phase) is `HIGH`.

One row for every task whose own text disagrees with itself: the test it specifies against the code it specifies, a file it creates against a file a later task says already exists, an acceptance check that cannot fail. `HIGH`.

## P2. Every AC and goal really covered

- For each `AC-NN`, the owning phase has a task that builds the behavior and a decisive check that would fail without it. A phase that only lists the ID is `HIGH`.
- Every `BR-NN` with behavior lands in a task; every `NEW COMPONENT` in the design's `## UI/UX mapping` is an explicit task; every design divergence rule (`D-NN`) is respected by the tasks that touch it. Gaps are `HIGH`.
- Each `G-NN` is reached through its ACs (see `PLAN-V-010`); report goals reached only by a check that cannot fail.

## P3. Proportion

- A plan much longer than `requirements.md` plus `design.md` (roughly more than three times), or tasks that transcribe whole function bodies, is `MEDIUM`. The plan states direction, interfaces (**Produces**), files and checks; the Code Writer writes the code.
- A task that mandates something review would reject - a test that asserts nothing, duplicated logic, a fake fallback that hides a failure - is `HIGH`.

## P4. Global constraints match the spec

Every value the plan repeats - in a Global Constraints section when the plan has one, otherwise in `## Checkpoints and shared files`, phase code direction or checks - equals its source: limits, page sizes, timeouts, roles, data scopes, messages, API fields and statuses in `requirements.md`, `codebase-notes.md` `## 4.` / `## 5.` and `design.md`. A mismatch is `HIGH`; resolve it in the plan, or raise a `Q-NN` if the spec value itself is in doubt.

## Coverage report (plan)

- P1: pairs checked, mismatches; tasks checked, self-contradictions.
- P2: `AC n/N` with a building task and a decisive check; BR and `NEW COMPONENT` gaps.
- P3: plan lines vs requirements + design lines; transcribed bodies found.
- P4: values compared, mismatches.
