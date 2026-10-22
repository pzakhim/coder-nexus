# Base rules (generic, every workspace)

Generalised from Coder Nexus `plugins/core/skills/clean-code` and the clean-code standard of a real fullstack workspace. Each rule goes into the generated skill with the workspace's facts **and its reason**, adapted to the workspace's contracts, or marked "not adopted" with a reason. If a gate already enforces a rule, cite the gate.

| # | Rule | Why | Default severity | Goes into |
|---|---|---|---|---|
| C1 | **One concept, one place.** No copy-pasted types, helpers, schemas or SQL; no aliases, wrappers or re-exports kept for old names. | Copies drift apart; the next fix lands in only one of them. | P1 | SKILL, 02 |
| C2 | **No dead code.** Remove unused functions, imports, files, variables; no commented-out code, no orphan `TODO`. | Dead code is read, maintained and trusted as if it ran. | P1 | 02 |
| C3 | **No debug code.** No `print`, `console.log`, `debugger`, `breakpoint()`, temporary flags. | Noise in logs, sometimes leaked data, and a sign the change was not cleaned up. | P1 | 03, 05 |
| C4 | **No swallowed errors.** Catch specific errors; handle or rethrow. Broad catches only at edges (global handler, worker loop) and always logged or recorded. | A swallowed error turns a loud failure into silent wrong data. | P1 | 03 |
| C5 | **Intention-revealing names.** Functions are verbs, booleans `is/has/can/should`, collections plural; no `data`, `info`, `tmp`, `Manager`, `Helper`, `Utils`, `process()`, `handle()`; one name per concept, matching the domain glossary. | Names are the main documentation; vague or double names cause misreads and duplicate concepts. | P2 | 01 |
| C6 | **Small, focused units.** Function ≤ ~30 lines, file ≤ ~300 lines, UI component ≤ ~150 lines, ≤ 3 parameters (else a named object), nesting ≤ 2 (use guard clauses) — for new or modified code. | Short units are easier to read, test and review; long ones hide several jobs. | P2 | 02 |
| C7 | **No magic values.** Named constants; enums / literal unions for states, roles, environments. | Scattered literals drift and break silently when one copy changes. | P2 | 04 |
| C8 | **Comments say why.** Explain non-obvious reasons and external constraints; never restate the code; keep unrelated existing comments. | "What" comments rot; "why" comments save the next reader an investigation. | P3 | 04 |
| C9 | **Full types.** No `any`, `# type: ignore`, unchecked casts or non-null assertions without a stated reason. | The type checker is free review; escapes hide real bugs. | P2 | 04 |
| C10 | **Change only the task's scope.** No drive-by renames, reformatting or modernising of untouched code. | Unrelated changes bury the real change in review and cause merge pain. | P2 | SKILL |
| C11 | **Workspace contracts win.** Follow the workspace's error/result types, nullability, state, DI, routing and formatting conventions over generic advice ("always throw", "never return null"). | Generic advice that contradicts a verified contract creates two styles in one codebase. | P1 | SKILL, 03 |
| C12 | **Visible side effects.** No DB, network, env reads or heavy work at import/module load (except the one settings object); side effects in clearly named functions. | Hidden side effects break tests and startup order. | P2 | 02 |
| C13 | **Explicit state changes.** Prefer immutable values; mutate only where the owner is clear. | Shared mutable state is the usual source of order-dependent bugs. | P3 | 04 |
| C14 | **Self-check before "done".** Run formatter, linter/analyzer, type checker and the task's tests; report what ran. | A rule without a check is a wish; an unrun check is not evidence. | P1 | 05 |

**Never "not adopted":** C1, C3, C4, C10, C11, C14.

## Severity scale (default)

| Level | Meaning | Review outcome |
|---|---|---|
| P1 | Correctness, safety or contract risk | Blocking (request changes) |
| P2 | Maintainability risk | Finding; not blocking on its own |
| P3 | Style / suggestion | Optional |

Reviewers grade only code changed in the phase; legacy debt outside the diff is not a blocker.

## Branch notes

- **Frontend:** components ≤ ~150 lines (split into subcomponents by UI responsibility); props ≤ ~6 (group or split); hooks return the minimum needed; no `useEffect` to sync derivable state; no premature `useMemo`/`useCallback`; no prop drilling beyond 2 levels.
- **Backend:** parameterised SQL only; repositories never commit; log with context (tenant, environment, request id); no work at import time outside settings.
- **Mobile:** widgets small and composable; no logic in `build()`; state holders own side effects.
