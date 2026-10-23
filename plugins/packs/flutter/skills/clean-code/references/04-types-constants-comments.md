# 04 - Types, Constants, and Comments (Flutter / Dart)

Maintain sound null safety, reusable constants, and meaningful code comments.

## 1. Sound Null Safety & Types

- **Avoid the Bang Operator (`!`):**
  - Using `!` (null assertion) tells Dart to bypass compile-time null safety. If the value is null at runtime, it throws an unhandled `NullCheckError`.
  - **Preferred:** Use null-aware operators (`?.`, `??`), null-coalescing defaults, or guard clauses:
    ```dart
    // BAD
    final title = order!.item!.name!;

    // GOOD
    final title = order?.item?.name ?? 'Untitled';
    ```
- **No `dynamic` or Raw Untyped Maps:**
  - Avoid `dynamic` in domain entities and presentation state.
  - Parse untyped JSON maps in the data layer using `app_util` helpers (`parseString`, `parseInt`, `parseList`) and map them immediately into strongly typed DTOs/Entities.
- **Strict Generics:** Always specify type arguments on Collections, Cubits, Streams, and Futures (e.g. `List<OrderEntity>`, `BlocBuilder<OrderCubit, OrderState>`).

## 2. Const Constructors & Magic Values

- **Const Constructors Everywhere:**
  - Declare `const` on widget constructors and instantiation sites whenever properties are immutable compile-time constants.
  - Const widgets are canonicalized by the Dart VM and reused across rebuilds without re-allocating memory.
- **Design Tokens & Magic Values:**
  - **Colors:** Use tokens from `app_ui_kit` (`AppColor.primary`, `AppColor.textSecondary`, etc.). Never write raw `Color(0xFF...)` in presentation widgets.
  - **Typography:** Use `Text12`, `Text14`, `Text16`, `Text20` widgets from `app_ui_kit` instead of ad-hoc `TextStyle(fontSize: 14)`.
  - **Dimensions:** Declare layout constants (e.g. `kSpacingSm = 8.0`, `kSpacingMd = 16.0`) or use shared constants instead of arbitrary numeric paddings.

## 3. Comments and Documentation

- **Explain "Why", Not "What":**
  - Good comments explain business domain edge cases, workaround rationale, or platform bug workarounds.
  - Redundant comments that simply parrot the method name must be deleted.
- **Preserve Existing Comments:** Do not delete existing comments or copyright headers during unrelated modifications.
