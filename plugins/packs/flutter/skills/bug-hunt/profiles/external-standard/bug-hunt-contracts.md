# External Standard Bug-Hunt Contracts

> Topic: Defect patterns in standard Flutter widgets, Dart 3 sealed states, Bloc/Riverpod/ChangeNotifier, and JSON/HTTP layers (external-standard profile)

## 1. `external-standard` Defect Patterns (Dimension 6 Extension)

When hunting bugs in a standard Flutter application, check every applicable row below:

| Looks like | Goes wrong when | Check |
|---|---|---|
| Wildcard `_ => const SizedBox.shrink()` on a Dart 3 `sealed class` state `switch` in the UI | Error or empty state is swallowed silently, rendering a blank screen when a request fails | Exhaustively match all `sealed` state subtypes (`Initial`, `Loading`, `Success`, `Failure`) without a catch-all wildcard |
| `ChangeNotifier` / `ValueNotifier` calling `notifyListeners()` after `dispose()` | Async operation completes after screen pop and throws `FlutterError: A ChangeNotifier was used after being disposed` | Track disposal state or cancel pending work in `dispose()` |
| `Riverpod` `ref.read` used inside `build()` instead of `ref.watch` | Widget never rebuilds when provider state changes | Use `ref.watch` in `build()` and `ref.read` only in event callbacks |
| Direct `jsonDecode(response.body)` without checking `response.statusCode` first | Non-2xx HTML error page or empty body throws `FormatException` instead of a typed domain/network error | Check HTTP status code before decoding JSON and handle non-2xx responses explicitly |
