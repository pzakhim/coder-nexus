# Structure rules CC1–CC5 in detail

Examples are neutral pseudocode. The stack's private and export conventions, entry-file names and grep patterns come from `{{slot:clean-code}}`; folder placement from `{{slot:clean-architecture}}`.

## CC1 — Is it a wrapper?

Delete it when every answer is "no":

| Question | Example of a "yes" (keep, name it for this) |
|---|---|
| Does it validate or reject input? | `requireActiveCustomer(id)` refuses archived customers |
| Does it map between two shapes owned by different layers? | `toOrderSummary(record)` |
| Does it enforce authorization or a data scope? | `loadOrderForActor(actor, id)` |
| Does it cache, retry or translate errors with a reason? | `fetchRatesWithRetry()` |
| Is it a port or seam that `{{slot:clean-architecture}}` or a `D-NN` requires? | The repository interface a use case depends on |

A wrapper that forwards the same arguments to the same target (`getUser(id) → userRepository.getUser(id)`), a component that only passes all its props through, or a class whose methods all delegate onward is removed; callers call the target directly.

## CC2 — Renames and moves

- Update every caller found with a repository-wide search in the same task; delete the old name, file or export.
- Never leave `oldName = newName`, a re-export from the old path, or a "deprecated" shim.
- The only exception is a contract consumed outside this repository (published package, public API). It needs a `D-NN` that sets the deprecation window; otherwise the rename is a `plan-change-request`.

## CC3 — Module-level and global names

| Allowed at module level | Not allowed |
|---|---|
| A constant read by two or more functions of the module, never reassigned | A constant read by one function (move it into that function) |
| The workspace's configuration object, read once | Runtime caches, counters, registries or singletons written after load |
| Type and function definitions | "Current user", "current request" or other per-call state |
| | Values computed by I/O at load time (CC12) |

When shared mutable state is truly needed, it belongs to an owner the architecture names (an injected service, a state holder), never to a module variable. Adding one is P1.

## CC4 — Helper locality

1. A new helper starts private in the file that uses it, using the stack's private convention.
2. When a second file needs it, move it in that task: into the module that owns the concept (placement per `{{slot:clean-architecture}}`), with a name that says what it does (`formatInvoiceNumber`, not `utils.format`).
3. Before writing a helper, search for an existing one that does the same job; reuse it instead of adding a near-duplicate.
4. Never create or extend files or classes named `utils`, `helpers`, `common`, `misc` or `shared` without a concept in the name.

Making a one-user helper public, or exporting it from an entry file "for later", exposes internals (P1).

## CC5 — Package entry files

- List each exported symbol explicitly; no wildcard export.
- Export a symbol only when another module imports it today; remove exports nobody imports.
- Never export private helpers, implementation classes behind a port, test-only hooks or internal constants.
- Tests import what they test from its own file, not through a widened entry file.

## Checks

Run on the files changed in the task; a hit is a prompt to look, not proof. Record a false positive with its reason.

| Rule | Check |
|---|---|
| CC1 | For each new function or class whose body is one call, apply the CC1 table |
| CC2 | Search the repository for the old name after a rename or move: zero hits outside history and changelogs |
| CC3 | List new module-level assignments in the diff; for each, count readers inside the module and look for reassignment |
| CC4 | For each new non-private helper, count importing files: fewer than two means make it private again |
| CC5 | For each symbol added to an entry file, find an importer outside the package; search entry files for wildcard exports |
| CC8, CC9 | The debug-call and broad-catch patterns from `{{slot:clean-code}}`; the analyzer's unused-code warnings |
