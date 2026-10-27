# 01 — Scope, Behavior Safety & Stop Criteria (Flutter / Dart)

Rules S1, S2, S3, S11, S12 and S13. Reason: simplifying at the wrong time, outside the diff or past the point where behavior or layout changes turns a cleanup into an unreviewed feature change.

> **Workspace Convention Rule (`C11` — `EXTEND` vs `INIT`):**
> - **Existing project (`EXTEND`):** Simplify strictly toward the state management (Cubit/Bloc/Notifier), base screen classes, UI kit components, and routing conventions already established in the workspace. Never introduce a competing state or widget pattern inside a simplification pass.
> - **Greenfield project (`INIT`):** Follow the approved `architecture_profile` (`design.md`) and active profile reference (`foundation-reuse.md`).

## 1. When

| Situation | Simplify? |
|---|---|
| The phase's checks pass (`flutter analyze`, affected `flutter test`) and the diff has a named smell | Yes, inside the changed code only — the simplicity pass of `incremental-implementation` |
| A review finding names unnecessary complexity in the phase's code | Yes, as the fix revision for that finding (`review-resolution`) |
| Checks are red | No: fix behavior first with `{{slot:root-cause-debugging}}` |
| The smell is outside the diff (an untouched screen or legacy module) | No: record it in the hand-off's Concerns |
| The code is already clear, or a later task in the plan rewrites it | No |
| Writing a new screen or feature, or fixing a bug | No: that changes behavior and follows the plan. While writing, `{{slot:clean-code}}` and `{{slot:clean-architecture}}` already apply |

## 2. Scope

Only the files and lines changed in this phase:

```bash
git diff --name-only <base>...HEAD -- '*.dart'
```

- Inside the diff: avoidable complexity under any of the four lenses is fair game.
- Outside the diff: report it, never touch it (`{{slot:clean-code}}` C10).
- Generated code (`*.g.dart`, `*.freezed.dart`, `*.gr.dart`, localization output) is regenerated, never hand-simplified.
- Foundation packages consumed by the app are read-only; reuse them, never edit them (`architecture_profile`).

## 3. Before editing

Read, for the code you are about to change:

- **Callers**: `rg -n "<Name>" lib/ test/`, plus route names, `GoRouter`/`AutoRoute` registrations, DI registrations (`get_it`/`injectable`) and string keys used in tests (`find.byKey`).
- **Widget lifecycle**: `initState`, `didChangeDependencies`, `didUpdateWidget`, `dispose`; which controllers, subscriptions and `FocusNode`s are owned here.
- **State flow**: which state holder (Cubit/Bloc/Notifier) emits what, `buildWhen` / `listenWhen` / `select` conditions, listeners that navigate or show dialogs.
- **Error paths**: how a failure reaches the UI (error state, snackbar, retry).
- **Tests** that cover it: widget tests, `bloc_test`, golden tests.

## 4. Must stay identical

Rendered layout (padding, alignment, sizes, tap targets) · visual states (loading, empty, error, disabled) · navigation and dialogs · emitted states and their order · side effects (API calls, analytics, persistence) · focus, scroll and text-input behavior · accessibility semantics · rebuild-triggered behavior · performance limits.

Existing tests (including goldens) pass **unchanged**; the only allowed test edit is an import path after a move. Reason: a test edited in the same step as the code no longer proves the old behavior.

Flutter-specific traps:

- Moving a subtree into a new widget class or wrapper changes its position in the element tree: descendant `State` (text input, scroll position, animation) can reset. Keep the tree shape or give the moved subtree a stable `Key`.
- A `_buildX()` method turned into a widget class gets its own `BuildContext`: `Theme.of`, `MediaQuery.of` and inherited lookups still resolve, but anything relying on the parent `setState` rebuilding it must now receive the value as a constructor parameter.
- Collapsing `Padding` + `DecoratedBox` + `SizedBox` into one `Container` can change layout (constraints, decoration vs padding order); compare before/after (golden or screenshot).
- `StatefulWidget` → `StatelessWidget` is safe only when no field, controller, mixin (`TickerProviderStateMixin`) or lifecycle method is still needed.
- Moving work from `build()` to `initState` stops it from reacting to new widget parameters; handle `didUpdateWidget` / `didChangeDependencies` when the input can change.
- Removing `buildWhen` / `listenWhen` / `select` changes how often a subtree rebuilds or a listener fires (duplicate navigation, double dialogs).
- `?.` / `??` replacements must keep the exact fallback values downstream code expects.

## 5. One step at a time

After each simplification run (`PASS` = `exit 0`, `FAIL` = non-zero):

```bash
dart format --output=none --set-exit-if-changed <changed files>
flutter analyze
flutter test <affected test files>
```

Keep each command and exit code as an evidence row (`evidence-standard`, handoff-and-status §4). For visual changes the `{{slot:visual-quality}}` comparison is the evidence. Red after a step and the cause is not obvious → revert that step (§7).

## 6. Never

- Change a test or regenerate a golden to make a simplification pass.
- Remove input validation, error-state handling, permission/role checks, DI registrations or package contracts. Guards owned by `{{slot:secure-coding-standards}}` stay even when they look redundant.
- Leave a wrapper widget, typedef alias or re-export after moving code: update every caller in the same step and delete the old name (`{{slot:clean-code}}` C1, C18).
- Drop a `dispose()` / `cancel()` while restructuring (`{{slot:clean-code}}` C17).
- Add `// ignore:` or `// ignore_for_file:` to make the analyzer pass.

## 7. Stop criteria

| Situation | Do instead |
|---|---|
| Layout, visual states, navigation, emitted states or a public widget/API signature would change | Stop; it is a design or contract change: `change-control` and the approval gate |
| A `D-NN`, the approved `architecture_profile` or a `{{slot:clean-architecture}}` boundary requires the abstraction | Leave it; mention it in Concerns if it looks unnecessary |
| The gain is cosmetic (renaming taste, reordering imports the formatter handles) | Leave it |
| A rebuild-heavy or scroll path would change without a measurement | Measure first (DevTools rebuild counts, `flutter run --profile`) or leave it |
| The next step, or the right depth for an Altitude fix, needs code outside the diff (a shared widget, theme or base class) | Record it in Concerns |
| A guard from `{{slot:secure-coding-standards}}` would be removed or merged away | Leave it |
| Checks turn red and the cause is not obvious | Revert the last step; do not debug a refactor |
| No named smell remains | Stop and report |
