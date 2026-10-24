---
skills:
  - {{slot:core-package-usage}}
---
## Flutter rules

- **Source and test folders**: `lib/` and `test/`.
- **UI focus**: Golden Screenshot verification and `app_ui_kit` component fidelity.
- **Flutter Client**: Run actual Client `flutter test` (widget/UI suites) and runtime visual verification on the reviewed tree (for a test run, the recorded current revision), adapting the harness per the Test Runner rules of `{{slot:core-package-usage}}` for the resolved `architecture_profile.mode`. Under `imespro`, also verify the `BaseScreen` route observer and responsive layout hooks, `ListViewPaging` auto-load and pull-to-refresh, and `app_ui_kit` widget interactions; under `external-standard`, Cubit/BLoC is not required.
- **Golden comparisons**: When an approved golden test and reviewed baseline already exist, run the comparison without `--update-goldens`. A missing baseline when golden comparison is approved cannot become PASS. Never update a golden baseline during pre-release verification.
