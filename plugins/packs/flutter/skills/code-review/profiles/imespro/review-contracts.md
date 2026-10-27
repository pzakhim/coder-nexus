# iMESPro Code Review Contracts

> Topic: Reviewing BaseScreen/BaseScreenState, BaseDataSource, DataState/tryCatch, app_ui_kit reuse, and Hub validator rules (imespro profile)

## 1. `imespro` Hub Validator Rule Matrix

Always pass `architecture_profile: "imespro"` to `validate_architecture_code` and `validate_module_architecture`. In addition to the universal rules in `01-scope-gates-and-validators.md`, enforce the `imespro`-specific rules below:

| Rule | Layer | Hub Severity | Reviewer Verification (`imespro`) |
|---|---|---|---|
| `DAT-001` BaseDataSource | Data | `ERROR` / `WARNING` | Verify remote/local data sources inherit from the approved `BaseDataSource` / `ApiService` (`app_util`). Direct missing base is `BLOCKER`; indirect inheritance requires source inspection. |
| `DAT-002` Repo TryCatch / DataState | Data | `ERROR` | Verify `RepositoryImpl` methods wrap network/storage calls with `.tryCatch` / `.tryCatchAsync` and return `DataState<T>` (`DataSuccess` / `DataFailure`). Missing wrapper is `BLOCKER`. |
| `DAT-003` Safe DTO Parsing | Data | `WARNING` | Verify `Model.fromJson` / `DataMapper` uses `parseString`, `parseInt`, `parseDouble`, `parseBool`, `parseDateTime`, `parseList` (`app_util`) instead of unsafe `as` casts (`MAJOR` / `BLOCKER`). |
| `PRE-002` State Pattern | Presentation | `WARNING` | Verify Cubit (`BaseCubit` / `ListViewPagingCubit` from `app_core`) and immutable `Equatable` State match sibling modules without inventing custom state bases. |
| `PRE-004` UI Kit Reuse | Presentation | `INFO` | Audit every UI component against the approved `Core usage` table in `design.md`; using raw Material widgets where an approved `app_ui_kit` widget (`AppButton`, `AppForm`, `AppDialog`, `AppTextField`, etc.) applies is `MAJOR`. |
| `PRE-006` BaseScreen Contract | Presentation | `ERROR` / `WARNING` | Verify top-level screens under `presentation/screens/*_screen.dart` inherit from `BaseScreen` / `BaseScreenState` (`app_core`), implement `getScreen()`, and override required responsive hooks (`buildMobilePortrait`, `buildTabletPortrait`, `buildLandscape`). Direct `StatelessWidget`/`StatefulWidget` on a screen is `BLOCKER`. |
| `STY-001` AppLogger | All | `WARNING` | Flag raw `print()` or `debugPrint()`; require `AppLogger` (`app_util`) with sensitive fields redacted (`MAJOR`). |

---

## 2. Foundation Package Boundary Audit (`../app-core`, `../app-util`, `../app-ui-kit`)

- **No Edits or Copies of Core Packages:** Verify `git status` and `git diff` confirm zero files were edited inside `../app-core`, `../app-util`, or `../app-ui-kit`, and no core package classes were copied into the Client's `lib/` tree (`BLOCKER`).
- **Core Gap Routing:** If the Code Writer encountered a genuine incompatibility or missing capability in `app_core`, `app_util`, or `app_ui_kit`, the Reviewer must **not** grant an informal waiver; verify it is documented as a Core gap in `design.md` or raise a `PLAN_CONFLICT` (`R7`).
