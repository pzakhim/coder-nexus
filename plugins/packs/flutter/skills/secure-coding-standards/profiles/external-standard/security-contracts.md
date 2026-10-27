# External-Standard Security Contracts

> Topic: Standard Flutter security patterns (`flutter_secure_storage`, `Dio` `QueuedInterceptorsWrapper`, `--dart-define-from-file`, and `Random.secure()`).

---

## 1. Standard Flutter Security Implementation (`external-standard`)

Under the `external-standard` profile, implement `SC1`–`SC14` directly with vetted ecosystem packages without custom framework wrappers:

| Security Need | Standard Flutter Pattern |
|---|---|
| **Credential Storage (`SC6`)** | Use `flutter_secure_storage` (`AndroidOptions(encryptedSharedPreferences: true)`, iOS Keychain accessibility `first_unlock_this_device`) for access/refresh tokens; use `--dart-define` / `--dart-define-from-file` for build-time config. |
| **Single-Flight Token Refresh (`SC7`)** | Use `Dio`'s `QueuedInterceptorsWrapper` so concurrent `401` responses wait for a single refresh call, and clear `flutter_secure_storage` + redirect to login if refresh fails. |
| **Input & Deep-Link Validation (`SC1`, `SC5`)** | Validate forms with `TextFormField.validator` (`obscureText: true`, `enableSuggestions: false`, `autocorrect: false` for passwords) and validate incoming deep links in the router's redirect/guard callback against an explicit route allow-list. |
| **Cryptographic Randomness (`SC12`)** | Use `Random.secure()` from `dart:math` for all nonces, PKCE verifiers, and state tokens. |
