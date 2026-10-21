# Flutter Bug Patterns

Stack checklist for dimension 6 of `bug-hunt`. Check only the patterns the changed code can hit; each hit still needs a failure scenario and verification.

## Async and lifecycle

- `BuildContext`, `Navigator`, `ScaffoldMessenger` or `setState` used after an `await` without a `mounted` (or `context.mounted`) check.
- `emit` after `close()` of a Cubit/Bloc, typically from a late Future or stream callback.
- `Future` not awaited where ordering matters (save then navigate, load then read state); errors of an unawaited Future are lost.
- Stale response: a slower earlier request (search, filter, paging) overwrites the result of a newer one; no cancel, token or debounce.
- Double submit: a button stays enabled while its request runs, so a second tap repeats the side effect.
- `StreamSubscription`, `TextEditingController`, `FocusNode`, `AnimationController`, `ScrollController` or `Timer` created by a State or Cubit and not disposed/cancelled there.
- `FutureBuilder`/`StreamBuilder` whose future or stream is created inside `build()`, so every rebuild restarts it.

## State and rebuild

- State class missing a field in `props`/`==`, so a changed value is not emitted or not rebuilt.
- List or map mutated in place and re-emitted with the same reference; UI does not rebuild.
- `buildWhen`/`listenWhen` that filters out a state the UI must react to (error, empty, reset).
- Screen-scoped Cubit registered as a singleton, so state leaks between screen visits.

## Data and parsing

- `as int`/`as String` casts or `!` on JSON fields that the API (or the Mockoon fail/empty rule) can omit, null or send as another type.
- `DateTime.parse` without timezone handling, or `toLocal()`/`toUtc()` applied twice.
- `double` used for money or quantities that must round exactly.
- Paging: total/last-page math off by one; the same item appended twice after refresh; empty first page shown as an error.
- Error mapped to an empty result, so a failure looks like "no data".

## UI behavior

- Form validator bypassed by a path that calls the use case directly (keyboard submit, second button).
- Layout that overflows or loses input in landscape or with a large text scale when the approved Visual AC covers it.
- `Navigator.pop` result read with the wrong type or ignored when null (back gesture).
