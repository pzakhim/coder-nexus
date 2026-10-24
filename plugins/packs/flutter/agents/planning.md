---
skills:
  - {{slot:core-package-usage}}
---
## Flutter rules

- **FE Data Pipeline**: `RemoteDataSource` calling `ApiService`, `Model.fromJson`, `RepoImpl`, `UseCase`, and DI.
- **UI & Design System**: `planning` performs **Codebase & UI Kit class mapping** via `{{slot:core-package-usage}}` (`app_core`, `app_util`, `app_ui_kit`), maps each UI need to exact widget/class names, records any `Core gap`, and specifies `BaseScreen`, `Router`, and `Cubit State` contracts.
- **Flutter Client**: resolve the `architecture_profile.mode` with `{{slot:core-package-usage}}` **first**; the selection rules and each profile's planning duties live there.
- **Step 1A scans**: Execute the 6 Codebase Intelligence scans following `{{slot:architecture-design}}` (`pubspec.yaml`, `{{slot:core-package-usage}}`, Router, DI, module code, `get_ux_error_patterns`).
- **`design.md` specifics**:
  1. **Architectural Decision & Profile**: Record the locked-in `architecture_profile` (`mode`, `core_source`, evidence paths, rationale).
  2. **Target Directory Tree**: reduce `get_project_structure` to the folders this feature actually needs under `lib/modules/<feature>/`.
  3. **Screen, Routing & DI Contract**: Specify screen base inheritance (`BaseScreen` in `imespro`, client base in `external-structured`, or standard widget in `external-standard`).
  4. **State Management & Data Flow**: Define Cubit states, Cubit methods, and only the UseCases and Repositories the behavior needs.
  5. **Mockoon design**: follow `{{slot:architecture-design}}` reference `references/05_api_mocking_strategy.md`.
  6. **Core Usage table**: `Core usage` table for `imespro`, `Client Core Mapping` for `external-structured`, or UI specification for `external-standard`.
  7. **UI/UX mapping** (when `design-uiux/` exists): each `S-NN` → screen class, route and arguments; each kit class → widget from `{{slot:ui-kit-mapping}}` §3 for the recorded profile; each `C-NN` → widget under `lib/modules/<feature>/presentation/widgets/` (or the shared folder when two modules need it) with a `Core gap` note when `app_ui_kit` has no fitting widget.
- **Task acceptance checks**: `flutter analyze` or a targeted unit test.
- **Review DoD**: developer unit tests (UseCases, Mappers, Cubit emissions covering the agreed Pass/Default and Fail data) and zero-error `flutter analyze` requirements for Code Reviewer.
