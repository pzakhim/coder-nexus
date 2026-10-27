# 02 — Secrets, Secure Storage, PII Protection & Cryptography

> Scope: Compile-time configuration & secret exclusion (`SC6`), hardware-backed secure storage (`SC6`), PII/log/UI redaction (`SC8`), and cryptographic randomness (`SC12`).

---

## 1. Zero Hardcoded Secrets & Compile-Time Config (`SC6`)

Mobile binaries (`.apk`, `.aab`, `.ipa`) can be decompiled and inspected by any end user:
1. **Never embed server secrets in the client:** Private API secret keys, cloud provider credentials, database passwords, or JWT signing secrets must never exist in Dart source files, `assets/`, or mobile build configs.
2. **Use `--dart-define` for public flavor configuration:** Inject environment-specific base URLs and public client identifiers at build time via `--dart-define` or `--dart-define-from-file`:
   ```bash
   flutter build apk --dart-define=API_BASE_URL=https://api.example.com
   ```
3. **Git-ignore local environment files:** Ensure `.env` files containing local developer credentials remain untracked in Git (`AGENTS.md` §5).
4. **Rotate on exposure:** Any credential or token accidentally committed or pasted into logs/tickets must be revoked and rotated immediately.

---

## 2. Hardware-Backed Secure Local Storage (`SC6`)

| Data Type | Allowed Storage | Forbidden Storage (`BLOCKER`) |
|---|---|---|
| **Access tokens, refresh tokens, PIN/biometric secrets, encryption keys** | Hardware-backed secure storage (Android Keystore / EncryptedSharedPreferences · iOS Keychain via the active workspace secure storage service or `flutter_secure_storage`) | Plaintext `SharedPreferences`, `UserDefaults`, unencrypted SQLite/Hive boxes, or world-readable files |
| **Non-sensitive UI preferences** (theme mode, locale, onboarding seen flag) | Standard `SharedPreferences` | — |

```dart
// Unsafe: storing bearer tokens in plaintext SharedPreferences
final prefs = await SharedPreferences.getInstance();
await prefs.setString('access_token', token); // Stored in cleartext XML/plist!

// Safe: storing bearer tokens in hardware-backed secure storage
await secureStorage.write(key: 'access_token', value: token);
```

---

## 3. Sensitive Data, Log Redaction & UI Privacy (`SC8`)

1. **Zero credentials or PII in logs:**
   - Never pass `access_token`, `refresh_token`, `password`, `Authorization` headers, or unmasked PII (national IDs, phone numbers, emails, payment data) to the application logger or `print()` / `debugPrint()`.
   - Redact sensitive headers and body fields in HTTP logging interceptors.
2. **UI masking:** Mask sensitive account numbers, phone numbers, or national IDs in list/detail views unless full display is explicitly required by the approved screen contract.
3. **Background task-switcher obscuring:** For screens displaying sensitive financial, authentication, or confidential operational data, obscure the application snapshot when the app transitions to `AppLifecycleState.inactive` / `paused` so OS task switchers do not capture sensitive content.

---

## 4. Vetted Cryptography & Secure Randomness (`SC12`)

- **Cryptographic randomness:** Always use `Random.secure()` from `dart:math` when generating nonces, PKCE code verifiers, state parameters, or local keys — never use `Random()`.
- **Vetted libraries:** Rely on platform Keystore/Keychain APIs and vetted Dart/native cryptographic packages; never implement custom encryption or hashing algorithms.
