# 05 - Simplification Reporting Format

Report all simplifications made during a phase in the handoff document according to [work-item-contract handoff-and-status section 9](../../work-item-contract/references/handoff-and-status.md).

## 1. Syntax

```text
simplify: <file:line> | <smell> | <replacement> | <lines diff>
```

## 2. Examples

```text
simplify: lib/modules/auth/presentation/screens/login_screen.dart:58 | custom text input widget | AppFormField with password type | -32 lines
simplify: lib/modules/orders/presentation/screens/order_list_screen.dart:102 | manual scroll pagination | ListViewPaging with ListViewPagingCubit | -85 lines
simplify: lib/modules/orders/presentation/widgets/order_card.dart:22 | imperative loop | collection-for with const constructor | -12 lines
```
