## Flutter rules

- **Source and test folders**: `lib/` and `test/`.
- **FE Data Pipeline owned by `planning`**: `RemoteDataSource` calling `ApiService` / HTTP client, `Model.fromJson`, `Repository`, `UseCase`, DI.
- **Detection signature**: `pubspec.yaml` and `lib/*.dart` $\implies$ Target Platform: `mobile` (App), Framework: `flutter` (Planning resolves the exact `architecture_profile` and UI Kit widget mapping via `{{slot:architecture-design}}` at Gate 2).
- **Verified baseline facts** include `pubspec.yaml`, route tables, and workspace foundation exports.
- **UI Kit boundary**: `planning` owns `architecture_profile` resolution (`.superpowers/setup.json` & `{{slot:architecture-design}}`), exact `app_ui_kit` / Client widget mapping, `BaseScreen`, `Router`, and `Cubit State` contracts in `design.md` (Gate 2).
