# Base rules (generic, every workspace)

Generalised from Coder Nexus simplification base rules, `plugins/ponytail` and the simplification standard of a real fullstack workspace. Goal: code a newcomer understands on first read — not the fewest lines. Each rule goes into the generated skill with the workspace's facts **and its reason**, or is marked "not adopted" with a reason.

| # | Rule | Why | Severity | Goes into |
|---|---|---|---|---|
| S1 | **Only after checks pass, only the changed code.** Simplify the phase's diff once behavior is green; record unrelated cleanup as a separate task. | Simplifying red code or code outside the diff mixes refactoring with behavior change and bloats review. | P1 | 01 |
| S2 | **Behavior stays identical.** Same inputs, outputs, errors, side effects, ordering, state transitions, accessibility and performance constraints; existing tests pass unchanged (import fixes after a move are the only exception). | A "simplification" that changes behavior is an unreviewed feature change. | P1 | 02 |
| S3 | **Understand first.** Read callers, side effects, error paths, lifecycle and tests before editing. | Code that looks redundant often guards an edge case. | P2 | 02 |
| S4 | **A concrete issue is required.** Name the smell (catalog row); skip code that is already clear or about to be rewritten. "Must read it twice to understand" is a valid smell. | Simplifying clear code is churn. | P3 | 01, 03 |
| S5 | **Delete before writing.** Ask in order: is it needed? does the repo already have it? does the stdlib/framework/platform ship it? — only then write the minimum. | The cheapest code to maintain is code that does not exist. | P2 | 03 |
| S6 | **YAGNI.** No interface, factory, config or layer with a single implementation, a constant value or a single caller — unless a workspace decision requires it. | Speculative flexibility costs every reader and is rarely used as imagined. | P2 | 03 |
| S7 | **Rule of three for logic.** Extract shared logic on the third repetition; two may stay. Definitions (types, schemas, SQL) are never duplicated (clean-code C1). | Early extraction couples things that later diverge; duplicated definitions drift. | P2 | 03 |
| S8 | **Flat and plain.** Guard clauses over nesting (limit from clean-code); no clever code (nested comprehensions/lambdas/reduce, metaprogramming, dynamic-import hacks, recursion where a loop is clearer); flat data over deep class hierarchies; no inheritance just to reuse code. | Clever code saves the writer seconds and costs every reader minutes. | P2 | 03 |
| S9 | **One way of doing things.** Reuse the patterns and libraries already in the repo; no new dependency for what a few lines do (if added, give the reason in the handoff). | Two ways of doing one thing double the learning and the bugs. | P2 | 03 |
| S10 | **Small steps.** One simplification at a time; run the formatter/analyzer and affected tests after each. | A failing check after one small step points straight at the cause. | P2 | 02 |
| S11 | **Never:** change tests to make a simplification pass; remove validation, error mapping, authorization checks, DI boundaries or package contracts; leave wrappers/aliases/shims after moving code. | These remove protection, not complexity. | P1 | 02 |
| S12 | **Stop** when behavior or a public contract would change (→ back to the approval gate), when a workspace decision keeps the abstraction, when the gain is cosmetic, or when a hot path would change without measurement. | Past these points it is no longer simplification. | P1 | 04 |
| S13 | **Report** one line: what was deleted/merged/simplified (and net lines if useful); deliberate shortcuts marked with the workspace's convention (e.g. `ponytail: <ceiling>, <upgrade path>`). | Reviewers see the intent; shortcuts do not silently become permanent. | P3 | 05 |

**Never "not adopted":** S1, S2, S11, S12.

## Review severity (default)

Unnecessary complexity in the diff is **P2** (P3 if small) and does not block on its own. **P1** only when it violates the no-wrapper rule, S11, or a workspace decision. Only code changed in the phase is reviewed.
