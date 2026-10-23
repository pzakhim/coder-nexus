---
name: clean-code
description: Flutter & Dart clean code standards (Effective Dart, flutter_lints, iMESPro packages app_core, app_util, app_ui_kit) - naming, const constructors, widget decomposition, error handling, sound null safety, and review severities.
---

# Flutter Clean Code Standard

Code written or reviewed in this Flutter pack follows **Effective Dart**, `flutter_lints`, and the iMESPro core package conventions ([`core-package-usage`](../flutter-core-package-usage/SKILL.md)).

Reviewers and coders evaluate every line and widget against this standard. Finding severities follow [work-item-contract handoff-and-status section 9](../work-item-contract/references/handoff-and-status.md).

## Rule Map (C1–C17)

| Rule | Statement | Why | Severity | Reference |
|---|---|---|---|---|
| **C1** | **One concept, one place.** Reuse `app_ui_kit`, `app_util`, and `app_core`. No duplicate helper widgets or copy-pasted mappers. | Copies drift; bug fixes land in only one copy. | P1 | [02-size-and-structure](references/02-size-and-structure.md) |
| **C2** | **No dead code.** Remove unused widgets, state fields, dead imports, commented-out blocks, and orphan TODOs. | Dead code creates confusion and false assumptions during debugging. | P1 | [02-size-and-structure](references/02-size-and-structure.md) |
| **C3** | **No debug code.** No `print()`, `debugPrint()`, `debugger()`, or temporary inspection flags in committed code. | Leaks sensitive data into system logs and clutters console output. | P1 | [03-errors-and-logging](references/03-errors-and-logging.md) |
| **C4** | **No swallowed errors.** Never catch exceptions without handling or logging with `AppLogger.I`. Always use `Future<ApiResponse>.tryCatch` in repositories. | Silent failures mask defects and leave the UI in broken or perpetual loading state. | P1 | [03-errors-and-logging](references/03-errors-and-logging.md) |
| **C5** | **Intention-revealing names.** `lowerCamelCase` for methods/variables, `UpperCamelCase` for classes/widgets/enums, `lowercase_with_underscores` for files. | Descriptive names eliminate ambiguity across presentation, domain, and data layers. | P2 | [01-naming](references/01-naming.md) |
| **C6** | **Small, focused units.** Widget `build()` $\le 40$ lines, methods $\le 30$ lines, files $\le 250$ lines. Extract private widget classes instead of helper methods. | Monolithic build methods trigger full-tree repaints and hinder readability. | P2 | [02-size-and-structure](references/02-size-and-structure.md), [02b-splitting](references/02b-splitting.md) |
| **C7** | **No magic values.** Use named constants, `AppColor.*` for palette colors, and `AppDimens`/`EdgeInsets` tokens instead of hardcoded numbers. | Scattered magic values break theme consistency and responsive adaptation. | P2 | [04-types-constants-comments](references/04-types-constants-comments.md) |
| **C8** | **Comments say why.** Document architectural rationale and external constraints; never restate what Dart code self-evidently does. | Outdated "what" comments mislead; "why" comments explain trade-offs. | P3 | [04-types-constants-comments](references/04-types-constants-comments.md) |
| **C9** | **Full sound null safety.** Avoid bang operator (`!`) and `dynamic`. Use null-aware operators (`?.`, `??`) or explicit pattern matching. | Unchecked bang operators throw runtime `NullCheckError` in production. | P1 | [04-types-constants-comments](references/04-types-constants-comments.md) |
| **C10** | **Scope discipline.** Modify only files within the approved phase task. Do not reformat untouched legacy files. | Drive-by modifications complicate pull request reviews and trigger merge conflicts. | P2 | [05-self-check](references/05-self-check.md) |
| **C11** | **Workspace contracts win.** Honor `BaseScreen` + `BaseScreenState`, `UseCasePower<T, P>`, `DataState<T>`, and `app_ui_kit` components. | Inconsistent architectural patterns splinter the codebase. | P1 | [01-naming](references/01-naming.md), [03-errors-and-logging](references/03-errors-and-logging.md) |
| **C12** | **Visible side effects.** Keep widget `build()` pure; trigger navigation, dialogs, and network requests inside Cubits or event callbacks. | Side effects in build methods execute repeatedly on every rebuild. | P1 | [02-size-and-structure](references/02-size-and-structure.md) |
| **C13** | **Immutable state.** States emitted by Cubit/Bloc must be immutable; never mutate state objects in place. | In-place mutation prevents `BlocBuilder` from detecting state transitions. | P1 | [02-size-and-structure](references/02-size-and-structure.md) |
| **C14** | **Self-check before done.** Run `flutter analyze`, `dart format`, and feature unit tests before submitting review. | Unverified changes fail CI and waste reviewer time. | P1 | [05-self-check](references/05-self-check.md) |
| **C15** | **Const constructors.** Add `const` to widget constructors and instances wherever possible. | Eliminates unnecessary widget rebuilds during state tree invalidation. | P2 | [04-types-constants-comments](references/04-types-constants-comments.md) |
| **C16** | **Never override BaseScreen.build().** Implement `buildMobilePortrait()` on `BaseScreenState`. Never override `build()`. | Overriding `build()` completely breaks screen analytics, tracking, and responsiveness. | P1 | [02-size-and-structure](references/02-size-and-structure.md) |
| **C17** | **Dispose controllers and streams.** Always cancel `StreamSubscription` and dispose `TextEditingController`, `AnimationController`, `FocusNode`. | Leaked controllers and uncancelled streams cause memory leaks and runtime crashes. | P1 | [02-size-and-structure](references/02-size-and-structure.md) |

## Severity Summary

- **P1 (Blocker):** Broken contract, runtime null crash risk, memory leak, swallowed error, debug call, state mutation, or broken `BaseScreen`. Blocks approval.
- **P2 (Major finding):** Size threshold breach, missing `const`, helper method instead of widget class, magic values, scope violation. Must resolve before final acceptance.
- **P3 (Minor suggestion):** Comment wording, optional micro-optimization. Non-blocking.

See [06-review-severity](references/06-review-severity.md) for grading guidance.
