# Smell → Technique Catalog (Universal)

Stack-neutral rows grouped by the four review lenses. The generated `02-smell-catalog.md` keeps only the rows that occur in the workspace, each with a **real** example (path + one line) or marked illustrative, plus the workspace's own rows found with `discovery-and-checks.md`. Tags follow Coder Nexus `ponytail` (`delete`, `stdlib`, `native`, `yagni`, `shrink`) plus readability, efficiency and altitude techniques.

Ask in order before writing anything: **needed?** → **already in the repo?** → **standard library / framework / platform?** → only then write the minimum.

## 1. Reuse lens (S5, S7)

| Tag | Smell | Technique | Watch out |
|---|---|---|---|
| `reuse` | New code re-implements a helper, component or query the repository already has | Call the existing one; delete the new copy | The existing one must cover the same edge cases; do not bend it with flags |
| `stdlib` | Hand-rolled thing the standard library ships (date math, path handling, grouping, copying, retries in a loop) | Replace with the named standard function | Same edge-case behavior (time zones, encoding, ordering) |
| `native` | Code or a dependency doing what the framework or platform already does | Use the platform feature; drop the dependency if now unused | A wrapper a workspace decision requires stays |
| `delete` | Duplicated definition (type, schema, enum, constant, query) | One definition in its owning module; every user imports it (`clean-code` C1) | Look-alikes for different concepts (create vs response contract) stay separate |
| `inline` | Premature extraction: a shared helper for two call sites that now grows flags or per-caller branches | Inline back into each caller; extract on the third real repetition | Logic only — definitions are never duplicated |

## 2. Simplification lens (S6, S8)

| Tag | Smell | Technique | Watch out |
|---|---|---|---|
| `yagni` | Interface/port with one implementation and no test need, factory with one product, option nobody sets, parameter always passed the same value | Use the concrete thing; inline the single user | Ports required by clean-architecture or a decision stay |
| `inline` | Pass-through layer, middle man, wrapper that only delegates | Call the target directly; delete the hop | Keep hops that add validation, authorization, mapping, caching or error translation |
| `inline` | Flag argument switching two jobs | Two functions named for each job | A flag that is real user data is not a flag argument |
| `shrink` | Redundant or derivable state kept in sync by hand | Derive it where it is read | Cached derived values on a measured hot path stay (S9) |
| `shrink` | Copy-paste with slight variation inside the diff | One parameterized form, or a lookup table for the varying part | Rule of three (S7) for logic across call sites |
| `shrink` | Long parameter list; the same values always travel together | One typed structure for values that belong together; drop derivable parameters | Do not invent a type for unrelated values |
| `flatten` | Deep nesting, arrow code, happy path at the deepest level | Guard clauses, early returns; one well-named function per branch | Error paths keep their order, types and messages |
| `shrink` | Clever code: nested one-liners, chained reductions, metaprogramming, dynamic dispatch, recursion where a loop is plainer | Plain loop or one level of the idiomatic construct | Plain is not longer for its own sake |

Dead code (unused functions, parameters, imports, commented-out blocks) is `clean-code` C2: delete it after checking dynamic use.

## 3. Efficiency lens (S9)

| Tag | Smell | Technique | Watch out |
|---|---|---|---|
| `dedupe` | The same computation or I/O repeated within one call path (same query, file read or parse twice) | Compute once and pass the result | Values that must be fresh per access (time, remote state) stay repeated |
| `batch` | Per-item I/O in a loop (one query or request per element) | One batched call | Batch size, ordering and partial-failure behavior stay the same |
| `concurrent` | Independent operations run one after another | Run them concurrently with the stack's standard construct | Only when truly independent; error and cancellation behavior stay the same |
| `defer` | Blocking or heavy work added to startup, import/load time or a render/hot path | Move it to the explicit lifecycle point or first use | Startup checks that must fail fast stay at startup |
| `narrow` | Long-lived object (callback, listener, cache entry) built from a closure that captures a large scope | Capture only the fields it needs (a small value type) | Lifetime and release behavior stay the same |

Any change here on a hot path needs a measurement first (S13).

## 4. Altitude lens (S10)

| Tag | Smell | Technique | Watch out |
|---|---|---|---|
| `generalize` | Special case for one caller layered onto shared code (`if caller == X`, per-feature flags in a shared helper) | Change the underlying mechanism so the special case is not needed, or keep the special case in the caller | The general change must stay inside the diff; otherwise record it in Concerns |
| `root` | Symptom patched where it surfaces (fallback values, retry, re-sort, swallow-and-default) while the cause lives upstream in the same diff | Fix the cause; delete the patch | A fix outside the diff is a Concerns note, never a drive-by edit |
| `merge` | Two mechanisms for the same job added side by side (a new path next to the old one) | Keep one; move callers to it in the same step | Old callers outside the diff → Concerns |

## Not smells (leave them)

- Duplication of two call sites (rule of three), unless it duplicates a definition.
- An abstraction a workspace decision or architecture port requires.
- Long but linear code with one responsibility (mapping tables, migrations, prompt text, generated code).
- Defensive checks at trust boundaries (input validation, authorization, data scope).

## Candidate line (before editing)

`<lens>/<tag> at <path:line>: <what to cut> -> <replacement>`
