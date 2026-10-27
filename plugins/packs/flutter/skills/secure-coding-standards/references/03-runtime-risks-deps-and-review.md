# 03 — Transport Security, WebViews, Dependencies & Review Rubric

> Scope: HTTPS/TLS enforcement (`SC9`), WebView & local file safety (`SC4`, `SC5`, `SC10`), third-party plugin vetting (`SC11`), deterministic `rg` audits, handoff triggers (`SC14`), and the `BLOCKER` / `MAJOR` / `MINOR` review rubric.

---

## 1. Mobile & Flutter Risk Matrix — Unsafe vs. Safe (`SC4`, `SC5`, `SC9`, `SC10`)

| Risk Area | Unsafe Pattern (Forbidden) | Safe Flutter Pattern | Rule |
|---|---|---|---|
| **Transport & TLS** | Cleartext `http://` endpoints; `badCertificateCallback = (cert, host, port) => true` | Enforce `https://` / `wss://` with default OS TLS certificate validation and explicit timeouts | `SC9` |
| **Deep Links** | `Navigator.pushNamed(context, uri.path)` on raw incoming URI | Validate `uri.path` against an explicit route allow-list and parse/validate parameters | `SC5` |
| **WebViews** | Loading arbitrary URLs; `JavaScriptMode.unrestricted` on untrusted pages; `allowFileAccess: true` | Restrict navigation via `NavigationDelegate` to allow-listed HTTPS domains; disable file access (`allowFileAccess: false`) | `SC5`, `SC10` |
| **Local SQL / Files** | String-interpolated SQL (`rawQuery("... '$input'")`); joining raw filenames into paths | Parameterized queries (`where: 'id = ?', whereArgs: [id]`); store files in app-private directory with sanitized/UUID filenames | `SC4`, `SC10` |
| **Token Storage** | Saving `access_token` / `refresh_token` in `SharedPreferences` | Hardware-backed Keystore / Keychain secure storage ([02](02-secrets-data-and-crypto.md#2-hardware-backed-secure-local-storage-sc6)) | `SC6` |

### Transport & TLS Example (`SC9`)
```dart
// Unsafe: disables TLS certificate verification, enabling MitM interception
client.badCertificateCallback = (X509Certificate cert, String host, int port) => true;

// Safe: keep default OS certificate validation and enforce explicit timeouts
final dio = Dio(
  BaseOptions(
    baseUrl: apiConfig.httpsBaseUrl, // Must start with https://
    connectTimeout: const Duration(seconds: 15),
    receiveTimeout: const Duration(seconds: 15),
  ),
);
```

---

## 2. Third-Party Plugin & Permission Vetting (`SC11`)

Native Flutter plugins execute with full application privileges on Android and iOS. Before adding or upgrading a package in `pubspec.yaml`:
1. **Approval gate:** Request approval before modifying dependencies (`AGENTS.md` §4).
2. **Publisher & maintenance check:** Verify `pub.dev` verified publisher status, recent maintenance, and Dart/Flutter SDK compatibility (`flutter pub outdated`).
3. **Native permission audit:** Inspect `android/app/src/main/AndroidManifest.xml` and `ios/Runner/Info.plist` for permissions required by the plugin. Reject plugins that request excessive permissions (e.g., background location, contacts, microphone, external storage) beyond the approved feature scope.

---

## 3. Handoff Triggers (`SC14`) & Review Severity Rubric (`BLOCKER` / `MAJOR` / `MINOR`)

### Handoff Triggers (`SC14`)
In the Code Writer handoff (`work-item-contract`), flag every touched area below together with its protecting guard:
- [ ] Login, logout, biometric auth, or `401` token refresh lifecycle (`SC7`)
- [ ] Reading/writing credentials or sensitive user data in local storage (`SC3`, `SC6`)
- [ ] Deep-link routing, push notification navigation, or external URI launches (`SC5`)
- [ ] HTTP client, TLS certificate handling, or base URL configuration (`SC9`)
- [ ] WebViews, file uploads/downloads, or `pubspec.yaml` / `AndroidManifest.xml` / `Info.plist` changes (`SC5`, `SC10`, `SC11`)

### Unified Review Severity Rubric (`BLOCKER` / `MAJOR` / `MINOR`)

Grade all security findings on the unified scale from `plugins/shared_contracts/flags_and_statuses.md` §3 (never use `P1`/`P2`/`P3`):

| Severity | Security Triggers |
|---|---|
| **`BLOCKER`** | • Hardcoded API keys, secrets, or credentials in Dart source, tests, or bundled assets (`SC6`)<br>• Storing access/refresh tokens or passwords in plaintext `SharedPreferences` (`SC6`)<br>• `badCertificateCallback = (...) => true` or cleartext `http://` production transport (`SC9`)<br>• Unvalidated deep-link route navigation or local SQL/path injection (`SC4`, `SC5`)<br>• Missing credential/cache wipe on logout or `401` token refresh failure (`SC3`, `SC7`)<br>• Fail-open error handling that returns fabricated success data on auth/parse failure (`SC13`) |
| **`MAJOR`** | • Sensitive tokens, passwords, or unmasked PII written to logs (`SC8`)<br>• Missing `obscureText: true` on password/PIN fields or missing required form input validation (`SC1`, `SC8`)<br>• WebView without domain allow-listing or with `allowFileAccess: true` (`SC5`, `SC10`)<br>• Unapproved or unvetted native plugin / permission addition (`SC11`) |
| **`MINOR`** | • Defense-in-depth hardening or missing `SC14` handoff trigger note when runtime guards are verified |
