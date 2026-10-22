# Splitting long code: clean-code ↔ clean-architecture

Shared by the clean-code and clean-architecture generators. Each generated skill writes **its own half** with the workspace's paths and links to the other half.

## Division of roles

| Skill | Answers | Owns | Protocol steps |
|---|---|---|---|
| **clean-code** | Should this be split? Into which pieces? What are they called? | Thresholds; boundaries by **responsibility** (one piece = one job); names | 1, 2, 5 (names) |
| **clean-architecture** | Where does each piece go? Who may import it? | Target **layer & folder**; dependency rules | 3, 4 |
| both | — | — | 5 (move), 6 (verify) |

Split by responsibility first, then decide placement. Never split purely because of line count. Thresholds live **only** in clean-code; clean-architecture links to them.

## 6-step protocol

1. **Detect** (clean-code): over a clean-code threshold, or more than one job even below it. Signs of several jobs: "and" in the honest name, mixed levels of abstraction (SQL next to business rules next to formatting), several reasons to change, long parameter lists, deep nesting.
2. **List responsibilities** (clean-code): give each block a one-line label ("validate input", "compute price", "call payment API", "render table"). Each label is a candidate piece; name it per the clean-code naming rules.
3. **Place each piece** (clean-architecture): run each label through clean-architecture's "where does new code go" decision tree to get layer + folder.
4. **Choose the form** (clean-architecture):
   - Same layer, same module/feature → sibling file next to the original.
   - Several pieces with one role → a whitelisted subfolder.
   - Different layer → that layer's folder in the same module/feature.
   - Reused by other modules/features → the shared location allowed by the dependency rules (and only then).
5. **Move** (both): move the code, update **every** caller and test, delete the old code. Keep only the module/feature's real public entry (its barrel / `__init__`), never a re-export shim kept "so imports do not break".
6. **Verify** (both): tests pass, the import/boundary gates pass, no cycles, the original file now has one responsibility; behavior unchanged.

## No clean-architecture skill in the workspace

When only clean-code exists, its splitting reference uses this fallback for steps 3–4:

- Keep every piece inside the **same module/feature**, as sibling files next to the original (or in an existing subfolder with the same role).
- Never create new top-level folders or new layers.
- Ask the user before moving anything to a shared/common location.

## Smell → destination (clean-architecture side)

| Smell in the long file | Move to |
|---|---|
| Business rules inside a controller/component/widget | Domain (entity / value object) or a use case |
| Direct DB/HTTP/SDK calls in a use case or UI | Infrastructure (repository/adapter); the use case calls it through an interface |
| Long data-mapping blocks (DTO ↔ entity ↔ model) | A mapper file in the layer that owns the source data |
| Long input-validation schemas | A schema/DTO file in the feature's presentation layer |
| Long type/interface/constant declarations | `*.types` / `*.constants` next to the original |
| Component/widget nesting many UI blocks | Sub-components in the feature's `components/`/`widgets/` |
| Component with lots of state & side effects | The feature's hook / controller / notifier / bloc |
| Long multi-step function | Private functions named after each step, same file if the file is still fine |
| Service/use case handling several operations | One use case per operation |
| Logic reused by ≥ 3 features | `shared` or its own feature |

## Do not split when

- The file is long but has one responsibility and reads linearly (mapping tables, config, migrations, generated code, prompt text).
- Splitting would create circular imports or break the dependency rule → redesign the boundary instead.
- The extracted piece would be tiny (< ~10 lines) and used once → keep it as a private function.
- A legacy file the current phase does not touch.

## Never

- Split into `part1`, `part2`, `utils2`.
- Push code into `shared` just to make the original file shorter.
- Change behavior while splitting; refactoring and logic changes are separate steps.
