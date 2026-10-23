# 03 - Effort, Severity, and Reporting Format

Follow [work-item-contract handoff-and-status section 9](../../work-item-contract/references/handoff-and-status.md) for grading and reporting defect findings.

## 1. Review Effort Levels

- **Quick:** Diff inspection for obvious red flags (debug statements, missing const, leaked controllers).
- **Standard:** Systematic pass across all 7 dimensions on modified files.
- **Deep:** Comprehensive state-machine flow analysis and concurrency boundary probing.

## 2. Severity Definitions

- **`BLOCKER`:** Prevents core feature operation, causes runtime crashes (`NullCheckError`, red screen of death), leaks authentication tokens, or permanently corrupts local state.
- **`MAJOR`:** Degrades key functionality, causes memory leaks, leads to stuck loading spinners on error, or fails responsive layout on tablets.
- **`MINOR`:** Minor UI misalignment, cosmetic glitch, or missing non-critical accessibility label.

## 3. Reporting Line Syntax

```text
bug-hunt: <file:line> | <severity> <confidence> | <dimension> | <description> | <fix>
```

### Examples
```text
bug-hunt: lib/modules/auth/presentation/screens/login_screen.dart:45 | BLOCKER CONFIRMED | data | unhandled null on userProfile.token! throws NullCheckError | use null-aware operator and check isSuccess
bug-hunt: lib/modules/orders/presentation/cubit/order_cubit.dart:88 | MAJOR CONFIRMED | async | rapid taps invoke checkout API multiple times concurrently | disable button or set isLoading true in state
bug-hunt: lib/modules/home/presentation/widgets/banner.dart:15 | MAJOR PLAUSIBLE | layout | Row children unbounded causes RenderFlex overflow on small screens | wrap title in Expanded
```
