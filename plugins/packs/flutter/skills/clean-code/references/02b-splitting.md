# 02b - Splitting Widgets and Classes

When Flutter code exceeds size thresholds or mixes concerns, follow these decomposition guidelines.

## 1. Helper Methods vs Private Widget Classes

**Rule:** Always prefer extracting dedicated private `StatelessWidget` / `StatefulWidget` classes over writing `_buildItem()` helper methods.

### Why Helper Methods are an Anti-Pattern
```dart
// BAD: Helper method inside State class
Widget _buildOrderItem(OrderItem item) {
  return Container(
    padding: const EdgeInsets.all(12),
    child: Text(item.title),
  );
}
```
1. **Inefficient Rebuilds:** Flutter cannot optimize rebuilds of helper methods. When `setState()` or `BlocBuilder` fires, every helper method re-executes, even if its inputs haven't changed.
2. **Missing Const Caching:** Helper methods cannot have `const` constructors. Dedicated widget classes can be declared `const`, preventing sub-tree invalidation.
3. **Bloated State Class:** The screen state class becomes 400+ lines of mixed layout and event logic.
4. **Poor Context Scoping:** Helper methods share the parent's `BuildContext`, creating subtle bugs with `Theme.of(context)` or `MediaQuery.of(context)`.

### Recommended Pattern
```dart
// GOOD: Dedicated private StatelessWidget with const constructor
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

## 2. When and Where to Split

1. **Screen file reaches ~200 lines:**
   - Extract private sub-widgets into separate files under `lib/modules/<feature>/presentation/widgets/`.
   - Keep the `*_screen.dart` strictly focused on route wiring, `BaseScreenState`, and top-level layout structure.
2. **State Management Extraction:**
   - Never hold complex business state directly in `StatefulWidget`. Extract state transitions into a dedicated `Cubit` in `presentation/cubit/`.
   - Use `StatefulWidget` only for local UI animations, scroll listener offsets, or transient focus handling.
3. **Domain & Data Layer Boundaries:**
   - Do not combine Data Sources, Repositories, and Mappers in a single file.
   - Maintain the standard Clean Architecture directory hierarchy per [clean-architecture](../../flutter-clean-architecture/SKILL.md).
