# 01 — Scope, Dimensions, and Flutter Bug Patterns

> Topic: Fixed revision scope, caller search, cold pass, the 7 defect dimensions, and Flutter/Dart failure patterns (`H1`–`H5`)

## 1. Fix the Scope (`H2`, `H3`)

- **Revision (`H2`):** Record `BASE_REVISION` and `REVIEW_REVISION` from the hand-off header ([handoff-and-status](../../work-item-contract/references/handoff-and-status.md) §1), plus staged, unstaged, and untracked files belonging to the item (`git status --short`, `git diff --stat <BASE_REVISION>..<REVIEW_REVISION>`). Review exactly that tree. The Code Writer's self-check runs on the phase diff before commit; the Reviewer runs on the committed `REVIEW_REVISION` only.
- **Whole Context (`H3`):** Read each changed hunk with its whole enclosing widget (`build`, `initState`, `didUpdateWidget`, `dispose`), state holder (`Cubit` / `Bloc` / `Notifier`), use case, repository, or mapper method.
- **Callers (`H3`):** For each changed public symbol, find and read its callers. A broken caller outside the diff is in scope because most regressions surface there:
  - Widget constructor parameters, required/optional callbacks, and route arguments (`GoRouter` / `Navigator` extra/path params).
  - `Cubit` / `Bloc` / `Notifier` public methods, emitted state classes, `copyWith` signatures, and `Equatable.props`.
  - Domain use case signatures, parameter objects, entity fields, and failure/result types.
  - DTO / `fromJson` / `toJson` keys, nullability, and repository interface contracts.
- **Caller Search (Read-Only):**
  - `rg -n -w "<symbol>" lib test` for Dart symbol references.
  - `rg -n "'<json_key>'|\"<json_key>\"" lib test` for serialized JSON keys.
  - `rg -n "<route_name_or_path>" lib test` for navigation callers.
  - GitNexus `context` / `impact`, where configured, for call graphs.

---

## 2. Cold Pass First (`H4`)

Hunt from the code **before** reading `requirements.md`, `design.md`, the phase file, or the hand-off's Concerns. Read them afterwards only to decide whether a suspicious behavior is intended (a `D-NN` decision or an AC) or a defect.

---

## 3. The Seven Defect Dimensions (`H5`)

Walk the scope once per dimension and write every suspicion as `file:line — hypothesis`:

1. **Logic and data flow** — wrong condition or operator, off-by-one in pagination (`page` 0-based vs 1-based, `hasReachedMax`), inverted boolean flag, stale variable read in closure, `copyWith` unable to clear a nullable field (`field: field ?? this.field` when `null` is passed intentionally), `double` precision errors on currency/quantities, local vs UTC `DateTime` mismatch.
2. **Error and edge paths** — null assertion (`!`) or unsafe `as` cast on nullable API/route data, `.first` / `.single` on a list that can be empty, network timeout or non-2xx response caught and ignored (leaving the UI stuck in loading or showing a false empty state), partial failure across sequential storage/API writes, form validation bypassed on keyboard submit (`onFieldSubmitted`).
3. **State, async, and lifecycle** — `setState()` or `BuildContext` used after an `await` gap without `if (!mounted) return;` / `if (!context.mounted) return;`, `emit()` called inside a `Cubit`/`Bloc` after `isClosed`, undisposed `TextEditingController` / `ScrollController` / `AnimationController` / `FocusNode` / `Timer` / `StreamSubscription`, in-place list/map mutation (`state.items.add(...)`) or missing field in `Equatable.props` preventing UI rebuilds, duplicate API mutations on rapid button taps.
4. **Contract and caller breakage** — callers from the scope step now receive a changed state type, null value, or unhandled failure; route arguments cast to the wrong type on navigation; `fromJson`/`toJson` keys or enum values drifting from the backend contract; stale generated `.g.dart` / `.freezed.dart` files out of sync with edited source fields.
5. **Security, scope, and data safety** — tokens, passwords, or PII written to `SharedPreferences` instead of encrypted storage or printed to console/logs; cached user/tenant data not cleared on logout or account switch; unvalidated deep-link parameters navigating to privileged screens; TLS certificate verification bypassed (`badCertificateCallback = (_) => true`).
6. **Stack and project patterns** — every row in Section 4 below (and the active workspace profile guide) that the changed code can hit.
7. **Test blind spots** — for each surviving candidate: would an existing test fail if it were real? Watch for tests that cannot fail: mocking the unit under test instead of its dependency, `blocTest` asserting only happy-path state types without checking field values, widget tests that never pump the error/empty state, or missing tests for null/malformed JSON payloads. Record the missing test with the finding.

`quick` effort runs dimensions **1–4** on changed hunks only.

---

## 4. Flutter / Dart Bug Patterns (Dimension 6)

### 4.1 Widget & State Lifecycle

| Looks like | Goes wrong when | Check |
|---|---|---|
| `await future; setState(...)` or `Navigator.of(context)...` | User pops screen while future is pending; throws `FlutterError (setState() called after dispose())` or uses defunct `BuildContext` | Guard every post-`await` UI action with `if (!mounted) return;` / `if (!context.mounted) return;` |
| `TextEditingController` / `ScrollController` / `FocusNode` created in `State` or `build()` | Created in `build()` resets cursor/scroll on every rebuild; created in `State` without `dispose()` leaks memory and listeners | Instantiate in `initState()`, dispose in `dispose()` |
| `didUpdateWidget` does not update controller or re-subscribe when `widget.id` changes | Parent passes a new item ID, but stateful child keeps displaying or editing the old item's state | Compare `oldWidget.prop != widget.prop` in `didUpdateWidget` |
| `emit(newState)` after `await` in a `Cubit` method | Screen closes before async call finishes; throws `StateError: Cannot emit new states after calling close` | Check `if (isClosed) return;` before `emit` after an async gap |
| `state.items.add(x); emit(state.copyWith(items: state.items))` | Same list reference mutated in place; `oldState == newState` is `true`, so `BlocBuilder` never rebuilds | Create a new list (`[...state.items, x]`) and include all state fields in `Equatable.props` |
| `copyWith({String? error})` using `error: error ?? this.error` | Passing `copyWith(error: null)` to clear an error keeps the old `this.error` forever | Use a sentinel/callback or explicit `clearError: true` flag for nullable state fields |

### 4.2 Async, Streams, Timers & Concurrency

| Looks like | Goes wrong when | Check |
|---|---|---|
| Submit / checkout button `onPressed` calls `cubit.submit()` while `state.isSubmitting` is true | Rapid double-tap fires two concurrent POST requests (duplicate order/payment) | Disable button (`onPressed: state.isSubmitting ? null : ...`) and guard inside `cubit.submit()` if already loading |
| Search-as-you-type firing `cubit.search(query)` on every keystroke | Earlier slow response arrives after a newer fast response and overwrites the UI with stale search results | Debounce input and cancel or ignore responses for superseded queries |
| `stream.listen(...)` or `Timer.periodic(...)` in `initState` / `Cubit` | Subscription or timer keeps firing after widget/cubit disposal, leaking memory and mutating dead state | Store `StreamSubscription` / `Timer` and cancel in `dispose()` / `close()` |
| Unawaited `Future` without `.catchError` / `try-catch` | Unhandled async exception crashes the zone or fails silently without updating UI state | `await` the future inside `try-catch` and emit an error state |

### 4.3 Data Serialization, Null-Safety & Numbers

| Looks like | Goes wrong when | Check |
|---|---|---|
| `json['price'] as double` in `fromJson` | Backend returns integer `100` instead of `100.0`; throws `_TypeError ('int' is not a subtype of 'double')` | Cast via `(json['price'] as num?)?.toDouble()` or safe parser helper |
| `user.profile!.address!.city` (`!` bang operator on optional API data) | Nullable nested field is absent for a valid user; throws `_CastError (Null check operator used on a null value)` | Use null-aware access (`?.`) with a safe fallback or explicit validation |
| `list.first` or `list.singleWhere(...)` without checking `isEmpty` / `orElse` | Empty API list throws `StateError (No element)` | Use `firstOrNull` (`collection` / Dart 3) |
| `catch (e) { return const []; }` in Repository or DataSource | Network timeout or 500 error looks identical to "0 items found"; user sees empty state instead of error retry | Propagate failure result to the state holder so the UI distinguishes error from empty |

### 4.4 Layout Constraints & Navigation

| Looks like | Goes wrong when | Check |
|---|---|---|
| Unbounded `Text` or dynamic child inside `Row` | Long localized string or user name overflows on narrow screens (`RenderFlex overflowed by N pixels`) | Wrap flexible children in `Expanded` / `Flexible` with `TextOverflow.ellipsis` |
| `ListView` / `Column` with `Expanded` inside a scrollable `SingleChildScrollView` | Unbounded vertical height constraint throws `Vertical viewport was given unbounded height` | Use `CustomScrollView` with slivers or `shrinkWrap: true` + `NeverScrollableScrollPhysics` for small bounded lists |
| `Navigator.pop(context)` called inside both a dialog button and a `BlocListener` | Pops both the dialog and the underlying screen, leaving the user on the wrong route | Separate dialog dismissal from screen navigation and verify route stack depth |

---

## 5. Non-Candidates (`H14`)

Missing `const` keywords, helper extraction ideas, or minor rebuild optimizations that do not cause a visible freeze, leak, or wrong behavior are not defects. Record them only as `NOTE` lines for `code-simplification`.
