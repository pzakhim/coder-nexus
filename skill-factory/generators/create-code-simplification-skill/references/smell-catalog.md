# Smell → technique catalog

Tags follow Coder Nexus `ponytail` (`delete`, `stdlib`, `native`, `yagni`, `shrink`) plus three readability techniques. The generated `03-smell-catalog.md` keeps the rows that occur in the workspace, each with a **real** example.

| Tag | Smell | Technique | Watch out |
|---|---|---|---|
| `delete` | Dead code, unused parameter/flag/config, speculative branch, commented-out code | Remove it and its callers' unused arguments | Check dynamic use (reflection, string imports, templates) before deleting |
| `stdlib` | Hand-rolled thing the standard library ships (date math, path handling, grouping, deep copy, retries in a loop) | Replace with the named stdlib function | Same edge-case behavior (time zones, encoding) |
| `native` | Dependency or code doing what the platform/framework already does (fetch wrapper re-implementing the framework client, CSS done in JS) | Use the platform feature; drop the dependency if unused | The workspace's chosen transport/wrapper stays if a decision requires it |
| `yagni` | Interface/port with one implementation and no test need, factory with one product, config nobody sets, layer with one caller | Inline into the single user; keep the type only where it marks a real boundary | Ports required by clean-architecture or a decision stay |
| `shrink` | Same logic in more lines than needed (manual loops building lists, repeated conditionals) | Show the shorter clear form (comprehension, early return, lookup table) | Not "clever": one level of comprehension, no reduce chains |
| `flatten` | Deep nesting, arrow code, flags controlling flow | Guard clauses, early returns, extract a well-named function per branch | Error paths keep their order and messages |
| `rename` | Misleading or vague names that force reading the body | Rename per clean-code naming (all callers, no alias) | Public API names follow the contract; change only inside the diff |
| `inline` | Pass-through function/component/hook, wrapper that only delegates, file exporting one trivial thing | Call the target directly; delete the wrapper | Keep wrappers that add real behavior (validation, auth, caching, mapping) |

## Not smells (leave them)

- Duplication of two (rule of three), unless it duplicates a definition.
- An abstraction a workspace decision requires.
- Long but linear code with one responsibility (mapping tables, migrations, prompt text).
- Defensive checks at trust boundaries (input validation, authorization).

## Output line per finding (when listing before applying)

`<tag> <what to cut>. <replacement>. [path:line]`
