# 06 - Review Severity & Violation Grading

Reviewers evaluate Flutter code changes against this rubric. Grading follows [work-item-contract handoff-and-status section 9](../../work-item-contract/references/handoff-and-status.md).

## 1. Severity Scale

| Severity | Definition | Impact on Review |
|---|---|---|
| **P1 (Blocker)** | Correctness bugs, runtime crashes, memory leaks, security leaks, or core contract violations. | **Blocks approval.** Must be fixed before code is merged. |
| **P2 (Major)** | Maintainability issues, structural antipatterns, missing `const`, oversized methods/classes, magic numbers. | Must be addressed or explicitly justified in review discussion. |
| **P3 (Minor)** | Minor naming polish, redundant comments, cosmetic suggestions. | Non-blocking; author may address at their discretion. |

## 2. Flutter Violation Catalog

| Violation Pattern | Severity | Rational & Required Action |
|---|---|---|
| `print()` or `debugPrint()` left in code | **P1** | Replace with `AppLogger.I` or remove. |
| Unhandled exception / swallowed error in Cubit or Data Source | **P1** | Handle error, emit failure state, or use `.tryCatch`. |
| Overriding `build()` in `BaseScreenState` | **P1** | Remove `build()`; override `buildMobilePortrait()`. |
| Mutating state object directly in Cubit | **P1** | Emit new immutable state instance with `copyWith`. |
| Undisposed Controller, FocusNode, or StreamSubscription | **P1** | Add disposal logic to `dispose()` or `close()`. |
| Unsafe bang operator (`!`) causing possible `NullCheckError` | **P1** | Replace with null-safe fallback or guard clause. |
| Custom widget duplicating `app_ui_kit` (`AppButton`, `AppFormField`) | **P1** | Replace custom widget with Kit component per [core-package-usage](../../flutter-core-package-usage/SKILL.md). |
| Helper `_buildX()` method returning `Widget` instead of widget class | **P2** | Extract to private `StatelessWidget` with `const` constructor. |
| Widget `build()` method > 40 lines | **P2** | Decompose into smaller sub-widgets. |
| Missing `const` constructor on immutable widget | **P2** | Add `const` constructor and instance annotation. |
| Hardcoded colors or ad-hoc typography | **P2** | Use `AppColor.*` and `Text12`...`Text34` from `app_ui_kit`. |
| Function parameters > 4 | **P2** | Group into request model or named parameter object. |
| Comment stating the obvious ("fetch data") | **P3** | Remove or rewrite to document why/edge cases. |
