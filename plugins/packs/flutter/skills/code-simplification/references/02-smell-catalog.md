# 02 — Smell Catalog (Four Lenses, Flutter / Dart)

Rules S4–S10. Reason: concrete examples tell the agent what avoidable complexity looks like in a Flutter app, which generic advice cannot. Every simplification names one row here, a row of the active profile's reuse reference, or a rule of `{{slot:clean-code}}`. Examples are **illustrative** (no workspace is scanned for a pack skill); the workspace may add its own rows.

Ask in order: **needed?** → **already in the repo or the workspace's foundation packages (`architecture_profile`)?** → **Flutter SDK / Dart core?** → only then write the minimum.

Pass the diff through the four lenses in order. A host that supports subagents may run the lenses in parallel; the findings and the rules are the same.

## 1. Reuse (S5, S7)

| Tag | Smell | Example (illustrative) | Technique | Watch out |
|---|---|---|---|---|
| `reuse` | Home-grown widget for something the workspace's UI kit or shared widgets already provide (button, text field, dialog, bottom sheet, paginated list, empty/error state) | `GestureDetector` + `Container` + `Text` + `CircularProgressIndicator` as a button | Use the existing component chosen per `design.md` and the active profile's reuse reference | Its "Use when" must fit; styling differences alone are not a reason to rebuild it |
| `reuse` | Second formatter, validator, extension or mapper next to an existing one | A new `formatMoney()` beside the workspace's currency formatter | Call the existing one; delete the copy | Do not bend the existing one with flags for one caller |
| `delete` | Duplicated definitions: the same model, enum, route name or constant in two features | `const kPageSize = 20` in two modules | One definition in its owning module (`{{slot:clean-code}}` C1) | Look-alikes for different concepts stay separate |
| `inline` | Premature extraction: a shared widget for two screens that now grows boolean flags | `SharedCard(isOrder: true, showBadge: false, ...)` | Inline back into each screen; extract on the third real repetition | Logic only; definitions are never duplicated |

### Already shipped (Dart / Flutter SDK)

| Hand-rolled | Use instead |
|---|---|
| `List<Widget> list = []; for (...) list.add(...)` | Collection-`for` / collection-`if` and spread `...` inside the literal |
| `a != null ? (a.b != null ? a.b : '') : ''` | `a?.b ?? ''` |
| `switch` on type with casts, or `is` chains | Dart 3 `switch` expression with patterns on a `sealed` class |
| Hand-written `copyWith`, `==`, `hashCode` | The data-class generator or record type the workspace already uses (`freezed`, `equatable`, records) |
| Class with only `static` helper methods | Top-level function, or an `extension` on the type it serves |
| Manual `Timer` debounce juggling in many widgets | The workspace's existing debounce helper or stream transformer |
| Custom inherited-data plumbing | `Theme.of(context)`, `MediaQuery`, or the workspace's chosen state-management lookup |

## 2. Simplification (S6, S8)

| Tag | Smell | Example (illustrative) | Technique | Keep it when |
|---|---|---|---|---|
| `shrink` | `Widget _buildHeader()` helper methods inside a large `build()` | `_buildHeader()`, `_buildItem(i)` | Private `class _Header extends StatelessWidget` with a `const` constructor (`{{slot:clean-code}}` C6, C15) | The method returns a trivial single widget used once |
| `flatten` | Deep layout pyramids | `Container(child: Padding(child: DecoratedBox(child: SizedBox(...))))` | One `Container` / `Padding` with the combined properties | Layout differs after collapsing (§4 traps in [01](01-scope-and-safety.md)) |
| `shrink` | `StatefulWidget` whose state is unused or fully owned by a state holder | `setState` never called; fields mirror Cubit state | `StatelessWidget` reading the state holder | It owns a controller, `FocusNode`, animation or lifecycle hook |
| `shrink` | Derivable state stored and synced by hand | `isEmpty` field kept next to `items` in a state class | Getter computed from `items` | — |
| `yagni` | Abstract class / interface with one implementation and no test fake; a base widget or base Cubit for one subclass | `abstract class OrderRepositoryBase` + only `OrderRepositoryImpl` | Use the concrete class | A `{{slot:clean-architecture}}` boundary (domain repository contract) or the profile's base classes require it |
| `inline` | Pass-through widget that only forwards all parameters | `class MyButton extends StatelessWidget { build => FilledButton(...same params) }` | Use the inner widget directly | It adds real behavior (analytics, permission check, fixed configuration used in 3+ places) |
| `inline` | Flag parameter switching two layouts | `OrderTile(isCompact: true)` rendering two unrelated trees | Two widgets named for each layout | The flag is real data |
| `flatten` | Nested ternaries in the widget tree | `a ? (b ? X() : Y()) : Z()` | `switch` expression on the state, or early return in a small widget | — |
| `shrink` | Clever code: long `..` cascades or chained `map/where/fold` used for side effects | `items.map((e) { list.add(e); return e; }).toList()` | Plain `for` loop or one level of collection-`for` | — |

Dead code (unused widgets, fields, imports, commented-out blocks) is `{{slot:clean-code}}` C2 (`dart_code_linter` `check-unused-code` / `check-unused-files`).

## 3. Efficiency (S9)

| Tag | Smell | Example (illustrative) | Technique | Watch out |
|---|---|---|---|---|
| `dedupe` | Work done in `build()` on every rebuild: sorting, filtering, parsing, `DateFormat(...)` construction | `final sorted = [...items]..sort(...)` inside `build()` | Compute in the state holder (once per state) or cache in `initState` / `didUpdateWidget` | Must still react to new inputs (§4 traps) |
| `defer` | Side effects or futures started in `build()` | `FutureBuilder(future: repo.load())` creating a new future every rebuild | Start it in the state holder or `initState`; keep the future in a field | Keep the same loading/error states |
| `narrow` | Whole subtree rebuilds for one field | `BlocBuilder` around the whole screen for a counter | `BlocSelector` / `context.select` / `buildWhen` around the part that changes; `const` for static children | Rebuild-count changes on hot paths need a measurement |
| `batch` | One request per list item from the UI | Each `ListTile` calling `repo.getDetail(id)` | One batched call in the state holder | Ordering and partial-failure behavior stay the same |
| `concurrent` | Independent awaits run one after another in a state holder | `final a = await repoA.load(); final b = await repoB.load();` | `Future.wait([...])` (or record destructuring with `.wait`) | Error and cancellation behavior stay the same |
| `narrow` | Long-lived listener or callback capturing a large scope | A stream listener in a singleton closing over a `BuildContext` | Pass only the values it needs; cancel it on dispose (`{{slot:clean-code}}` C17) | Never keep a `BuildContext` past its widget's life |

Any change here on a scroll or rebuild-heavy path needs a measurement first ([01](01-scope-and-safety.md) §7).

## 4. Altitude (S10)

| Tag | Smell | Example (illustrative) | Technique | Watch out |
|---|---|---|---|---|
| `generalize` | Special case for one screen inside a shared widget, theme or base class | `if (routeName == '/orders') padding = 8` inside a shared list widget | Pass the variation as a parameter from that screen, or adjust the shared mechanism | Shared code outside the diff → Concerns |
| `root` | Symptom patched in the widget | `?? ''` / `!` / `try-catch` around a value that is wrong because the mapper or state holder in the same diff produces it | Fix the mapper or state; delete the patch | Never swallow errors (`{{slot:clean-code}}` C4) |
| `root` | Layout patched with magic offsets | `Transform.translate(offset: Offset(0, -3))` to fix an alignment | Fix the constraint or alignment that causes it | Must match the approved design (`{{slot:visual-quality}}`) |
| `merge` | A new widget or state path added beside the old one for the same job | `OrderCardV2` next to `OrderCard`, both still used | Keep one; move callers in the same step | Callers outside the diff → Concerns |

## Rule of three

Extract shared logic or a shared widget on the third repetition; two may stay. Definitions (models, enums, routes, constants) are never duplicated (`{{slot:clean-code}}` C1). A widget moves to a shared folder only when two or more features import it (`{{slot:clean-code}}` C16).

## Leave these alone

- Base classes, state holders and DI the approved `architecture_profile` requires (`{{slot:clean-architecture}}`, `D-NN`).
- Domain repository contracts with a single data implementation when the architecture defines them as the domain boundary.
- Long but linear code with one job: route tables, localization maps, theme definitions, generated code.
- Defensive checks at trust boundaries: input validation, permission checks, error states.
- Dart 3 `sealed` state classes with exhaustive `switch` expressions: do not replace them with class polymorphism hierarchies.

## Reduce or relocate?

Count the concepts a reader must hold (widgets, flags, branches, layers) before and after. Same count means the complexity only moved: revert it. Prefer the change that makes a whole branch, flag or layer disappear.

## Candidate line

`<lens>/<tag> at <path:line>: <what to cut> -> <replacement>`

## 5. Before / After Reference Examples

### Example A — `simplification/shrink` + `efficiency/dedupe` (`_buildX()` helper & sorting in `build()` → Private `const StatelessWidget` & pre-sorted state)

```dart
// ❌ BEFORE (Smell: sorting inside build() on every frame + _buildHeader() helper method)
@override
Widget build(BuildContext context) {
  final sorted = [...state.orders]..sort((a, b) => b.createdAt.compareTo(a.createdAt));
  return Column(
    children: [
      _buildHeader(context, sorted.length),
      Expanded(child: OrderListView(orders: sorted)),
    ],
  );
}

Widget _buildHeader(BuildContext context, int count) => Padding(
  padding: const EdgeInsets.all(16),
  child: Text('Orders ($count)', style: Theme.of(context).textTheme.titleMedium),
);

// ✅ AFTER (Simplified: `state.sortedOrders` computed once in Cubit/state; private const StatelessWidget)
@override
Widget build(BuildContext context) {
  return Column(
    children: [
      _OrderHeader(count: state.sortedOrders.length),
      Expanded(child: OrderListView(orders: state.sortedOrders)),
    ],
  );
}

class _OrderHeader extends StatelessWidget {
  const _OrderHeader({required this.count});
  final int count;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.all(16),
    child: Text('Orders ($count)', style: Theme.of(context).textTheme.titleMedium),
  );
}
```

### Example B — `simplification/flatten` (Nested ternary widget tree → Exhaustive `switch` expression)

```dart
// ❌ BEFORE (Smell: nested ternaries in widget tree)
child: state.isLoading
    ? const LoadingIndicator()
    : state.errorMessage != null
        ? ErrorBanner(message: state.errorMessage!)
        : OrderContent(items: state.items),

// ✅ AFTER (Simplified: flat exhaustive switch on sealed OrderState)
child: switch (state) {
  OrderLoading() => const LoadingIndicator(),
  OrderFailure(:final message) => ErrorBanner(message: message),
  OrderLoaded(:final items) => OrderContent(items: items),
},
```
