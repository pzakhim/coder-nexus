# External Standard Root-Cause Debugging Contracts

> Topic: Debugging standard Flutter widgets, Cubit/Bloc/Notifier, Dart 3 sealed states, and JSON/HTTP layers (external-standard profile)

## 1. Layer-by-Layer Fault Isolation (`external-standard`)

When isolating a defect in a standard Flutter application, bisect along the presentation, domain/service, and data boundaries:

| Boundary Check | What to Inspect | Common Root Causes |
|---|---|---|
| **Widget & State (`StatefulWidget` / `Bloc` / `Riverpod` / `ChangeNotifier`)** | `setState` lifecycle; Dart 3 `sealed class` state pattern matching (`switch (state)`); `Listenable` / `Stream` subscriptions | Mutating list/map in-place so `oldState == newState` evaluates to `true`; calling `setState` or `notifyListeners()` after `dispose()`; forgetting to cancel `StreamSubscription` |
| **Domain / Application Logic** | Business rules, value objects, async orchestration | Race condition when user triggers multiple async actions (e.g., rapid button taps or search-as-you-type without debounce/cancellation) |
| **Data & Serialization (`Dio` / `http` / `fromJson`)** | HTTP status handling; `jsonDecode` / `fromJson` type casts; local storage (`SharedPreferences` / `Drift` / `SQLite`) | Unsafe cast `json['amount'] as double` when JSON contains an `int` (`(json['amount'] as num?)?.toDouble()`); non-2xx HTTP response body parsed as success JSON |

---

## 2. Dart 3 Pattern Matching & Null-Safety Traps

- **Exhaustiveness vs Runtime Type**: Verify whether a `switch` on a `sealed class` state handles error and loading branches explicitly rather than falling into a wildcard `_ => const SizedBox.shrink()` that hides failures.
- **Numeric JSON Casts**: In standard Dart `fromJson`, always cast JSON numbers via `num` (`(json['key'] as num).toDouble()`) to prevent `_TypeError (type 'int' is not a subtype of type 'double')`.
