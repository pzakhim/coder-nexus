# 01 — Structure, Naming, and Types (Flutter / Dart)

Consolidated rules for naming (**C5**), size thresholds and widget decomposition (**C6**), one-concept-one-place (**C1**), sound null safety (**C9**), `const` & design tokens (**C7, C15**), comments (**C8**), immutable state (**C13**), helper locality (**C16**), and barrel exports (**C18**).

---

## 1. Identifier & Layer Naming (C5, C11)

Follow **Effective Dart** (`UpperCamelCase` types, `lowerCamelCase` members/constants, `lowercase_with_underscores` files, `is`/`has`/`can`/`should` boolean prefixes, leading `_` for single-file privates) and the active `architecture_profile`.
- **Forbidden vague names**: `data`, `info`, `temp`, `val`, `process()`, `handle()`, `Manager`, `Helper`, `Utils`.

---

## 2. Unified Size Thresholds & Widget Decomposition (C6)

| Unit | Threshold | Remedy when exceeded |
|---|---|---|
| Method / Function | ≤ 30 lines | Extract focused private helper methods with guard clauses. |
| Widget `build()` method | ≤ 50 lines | Extract dedicated private `StatelessWidget` / `StatefulWidget` classes. |
| Class | ≤ 200 lines | Separate presentation layout from state management (`Cubit`/`Bloc`). |
| File | ≤ 300 lines | Split sub-widgets into `presentation/widgets/` (or cohesive files in the same layer). |
| Parameters | ≤ 4 parameters | Use named parameters or group cohesive inputs into a parameter object. |
| Widget tree nesting | ≤ 4 levels | Extract intermediate sub-widgets to flatten the tree. |

- **Split Ownership Rule**: Routine internal widget/helper extraction inside the same module (e.g., splitting a screen file > 300 lines into `presentation/widgets/`) is performed **directly by `code_writer`** without a `PCR-NN`. Escalate via `PCR-NN` (`PLAN_CONFLICT`) **only** when splitting crosses module boundaries, shared public APIs, or plan ownership.
- **Extract Private Widget Classes, Never `_buildX()` Methods**: Helper methods returning `Widget` cannot use `const`, re-run on every parent rebuild, bloat `State`, and risk capturing stale `BuildContext`. Extract `class _SectionWidget extends StatelessWidget` with a `const` constructor instead.

---

## 3. One Concept, One Place & Helper Locality (C1, C16)

- **No pass-through wrappers or aliases (C1)**: Never add a class or function that merely forwards calls without adding behavior, transformation, or boundary translation. When renaming a symbol, update all call sites in the same task—never leave compatibility typedefs or re-exports.
- **Reuse approved foundations (C1, C11)**: Check the workspace's resolved foundation profile (`architecture_profile`) before creating custom buttons, inputs, dialogs, or network wrappers.
- **Helper locality (C16)**: Keep single-file helpers private (`_name`). Promote to a shared module only when **2+ files** import it, owned by the feature/domain concept—never create `utils.dart`, `helpers.dart`, or `common.dart` buckets.

---

## 4. Explicit Export Surface (C18)

- Prefer direct imports from defining files; add a barrel only when multiple external modules consume the same cohesive set of symbols.
- Every `export` directive must use `show` listing **only** symbols actually imported externally (`export 'domain/entities/order.dart' show Order;`). Never use bare `export 'file.dart';` or export `src/` internals, data implementations, or test hooks.

---

## 5. Sound Null Safety, `const`, Tokens & Comments (C7, C8, C9, C13, C15)

- **Sound Null Safety (C9)**: Avoid `!` unless immediately guarded in the same scope; prefer `?.`, `??`, guard clauses, or Dart 3 pattern matching (`if (state case OrderLoaded(:final items))`). Never use `dynamic` or untyped `Map` in domain entities or presentation states.
- **Immutable State & Value Objects (C13)**: Keep all entity, DTO, and `State` fields `final`; emit new instances via `copyWith` or sealed subclasses.
- **`const` Everywhere (C15) & Design Tokens (C7)**: Mark widget constructors and instances `const` whenever compile-time constant. Use theme/design-system tokens instead of hardcoded `Color(0xFF...)`, `TextStyle(fontSize: ...)`, or raw layout magic numbers.
- **Comments Explain WHY (C8)**: Document business invariants or platform workarounds only; delete comments restating code.
