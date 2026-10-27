# iMESPro Flutter Verification Contracts (`app_core`, `app_util`, `app_ui_kit`)

> Topic: iMESPro verification gates (`coder-nexus setup flutter --check`), `BaseScreen` / `BaseScreenState` runtime & analyzer verification, `app_ui_kit` 4-state checks, and `Core usage` / `Core gap` audit.

This reference is auto-injected when `.superpowers/setup.json` sets `"architecture_profile": "imespro"`.

---

## 1. Mandatory iMESPro Setup Gate (`PHASE-00` & Pre-Verification)

Before running `G1`–`G8` on an `imespro` workspace, verify that the local sibling packages (`../app-core`, `../app-util`, `../app-ui-kit`) are resolved and clean:

```bash
coder-nexus setup flutter --check
coder-nexus setup tools --pack flutter --check
```

- **Gate Result**: Both commands must exit `0` (`STATUS: READY` and `TOOLS: READY` → `PASS`).
- If `coder-nexus setup flutter --check` fails, verification is immediately **`BLOCKED`** until the sibling packages (`../app-core`, `../app-util`, `../app-ui-kit`) are resolved.
- Never edit, copy, or vendor code from `../app-core`, `../app-util`, or `../app-ui-kit` into the Client repository.

---

## 2. Verifying iMESPro Screen, State & Data Foundations

During `G2` (`flutter analyze`), `G5` (`flutter test`), `G6` (Golden comparison), and `G7` (`{{slot:visual-quality}}`), verify compliance with the `Core usage` table in `design.md` and the package `GUIDE.md` contracts:

| Foundation Area | Verification Contract (`PASS` vs `FAIL` / `UNVERIFIED`) |
|---|---|
| **Screen Lifecycle (`BaseScreen` / `BaseScreenState`)** | • Every full-page screen (`presentation/screens/*_screen.dart`) must extend `BaseScreen` / `BaseScreenState` from `app_core` and override `buildView(BuildContext context)`.<br>• Verify with `flutter analyze` (`G2`) and runtime rendering (`G7`); a lexical check alone is `UNVERIFIED`.<br>• When the approved spec relies on inherited screen tracking or responsive layout (`isTablet` / portrait & landscape), collect observable tracking logs and portrait/landscape screenshot evidence on the target device.<br>• Child widgets and dialogs under `presentation/widgets/` must **not** extend `BaseScreen`. |
| **Paginated Lists (`ListViewPaging` / `ListViewPagingCubit`)** | • Paginated list screens must use `ListViewPaging` + `ListViewPagingCubit` from `app_core` rather than custom scroll listeners or manual page counters.<br>• Verify `Loading`, `Content`, `Empty` (`[]`), and `Error` (with retry) states in `G5` (`bloc_test`) and `G7` (`{{slot:visual-quality}}`). |
| **Domain & Data Pipeline (`UseCasePower`, `DataState<T>`, `BaseRemoteDataSource`, `DataMapper<Entity>`)** | • Verify `UseCasePower<Result, Params>`, `DataState<T>` (`DataSuccess` / `DataFailed`), `BaseRemoteDataSource` calling `ApiService` (`ApiConfig.domain`), and `DataMapper<Entity>` are used without raw `Dio` instances or fake `Mock*DataSource` classes in `lib/`.<br>• Verify DTO `fromJson` parsers use safe `parse*` helpers from `app_util`. |
| **UI Kit (`app_ui_kit`) & 4 Visual States** | • Verify that screens and widgets reuse approved `app_ui_kit` components (`AppButton`, `AppFormField`, `AppDialog`, `AppLoadingIndicator`, `AppNoData`) per `design.md` (`Core usage` table) and `../app-ui-kit/guidance/GUIDE.md`.<br>• Any custom widget in `lib/modules/<feature>/presentation/widgets/` that duplicates an existing `app_ui_kit` widget without an approved `Core gap` entry in `design.md` is a `FAIL` (`BLOCKER`). |
