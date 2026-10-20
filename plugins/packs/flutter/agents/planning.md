---
skills:
  - {{slot:core-usage}}
---
## Flutter rules

- **UI & Design System**: `planning` performs **Codebase & UI Kit class mapping** via `{{slot:core-usage}}` (`app_core`, `app_util`, `app_ui_kit`), maps each UI need to exact widget/class names, records any `Core gap`, and specifies `BaseScreen`, `Router`, and `Cubit State` contracts.
- **Flutter Client**: Apply `{{slot:core-usage}}` **first** to determine the `architecture_profile.mode`:
  1. **Mode 1 (`imespro`)**: Explicitly selected or supported by actual Client dependencies/consumers. Sibling folders alone never select it. Run company setup, read resolved package guides, and map fitting APIs or Core gaps.
  2. **Mode 2 (`external-structured`)**: Client foundations with real consumers. Record actual bases, state, network, UI tokens, folder and DI conventions in Client Core Mapping; no company setup or guides.
  3. **Mode 3 (`external-standard`)**: Vanilla Flutter repository without pre-existing core. Design a minimalist, feature-first Clean Architecture under `lib/modules/<feature>/` adhering to Ponytail (smallest clear solution, standard Flutter widgets).
- **Step 1A scans**: Execute the 6 Codebase Intelligence scans following `{{slot:architecture-design}}` (`pubspec.yaml`, `{{slot:core-usage}}`, Router, DI, module code, `get_ux_error_patterns`).
- **`design.md` specifics**:
  1. **Architectural Decision & Profile**: Record the locked-in `architecture_profile` (`mode`, `core_source`, evidence paths, rationale).
  2. **Target Directory Tree**: reduce `get_project_structure` to the folders this feature actually needs under `lib/modules/<feature>/`.
  3. **Screen, Routing & DI Contract**: Specify screen base inheritance (`BaseScreen` in `imespro`, client base in `external-structured`, or standard widget in `external-standard`).
  4. **State Management & Data Flow**: Define Cubit states (follow the Client's existing state convention), Cubit methods, and only the UseCases and Repositories the behavior needs.
  5. **Mockoon design**: follow `{{slot:architecture-design}}` reference `references/05_api_mocking_strategy.md`.
  6. **Core Usage table**: `Core usage` table for `imespro`, `Client Core Mapping` for `external-structured`, or UI specification for `external-standard`.
- **Task acceptance checks**: `flutter analyze` or a targeted unit test.
- **Review DoD**: developer unit tests (UseCases, Mappers, Cubit emissions covering the agreed Pass/Default and Fail data) and zero-error `flutter analyze` requirements for Code Reviewer.
