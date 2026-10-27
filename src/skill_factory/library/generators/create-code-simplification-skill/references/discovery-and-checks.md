# Discovery of Real Examples & Per-Step Checks

Stack-neutral guide for finding the workspace's own avoidable complexity (catalog examples), its "already shipped" replacements, and the checks rerun after each simplification step.

---

## 1. Finding Real Catalog Examples (For `02-smell-catalog.md`)

Sample recent diffs (`git log -p` on the last 10–20 changes) and the longest changed files. For each lens, look for 1–2 real spots; a row with no real example is kept only when marked illustrative.

| Lens | What to look for | How to find it |
|---|---|---|
| **Reuse** | New helpers/components that duplicate an existing one; hand-rolled logic the standard library, framework or platform ships; two libraries for one job | For a new symbol, `rg -n "<distinctive part of its body or name>"` across the source tree; read the dependency manifest for overlapping libraries |
| **Simplification** | Interfaces with one implementation, pass-through layers, flag arguments, derivable state, deep nesting | `rg -n "<interface/abstract keyword>"` then count implementations; `rg -c` call sites of wrappers; complexity output from the workspace's analyzer |
| **Efficiency** | Repeated reads/queries in one path, per-item I/O in loops, sequential independent awaits/calls, heavy work at load time or in render/hot paths | Read the changed call path once end to end; `rg -n "<I/O call>"` inside loop bodies of changed files; query or request logs from an integration test |
| **Altitude** | Special cases in shared code (`if <caller> ==`, per-feature flags in shared helpers), fallbacks that hide an upstream cause, a new path added next to an old one | `rg -n "<feature or caller name>"` inside shared modules; read fallbacks/defaults added in the diff and trace where the bad value originates |

### "Already shipped" replacement table
Build a short table of hand-rolled patterns seen in the workspace → the standard library, framework or platform feature that replaces them, limited to what the workspace's language version and installed dependencies actually support. Put it in `02-smell-catalog.md` under the Reuse lens.

### Abstractions to leave alone
List the abstractions a workspace decision or an architecture port requires (from decision records and the clean-architecture skill). They go under "Leave these alone" in `02-smell-catalog.md`.

---

## 2. Per-Step Checks (For `01-scope-and-safety.md`)

Use only commands that exist in the workspace (configs, CI, task scripts). Each one is binary: `exit 0` = `PASS`, `exit != 0` = `FAIL`.

| Step | Command category | Purpose |
|---|---|---|
| **Scope** | Diff listing against the task's base (e.g. `git diff --name-only <base>...HEAD`) | The only files simplification may touch (S1) |
| **Before** | Affected unit tests | Prove the starting point is green (S1) |
| **After each step** | Formatter (check mode) → analyzer/linter → type checker → affected unit tests | Catch a behavior or contract change at the step that caused it (S2, S11) |
| **Callers** | `rg -n "<symbol>"` across source and tests, plus string/dynamic use (route names, reflection, config keys, task names) | Nothing outside the diff depends on what is being removed or renamed (S3) |
| **No leftovers** | `rg -n "<old symbol name>"` after a move or rename | No wrapper, alias or re-export left behind (S12, `clean-code` C1) |
| **No suppressions** | `rg -n "<lint/type suppression directive>" <changed files>` | No check silenced to make a simplification pass (S12) |

Keep each command and its exit code as an evidence row for the hand-off.
