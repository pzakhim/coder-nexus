# Smell catalog

Every simplification names one row. The stack's own smells and standard-library replacements come from `{{slot:clean-code}}`; it adds rows, it never removes these.

| Smell | How to recognise it | Technique | Watch out |
|---|---|---|---|
| Deep nesting | More than the nesting limit of `clean-code` CC7; arrow-shaped code; the happy path sits at the deepest level | Guard clauses and early returns; extract one well-named function per branch | Error paths keep their order and messages |
| Clever code | Nested comprehensions or lambdas, reduce chains, metaprogramming, dynamic-import tricks, recursion where a loop reads plainer, nested ternaries | Rewrite in the plain form a newcomer reads at once | Plain is not longer for its own sake: one level of a familiar construct is fine |
| Speculative abstraction | Interface or port with one implementation and no test fake, factory with one product, config nobody sets, parameter always passed the same value, hook for a need the spec does not have | Inline into the single user; keep the type only where it marks a real boundary | Ports required by `{{slot:clean-architecture}}` or a `D-NN` stay |
| Premature extraction | A shared function or base class extracted for two call sites that are starting to diverge (flags appear, branches per caller) | Inline it back into each caller; extract on the third real repetition (rule of three) | Applies to logic only, never to definitions (next row) |
| Duplicated definitions | The same type, schema, query, constant or validation rule written in two places | Keep one definition in its owning module; every user imports it (`clean-code` CC2, CC4) | Two definitions that only look alike but belong to different concepts stay separate |
| Long parameter list | More than the parameter limit of CC7; the same few values always travel together | Pass one named object for the values that belong together; drop parameters the function can derive | Do not invent a type for values that do not belong together |
| Flag argument | A boolean or mode parameter that switches the function between two jobs (`save(item, true)`) | Split into two functions named for each job; callers call the one they mean | A flag that is real data (a user's choice) is not a flag argument |
| Needless indirection | Pass-through layer, middle man, long call chains a caller should not depend on, a file that exports one trivial thing | Call the target directly; delete the hop (`clean-code` CC1) | Keep hops that add behavior: validation, authorization, mapping, caching |
| Dead code | Unused function, parameter, branch, flag, config, import or file; commented-out code | Delete it and the arguments its callers no longer need | Check dynamic use (reflection, string lookups, templates, routes) before deleting |

## Not smells (leave them)

- Logic repeated twice (rule of three), unless it duplicates a definition.
- An abstraction a `D-NN` or the stack's architecture requires.
- Long but linear code with one job: mapping tables, migrations, prompt text, generated code.
- Defensive checks at trust boundaries (input validation, authorization, data scope).

## Reduce or relocate?

Before keeping a change, count the concepts (names, branches, modes, layers) a reader must hold to follow the code, before and after. Same count means the complexity only moved: revert it. Prefer the change that makes a whole branch, mode or layer disappear.

## Candidate line (when listing before applying)

`<smell> at <path:line>: <what to cut> -> <replacement>`
