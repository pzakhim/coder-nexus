## Flutter rules

Read the approved `architecture_profile` from `design.md` (and `.superpowers/setup.json`) and apply the profile contracts in `{{slot:code-review}}`, `{{slot:clean-architecture}}`, `{{slot:unit-testing}}`, `{{slot:visual-quality}}`, and `{{slot:ui-kit-mapping}}`. Also check `.agents/skills/` for workspace overrides including `visual-quality` and `ui-kit-mapping`. Company examples in the test audit (`parse_util`, `DataFailure`, `ListViewPagingCubit`) apply only when that API is actually used; external profiles test their own result/state/paging contracts and required failure paths.

### Flutter Checks
- **Profile checks**: Apply the profile review contract in `{{slot:code-review}}` for `architecture_profile.mode` in `design.md`; under `imespro` also every package's `guidance/GUIDE.md` review checklist — any failure is **automatic `CHANGES_REQUESTED` (`BLOCKER`)**. Under `external-structured`, check error/state and DI conventions against `Client Core Mapping`; `external-standard` requires no company classes.
- **MCP Validators**: Invoke `validate_architecture_code` (every changed Dart file) and `validate_module_architecture` (affected complete module) directly, passing the approved `architecture_profile` (from `design.md`, `brief.md`, or debug `brief.md` → `## 7`). Never omit `architecture_profile` (an omitted argument runs legacy iMESPro checks). For scoped UI-only work, record module structure `N/A` with reason and inspect imports, state ownership, and integration directly.
- Independently classify changed destinations and verify the approved profile's screen naming, superclass, lifecycle hooks, route/DI, and owned resources. Only iMESPro requires `screens/*_screen.dart`, `*Screen`, and `BaseScreen` hooks; exempt dialogs, sheets, and child widgets.
- **Data sources** (`PHASE-01+`): `lib/` implements only the real `RemoteDataSource` (`ApiService`); a `Mock<Feature>DataSource` or `FakeRepository` class is a finding under the frontend rules above.

### Flutter Visual Verification (Mandatory on UI Phases & `[REVIEW_CHECKPOINT]`)
1. **Verify `Visual Artifacts:` in `writer-handoff.md`**: Confirm revision-bound 4-state `.png`s (`Loading`, `Content`, `Empty`, `Error`) exist under `vN/evidence/<phase-id>/<REVIEW_REVISION>/visual/`.
2. **Re-run Golden Tests (when configured)**: Execute `flutter test <golden_test_path>` strictly **without `--update-goldens`** (`--update-goldens` during review is forbidden).
3. **Side-by-Side Multimodal `read_file` Comparison**: Load captured 4-state `.png`s and reference `.png`s — Figma (`.superpowers/sources/<ISSUE-ID>/figma/<stem>-SNN.png`, `tokens.json`, `<stem>.spec.json`) **OR** HTML sitemap (`.superpowers/sources/<ISSUE-ID>/sitemap/screens/<id>_<code>.png`, `sitemap/*.spec.json`) — in parallel via multimodal **`read_file`** (`{{slot:visual-quality}}`).
4. **Audit `## UI/UX mapping` (`{{slot:ui-kit-mapping}}`)**: Verify mapped `app_ui_kit` / Client widgets, design tokens, and `C-NN` / `Core gap` records match `design.md` with zero unauthorized raw Material replacements.
5. **Record `## Visual Comparison`**: Log per-screen/per-state grades (`PASS`/`FAIL`/`BLOCKED`/`NOT_RUN`) and `BLOCKER`/`MAJOR`/`MINOR` findings in `## Visual Comparison` of the review report.

### Flutter Unit Test Audit (`PHASE-01+`)
- Inspect `test/modules/<feature>/..._test.dart` for **Happy-Path Bias** and shallow assertions (e.g. `expect(result, isNotNull)` without checking internal properties).
- **Data Models (`fromJson`)**: Probe omitted/null optional keys, empty arrays `[]`, and safe type variations via `parse_util`.
- **Domain UseCases**: Verify explicit `DataFailure(ApiErrorEntity)` and error propagation tests.
- **Cubit / State Machines**: Verify `[LoadingState, ErrorState(message)]`, form validation guards halting before usecases, and sequential/debounce safety.
- **Paging (`ListViewPagingCubit`)**: Verify `total = 0` (empty) and last-page behavior.
- Run `flutter analyze`, `dart run dart_code_linter:metrics analyze lib` *(when configured)*, and `flutter test test/modules/<feature>/` via `run_command`.
