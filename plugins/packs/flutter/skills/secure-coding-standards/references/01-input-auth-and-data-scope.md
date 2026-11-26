# 01 — Input Validation, Deep Links, Authentication & Session Scope

> Scope: Untrusted mobile input & deep-link validation (`SC1`, `SC5`), single-flight token refresh (`SC7`), server-authoritative permissions (`SC2`), user/tenant local data isolation (`SC3`), and fail-closed error handling (`SC13`).

---

## 1. Trust Boundaries & Input Validation (`SC1`, `SC5`)

Validate all data crossing mobile trust boundaries before dispatching UseCases or navigating:

| Boundary | Entry Surface | Mandatory Validation Contract |
|---|---|---|
| **User Form Inputs** | Form fields, search bars, clipboard paste | Trim whitespace; validate required fields, email/phone format, length caps, and numeric bounds before calling Cubit/UseCase actions |
| **Sensitive Text Inputs** | Password, PIN, OTP, secret token fields | Set `obscureText: true`, `enableSuggestions: false`, `autocorrect: false` |
| **Deep Links & Push Intents** | App links, custom URI schemes, push payloads | Validate `uri.path` against an explicit route allow-list and parse/validate typed query parameters (`int.tryParse`, bounds) before pushing any route; reject unknown routes silently |
| **External API Responses** | `data/models/*_model.dart` (`fromJson`) | Parse using type-safe helpers and validate mandatory fields explicitly; fail fast on missing/malformed required fields (`SC13`) |

---

## 2. Authentication & Single-Flight Token Refresh (`SC7`)

1. **Centralized Bearer attachment:** Attach access tokens exclusively through the configured HTTP client's auth interceptor—never construct `Authorization` headers ad-hoc inside feature DataSources.
2. **Serialized single-flight `401` refresh:**
   - When an API call returns `401 Unauthorized`, lock/queue concurrent requests and execute the refresh handshake **once**.
   - On refresh success, persist the new token pair in secure storage and replay queued requests.
   - On refresh failure, **immediately wipe all stored credentials and user-scoped caches**, reset session state, and redirect to login without retry loops.

---

## 3. Server Authorization (`SC2`), Local Scope Isolation (`SC3`) & Fail-Closed (`SC13`)

1. **UI gating is UX only (`SC2`):** Hiding or disabling controls by role is UX only; handle `401` and `403` responses explicitly in every protected Cubit/Repository action.
2. **User & tenant local scope isolation (`SC3`):** Partition local caches, offline databases, and downloaded files by `userId` / `tenantId`. On logout, account switch, or `401` refresh failure, purge all user/tenant-scoped local storage and in-memory state.
3. **Fail closed (`SC13`):** Never catch an auth, network, or DTO parsing error and return fabricated success/empty (`[]`) data.
