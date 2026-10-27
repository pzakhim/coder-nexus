# Base Simplification Rules (Universal)

Universal rules for reducing a working diff to its simplest clear form. Goal: code a newcomer understands on first read — not the fewest lines. A change is a simplification only when a reader holds **fewer concepts** afterwards (names, branches, modes, layers); moving the same complexity elsewhere is not simpler.

Every rule goes into the generated skill with the workspace's verified facts **and its rationale**, adapted to the workspace's contracts, or marked "not adopted" with a stated reason. If an automated CLI gate already enforces a rule, cite that gate. Rules already owned by `clean-code` (dead code C2, wrappers and aliases C1, size and nesting thresholds C6) are **linked, never repeated**.

The diff is examined through four lenses: **Reuse** (S5), **Simplification** (S8), **Efficiency** (S9) and **Altitude** (S10).

| # | Rule | Why | Goes into |
|---|---|---|---|
| S1 | **Only after checks pass, only the changed code.** Simplify the phase's diff once its checks are green; anything worth simplifying outside the diff goes into the hand-off's Concerns. | Simplifying red code or code outside the diff mixes refactoring with behavior change and bloats review. | `SKILL`, `01` |
| S2 | **Behavior stays identical.** Same inputs, outputs, errors and messages, side effects and their order, state transitions, transaction/lifecycle boundaries, accessibility and performance limits. Existing tests pass unchanged (an import path after a move is the only allowed edit). | A "simplification" that changes behavior is an unreviewed feature change. | `SKILL`, `01` |
| S3 | **Understand first.** Read callers (including dynamic use by string or reflection), side effects, error paths, lifecycle and the tests that cover the code before editing. | Code that looks redundant often guards an edge case. | `01` |
| S4 | **A named smell is required.** Each change names one catalog row (under one of the four lenses) or one `clean-code` rule; skip code that is already clear or about to be rewritten. "I had to read it twice" counts only when you can say what forced the second read. | Simplifying clear code is churn that costs a review round. | `SKILL`, `02` |
| S5 | **Reuse before writing** *(Reuse lens)*. Ask in order: is it needed? does the repository already have it? does the standard library, framework or platform ship it? — only then write the minimum. One way of doing each thing; no new dependency for what a few lines do (if one is added, the reason goes into the hand-off). | The cheapest code to maintain is code that does not exist; two ways of doing one thing double the learning and the bugs. | `02` |
| S6 | **YAGNI.** No interface, factory, configuration option or layer with a single implementation, a constant value or a single caller — unless a workspace decision or an architecture port requires it. | Speculative flexibility costs every reader and is rarely used as imagined. | `02` |
| S7 | **Rule of three for logic.** Extract shared logic on the third repetition; two may stay. Definitions (types, schemas, queries, constants) are never duplicated (`clean-code` C1). | Early extraction couples code that later diverges; duplicated definitions drift. | `02` |
| S8 | **Flat and plain** *(Simplification lens)*. Remove redundant or derivable state, copy-paste with slight variation, deep nesting (limit from `clean-code` C6) and clever code (nested one-liners, metaprogramming, dynamic dispatch where a plain call reads at once). Dead code follows `clean-code` C2. | Clever code saves the writer seconds and costs every reader minutes. | `02` |
| S9 | **No wasted work** *(Efficiency lens)*. Remove redundant computation and repeated I/O, run independent operations without needless serialization, keep blocking work off startup and hot paths, and do not keep large scopes alive through long-lived closures. A hot-path change needs a measurement (S13). | Wasted work in new code is paid on every run. | `02` |
| S10 | **Fix at the right depth** *(Altitude lens)*. Prefer the simpler, more general change to the underlying mechanism over special cases layered on shared code. When the right depth lies outside the diff, record it in Concerns instead (S1). | A patched symptom adds special cases every later reader must remember. | `02` |
| S11 | **Small steps with checks.** One simplification at a time; run the formatter, analyzer and affected tests after each and keep the evidence. | A failing check after one small step points straight at the cause. | `01` |
| S12 | **Never weaken protection.** Never edit a test to make a simplification pass; never remove validation, error mapping, authorization or data-scope checks, dependency-injection boundaries, transactions or package contracts; never leave a wrapper, alias or re-export after moving code (`clean-code` C1); never add a suppression directive to make a check pass. | These remove safety, not complexity. | `01` |
| S13 | **Stop** when behavior or a public contract would change, when a workspace decision or architecture port keeps the abstraction, when the gain is cosmetic, when a hot path would change without a measurement, or when the next step needs code outside the diff. | Past these points it is a design change that needs change control, not simplification. | `SKILL`, `01` |
| S14 | **Report one line.** The `simplify:` line of `work-item-contract` handoff-and-status §9; findings skipped because they would change behavior or reach outside the diff are listed in Concerns; deliberate shortcuts name their limit and upgrade path. | Reviewers see the intent; skipped findings and shortcuts do not silently disappear or become permanent. | `03` |

**Mandatory rules (never "not adopted"):** S1, S2, S12, S13.

---

## Unified Tool Gate (`PASS` / `FAIL`) & Review Severity (`BLOCKER` / `MAJOR` / `MINOR`)

The checks rerun after each step (formatter, analyzer, type checker, affected tests) are strictly binary (`exit 0` = `PASS`, `exit != 0` = `FAIL`). Reviewers grade findings on the unified 3-tier scale (`shared_contracts/flags_and_statuses.md` §2):

| Severity | Finding | Review Verdict Impact |
|---|---|---|
| `BLOCKER` | A check `FAIL`s after simplification; a wrapper, alias or re-export left after a move; S12 violated; a workspace decision ignored | `CHANGES_REQUESTED` (blocks approval) |
| `MAJOR` | Unnecessary complexity in the diff with a named catalog row (any of the four lenses) | Fixed in the same revision when inside the phase's scope |
| `MINOR` | Small, local simplification opportunity | Optional (never blocks approval) |

A "simplification" that changed a result, status, transaction or error path is a **defect** graded under §9 with its failure scenario, not a simplification finding. Reviewers grade only code changed in the phase; complexity outside the diff is a note in Concerns, never a finding.
