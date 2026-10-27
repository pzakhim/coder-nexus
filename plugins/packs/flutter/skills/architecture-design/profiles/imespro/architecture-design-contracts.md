# iMESPro Architecture Design Contracts

> Topic: Designing against app_core, app_util, and app_ui_kit, reading GUIDE.md, and authoring the Core usage table (imespro profile)

## 1. Activation & Pre-Design Setup Gate (`imespro`)

1. Verify sibling packages `../app-core`, `../app-util`, `../app-ui-kit` are referenced in the Client's `pubspec.yaml`.
2. Run `coder-nexus setup flutter --check` in the Client root (`STATUS: READY` is required; any other status is `BLOCKED`).
3. Read the package guides and verify signatures in source (**Source wins over `GUIDE.md`**):
   - `../app-core/guidance/GUIDE.md` & `../app-core/lib/`
   - `../app-util/guidance/GUIDE.md` & `../app-util/lib/`
   - `../app-ui-kit/guidance/GUIDE.md` & `../app-ui-kit/lib/`

---

## 2. `imespro` Component Inventory & Decision Matrix

### 2.1 `app_core`
| Need | Mandated Component | Design & Architecture Contract |
|---|---|---|
| Route destination screen | `BaseScreen` + `BaseScreenState` | Mandatory for every screen in `presentation/screens/*_screen.dart`. Overrides `getScreen()`, `createState()`, `buildMobilePortrait()` (and `buildTabletPortrait()` / `buildLandscape()` when applicable). **Never override `build()`**. |
| State root (`INIT` vs `EXTEND`) | `BaseBlocState` (`equatableProps`) or `Equatable` (`props`) | For `INIT`, use `BaseBlocState` (`Pattern A`) or the Client's established state base; for `EXTEND`, preserve the existing module's state pattern. |
| Business operation | `UseCasePower<T, P>` / `UseCasePowerNoParams<T>` | Pure Dart domain operation (validates via `validate(param)`, executes via `execute(param)`). |
| Paged vertical list | `ListViewPaging<T>` + `ListViewPagingCubit<T>` | Integrates `PagingUseCase<T>` and `ListViewPagingRepository<T>`. Requires API response to carry `pagination.total`. |
| Remote data source | `BaseRemoteDataSource` | Injects `ApiService` and `ApiConfig`. |
| Data mapper | `DataMapper<Entity>` | Implemented by DTO `Model` classes (`mapToEntity()` / `toEntity()`). |
| Form label & analytics | `LabelText`, `FlavorBanner`, `MatomoHelper` | Standard form label markers, environment banner, and screen tracking. |

### 2.2 `app_util`
| Need | Mandated Component | Design & Architecture Contract |
|---|---|---|
| Result wrapper | `DataState<T>` (`DataSuccess`, `DataFailure`) | Returned by all `Repository` and `UseCasePower` methods (`Future<DataState<T>>`). |
| Exception-to-result conversion | `Future<ApiResponse>.tryCatch(...)` | Used inside `RepositoryImpl` to convert network/parsing exceptions into `DataFailure`. |
| HTTP client | `ApiService` | Singleton handling REST verbs, `ApiConfig.domain` base URL, and automatic 401 token refresh. |
| Safe JSON parsing | `parseString`, `parseInt`, `parseDouble`, `parseBool`, `parseDateTime`, `parseList` | Mandatory inside `Model.fromJson` to prevent runtime `_TypeError` crashes. |
| Local storage & device | `LocalStorageService`, `DeviceHelper`, `ApiConfig` | Key-value persistence and device metadata. |

### 2.3 `app_ui_kit`
| Need | Mandated Component | Design & Architecture Contract |
|---|---|---|
| Buttons | `AppButton`, `AppButton.rounded` | Primary, secondary, destructive, and `isLoading` states. |
| Form inputs & pickers | `AppForm`, `AppFormField`, `AppDatePicker`, `AppMultiDropdownFormFieldV1` | Standardized validation, password toggles, and date/dropdown pickers. |
| Dialogs & bottom sheets | `AppDialog.show(...)`, `AppBottomSheetCommonLayout.show(...)` | Modal alerts, confirmations, and bottom sheets. |
| Visual states & feedback | `AppLoadingIndicator`, `AppNoData`, `ImageShimmer`, `BadgeWidget` | Standard loading state (`1. Loading`), empty state (`3. Empty`), image shimmer, and status badges. |
| Appbar, nav & tokens | `AppDefaultAppbar`, `AppBottomNavigationBar`, `Text12`..`Text34`, `AppColor.*` | Standard navigation bars, typography, and color tokens. |

---

## 3. Data Pipeline & `Core usage` Table in `design.md`

- **Standard `imespro` Network Pipeline:**
  ```text
  RemoteDataSource (extends BaseRemoteDataSource, uses ApiService + ApiConfig.domain)
    → Model.fromJson (app_util parse* helpers) implements DataMapper<Entity>
    → RepoImpl: remote.call().tryCatch(...) → Future<DataState<Entity>>
    → UseCasePower (when business rule/shared) → Cubit → UI consumes Entity only
  ```
- **Authoring `## Foundation reuse (Core usage)` in `design.md`:**
  - Map every feature need to its exact `app_core`, `app_util`, or `app_ui_kit` class and `GUIDE.md` section.
  - Only when a need matches an explicit `"Do not use when"` rule in `GUIDE.md` or is absent from all three packages, record a justified **`Core gap`** row (`Client location` under `lib/modules/<feature>/` + reason) and queue a `Q-NN` → `D-NN` when architectural.
