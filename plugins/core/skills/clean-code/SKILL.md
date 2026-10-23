---
name: clean-code
description: Stack-neutral clean-code rules for code written or changed inside an approved task - no wrappers or kept aliases, no meaningless module-level or global variables, helpers private to their file until a second file needs them, package entry files that export only what other modules use, plus naming, small units, no dead or debug code, no swallowed errors, no magic values, why-comments, visible side effects and scope discipline - with P1/P2/P3 review severities and a self-check before done. Use while the Code Writer implements a task, during the self-check before READY_FOR_REVIEW, and when the Code Reviewer grades code quality. The stack's idioms come from the stack's clean-code slot.
---

# Clean Code

Goal: code a newcomer reads correctly on the first pass and changes in exactly one place. Every rule below carries its reason; a rule you cannot explain to the writer is not a finding.

## Where the rules come from

| Order | Source | Gives |
|---|---|---|
| 1 | Approved plan, `## Global constraints`, every `D-NN` | What this phase may and may not change |
| 2 | Workspace contracts and `.agents/skills/clean-code/` (when the workspace has one) | Real names, thresholds, error/result types, commands |
| 3 | `{{slot:clean-code}}` | The stack's idioms, private/export conventions, debug calls, simplification smells |
| 4 | This skill | The rules below where nothing above is more specific |

Structure and placement (layers, modules, where a shared piece goes) belong to `{{slot:clean-architecture}}`; it wins on conflict. Reducing a working diff belongs to `code-simplification`; security rules to `secure-coding`.

## Rules

Structure rules CC1–CC5 are mandatory: only a `D-NN` can make an exception, and the exception is cited at the code site's review row. Detail, tests and examples: [references/structure-rules.md](references/structure-rules.md).

| # | Rule | Why | Severity |
|---|---|---|---|
| CC1 | **No wrappers or pass-through functions.** A function, class or component that only forwards to another is deleted; callers call the target. Keep a wrapper only when it adds behavior (validation, mapping, authorization, caching, error translation) and name it for that behavior. | Each hop is a file the reader opens to learn nothing, and a second place to fix. | P1 |
| CC2 | **No aliases or re-exports kept for old names.** A rename or move updates every caller in the same task and deletes the old name. | Two names for one thing: readers cannot tell which is canonical, and the old one never dies. | P1 |
| CC3 | **No meaningless module-level or global variables.** Module level holds only true shared constants (read by two or more functions, never reassigned) and the workspace's configuration object. No mutable global state. A constant used by one function lives inside that function. | Every module-level name widens what a reader must track; mutable globals cause order-dependent bugs and leak between tests. | P1 mutable state added, else P2 |
| CC4 | **Helpers stay local until a second file needs them.** A helper used by one file is private to that file. Move it to a shared place only when a second file needs it, into the module that owns the concept, named for what it does; never `utils`, `helpers`, `common` or `misc`. | A shared helper with one user is a public API nobody asked for; generic buckets become junk drawers. | P1 when internals get exposed, else P2 |
| CC5 | **Package entry files export only what other modules use.** Barrel, index or init files list each symbol another module actually imports; no wildcard export; never expose internals (private helpers, implementation classes, test hooks). | Every export is a contract to keep; wildcards leak internals and hide unused code. | P1 when internals exposed, else P2 |
| CC6 | **Intention-revealing names.** Verbs for functions, `is/has/can/should` for booleans, plurals for collections, the domain glossary's term for each concept; no `data`, `info`, `tmp`, `Manager`, `process()`, `handle()`. | Names are the main documentation; vague names cause misreads and duplicate concepts. | P2 |
| CC7 | **Small, focused units.** One job per function, class or file; thresholds from the workspace skill, else ~30 lines per function, ≤ 3 parameters (else a named object), nesting ≤ 2 with guard clauses, for new or modified code. | Short units are easier to read, test and review; long ones hide several jobs. | P2 |
| CC8 | **No dead or debug code.** No unused functions, imports, files, variables or parameters; no commented-out code, orphan `TODO`, debug prints or temporary flags. | Dead code is read and trusted as if it ran; debug output leaks data and noise. | P1 |
| CC9 | **No swallowed errors.** Catch specific errors and handle or rethrow them; broad catches only at edges (global handler, worker loop), always logged or recorded. Never return fake data to look successful. | A swallowed error turns a loud failure into silent wrong data. | P1 |
| CC10 | **No magic values.** Named constants, enums or literal unions for states, roles, environments and limits. | Scattered literals drift and break silently when one copy changes. | P2 |
| CC11 | **Comments say why.** Explain non-obvious reasons and external constraints; never restate the code; leave unrelated existing comments alone. | "What" comments rot; "why" comments save the next reader an investigation. | P3 |
| CC12 | **Visible side effects.** No I/O, network, environment reads or heavy work at import or module load (except the configuration object); side effects live in clearly named functions. | Hidden side effects break tests and startup order. | P2 |
| CC13 | **Workspace contracts win.** Follow the workspace's error/result types, nullability, state, dependency wiring and formatting over generic advice ("always throw", "never return null"). | Generic advice against a verified contract creates two styles in one codebase. | P1 |
| CC14 | **Change only the task's scope.** No drive-by renames, reformatting or modernising of untouched code; debt found outside the scope goes into the handoff's Concerns. | Unrelated edits bury the real change in review and invalidate evidence for nothing. | P2 |
| CC15 | **Self-check before done.** Run the checks below on the changed files and record each result. | A rule without a check is a wish; an unrun check is not evidence. | P1 |

Labelled smells from `code-simplification` are judgement calls; the rules above are not.

## Self-check before READY_FOR_REVIEW

1. Run the formatter, analyzer, type checker and the task's tests named by `{{slot:verification}}` and the task's `Acceptance Criteria`. Record each as an evidence row (`evidence-before-claims`); a check that did not run is `NOT_RUN`, never PASS.
2. Run the rule checks from [references/structure-rules.md](references/structure-rules.md) "Checks" on the changed files: new module-level names, helper users, entry-file exports, debug calls and broad catches from `{{slot:clean-code}}`.
3. Fix every hit inside the task's scope in the same revision. A hit outside the scope goes into Concerns; a fix that needs a plan change goes through `plan-change-request`.
4. List what you removed or merged (wrappers, aliases, dead code) in the handoff.

## Review severity

The Code Reviewer grades only code changed in the phase; legacy debt outside the diff is never a blocker.

| Level | Meaning | Review outcome |
|---|---|---|
| P1 | Correctness, contract or maintainability trap that spreads (wrapper, alias, exposed internals, mutable global, swallowed error, dead/debug code, skipped self-check) | `CHANGES_REQUESTED` |
| P2 | Maintainability risk | Finding; fixed in the same revision when inside scope, does not block alone |
| P3 | Style or suggestion | Optional |

A violation that also produces a wrong result, crash or leak is reported by `bug-hunt` on its scale (`BLOCKER` / `MAJOR` / `MINOR`), not here. Finding row: `file:line | rule | severity | one-sentence reason | fix direction`. Lead with P1; a few high-conviction findings beat a long list of P3.

## Sources

[references/sources.md](references/sources.md)
