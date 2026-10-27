# Base Clean Code Rules (Universal)

Universal clean-code rules for any codebase. Every rule goes into the generated skill with the workspace's verified conventions **and its rationale**, adapted to the workspace's contracts, or marked "not adopted" with a stated reason. If an automated CLI gate already enforces a rule, cite that gate.

| # | Rule | Why | Goes into |
|---|---|---|---|
| C1 | **One concept, one place.** No copy-pasted types, helpers, schemas, or queries; no compatibility aliases, pass-through wrappers, or re-export shims kept for old names. | Copies drift apart; the next bug fix lands in only one copy. | `SKILL`, `01` |
| C2 | **No dead code.** Remove unused functions, imports, files, variables, commented-out code blocks, and orphan `TODO`s. | Dead code is read, maintained, and trusted as if it executed. | `SKILL`, `01` |
| C3 | **No debug leftovers.** Remove ad-hoc console/stdout debug prints, interactive breakpoints, and temporary inspection flags before handoff. | Pollutes production logs, risks leaking sensitive data, and signals unfinished cleanup. | `SKILL`, `02`, `03` |
| C4 | **No swallowed errors.** Catch specific error types; translate, handle, or rethrow with cause context. Broad catches are allowed only at top-level runtime boundaries and must be logged or recorded. | A swallowed error turns a visible failure into silent corrupted state. | `SKILL`, `02` |
| C5 | **Intention-revealing names.** Functions/methods use verbs or verb phrases, booleans use predicate prefixes (`is`/`has`/`can`/`should`), collections use plural nouns; ban vague identifiers (`data`, `info`, `tmp`, `val`, `Manager`, `Helper`, `Utils`, `process()`, `handle()`); use one name per domain concept. | Names are the primary documentation; vague or duplicate names cause misreads and duplicate concepts. | `SKILL`, `01` |
| C6 | **Small, focused units.** Function/method ≤ ~30 lines, file/module ≤ ~300 lines, ≤ 3 parameters (group cohesive inputs into a typed structure), nesting depth ≤ 2 (use guard clauses and early returns). | Short, single-responsibility units are easier to read, test, and review. | `SKILL`, `01` |
| C7 | **No magic values.** Replace scattered raw literals with named constants, design tokens, or typed enumerations for states, roles, and limits. | Scattered literals drift and break silently when one occurrence changes. | `SKILL`, `01` |
| C8 | **Comments explain WHY.** Explain non-obvious rationale, invariants, and external constraints; never restate what the syntax already says; preserve unrelated existing comments. | "What" comments rot quickly; "why" comments save future readers an investigation. | `SKILL`, `01` |
| C9 | **Full static types.** Annotate public signatures and data contracts explicitly; avoid untyped escape hatches, unchecked casts, or suppression directives without a documented reason. | Static type checking catches contract mismatches before runtime. | `SKILL`, `01` |
| C10 | **Scope discipline.** Modify only files and symbols required by the current task; no drive-by renames, reformatting, or refactoring of untouched code. | Unrelated edits obscure the real change in review and cause merge conflicts. | `SKILL`, `03` |
| C11 | **Workspace contracts win.** Follow the workspace's established foundation classes, error/result types, state management, dependency injection, and routing conventions over generic habits. | Generic patterns that contradict an established workspace contract split the codebase into competing styles. | `SKILL`, `01`, `02` |
| C12 | **Visible side effects & lifecycle purity.** Keep module import/load and declarative render/build paths pure; perform I/O, network, persistence, and navigation inside explicit lifecycle or action handlers, and release acquired resources on teardown. | Hidden side effects break test isolation, startup order, and runtime performance. | `SKILL`, `02` |
| C13 | **Explicit state changes.** Prefer immutable value objects and state snapshots; mutate state only through its designated owner. | Shared mutable state causes order-dependent defects and missed updates. | `SKILL`, `01` |
| C14 | **Self-check before handoff.** Run the workspace's formatter, static analyzer/linter, type checker, pattern checks (`rg`), and unit tests before marking work ready for review. | An unrun check is `NOT_RUN`, never `PASS`. | `SKILL`, `03` |
| C15 | **Module-level purity.** Module/top-level scope holds only true immutable constants (read by 2+ units) and static configuration/logger bindings; never store mutable runtime state (caches, counters, registries) at module top level. | Mutable globals leak state across requests and tests. | `SKILL`, `01` |
| C16 | **Helper locality.** Keep a single-caller helper private to its file; promote it to a shared module only when imported by 2+ files, placed in the module that owns the concept and named for its behavior—never `utils`, `helpers`, `common`, or `misc`. | Single-caller public helpers bloat the API surface; generic utility buckets become junk drawers. | `SKILL`, `01` |
| C17 | **Explicit export surface.** Package entry/barrel files export only the symbols external modules actually import; forbid wildcard re-exports and never expose private helpers, internal implementations, or test hooks. | Every exported symbol is a maintenance contract; wildcard exports leak internals and hide dead code. | `SKILL`, `01` |

**Mandatory rules (never "not adopted"):** C1, C3, C4, C10, C11, C14, C15, C16, C17.

---

## Unified Tool Gate (`PASS` / `FAIL`) & Review Severity (`BLOCKER` / `MAJOR` / `MINOR`)

Automated CLI checks (formatter, linter/analyzer, complexity checker, type checker, test runner) are strictly binary (`exit 0` = `PASS`, `exit != 0` = `FAIL`). Design and craft principles written in the skill are mandatory compliance; reviewers grade violations on the unified 3-tier scale (`shared_contracts/flags_and_statuses.md` §2):

| Severity | Meaning | Review Verdict Impact |
|---|---|---|
| `BLOCKER` | Any failed CLI tool gate (`FAIL`), correctness/security defect, or violation of a mandatory design/contract rule (C1, C2, C3, C4, C11, C12, C14, C15, C16, C17) | `CHANGES_REQUESTED` (blocks approval) |
| `MAJOR` | Maintainability or structural issue not caught by CLI linters (C5, C6, C7, C10, C13) | Must be fixed in the same revision when inside task scope |
| `MINOR` | Redundant "what" comment (C8) or optional readability polish | Optional (never blocks approval) |

Reviewers grade only code modified in the current phase diff; pre-existing debt outside the diff is noted in `Concerns`, never as a blocker.
