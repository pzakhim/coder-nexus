# iMESPro Security & Foundation Contracts

> Topic: Mandatory iMESPro security APIs (`AppFormField` password obscuring, `app_util` safe parsers, `ApiService` HTTPS & single-flight token refresh, `LocalStorageService`, and `AppLogger.I` redaction).

---

## 1. Mandatory `imespro` Security Component Mapping

When working under the `imespro` profile (`app_core`, `app_util`, `app_ui_kit`), enforce `SC1`–`SC14` through the verified company foundation APIs:

| Security Area | Mandatory `imespro` API & Contract |
|---|---|
| **Form Input & Password Obscuring (`SC1`, `SC8`)** | • Use `AppFormField` from `app_ui_kit` and always provide a `validator` when `isRequired: true`.<br>• For password, PIN, or secret fields, set `fieldType: AppFormFieldType.password` and `obscureText: true` (with `onObscureToggle` when user reveal is required). |
| **Safe DTO Parsing (`SC1`, `SC13`)** | • Use `app_util` safe parsers (`parseString`, `parseInt`, `parseDouble`, `parseBool`, `parseList`) inside `data/models/*_model.dart` (`fromJson`) and validate mandatory fields explicitly without fabricating fallback records. |
| **Deep-Link Route Validation (`SC5`)** | • Validate incoming deep-link paths against `AppRoute.isValidRoute(path)` and parse query parameters via `app_util` safe parsers before navigating; log rejected routes via `AppLogger.I.w(...)`. |
| **HTTPS Transport & Token Refresh (`SC7`, `SC9`)** | • Route all HTTP traffic through `ApiService` (`app_util`) with `isHttps: true` (never override `isHttps: false` in production).<br>• Supply access tokens via `generateAccessToken()`, handle single-flight `401` refresh via `refreshToken`, and on `onRefreshTokenFail` clear `LocalStorageService` credentials, reset user state, and navigate to login. |
| **Encrypted Credential Storage (`SC6`)** | • Read build flavor endpoints/config through `FlavorConfig` / `ApiConfig` (`app_util`) populated via `--dart-define`.<br>• Persist tokens and sensitive user credentials exclusively via encrypted `LocalStorageService` — never raw `SharedPreferences`. |
| **Log Redaction & Error Dialogs (`SC2`, `SC8`)** | • Never pass tokens, passwords, or raw PII to `AppLogger.I`.<br>• Surface `401` / `403` authorization errors using `AppDialog.show(..., dialogType: DialogType.error)`. |
