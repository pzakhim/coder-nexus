# Profile 1: iMESPro Core System (Internal)

This profile activates when the target workspace is an **iMESPro Flutter Client** equipped with the three sibling foundation packages:
- `../app-core` (Clean Architecture base, Screen tracking & responsive layout, ListViewPaging super-component)
- `../app-util` (Result type `DataState`, HTTP client `ApiService`, safe parsing, local storage, device info)
- `../app-ui-kit` (Design-system widgets: buttons, inputs, dialogs, bottom sheets, loading/empty states, typography, colors)

---

## 1. Activation & Verification Gate

1. Verify package availability: Sibling directories `../app-core`, `../app-util`, `../app-ui-kit` exist and `pubspec.yaml` references `app_core`, `app_util`, `app_ui_kit`.
2. Run `coder-nexus setup flutter --check` in the Client root.
   - Status must be `READY`.
   - Any other status is `BLOCKED` for feature build.

---

## 2. Core Knowledge Discovery & Reading Contract

Knowledge lives inside the packages alongside their versioned code:
```text
../app-<name>/
├── guidance/
│   ├── GUIDE.md        # Decision table, components, contracts, gotchas, review checklist
│   └── examples/*.dart # Analyzer-verified examples to copy patterns from
└── lib/                # Source code (Source wins over GUIDE if signatures differ)
```

- **Agents are authorized and required to read:**
  - `../app-core/guidance/GUIDE.md`
  - `../app-util/guidance/GUIDE.md`
  - `../app-ui-kit/guidance/GUIDE.md`
  - Verified examples in each package's `guidance/examples/`.
  - Source files in `lib/` to confirm exact signatures, parameter types, or behavior.
- **Rule of Authority:** **Source wins** over `GUIDE.md`. If a signature or parameter in code differs from documentation, adhere to the real source implementation.

---

## 3. Component Inventory & Decision Matrix

### A. app_core
| Need | Mandated Component | Contract & Usage Rules |
| :--- | :--- | :--- |
| Route destination screen | `BaseScreen` + `BaseScreenState` | **Mandatory** for every screen in `presentation/screens/*_screen.dart`. Overrides `getScreen()`, `createState()`, `buildMobilePortrait()`. **NEVER override `build()`**. |
| Business operation | `UseCasePower<T, P>` / `UseCasePowerNoParams<T>` | Pure Dart. Deprecated: `UseCase<T, P>`, `NoInputUseCase<T>`, `.execute()`. |
| Paged vertical list | `ListViewPaging<T>` + `ListViewPagingCubit<T>` | Integrates `PagingUseCase<T>` and `ListViewPagingRepository<T>`. Automatic pull-to-refresh & load-more. Paging total comes from API `pagination.total`. |
| Remote data source | `BaseRemoteDataSource` | Injects `ApiService` and `ApiConfig`. |
| Data mapper | `DataMapper<Entity>` | Implemented by data models to map API response to pure domain entities. |
| Widgets & Helpers | `LabelText`, `FlavorBanner`, `MatomoHelper` | Required form label markers, environment ribbon, and analytics tracking. |

### B. app_util
| Need | Mandated Component | Contract & Usage Rules |
| :--- | :--- | :--- |
| Method return type | `DataState<T>` (`DataSuccess`, `DataFailure`) | Every repository and use case returns `Future<DataState<T>>`. Callers branch on `isSuccess`. |
| API call conversion | `Future<ApiResponse>.tryCatch(...)` | Extension on API responses. Catches network, HTTP, and parsing exceptions safely. |
| HTTP requests | `ApiService` (GetIt singleton) | Handles GET/POST/PUT/PATCH/DELETE, token refresh on 401, multi-part requests. |
| Safe JSON parsing | `parseString`, `parseInt`, `parseDouble`, `parseList` | Used in data models `fromJson` to prevent runtime type exceptions. |
| Persistence & Device | `LocalStorageService`, `DeviceHelper`, `ApiConfig` | Key-value storage and device information detection. |

### C. app_ui_kit
| Need | Mandated Component | Contract & Usage Rules |
| :--- | :--- | :--- |
| Buttons | `AppButton`, `AppButton.rounded` | Replaces all raw Material buttons. Supports primary, secondary, destructive, and loading states. |
| Text / Form inputs | `AppFormField`, `AppDatePicker`, `AppMultiDropdownFormFieldV1` | Packaged validation, password toggle, and calendar picker. |
| Dialogs & Sheets | `AppDialog.show(...)`, `AppBottomSheetCommonLayout.show(...)` | Standardized alert, confirmation, and modal bottom sheet. |
| Feedback states | `AppLoadingIndicator`, `AppNoData`, `ImageShimmer`, `BadgeWidget` | Standard loading spinner, empty illustration, image skeleton, and badges. |
| Navigation & Appbar | `AppDefaultAppbar`, `AppBottomNavigationBar` | Common top bar and bottom navigation layout. |
| Typography & Colors | `Text12` ... `Text34`, `AppColor.*` | Central design system tokens. |

---

## 4. Strict Import Rules

- **Domain Layer:** Pure Dart only.
  - Allowed: `package:app_core/domain/...`, `package:app_util/domain/...`, pure Dart third-party packages (e.g. `equatable`), and sibling domain files.
  - **PROHIBITED:** `package:flutter`, `package:app_ui_kit`, and the root barrels `package:app_core/app_core.dart` or `package:app_util/app_util.dart`.
- **Data & Presentation Layers:** Barrel imports are encouraged:
  - `import 'package:app_core/app_core.dart';`
  - `import 'package:app_util/app_util.dart';`
  - `import 'package:app_ui_kit/app_ui_kit.dart';`

---

## 5. Non-Negotiable Boundaries (Company Knowledge Preservation)

1. **Zero Reinvention:** If a component or helper exists in `app-core`, `app-util`, or `app-ui-kit`, writing a custom implementation in the Client is an **automatic review failure (`FAIL`)**.
2. **Zero Modification:** Never edit, commit, format, or patch files inside `../app-core`, `../app-util`, or `../app-ui-kit`.
3. **Core Gap Exception:** Only if a need matches an explicit `"Do not use when"` rule in `GUIDE.md` (e.g. reverse chat list for `ListViewPaging`), or is absent from all 3 packages, can a Client-specific solution be built under `lib/modules/<feature>/` and documented as a `Core gap`.
