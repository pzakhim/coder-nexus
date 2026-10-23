# 05 - Flutter Bug Patterns by Dimension

Concrete defect patterns commonly found in Flutter codebases.

## Dimension 1: Lifecycle & State

- **`setState()` called after `dispose()`:** An async `await` operation finishes after the user popped the screen, calling `setState()` on an unmounted state.
  - *Fix:* Check `if (!mounted) return;` before calling `setState()`.
- **Undisposed Controller:** `TextEditingController`, `AnimationController`, or `ScrollController` instantiated in `initState()` without `dispose()`.
  - *Fix:* Call `_controller.dispose()` in `dispose()`.
- **In-place State Mutation:** Mutating a list in `OrderState` (e.g. `state.orders.add(...)`) and calling `emit(state)`.
  - *Fix:* Emit a new immutable state instance using `state.copyWith(orders: [...state.orders, newItem])`.

## Dimension 2: Async & Concurrency

- **Duplicate Action on Rapid Taps:** Submitting an order twice because the submit button remains interactive while the first request is pending.
  - *Fix:* Set `isLoading: true` on `AppButton` while state is loading.
- **Uncancelled Stream Subscription:** Listening to a global event stream without cancelling the subscription when the widget is disposed.
  - *Fix:* Store `StreamSubscription` and invoke `.cancel()` in `dispose()`.

## Dimension 3: Layout & Responsive

- **RenderFlex Overflow in Row/Column:** Text widget or container with fixed width placed inside a `Row` without wrapping in `Expanded` or `Flexible`.
  - *Fix:* Wrap dynamic children in `Expanded` or use `ListView`.
- **Ignoring Tablet Breakpoints:** Using phone-sized layout on tablets without utilizing `buildTabletPortrait()` in `BaseScreenState`.

## Dimension 4: Data Handling & Null Safety

- **Unchecked `DataState.data`:** Accessing `result.data` when `result.isFailure` is true throws `StateError`.
  - *Fix:* Guard with `if (result.isSuccess)` or pattern match.
- **Bang Operator on API Field:** Using `model.discount!.amount` when discount is optional in JSON.
  - *Fix:* Use `model.discount?.amount ?? 0`.

## Dimension 5: Performance & Rebuilds

- **Computations in `build()`:** Formatting dates, parsing JSON, or sorting lists inside `Widget build(BuildContext context)`.
  - *Fix:* Compute in Cubit or memoize outside `build()`.
- **Missing `const` on Stateless Subtrees:** Omission of `const` causing entire subtrees to rebuild on every parent state change.

## Dimension 6: UX & Accessibility

- **Silent Failures:** Network failure caught by Cubit without updating UI state or showing `AppDialog.show` / error banner.
- **Hit Target Too Small:** Custom icon button smaller than 48x48 logical pixels.

## Dimension 7: Security & Input

- **Plaintext Secret Logging:** Logging JWT tokens or passwords via `AppLogger.I`.
- **SSL Bypass:** Setting `badCertificateCallback` to return `true`.
