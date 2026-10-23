# 03 - Flutter & Dart Smell Catalog

Identify common code smells in Flutter applications and replace them with standard solutions.

## 1. Widget & UI Smells

### A. Reinventing `app_ui_kit` Components
- **Smell:** Assembling a `GestureDetector` + `Container` + `Text` + `CircularProgressIndicator` to make a button.
- **Replacement:** `AppButton(buttonType: AppButtonType.primary, title: 'Submit', isLoading: state.isLoading, onPressed: () => ...)`.

### B. Helper Methods Returning Widgets
- **Smell:** `Widget _buildHeader() { return ...; }` inside a `StatefulWidget`.
- **Replacement:** Dedicated `class _HeaderWidget extends StatelessWidget` with `const` constructor.
- **Why:** Enables Dart VM const canonicalization and prevents full subtree rebuilds on parent `setState()`.

### C. Overly Deep Layout Pyramids
- **Smell:** `Container` wrapping `Padding` wrapping `DecoratedBox` wrapping `SizedBox`.
- **Replacement:** Combine padding, decoration, and dimensions into a single `Container` or `Padding` widget.

## 2. Dart & State Management Smells

### A. Imperative Collection Loops in Widget Trees
- **Smell:** Creating a temporary `List<Widget> list = []`, running a `for` loop with `list.add(...)`, then passing `list` to `Column.children`.
- **Replacement:** Declarative collection-`for` and spread operator `...`:
  ```dart
  Column(
    children: [
      for (final item in items)
        _ItemCard(item: item),
    ],
  )
  ```

### B. Verbose Null Checks & Ternaries
- **Smell:** `final name = user != null ? (user.name != null ? user.name : '') : '';`
- **Replacement:** `final name = user?.name ?? '';`

### C. Manual Paging State Logic
- **Smell:** Manually tracking `page`, `pageSize`, `ScrollController.addListener`, and load-more spinners in screens.
- **Replacement:** Use `ListViewPaging<T>` from `app_core`.
