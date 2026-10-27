# iMESPro Foundation Reuse for Simplification

> Topic: Replace home-grown widgets, paging and error plumbing with `app_ui_kit`, `app_core` and `app_util` (Reuse lens)

Applies **S5** (Reuse before writing) and **S6** (YAGNI) when the workspace profile is **`imespro`**. Package choice and "Use when" fit follow `design.md` (`Core usage`) and the `../app-*/guidance/GUIDE.md` files; the packages are read-only.

## Reuse rows

| Tag | Home-grown in the diff | Replace with | Watch out |
|---|---|---|---|
| `reuse` | Custom button (`GestureDetector`/`ElevatedButton` + loading spinner) | `AppButton` (`app_ui_kit`) | Keep the same enabled/loading behavior and tap target |
| `reuse` | Custom text input with obscure toggle, validation or error label | `AppFormField` (`app_ui_kit`) | Same validators and error messages |
| `reuse` | Hand-built alert/confirm dialog via raw `showDialog` | `AppDialog.show` (`app_ui_kit`) | Same barrier-dismiss and result value |
| `reuse` | Hand-built bottom sheet via raw `showModalBottomSheet` | `AppBottomSheetCommonLayout.show` (`app_ui_kit`) | Same drag/dismiss behavior and returned value |
| `reuse` | Manual pagination: `page`, `pageSize`, `ScrollController.addListener`, load-more spinner, pull-to-refresh | `ListViewPaging<T>` with `ListViewPagingCubit` (`app_core`) | Same page size, empty and error states |
| `reuse` | Manual `try`/`catch` around an `ApiResponse` call in a repository | `.tryCatch` on `Future<ApiResponse>` returning `DataState<T>` (`app_util`) | Same failure mapping seen by the use case |
| `yagni` | A new base screen, base view model or result wrapper beside the `app_core` ones | The existing `app_core` base classes | They are required by the profile: never "simplify" them away |

## Leave alone

- `BaseScreen`, `BaseViewModel`, `UseCasePower`, `DataMapper` and `DataState` usages: required by the profile even where a single implementation exists.
- A documented `Core gap` in `design.md`: the local widget stays until the gap is closed.

## Report example

`simplify: manual pagination -> ListViewPaging at lib/modules/order/presentation/screens/order_list_screen.dart:102; net -85 lines; checks: flutter test test/modules/order exit 0`
