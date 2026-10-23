---
name: code-simplification
description: Flutter and Dart code simplification rules - eliminate reinvented widgets, redundant helpers, nested layout pyramids, and boilerplate using app_ui_kit, app_util, app_core, and Dart idioms.
---

# Flutter Code Simplification

Simplify Flutter code by replacing boilerplate, deep widget pyramids, and home-grown widgets with idiomatic Dart constructs and approved iMESPro packages (`app_ui_kit`, `app_util`, `app_core`).

Simplification must be strictly behavior-preserving and confined to the current task scope. Report simplifications using the single-line format defined in [work-item-contract handoff-and-status section 9](../work-item-contract/references/handoff-and-status.md).

## 1. Quick Replacement Reference

| Smell / Boilerplate | Clean Replacement | Benefit | Reference |
|---|---|---|---|
| Re-invented custom button | `AppButton` / `AppButton.rounded` | Standard design tokens, loading state, accessibility | [03-smell-catalog](references/03-smell-catalog.md) |
| Re-invented form input / textfield | `AppFormField` | Built-in obscure toggle, validation, error labels | [03-smell-catalog](references/03-smell-catalog.md) |
| Home-grown alert / confirm dialog | `AppDialog.show` | Uniform styling, responsive width, barrier handling | [03-smell-catalog](references/03-smell-catalog.md) |
| Home-grown bottom modal sheet | `AppBottomSheetCommonLayout.show` | Drag handles, scroll behavior, dismiss logic | [03-smell-catalog](references/03-smell-catalog.md) |
| Manual pagination & pull-to-refresh | `ListViewPaging<T>` | Eliminates 100+ lines of scroll/refresh/page logic | [03-smell-catalog](references/03-smell-catalog.md) |
| Monolithic `_buildItem()` methods | Private `_ItemWidget` with `const` | Enables subtree caching; prevents full tree rebuilds | [03-smell-catalog](references/03-smell-catalog.md) |
| Imperative list loops in build | Collection-`for` and spread `...` | Declarative widget tree; reduces intermediate lists | [03-smell-catalog](references/03-smell-catalog.md) |
| Nested ternary null checks | Null-aware `?.` and fallback `??` | Eliminates null assertion errors and improves flow | [03-smell-catalog](references/03-smell-catalog.md) |
| Manual try-catch in repository | `Future<ApiResponse>.tryCatch` | Converts all exceptions into safe `DataState<T>` | [03-smell-catalog](references/03-smell-catalog.md) |

## 2. Reporting Format

Record simplifications in the handoff using the format from [05-report](references/05-report.md):

```text
simplify: <file:line> | <smell> | <replacement> | <lines diff>
```

Example:
```text
simplify: lib/modules/order/presentation/screens/order_screen.dart:45 | _buildOrderItem helper | private _OrderItemCard widget with const | -24 lines
```
