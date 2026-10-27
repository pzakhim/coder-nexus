# 02 — Isolate, Hypothesize & Symptom Matrix (Flutter / Dart)

Rules **D4**, **D5**, **D6**, and **D11**.

---

## 1. Layer Isolation Across Clean Architecture (`D4`)

Trace the failing data flow across the 4 Clean Architecture boundaries (`Widget → State Holder (Cubit/Bloc/Notifier) → Domain UseCase → Data Repository / Mapper / DataSource`) to pinpoint the exact boundary where good input turns into a wrong state or exception:

```text
[1. Presentation Widget]  ── Does BlocBuilder/Selector rebuild? Does buildWhen filter out the state?
           │
[2. Cubit / State Holder] ── Does it call the UseCase? Does it emit [Loading, Failure] or mutate state in place?
           │
[3. Domain UseCase]       ── Are parameters valid? Is the repository failure propagated without swallowing?
           │
[4. Data Repo & Mapper]   ── Does fromJson parse nulls/types safely? Does DataSource map HTTP 4xx/5xx/timeout?
```

1. **Minimize the Case:** Strip JSON fields, Cubit events, or widget wrappers one at a time while re-running `--plain-name` until every remaining element is load-bearing.
2. **Diff Since Last Green:** Check `git diff <last-green-sha> -- lib/ test/ pubspec.lock` to spot recent state, mapper, or dependency changes.

---

## 2. Ranked Falsifiable Hypotheses (`D5`, `D6`)

Write **3–5 ranked hypotheses** before editing code. Every hypothesis must state a **falsifiable prediction** ("if X is the cause, changing Y eliminates the failure"). Test the top hypothesis with a single probe, **one variable at a time**:

```text
H1 (rank 1): <suspected cause> | predicts: <changing Y removes the failure> | probe: <command or read> | result: CONFIRMED / RULED OUT
H2 (rank 2): <suspected cause> | predicts: <...> | probe: <...> | result: RULED OUT
Fix attempts: 1/3 <what changed> -> reproduction <PASS/FAIL>
```

When a hypothesis is `CONFIRMED`, trace the bad value backwards caller-by-caller until you reach the layer that owns the invariant (`D6`), and search the diff (`rg -n`) for sibling occurrences of the same mistake.

---

## 3. Temporary Tagged Instrumentation & Cleanup (`D11`)

- Prefer non-invasive `blocTest` state expectations and `--reporter=expanded` stack traces first.
- When temporary logging is required to inspect event ordering or boundary values during a test run, tag every statement with a unique marker (e.g., `// [DEBUG-7f3a]`) and never log tokens, passwords, or PII.
- **Mandatory Pre-Handoff Cleanup:** Delete all temporary logs before hand-off and prove zero matches via `rg -n "DEBUG-|print\(|debugPrint\(|debugger\(" lib test` (0 matches) and `flutter analyze` (`PASS`).

---

## 4. Flutter / Dart Symptom → First Moves → Typical Root Cause Matrix

*(For profile-specific classes such as `BaseScreenState`, `UseCasePower`, `DataState`, and `ApiService`, also check the active profile's `debugging-contracts.md` guide.)*

| Symptom | First Moves | Typical Root Cause in Flutter / Dart |
|---|---|---|
| **`NullCheckError: Null check operator used on a null value`** | Read the exact `lib/` file and line in the stack trace; trace where that nullable property was populated | Unchecked `!` bang operator (`C9`) on an optional field or uninitialized state property |
| **`type 'Null' is not a subtype of type '...' in type cast`** | Replay the raw JSON map in a `Model.fromJson` unit test | Unsafe `json['key'] as String` cast when backend returns `null` or omits an optional key |
| **Screen stuck on loading spinner / state never updates** | Write a `blocTest` for the failure/empty path; inspect `==` / `hashCode` (`equatable` `props` / `freezed`) and `buildWhen` | Cubit catches/ignores failure without emitting `FailureState`, mutates existing state list in place (`C13`), or omits a field from `props` so `BlocBuilder` skips rebuild |
| **`A RenderFlex overflowed by N pixels`** | Read `The relevant error-causing widget was:` in test output; reproduce in `testWidgets` with small screen size | Unbounded `Text` or child inside `Row`/`Column` missing `Expanded`/`Flexible`, or fixed height inside a scrollable viewport |
| **`Looking up a deactivated widget's ancestor is unsafe` / `setState() called after dispose()`** | Trace async callbacks (`await`, `Timer`, `Stream.listen`) inside the `State` class | Missing `if (!mounted) return;` after `await`, or `StreamSubscription` / `TextEditingController` / `ScrollController` not cancelled/disposed in `dispose()` (`C17`) |
| **`Bad state: Cannot emit new states after calling close`** | Inspect async methods inside the `Cubit` | `emit(...)` called after an `await` when the `Cubit` was already closed (`if (isClosed) return;`) |
| **`setState() or markNeedsBuild() called during build`** | Check `build()` and widget constructors for navigation, dialog, or Cubit mutation calls | Side effect triggered directly inside `build()` instead of `BlocListener` / `initState` / event callback (`C12`) |
| **Descendant widget loses focus, scroll position, or text input on rebuild** | Inspect widget tree changes or conditional wrappers in `build()` | Subtree moved into a `_buildX()` helper or conditional branch without a stable `Key`, resetting its `Element`/`State` |
| **Duplicate dialogs or double navigation on state change** | Inspect `BlocListener` / `BlocConsumer` conditions | Missing `listenWhen` filter, causing the listener to fire again when unrelated state fields update |
| **Analyzer errors on `.g.dart` / `.freezed.dart` files** | Check whether model/state definitions changed without regenerating codegen | Out-of-date generated files (`dart run build_runner build --delete-conflicting-outputs`) |
