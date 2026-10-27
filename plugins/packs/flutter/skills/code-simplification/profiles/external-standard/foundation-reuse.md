# External Standard Foundation Reuse for Simplification

> Topic: Prefer Flutter SDK / Material 3 widgets and `shared/widgets/` over custom equivalents; no speculative bases (Reuse lens)

Applies **S5** (Reuse before writing) and **S6** (YAGNI) when the workspace profile is **`external-standard`**.

## Reuse rows

| Tag | Home-grown in the diff | Replace with | Watch out |
|---|---|---|---|
| `native` | Custom button or input built from `GestureDetector`/`Container` | `FilledButton`, `OutlinedButton`, `TextButton`, `TextFormField` | Same tap target, states and validation |
| `native` | Custom modal or sheet scaffolding | `showDialog` + `AlertDialog`, `showModalBottomSheet` | Same dismiss behavior and returned value |
| `native` | Raw `Color(0xFF...)` / inline `TextStyle` | `Theme.of(context).colorScheme` / `.textTheme` | Same rendered values in light and dark themes |
| `reuse` | A widget duplicated across features | One widget in `lib/shared/widgets/` once two or more features import it | Not before the second real user (`{{slot:clean-code}}` C16) |
| `yagni` | Invented `BaseScreen`, `BaseViewModel` or abstract wrapper hierarchy | Plain `StatelessWidget`/`StatefulWidget` and the chosen state holder | Only the layers the approved feature needs |

## Report example

`simplify: custom button -> FilledButton at lib/modules/auth/presentation/login_page.dart:40; net -18 lines; checks: flutter test test/modules/auth exit 0`
