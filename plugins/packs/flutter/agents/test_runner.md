---
skills:
  - {{slot:core-package-usage}}
---
## Flutter rules

- **Developer unit tests** (owned by `code_writer`, graded by `code_reviewer`) cover `Model.fromJson`, `RemoteDataSource`, `UseCase`, and `Cubit` logic with Mockoon/API payloads.
- **UI focus**: Golden Screenshot verification and `app_ui_kit` component fidelity; developer unit tests cover `Cubit` logic.
- **Flutter Client**: Run actual Client `flutter test` (widget/UI suites) and runtime visual verification on the reviewed tree. Apply `{{slot:core-package-usage}}` across the resolved `architecture_profile.mode`:
  - **Mode 1 (`imespro`)**: Verify `BaseScreen` route observer and responsive layout hooks; verify `ListViewPaging` UI states (auto-load, pull-to-refresh, load-more with total, empty, error); verify `app_ui_kit` widget interactions.
  - **Mode 2 (`external-structured`)**: Verify screen layout and UI behavior using client's test harnesses and base widgets.
  - **Mode 3 (`external-standard`)**: Verify standard Flutter widget trees and the UI state transitions actually used; Cubit/BLoC is not required.
  Unit test logic has already been verified by `code_reviewer`; focus on user acceptance and visual fidelity.
- **Golden comparisons**: When an approved golden test and reviewed baseline already exist, run the comparison without `--update-goldens`. A missing baseline when golden comparison is approved cannot become PASS. Never update a golden baseline during pre-release verification.
