# 02 — Secrets, Secure Storage, PII Protection & Cryptography

> Scope: Compile-time configuration & secret exclusion (`SC6`), hardware-backed secure storage (`SC6`), PII/log/UI redaction (`SC8`), and cryptographic randomness (`SC12`).

---

## 1. Zero Hardcoded Secrets & Compile-Time Config (`SC6`)

1. **Never embed server secrets in the client:** Keep private API keys, cloud credentials, DB passwords, and JWT signing secrets out of Dart source, `assets/`, and mobile build configs.
2. **Use `--dart-define` / `--dart-define-from-file`** for public flavor config (e.g., `API_BASE_URL`).
3. **Keep `.env` untracked in Git** (`AGENTS.md` §5) and immediately rotate any accidentally exposed token or credential.

---

## 2. Hardware-Backed Secure Local Storage (`SC6`)

| Data Type | Allowed Storage | Forbidden Storage (`BLOCKER`) |
|---|---|---|
| **Access/refresh tokens, PIN/biometric secrets, encryption keys** | Hardware-backed secure storage (Android Keystore / EncryptedSharedPreferences · iOS Keychain via active workspace secure storage service or `flutter_secure_storage`) | Plaintext `SharedPreferences`, `UserDefaults`, unencrypted SQLite/Hive boxes, or world-readable files |
| **Non-sensitive UI preferences** (theme, locale, onboarding flag) | Standard `SharedPreferences` | — |

---

## 3. Sensitive Data, Log Redaction & UI Privacy (`SC8`)

1. **Zero credentials or PII in logs:** Never log `access_token`, `refresh_token`, `password`, `Authorization` headers, or unmasked PII; redact sensitive headers/body fields in HTTP logging interceptors.
2. **UI masking:** Mask sensitive account numbers, phone numbers, or national IDs unless full display is explicitly approved.
3. **Background task-switcher obscuring:** Obscure app snapshots on `AppLifecycleState.inactive` / `paused` for screens displaying financial, auth, or confidential operational data.

---

## 4. Vetted Cryptography & Secure Randomness (`SC12`)

- Use `Random.secure()` (`dart:math`) for nonces, PKCE verifiers, state parameters, or keys — never `Random()`.
- Rely on platform Keystore/Keychain APIs and vetted Dart/native crypto packages; never invent custom encryption or hashing.
