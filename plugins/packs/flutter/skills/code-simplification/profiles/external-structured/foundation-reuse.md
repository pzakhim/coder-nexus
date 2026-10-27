# External Structured Foundation Reuse for Simplification

> Topic: Replace home-grown widgets and plumbing with the client's own `lib/core/` and `lib/shared/` (Reuse lens)

Applies **S5** (Reuse before writing) and **S6** (YAGNI) when the workspace profile is **`external-structured`**. The client's mapping lives in `design.md` (`Client Core Mapping`).

## Reuse rows

| Tag | Home-grown in the diff | Replace with | Watch out |
|---|---|---|---|
| `reuse` | Feature-local button, input, dialog, loading or error state | The client's shared widget in `lib/shared/` (or `lib/core/`) | Same states, validators and results |
| `reuse` | New network wrapper, result/failure type or base class in a feature | The client's existing one in `lib/core/` | Never add a second competing base |
| `reuse` | Raw colors, text styles or spacing numbers | The client's theme extensions and design tokens | Same rendered values |
| `yagni` | Company-template symbols (`BaseScreen`, `DataState`, `ApiService`, `AppLogger`) the client does not define | The client's own equivalents, or plain Flutter | Only symbols the client repository defines |

## Leave alone

- Base classes and contracts the client's `lib/core/` defines and other features already use.

## Report example

`simplify: feature-local dialog -> shared ConfirmDialog at lib/features/orders/presentation/order_page.dart:58; net -30 lines; checks: flutter test test/features/orders exit 0`
