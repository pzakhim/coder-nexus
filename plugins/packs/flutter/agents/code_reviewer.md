---
skills:
  - {{slot:core-package-usage}}
---
## Flutter rules

Read the approved profile through `{{slot:core-package-usage}}`. Company examples in the test audit (`parse_util`, `DataFailure`, `ListViewPagingCubit`) apply only when that API is actually used. External profiles test their own result/state/paging contracts and required failure paths.

### Flutter Checks
- Evaluate according to `architecture_profile.mode` specified in `design.md`:
  - **Mode 1 (`imespro`)**: Apply `{{slot:core-package-usage}}` Reviewer checks (every package's `guidance/GUIDE.md` review checklist): `setup --check` READY; no change under `../app-*`; no Client class reimplementing a core API; domain imports pure (no Flutter, no barrel); every screen extends `BaseScreen`, overrides `getScreen()`/`buildMobilePortrait()`, never `build()`; `Core usage` table matches the code. Any failure is **automatic `CHANGES_REQUESTED` (FAIL)**.
  - **Mode 2 (`external-structured`)**: Verify Coder inherited client's existing base classes and reused client's shared widgets per `Client Core Mapping`. Reject any new redundant/competing base classes.
  - **Mode 3 (`external-standard`)**: Verify Ponytail simplicity, Clean Architecture layer separation, and absence of speculative abstractions.
- Run `validate_architecture_code` for changed Dart files with `architecture_profile` set to the approved `architecture_profile.mode` (design, or brief for phase-free work). Pass the same value to `validate_module_architecture` for an affected complete module; for scoped UI-only work, record module structure `N/A` with reason and inspect affected imports, state ownership, and integration directly. Never omit the profile: omitted arguments retain legacy iMESPro checks. `FAILED` blocks; `UNVERIFIED` or unresolved warnings require explicit Client inspection. For external-structured, verify actual base inheritance, shared widgets, error/state and DI conventions against the Client Core Mapping; external-standard requires no company classes.
- Independently classify changed destinations and verify the approved profile's screen naming, superclass, applicable lifecycle hooks, route/DI and owned resources. Only iMESPro requires `screens/*_screen.dart`, `*Screen` and BaseScreen hooks; external-structured follows Client conventions and external-standard permits standard Flutter widgets. Exempt dialogs, sheets and child widgets.
- **Validator is a hard gate**: run `validate_architecture_code` on every changed Dart file with the approved `architecture_profile`. Any `ERROR` violation means the verdict cannot be `APPROVED`.
- **`PHASE-00`**: Do not demand Dart files or `validate_architecture_code` when `PHASE-00` only prepares `mocks/<feature>_mockoon.json`. In `PHASE-01+`, verify `lib/` implements only the real `RemoteDataSource` (`ApiService`) with relative endpoint paths, without any fake `Mock<Feature>DataSource` classes, `FakeRepository`, hardcoded `localhost` hosts, or production fallbacks.

### Flutter Unit Test Audit (`PHASE-01+`)
- Inspect unit test files under `test/modules/<feature>/..._test.dart` for **Happy-Path Bias**.
- Detect shallow or trivial assertions (e.g. `expect(result, isNotNull)` without verifying internal data properties).
- **Data Models (`fromJson`)**: Probe whether optional keys can be omitted or null, empty arrays `[]` don't crash, and type variations (numeric strings vs ints) are handled safely via `parse_util`.
- **Domain UseCases**: Verify explicit tests for `DataFailure(ApiErrorEntity)` and error handling/propagation.
- **Cubit / State Machines**: Verify emissions for `[LoadingState, ErrorState(message)]`, form validation guards that halt execution before calling usecases, and sequential call/debounce safety.
- **Paging (`ListViewPagingCubit`)**: Verify behavior when `total = 0` (empty state) and when reaching the last page.
- Run `flutter test test/modules/<feature>/` via `run_command`.
