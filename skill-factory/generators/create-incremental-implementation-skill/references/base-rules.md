# Base rules (generic, every workspace)

Extracted from Coder Nexus `plugins/core/skills/incremental-implementation` without its workspace specifics (Huly, Mockoon, Flutter, slot names). Each rule must appear in the generated skill with the workspace's real facts **and its reason** (the Why column, reworded for the workspace), or be marked "not adopted" with a reason.

| # | Rule | Why | Goes into |
|---|---|---|---|
| I1 | **Approved scope only.** Implement only what an approved plan/brief covers; never brainstorm, widen scope or start before the required gates are approved. | Unapproved work is work the user may reject; it also hides scope creep from review. | 01 |
| I2 | **One phase at a time.** A Code Writer takes one phase; all phases it depends on are `PASSED`; a preparation phase (if the workspace has one) is completed first. | Parallel or out-of-order phases build on code nobody has verified yet. | 01 |
| I3 | **Concrete before coding.** The phase states file scope, reused components/contracts and verification commands; if not, it is a planning gap, not something to guess. | Guessing scope or checks turns the Code Writer into the planner without the planner's context. | 01 |
| I4 | **Task loop.** For each task top to bottom: A read & ground (target files, reused components, signatures to produce, acceptance criteria; earlier tasks ticked) → B implement → C immediate local check → D tick the task and **re-read the plan** before the next task. No bulk coding across tasks. | Bulk coding drifts from the plan; re-reading reloads the exact scope and contracts before each change. | 02 |
| I5 | **Edit only the task's files.** Use the components and conventions the design mapped; a mapped component/contract that does not fit is a planning blocker, never a local workaround. | Local workarounds silently break the design other phases rely on. | 02 |
| I6 | **Immediate local check.** After each task run its own check (analyzer on changed files, the task's unit test) and fix errors before ticking. | An error found right after the change is cheap; found at phase end it is tangled with other tasks. | 02, 06 |
| I7 | **Phase verification.** When all tasks are ticked, run the phase's full suite (analyzer, tests, build as applicable). | Task checks are narrow; only the full suite shows interactions between tasks. | 03, 06 |
| I8 | **Visual verification** for UI-impacting phases on the approved targets/states. | Tests rarely catch layout and state regressions a user would see. | 03, fe/06 |
| I9 | **Self bug-hunt.** Run the workspace's bug-hunt (quick effort) on the phase diff; fix confirmed findings together with the missing tests; rerun affected checks. | The author is the cheapest reviewer; confirmed defects with tests do not come back. | 03 |
| I10 | **Evidence.** Report exact command, revision, target and result. `NOT_RUN`, `BLOCKED`, `UNVERIFIED` are never `PASS`. | A check that did not run is not evidence; reporting it as PASS misleads every later gate. | 03, 05 |
| I11 | **Back to the gate.** A fix that changes behavior, API, architecture, dependencies or a component contract goes back to the relevant planning/design gate instead of being done in place. | Changing contracts in place bypasses the people who approved them. | 03 |
| I12 | **Simplicity pass.** After behavior passes, inspect only the changed code; call code-simplification only for concrete complexity. No drive-by refactors, no changing tests to fit, no removing validation/error paths; rerun affected checks. | Simplifying outside the diff or bending tests mixes refactoring with behavior change and hides regressions. | 04 |
| I13 | **Handoff.** Phase ID, approved revisions, changed files and the actual code revision. Review uses that revision; verification uses the reviewed revision; any fix creates a new revision and restarts affected review/tests. The approved plan stays stable; results are recorded separately. | Review and tests must refer to one exact revision, or their results prove nothing. | 05 |
| I14 | **No fabrication.** Never invent business data, services, mock fallbacks or "successful" placeholders to make a missing source look available; fail explicitly. | Fake data makes a missing dependency look solved and ships broken behavior. | 01, 03 |

## Order of work (file 07, per branch)

Default inside a phase, unless the plan orders tasks differently (the plan wins):

| Branch | Default order |
|---|---|
| Backend | contract/schema → domain → application (use case + ports) → infrastructure → presentation → wiring → tests per layer as you go |
| Frontend | contract types → pure utils (+ tests) → hooks/state → components/views → route composition → styles → visual check |
| Mobile | domain → data → state holder → widgets/screens → routing → widget tests |
| Fullstack | BE API finished and tested before the FE client (see the workspace's integration rules) |

## Not adopted is allowed

A small workspace may mark I8 (no UI), I9 (no bug-hunt skill yet → "manual diff review"), or the preparation phase as not adopted. Never mark I1, I4, I5, I10, I11 or I14 as not adopted.
