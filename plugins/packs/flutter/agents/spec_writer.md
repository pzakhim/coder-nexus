---
skills:
  - {{slot:core-usage}}
---
## Flutter rules

- **FE Data Pipeline owned by `planning`**: `RemoteDataSource` calling `ApiService`, `Model.fromJson`, `Repository`, `UseCase`, DI.
- **Detection signature**: `pubspec.yaml` and `lib/*.dart` $\implies$ Target Platform: `mobile` (App), Framework: `flutter` (Planning resolves the exact `{{slot:core-usage}}` profile and UI Kit widget mapping at Gate 2).
- **Verified baseline facts** include `pubspec.yaml`, route tables, and `{{slot:core-usage}}` package exports.
- **UI Kit boundary**: `planning` owns `{{slot:core-usage}}` profile resolution, exact `app_ui_kit` / Client widget mapping, `BaseScreen`, `Router`, and `Cubit State` contracts in `design.md` (Gate 2).
