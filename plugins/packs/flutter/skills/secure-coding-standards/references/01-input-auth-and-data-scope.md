# 01 — Input Validation, Deep Links, Authentication & Session Scope

> Scope: Untrusted mobile input & deep-link validation (`SC1`, `SC5`), single-flight token refresh (`SC7`), server-authoritative permissions (`SC2`), user/tenant local data isolation (`SC3`), and fail-closed error handling (`SC13`).

---

## 1. Trust Boundaries & Input Validation (`SC1`, `SC5`)

Mobile applications execute on an untrusted device. Validate all data crossing these boundaries before dispatching UseCases or navigating:

| Boundary | Entry Surface | Mandatory Validation Contract |
|---|---|---|
| **User Form Inputs** | Form fields, search bars, clipboard paste | Trim whitespace; validate required fields, email/phone format, string length caps, and numeric bounds before calling Cubit/UseCase actions |
| **Sensitive Text Inputs** | Password, PIN, OTP, secret token fields | Enable `obscureText: true`, disable autocorrect and system suggestions (`enableSuggestions: false`, `autocorrect: false`) |
| **Deep Links & Push Intents** | App links, custom URI schemes, push notification payloads | Validate `uri.path` against an explicit route allow-list and parse/validate query parameters before navigating |
| **External API Responses** | `data/models/*_model.dart` (`fromJson`) | Parse using type-safe helpers and validate mandatory fields explicitly; fail fast on missing/malformed required fields (`SC13`) |

### Deep-Link Validation Example (`SC5`)
```dart
// Unsafe: navigating directly to an unvalidated URI path and raw query parameter
void handleDeepLink(BuildContext context, Uri uri) {
  Navigator.pushNamed(context, uri.path, arguments: uri.queryParameters['id']);
}

// Safe: route allow-list check + typed parameter validation
void handleDeepLink(BuildContext context, Uri uri, Set<String> allowedRoutes) {
  final path = uri.path;
  if (!allowedRoutes.contains(path)) {
    return; // Reject unknown or external route target
  }
  final id = int.tryParse(uri.queryParameters['id'] ?? '');
  if (id == null || id <= 0) {
    return; // Reject malformed identifier
  }
  Navigator.pushNamed(context, path, arguments: id);
}
```

---

## 2. Authentication & Single-Flight Token Refresh (`SC7`)

1. **Centralized Bearer attachment:** Attach access tokens exclusively through the configured HTTP client's auth interceptor—never construct `Authorization` headers ad-hoc inside feature DataSources.
2. **Serialized single-flight `401` refresh:**
   - When an API call returns `401 Unauthorized`, lock/queue concurrent requests and execute the refresh handshake **once**.
   - On refresh success, persist the new token pair in secure storage and replay queued requests.
   - On refresh failure, **immediately wipe all stored credentials and user-scoped caches**, reset session state, and redirect to the login screen without infinite retry loops.

---

## 3. Server Authorization (`SC2`), Local Scope Isolation (`SC3`) & Fail-Closed (`SC13`)

1. **UI gating is UX only (`SC2`):** Hiding or disabling a button based on the user's role improves UX, but the server remains the Single Source of Truth. Every Cubit/Repository action must handle `401` and `403` responses gracefully and surface a clear user error state.
2. **User & tenant local scope isolation (`SC3`):**
   - Prefix or partition local caches, offline database tables, and downloaded documents by the active `userId` / `tenantId`.
   - On logout, account switch, or `401` refresh failure, purge all user/tenant-scoped local storage and in-memory state so the next user on the same device never sees stale data.
3. **Fail closed (`SC13`):**
   - Never catch a network, auth, or DTO parsing failure and return a fabricated `DataSuccess` / empty list `[]` that masks an authentication or permission error.
