# External-Structured Security Contracts

> Topic: Mapping mobile security rules (`SC1`–`SC14`) onto an existing structured Client's `lib/core/` auth interceptor, secure storage, router guard, and logger.

---

## 1. Client Core Security Mapping (`external-structured`)

Under the `external-structured` profile, the Client workspace provides its own security infrastructure under `lib/core/` or `lib/shared/`. Do not import `iMESPro` packages (`app_core`, `app_util`, `app_ui_kit`).

Inspect `design.md` (`## Client Core Mapping`) and verify the real Client source for each security boundary before writing code:

| Security Need | How to Resolve in `external-structured` |
|---|---|
| **Input & Deep-Link Validation (`SC1`, `SC5`)** | Reuse the Client's shared form validators and router route-guard (`AutoRouteGuard` or `GoRouter.redirect`) to reject unauthenticated or non-allow-listed deep links. |
| **Token Refresh & Session Wipe (`SC7`)** | Reuse the Client's existing HTTP auth/refresh interceptor (`QueuedInterceptorsWrapper` or equivalent in `lib/core/network/`) and invoke the Client's session-clear hook on refresh failure. |
| **Encrypted Credential Storage (`SC6`)** | Reuse the Client's secure storage wrapper in `lib/core/storage/` (backed by Keystore/Keychain) for tokens and secrets; never store credentials in plaintext `SharedPreferences`. |
| **Logging & Error Redaction (`SC8`)** | Use the Client's structured logger in `lib/core/` with token/header redaction enabled. |
