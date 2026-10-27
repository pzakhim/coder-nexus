# 03 — Report & Review Severity (Flutter / Dart)

Rule S14 and the review severity. Reason: one line of what was cut lets reviewers see intent, skipped findings stay visible, and named shortcuts do not silently become permanent.

## 1. Report line (in the Code Writer hand-off)

Use the `simplify:` line defined in [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md) exactly; it is not redefined here. Illustrative filled example:

```
simplify: _buildX helper -> private const widget at lib/modules/order/presentation/screens/order_screen.dart:45; sort in build() -> computed in OrderCubit at lib/modules/order/presentation/cubit/order_cubit.dart:30; net -24 lines; checks: flutter test test/modules/order exit 0
```

When nothing qualified, use the §9 "nothing worth changing" form and list the files looked at. One line per task or phase, next to the `bug-hunt:` line.

## 2. Skipped findings

A finding whose fix would change behavior or layout, or needs code outside the diff, is **not applied**. List it in the hand-off's Concerns:

```
<lens>/<tag> at <path:line>: <why skipped>
```

Example: `altitude/generalize at lib/shared/widgets/paged_list.dart:52: route-specific padding belongs in the shared widget, outside this phase's diff`.

## 3. Deliberate shortcuts

A shortcut kept on purpose (a simple implementation with a known limit) is named in the hand-off with its limit and upgrade path, for example "client-side filter, fine below ~200 items; move to the API query when the list is paginated". Reason: without the limit it silently becomes permanent. The workspace may add a code-comment marker convention; none is imposed here.

## 4. Review severity (`BLOCKER` / `MAJOR` / `MINOR`)

Graded on the unified scale of `shared_contracts/flags_and_statuses.md` §2, with verdict impact from [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md):

| Severity | Finding | Review Verdict Impact |
|---|---|---|
| `BLOCKER` | A check `FAIL`s after simplification; wrapper widget, alias or re-export left after a move (`{{slot:clean-code}}` C1, C18); a `dispose()`/`cancel()` lost; S12 violated; a `D-NN` or the approved profile ignored | `CHANGES_REQUESTED` |
| `MAJOR` | Unnecessary complexity in the diff with a named catalog row (any lens) | Fixed in the same revision when inside the phase's scope |
| `MINOR` | Small, local simplification opportunity | Optional; never blocks |

A "simplification" that changed layout, a visual state, navigation or an emitted state is a **defect** (severity + `CONFIRMED`/`PLAUSIBLE` + failure scenario), not a simplification finding.

Only code changed in the phase is graded; complexity outside the diff is a note in Concerns, never a finding.
