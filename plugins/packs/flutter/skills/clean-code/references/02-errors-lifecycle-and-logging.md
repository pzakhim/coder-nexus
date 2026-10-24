# 02 — Errors, Lifecycle, and Logging (Flutter / Dart)

Consolidated rules for error handling (**C4, C11**), pure `build()` and widget lifecycle (**C12**), controller/stream disposal (**C17**), and structured logging without debug leftovers (**C3**).

---

## 1. Error Handling & Boundary Translation (C4, C11)

Swallowing exceptions creates silent bugs and leaves screens stuck in perpetual loading states.

- **No swallowed errors**: Never write an empty `catch (_) {}` or ignore a failed result.
- **Data / Repository boundary translation**:
  - Catch specific exceptions (`DioException`, `FormatException`, `TimeoutException`, platform exceptions) at the data/repository boundary and translate them into the workspace's typed result/failure contract (per `flutter-core-package-usage`, e.g., `Result<T>` / `Either<Failure, T>` / `DataState<T>`).
  - Never let raw network or JSON parsing exceptions bubble unhandled into the UI widget tree.
- **State holder handling**:
  - Every asynchronous action in a `Cubit` / `Bloc` / `Notifier` must handle both success and failure outcomes, logging operational errors and emitting an explicit failure state so the UI can render error feedback or retry controls.

```dart
// BAD: Swallowing error
try {
  await repository.submitOrder(request);
} catch (e) {
  // Silent ignore — BLOCKER violation!
}

// GOOD: Explicit error handling, logging, and state emission
final result = await repository.submitOrder(request);
switch (result) {
  case Success(:final data):
    emit(state.copyWith(status: OrderStatus.success, order: data));
  case Failure(:final error):
    logger.error('Failed to submit order', error: error);
    emit(state.copyWith(status: OrderStatus.failure, errorMessage: error.message));
}
```

---

## 2. Pure `build()` & Widget Lifecycle (C12, C11)

- **Pure `build()` methods (C12)**:
  - `build(BuildContext context)` (or the workspace's base screen builder method per `flutter-core-package-usage`) must be deterministic and free of side effects.
  - **Never** trigger network calls (`cubit.load()`), navigation (`Navigator.push` / `context.go`), dialogs/snackbars, or state mutations directly inside `build()`.
  - Trigger initialization in `initState()` or route provider creation, and trigger navigation/dialogs inside `BlocListener` or user event callbacks.
- **Async `BuildContext` safety**:
  - After any `await` in a `StatefulWidget` or callback, check `if (!context.mounted) return;` before using `context`.
- **Workspace Base Screen contracts (C11)**:
  - Follow the approved `architecture_profile` (`flutter-core-package-usage`). If the project uses a custom base screen lifecycle (such as responsive/analytics base states), override only the designated layout builders and never bypass lifecycle hooks.

---

## 3. Resource & Subscription Disposal (C17)

Every `State` or state holder (`Cubit` / `Bloc` / `ChangeNotifier`) that owns disposable resources **must** release them in `dispose()` or `close()`:
- `TextEditingController`, `ScrollController`, `PageController`, `TabController`
- `AnimationController`, `FocusNode`
- `StreamSubscription`, `Timer`, `Debouncer`

```dart
@override
void dispose() {
  _searchController.dispose();
  _scrollController.dispose();
  _focusNode.dispose();
  _statusSubscription?.cancel();
  super.dispose();
}
```

---

## 4. Structured Logging & No Debug Leftovers (C3)

- **No debug leftovers (C3)**:
  - Never commit `print()`, `debugPrint()`, `debugger()`, or temporary debug flags.
- **Use the workspace's structured logger**:
  - Route diagnostic, warning, and error logs through the project's configured logger (resolved via `flutter-core-package-usage`), including error objects and stack traces on failures.
- **Privacy & security**:
  - Never log authentication tokens, bearer headers, passwords, session secrets, or personal user data (PII).
