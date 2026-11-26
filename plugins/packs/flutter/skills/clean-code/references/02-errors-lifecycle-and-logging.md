# 02 — Errors, Lifecycle, and Logging (Flutter / Dart)

Consolidated rules for error handling (**C4, C11**), pure `build()` and widget lifecycle (**C12**), controller/stream disposal (**C17**), and structured logging without debug leftovers (**C3**).

---

## 1. Error Handling & Boundary Translation (C4, C11)

- **No swallowed errors**: Never write an empty `catch (_) {}`, silently return fabricated fallback defaults (`0`, `""`, `[]`), or ignore a failed result.
- **Data / Repository boundary translation**: Catch specific transport/parse/platform exceptions at the repository boundary and translate them into the workspace's typed result/failure contract (`architecture_profile`). Never let raw network or JSON exceptions bubble unhandled into widgets.
- **State holder handling**: Every async action in a `Cubit` / `Bloc` / `Notifier` must handle both success and failure outcomes, logging operational errors via the structured logger and emitting an explicit failure state so the UI renders error feedback/retry controls.

---

## 2. Pure `build()` & Widget Lifecycle (C12, C11)

- **Pure `build()` methods (C12)**: Keep `build(BuildContext context)` (and profile base-screen builders) deterministic and side-effect-free. Never trigger network calls (`cubit.load()`), navigation, dialogs/snackbars, or state mutations directly inside `build()`. Trigger initial loads in `initState()` or route provider creation, and side effects inside `BlocListener` or event callbacks.
- **Async `BuildContext` safety**: After any `await` in a `StatefulWidget` or callback, guard `if (!context.mounted) return;` before using `context`.
- **Workspace Base Screen contracts (C11)**: Follow the approved `architecture_profile`; override only the designated layout builders and never bypass base lifecycle hooks.

---

## 3. Resource & Subscription Disposal (C17)

Every `State` or state holder (`Cubit` / `Bloc` / `ChangeNotifier`) that owns disposable resources **must** release them in `dispose()` or `close()` before `super.dispose()`:
- `TextEditingController`, `ScrollController`, `PageController`, `TabController`
- `AnimationController`, `FocusNode`
- `StreamSubscription`, `Timer`, `Debouncer`

---

## 4. Structured Logging & No Debug Leftovers (C3)

- **No debug leftovers (C3)**: Never commit `print()`, `debugPrint()`, `debugger()`, or temporary debug flags.
- **Use the workspace's structured logger**: Route warnings and errors through the configured logger (`architecture_profile`) with error objects and stack traces.
- **Privacy & security**: Never log access/refresh tokens, bearer headers, passwords, secrets, or PII.
