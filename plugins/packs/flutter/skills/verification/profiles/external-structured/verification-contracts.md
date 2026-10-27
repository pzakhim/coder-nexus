# External-Structured Flutter Verification Contracts (`lib/core/`, `lib/shared/`)

> Topic: Verification rules for `external-structured` Flutter workspaces using project-internal `lib/core/` and `lib/shared/` foundations.

This reference is auto-injected when `.superpowers/setup.json` sets `"architecture_profile": "external-structured"`.

---

## 1. Pre-Verification Toolchain Gate (`G0`)

- Run `coder-nexus setup tools --pack flutter --check` (`PASS` when `TOOLS: READY`).
- **Never run `coder-nexus setup flutter --check`** and never require `../app-core`, `../app-util`, or `../app-ui-kit` in an `external-structured` workspace.

---

## 2. Verifying `Client Core Mapping` & Non-Fragmentation

During `G2` (`flutter analyze`), `G4` (architecture validators), `G5` (`flutter test`), and `G7` (`{{slot:visual-quality}}`), verify compliance with the `Client Core Mapping` table in `design.md`:

| Foundation Area | Verification Contract (`PASS` vs `FAIL`) |
|---|---|
| **Base Screen & Routing (`lib/core/`)** | • Verify that screens under `presentation/screens/*_screen.dart` use the project's established scaffold/base screen wrapper and route registration convention documented in `design.md`.<br>• Introducing a second competing base screen or router pattern is a `FAIL`. |
| **Network & Error Handling (`lib/core/network/`, `Result<T>` / `Either<L, R>`)** | • Verify that `RemoteDataSource` uses the project's shared HTTP client (`Dio` / `ApiClient`) and that repositories return the project's standard result wrapper (`Result<T>`, `Either<Failure, T>`, or `DataState<T>`).<br>• Zero fake `Mock*DataSource` classes inside `lib/`. |
| **Shared Design System (`lib/shared/` / `lib/commons/widgets/`)** | • Verify that all 4 visual states (`Loading`, `Content`, `Empty`, `Error`) reuse the project's shared loading, empty, error, button, and input widgets listed in `Client Core Mapping`.<br>• Inspect Golden (`G6`) and Runtime (`G7`) screenshots against the project's theme tokens (`ThemeData` / `ThemeExtension`). |
