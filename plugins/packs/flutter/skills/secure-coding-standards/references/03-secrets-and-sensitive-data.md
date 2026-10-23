# 03 - Secrets and Sensitive Data Protection

Mobile application binaries (APKs/IPAs) can be unpacked, decompiled, and analyzed. Never store plaintext secrets or raw tokens in the code repository or unencrypted storage.

## 1. Zero Hardcoded Credentials

- **Prohibited:**
  - Hardcoded API secret keys, AWS/cloud credentials, database passwords, or JWT signing keys in Dart source files or JSON fixtures.
  - Committing `.env` files with production keys to Git repositories.
- **Enforcement:**
  - Inject compile-time environment keys using `--dart-define` flags or native build flavor configurations:
    ```bash
    flutter build apk --dart-define=API_BASE_URL=https://api.example.com --dart-define=CLIENT_SECRET=xxx
    ```
  - Read configuration values through `FlavorConfig` or `ApiConfig` in `app_util`.

## 2. Secure Local Storage

- **Forbidden:**
  - Storing user access tokens, refresh tokens, passwords, or sensitive biometric flags in unencrypted Android `SharedPreferences` or iOS `UserDefaults`.
- **Approved Storage:**
  - Persist credentials using `LocalStorageService` with hardware-backed encryption or `flutter_secure_storage` (Android Keystore / iOS Keychain).
  - Clear sensitive tokens immediately on logout or account termination.

## 3. PII & Log Protection

- Never write sensitive Personally Identifiable Information (PII), payment card details, passwords, or auth tokens to `AppLogger.I` or system console output.
- Mask account numbers, emails, and phone numbers in UI presentations where full details are not required.
