---
skills:
  - {{slot:core-package-usage}}
---
## Flutter rules

Read the approved profile through `{{slot:core-package-usage}}`. Company examples in the test audit (`parse_util`, `DataFailure`, `ListViewPagingCubit`) apply only when that API is actually used. External profiles test their own result/state/paging contracts and required failure paths.

### Flutter Checks
- **Profile checks**: apply the Code Reviewer checks of `{{slot:core-package-usage}}` for the `architecture_profile.mode` in `design.md`; under `imespro` also every package's `guidance/GUIDE.md` review checklist, and any failure is **automatic `CHANGES_REQUESTED` (FAIL)**. Under `external-structured`, also check error/state and DI conventions against the `Client Core Mapping`; `external-standard` requires no company classes.
- **Validators**: pass the approved mode (from design, brief for phase-free work, or the debug `brief.md` → `## 7` → **Architecture profile** line for a bug) as `architecture_profile` to `validate_architecture_code` on every changed Dart file, and to `validate_module_architecture` for an affected complete module. Never omit it: an omitted argument runs legacy iMESPro checks. For scoped UI-only work, record module structure `N/A` with reason and inspect affected imports, state ownership and integration directly.
- Independently classify changed destinations and verify the approved profile's screen naming, superclass, applicable lifecycle hooks, route/DI and owned resources. Only iMESPro requires `screens/*_screen.dart`, `*Screen` and BaseScreen hooks; external-structured follows Client conventions and external-standard permits standard Flutter widgets. Exempt dialogs, sheets and child widgets.
- **Data sources** (`PHASE-01+`): `lib/` implements only the real `RemoteDataSource` (`ApiService`); a `Mock<Feature>DataSource` or `FakeRepository` class is a finding under the frontend rules above.

### Flutter Unit Test Audit (`PHASE-01+`)
- Inspect unit test files under `test/modules/<feature>/..._test.dart` for **Happy-Path Bias**.
- Detect shallow or trivial assertions (e.g. `expect(result, isNotNull)` without verifying internal data properties).
- **Data Models (`fromJson`)**: Probe whether optional keys can be omitted or null, empty arrays `[]` don't crash, and type variations (numeric strings vs ints) are handled safely via `parse_util`.
- **Domain UseCases**: Verify explicit tests for `DataFailure(ApiErrorEntity)` and error handling/propagation.
- **Cubit / State Machines**: Verify emissions for `[LoadingState, ErrorState(message)]`, form validation guards that halt execution before calling usecases, and sequential call/debounce safety.
- **Paging (`ListViewPagingCubit`)**: Verify behavior when `total = 0` (empty state) and when reaching the last page.
- Run `flutter test test/modules/<feature>/` via `run_command`.
