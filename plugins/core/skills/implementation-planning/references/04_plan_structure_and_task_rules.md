# 04 — Plan Structure, Task Sizing and Order

Rules that make a plan executable by a single Code Writer without asking, and reviewable without re-deriving it. They add to [01_phase_slicing_rules.md](01_phase_slicing_rules.md); they never replace `PHASE-00`, vertical phases, sequential order or a validated heading.

## 1. Two plan-level sections

Place both in `implementation-plan.md` above `## AC coverage`. Neither is checked by `validate_plan_slices`; they are still required by this skill and by `gate-review` `modes/plan.md`. Their format, and the frozen status they get at Gate 3, are in [plan-and-task-contract.md](../../work-item-contract/references/plan-and-task-contract.md) §1, §4; this section covers how to choose their content.

### `## Global constraints`

Rules every task implicitly includes, so no task repeats them and none forgets them.

| Rule | Why |
|---|---|
| One line per constraint, citing its source (`BR-NN`, `D-NN`, foundation profile, `{{slot:clean-architecture}}`) | The source stays the single home of the fact; the line is a pointer |
| Write the exact value the source pins (a limit, a status code, copy text, a version floor) | A paraphrased value drifts; a pinned one can be checked |
| Only rules that apply to more than one task | A rule for one task belongs in that task |
| Never add a rule the sources do not contain | New rules are scope; route them to the Spec Writer (`requirements.md`) or back to Gate 2 (`design.md`) |

### `## Review focus`

Up to five input classes or failure modes that `requirements.md` implies but no AC's decisive check exercises (for example an empty list after a filter, a duplicate submit, a value at a `BR-NN` limit, a slow response, a revoked permission). Most likely to hurt a user first.

- One line each: the input or condition, and the behavior a reasonable user expects according to an existing `BR-NN` / `AC-NN` / `D-NN`.
- For each line, add a check to the task that owns the code and name that task on the line.
- If the expected behavior is not stated anywhere, do not decide it: queue a `Q-NN` (scope belongs to the user, Gate 1).
- Write `None found after checking every AC and BR` when nothing qualifies. An empty section means checked, never skipped.
- The Code Reviewer checks each line deliberately, because no AC test pins it.

## 2. Right-sizing tasks

A task is the smallest unit that has its own check and that a reviewer could reject while accepting its neighbour.

- Fold setup, configuration, registration and documentation steps into the task whose deliverable needs them. Reason: a task with nothing to verify cannot fail its **Acceptance Criteria**.
- Split a task when one part could be wrong while the other is right.
- Every task ends with a check that can fail (the stack's analyzer on the touched path, a named test).
- A phase that delivers more than one observable behavior is two phases.

## 3. Order

| Rule | What to do | Why |
|---|---|---|
| Highest risk first | Right after `PHASE-00`, schedule the behavior with the most uncertainty (an unproven integration, the hardest AC, a new foundation component). Make `PHASE-01`'s walking skeleton pass through it | A wrong assumption found in the last phase reworks every phase before it |
| Prefactor first | When existing code must be reshaped to make the change easy, put the behavior-preserving refactor as the first task(s) of the phase that needs it, accepted by the existing tests staying green | Mixing reshaping and new behavior in one task hides which one broke a test |
| Dependencies only backwards | A phase depends only on earlier phases (`PLAN-V-009`); a task only on earlier tasks | Single Code Writer runs top to bottom |

Prefactor never becomes its own phase: a phase must be an observable behavior.

### Exception: expand → migrate → contract

When a storage schema or a public contract that live consumers use must change, a single vertical change would break those consumers. Split it:

1. **Expand** — add the new field, column, endpoint or format beside the old one, backward compatible. First phase that needs it.
2. **Migrate** — move data and consumers to the new path. Same or later phase.
3. **Contract** — remove the old path, only after every consumer has moved. Last phase, or a later `vN` recorded as a `D-NN`.

Each step leaves the system working and has its own check. Never put expand and contract in one task. This is the only case where a phase may contain work that is not itself observable (the contract step). It applies only inside the repository that owns the schema or contract; the cross-repo rule in [01_codebase_readiness_and_gap_analysis.md](01_codebase_readiness_and_gap_analysis.md) still holds. Concrete migration commands come from `{{slot:verification}}` or the workspace's migration skill.

## 4. No transcribed code

A plan holds the decisions the Code Writer cannot make alone, not the program.

| A task gives | A task never gives |
|---|---|
| File path and the class or function name | Full function or class bodies the signature and test already determine |
| Exact signature: name, parameters, return type | "TBD", "handle edge cases", "add validation as needed" |
| Values `requirements.md` / `design.md` pin (limits, codes, copy, keys) | A type or symbol no task produces |
| The test name and what it asserts | A paraphrase of a pinned value |

A body is allowed only for an algorithm the signature and test do not determine, or for exact copy text the spec fixes. A plan longer than the code it describes has written the code: replace bodies with signatures and assertions.

## 5. Self-check before gate-review

1. Every AC has a phase and a decisive check (`02_ac_coverage_matrix.md`).
2. Every **Consumes** line matches an earlier **Produces** line character for character.
3. Every `## Review focus` line names its owning task, and that task has the check.
4. No task line decides nothing; no task carries a transcribed body.
5. Order: `PHASE-00`, highest risk next, prefactor before behavior, expand before contract.

Fix inline, then run `validate_plan_slices`, `gate-review` `modes/plan.md` and `cold-reader-check` as in [SKILL.md](../SKILL.md) step 10.
