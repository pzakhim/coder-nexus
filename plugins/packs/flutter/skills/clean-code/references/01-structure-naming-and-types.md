# 01 — Structure, Naming, and Types (Flutter / Dart)

Consolidated rules for naming (**C5**), size thresholds and widget decomposition (**C6**), one-concept-one-place (**C1**), sound null safety (**C9**), `const` & design tokens (**C7, C15**), comments (**C8**), immutable state (**C13**), helper locality (**C16**), and barrel exports (**C18**).

---

## 1. Identifier & Layer Naming (C5, C11)

Follow **Effective Dart** and the active workspace conventions (`flutter-core-package-usage`):

| Element | Convention | Good | Bad |
|---|---|---|---|
| Classes, Mixins, Enums, Extensions, Typedefs | `UpperCamelCase` | `OrderRepository`, `OrderListCubit` | `order_repository`, `orderListCubit` |
| Libraries, packages, files, directories | `lowercase_with_underscores` | `order_details_screen.dart` | `OrderDetailsScreen.dart`, `orderDetails.dart` |
| Variables, parameters, getters, methods | `lowerCamelCase` (verbs for actions) | `fetchOrders()`, `itemCount` | `FetchOrders()`, `item_count` |
| Booleans | Prefix `is`, `has`, `can`, `should` | `isLoading`, `hasMore`, `canSubmit` | `loading`, `flag`, `statusBool` |
| Constants | `lowerCamelCase` or `kCamelCase` | `kDefaultTimeout`, `defaultPadding` | `DEFAULT_TIMEOUT` |
| Private members / local widgets | Leading `_` | `_OrderSummaryCard`, `_parseItem()` | Public helper used in only one file |

- **Vague names forbidden**: Never name variables or classes `data`, `info`, `temp`, `val`, `process()`, `handle()`, `Manager`, `Helper`, or `Utils`.

---

## 2. Size Thresholds & Widget Decomposition (C6)

| Unit | Threshold | Remedy when exceeded |
|---|---|---|
| Method / Function | ≤ 30 lines | Extract focused private helper methods with guard clauses. |
| Widget `build()` method | ≤ 40 lines | Extract dedicated private `StatelessWidget` / `StatefulWidget` classes. |
| Class | ≤ 200 lines | Separate presentation layout from state management (`Cubit`/`Bloc`). |
| File | ≤ 250 lines | Split sub-widgets into `presentation/widgets/`. |
| Parameters | ≤ 4 parameters | Use named parameters or group cohesive inputs into a parameter object. |
| Widget tree nesting | ≤ 4 levels | Extract intermediate sub-widgets to flatten the tree. |

### Extract Private Widget Classes, Never `_buildX()` Methods
- **Anti-pattern (`Widget _buildOrderItem(...)`)**: Helper methods returning `Widget` cannot have `const` constructors, re-execute on every parent rebuild, bloat the `State` class, and risk capturing stale parent `BuildContext`.
- **Required pattern**:
  ```dart
  class _OrderItemCard extends StatelessWidget {
    const _OrderItemCard({required this.item});
    final OrderItem item;

    @override
    Widget build(BuildContext context) {
      return Padding(
        padding: const EdgeInsets.all(12),
        child: Text(item.title),
      );
    }
  }
  ```

---

## 3. One Concept, One Place & Helper Locality (C1, C16)

- **No pass-through wrappers or aliases (C1)**: Never create a class or function that merely forwards calls without adding behavior, transformation, or boundary translation. When renaming a symbol, update all call sites in the same task—never leave compatibility typedefs or re-exports.
- **Reuse approved foundations (C1, C11)**: Before creating a custom button, input, dialog, or network wrapper, check the workspace's resolved foundation profile (`flutter-core-package-usage`).
- **Helper locality (C16)**:
  - A helper function or sub-widget used by a single file stays private (`_name`) inside that file.
  - Extract to a shared file only when **two or more files** import it, placing it in the domain/feature module that owns the concept.
  - Never create generic `utils.dart`, `helpers.dart`, or `common.dart` junk-drawer files.

---

## 4. Explicit Export Surface (C18)

Applies to barrel files owned by the Client (library entry files containing `export` directives):
- Prefer direct imports from the defining file; add a barrel only when multiple external modules import the same cohesive set of symbols.
- Every `export` directive must use `show` to list **only** the symbols actually imported by other modules (including tests).
- Never use bare `export 'file.dart';` (which leaks all public symbols of that file).
- Never export `src/` internals, `_private` helpers, data models/mappers (when callers only need domain entities), or test hooks.

```dart
// GOOD: explicit export surface
export 'domain/entities/order.dart' show Order;
export 'presentation/screens/order_list_screen.dart' show OrderListScreen;

// BAD: bare exports leaking internal implementations
export 'data/order_repository_impl.dart';
export 'src/order_mapper.dart';
```

---

## 5. Sound Null Safety, `const`, Tokens & Comments (C7, C8, C9, C13, C15)

- **Sound Null Safety (C9)**:
  - Do not use the bang operator (`!`) unless immediately preceded by an explicit null check in the same scope; prefer `?.`, `??`, guard clauses (`if (value == null) return ...;`), or Dart 3 pattern matching (`if (state case OrderLoaded(:final items))`).
  - Never use `dynamic` or raw untyped `Map` in domain entities or presentation states. Always specify explicit generic type arguments (`List<OrderEntity>`, `BlocBuilder<OrderCubit, OrderState>`).
- **Immutable State & Value Objects (C13)**:
  - All fields on domain entities, DTOs, and presentation `State` classes must be `final`. Emit new state instances via `copyWith` or sealed subclasses—never mutate state fields in place.
- **`const` Everywhere (C15) & Design Tokens (C7)**:
  - Mark widget constructors and instantiations `const` whenever inputs are compile-time constants.
  - Use theme colors, text styles, and spacing tokens from the workspace's design system/theme instead of hardcoded `Color(0xFF...)`, `TextStyle(fontSize: ...)`, or magic numbers.
- **Comments Explain WHY (C8)**:
  - Document non-obvious business constraints, platform workarounds, or invariants. Delete comments that merely restate the method or variable name. Preserve unrelated existing comments.
