# Splitting long files: clean-code ↔ clean-architecture

## Division of roles

| | Answers | Decides |
|---|---|---|
| **clean-code** | Should this be split? Into which pieces? | Boundaries by **responsibility** (each piece does one thing) |
| **clean-architecture** | Where does each piece go? Who may import whom? | Target **layer & folder**, keeping the dependency rule intact |

Split by responsibility first, then decide placement. Never split purely because of line count.

## 6-step protocol

1. **Detect:** a file/function/component exceeds the project threshold, or a file does more than one thing even below the threshold.
2. **List responsibilities:** read the file and give each block a one-line label ("validate input", "compute price", "call payment API", "render table").
3. **Classify into layers:** run each label through the decision tree in file 03 (creating files) to get the target layer + folder.
4. **Choose the split form:**
   - Same layer, same feature → sibling file next to the original.
   - Several pieces in the same layer → group in a subfolder with a public API (`index`).
   - Different layer → move into that layer's folder within the same feature.
   - Used by ≥ 3 features → `shared` (following the shared-code rules).
5. **Execute:** move code, keep the old public API so external imports do not break, fix imports in the allowed direction.
6. **Verify:** tests pass, import-boundary lint passes, no circular imports, the original file now has a single responsibility.

## Smell → destination

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

- The file is long but has one responsibility and reads linearly (mapping tables, config, migrations, generated code).
- Splitting would create circular imports or break the dependency rule → redesign the boundary instead.
- The extracted piece would be tiny (< ~10 lines) and used once → keep it as a private function.

## Never

- Split into `part1`, `part2`, `utils2`.
- Push code into `shared` just to make the original file shorter.
- Change behavior while splitting; refactoring and logic changes are separate commits.
