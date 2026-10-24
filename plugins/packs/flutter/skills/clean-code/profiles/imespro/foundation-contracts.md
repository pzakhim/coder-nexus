# iMESPro Core & UI Kit Clean Code Contracts

> Topic: Mandatory `BaseScreen`, `UseCasePower`, `DataMapper`, `app_ui_kit` reuse, `DataState`/`.tryCatch`, and `AppLogger.I` rules

This reference enforces **C1** (One concept, one place), **C4** (No swallowed errors), **C7** (No magic values), and **C11** (Workspace contracts win) when the workspace profile is **`imespro`** (`app_core`, `app_util`, `app_ui_kit`).

---

## 1. Base Architecture Contracts (**C11** — `BLOCKER` on violation)

| Layer | Mandatory iMESPro Base Contract | Prohibited Custom Alternative |
|---|---|---|
| **Presentation (Route Screen)** | Extend `BaseScreen<VM>` + `BaseScreenState`. Override `getScreen()`, `createState()`, and `buildMobilePortrait()` (plus tablet/landscape builders when required). | Raw `StatelessWidget` / `StatefulWidget` as a route destination screen, or overriding `build()` inside a `BaseScreen` subclass. |
| **Presentation (State Holder)** | Extend `BaseViewModel` / approved Cubit base from `app_core`. | Ad-hoc state holders that bypass `app_core` lifecycle and loading/error handling. |
| **Domain (Use Case)** | Extend `UseCasePower<Output, Params>` (or `UseCaseNoParams<Output>`) returning `ResultFuture<T>`. Use pure Dart deep imports (`package:app_core/domain/...`, `package:app_util/domain/...`). | Custom use case base classes, raw `Future<T>` without typed failure handling, or importing barrel files (`package:app_core/app_core.dart`) inside Domain. |
| **Data (DTO Mapping)** | Extend `DataMapper<Model, Entity>` for every DTO-to-Entity conversion. | Static `Model.toEntity()` helpers, ad-hoc conversion functions, or leaking DTO models into Domain/Presentation. |

---

## 2. Zero UI Kit & Utility Reinvention (**C1**, **C7** — `BLOCKER` / `MAJOR` on violation)

Before writing any widget, dialog, formatter, or network wrapper, check `../app-ui-kit/guidance/GUIDE.md`, `../app-core/guidance/GUIDE.md`, and `../app-util/guidance/GUIDE.md`:

- **Buttons, Inputs & Selection (`app_ui_kit`)**: Always reuse `AppButton`, `AppFormField` / `AppTextField`, `AppDropdown`, and `AppCheckbox`. Never build custom `ElevatedButton` or `TextField` wrappers unless documented as an approved `Core gap` in `design.md`.
- **Dialogs, Bottom Sheets & Feedback (`app_ui_kit`)**: Always reuse `AppDialog`, `AppBottomSheet`, and `AppToast` / snackbar helpers instead of raw `showDialog()` or `ScaffoldMessenger` boilerplate.
- **Paginated Lists (`app_ui_kit`)**: Always reuse `ListViewPaging` for paginated lists (handles initial load, load-more, empty, and error states).
- **Design Tokens (`app_ui_kit`)**: Always use `app_ui_kit` color, typography, spacing, and radius tokens instead of hardcoded `Color(0xFF...)`, `TextStyle(fontSize: ...)`, or magic `EdgeInsets.all(...)`.

---

## 3. Error Handling, Network & Logging (**C3**, **C4** — `BLOCKER` / `MAJOR` on violation)

- **Repository Error Mapping (`app_core` / `app_util`)**: Wrap remote/local calls via `ApiService` and `.tryCatch` returning `DataState<T>` (`DataSuccess` / `DataFailed`). Never swallow exceptions with empty `catch (_) {}` or return untyped `null` on failure.
- **Structured Logging (`app_util`)**: Log failures and diagnostic events exclusively through `AppLogger.I.e(message, error: e, stackTrace: st)` (or `.i` / `.w` / `.d`). Never commit `print()` or `debugPrint()`.
