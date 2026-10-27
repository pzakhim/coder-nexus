---
name: secure-coding-standards
description: Mobile and Flutter security standards (OWASP MASVS, boundary input and deep-link validation, token refresh and session isolation, hardware-backed secret storage, PII log redaction, TLS and WebView hardening, plugin vetting, deterministic PASS/FAIL gates, and BLOCKER/MAJOR/MINOR review grading).
---

# Secure Coding Standards — Flutter & Mobile

Use this skill when writing or reviewing Flutter code that handles user input, deep links, authentication, session tokens, local storage, network transport, WebViews, file handling, logging, or native plugin dependencies. Apply the active workspace profile (`architecture_profile` in `.superpowers/setup.json`).

---

## 1. Deterministic Security Gates (`PASS` / `FAIL`)

Run these checks on touched files before handoff (`READY_FOR_REVIEW`) and during Code Review. Each gate produces a binary **`PASS`** or **`FAIL`** status (`plugins/shared_contracts/flags_and_statuses.md` §1):

| Check | Command | Gate Status |
|---|---|---|
| **Static Analyzer** | `flutter analyze` | `PASS` / `FAIL` |
| **Hardcoded Secrets Audit (`rg`)** | `rg -n -i "(api_key|client_secret|password|bearer|private_key)\s*[:=]\s*['\"][A-Za-z0-9_\-]{8,}['\"]" lib/` (expect 0 matches) | `PASS` / `FAIL` |
| **TLS Certificate Bypass Audit (`rg`)** | `rg -n "badCertificateCallback\s*=\s*\(.*?\)\s*=>\s*true" lib/` (expect 0 matches) | `PASS` / `FAIL` |
| **Plaintext Token in `SharedPreferences` Audit (`rg`)** | `rg -n -i "SharedPreferences.*?(token|password|secret)|setString\(.+(access_token|refresh_token|password)" lib/` (expect 0 matches) | `PASS` / `FAIL` |
| **Sensitive Logging Audit (`rg`)** | `rg -n -i "(logger|log|print)\b.*?(access_token|refresh_token|password|client_secret|authorization)" lib/` (expect 0 matches) | `PASS` / `FAIL` |
| **Dependency & Outdated Advisory Check** | `flutter pub outdated` | `PASS` / `FAIL` |

---

## 2. Core Security Rules (`SC1`–`SC14` — Mandatory Compliance)

All 14 security rules are **mandatory compliance** when designing, writing, or modifying Flutter code (`SC1`, `SC2`, `SC3`, `SC4`, `SC6`, and `SC13` have zero exceptions). During Code Review, violations are graded on the unified 3-tier scale (`BLOCKER` / `MAJOR` / `MINOR` — see [03-runtime-risks-deps-and-review.md](references/03-runtime-risks-deps-and-review.md)):

| ID | Rule | Flutter / Dart Mobile Contract | Reference |
|---|---|---|---|
| **SC1** | **Validate Untrusted Input at the Boundary** | Validate all form inputs (required fields, format, length, numeric bounds), clipboard pastes, push payloads, and external JSON DTO responses (fail-fast on missing mandatory fields) before dispatching UseCases or state updates | [01 — Input, Auth & Data Scope](references/01-input-auth-and-data-scope.md) |
| **SC2** | **Respect Server Authorization as SSOT** | Treat UI visibility/role checks as UX only, never as a security boundary; handle `401 Unauthorized` and `403 Forbidden` responses explicitly on every protected action | [01 — Input, Auth & Data Scope](references/01-input-auth-and-data-scope.md) |
| **SC3** | **Isolate User & Tenant Data Scopes** | Key local caches, offline databases, and downloaded files by the active user/tenant scope, and purge all user-scoped local state upon logout, account switch, or token refresh failure | [01 — Input, Auth & Data Scope](references/01-input-auth-and-data-scope.md) |
| **SC4** | **Prevent Local SQL, Path & Script Injection** | Use parameterized queries in local SQLite/Drift databases, sanitize local file names against path traversal, and never evaluate dynamic script strings from untrusted payloads | [03 — Runtime Risks, Deps & Review](references/03-runtime-risks-deps-and-review.md) |
| **SC5** | **Validate Deep Links & Sandbox WebViews** | Validate incoming deep-link routes against an approved route allow-list and parse query parameters safely; restrict WebViews to allow-listed HTTPS origins with local file access disabled | [01 — Input, Auth & Data Scope](references/01-input-auth-and-data-scope.md), [03 — Runtime Risks, Deps & Review](references/03-runtime-risks-deps-and-review.md) |
| **SC6** | **Protect Secrets & Store Credentials in Secure Storage** | Never hardcode API secrets or signing keys in Dart source or bundled assets; inject public build config via `--dart-define`; persist access/refresh tokens exclusively in hardware-backed secure storage (Keystore / Keychain), never in plaintext `SharedPreferences` | [02 — Secrets, Data & Crypto](references/02-secrets-data-and-crypto.md) |
| **SC7** | **Enforce Single-Flight Token Refresh & Session Wipe** | Centralize Bearer token attachment and serialized single-flight `401` token refresh in the network interceptor; on refresh failure, wipe stored credentials and route to login without retry loops | [01 — Input, Auth & Data Scope](references/01-input-auth-and-data-scope.md) |
| **SC8** | **Redact Sensitive Data & PII from Logs & UI** | Never log tokens, passwords, `Authorization` headers, or PII; obscure password/PIN inputs (`obscureText: true`), mask sensitive account identifiers in UI, and obscure app snapshots in the background task switcher | [02 — Secrets, Data & Crypto](references/02-secrets-data-and-crypto.md) |
| **SC9** | **Enforce HTTPS/TLS Without Certificate Bypasses** | Use HTTPS/WSS for all API and external traffic with explicit connect/receive timeouts; never ship `badCertificateCallback = (...) => true` in release/production code | [03 — Runtime Risks, Deps & Review](references/03-runtime-risks-deps-and-review.md) |
| **SC10** | **Handle Local Files & Uploads Defensively** | Enforce file size and MIME/extension checks before upload or local parsing; store sensitive local files in app-private directories rather than shared external storage | [03 — Runtime Risks, Deps & Review](references/03-runtime-risks-deps-and-review.md) |
| **SC11** | **Vet Third-Party Packages & Native Permissions** | Vet `pub.dev` publisher status, maintenance activity, and native `AndroidManifest.xml` / `Info.plist` permissions before adding dependencies; keep `pubspec.lock` committed | [03 — Runtime Risks, Deps & Review](references/03-runtime-risks-deps-and-review.md) |
| **SC12** | **Use Vetted Cryptography & `Random.secure()`** | Use `Random.secure()` for cryptographic nonces, PKCE verifiers, and state tokens (never `Random()`); rely on platform Keystore/Keychain and vetted crypto packages | [02 — Secrets, Data & Crypto](references/02-secrets-data-and-crypto.md) |
| **SC13** | **Fail Closed on Auth, Parse & Network Errors** | When token refresh, deep-link validation, or mandatory DTO field parsing fails, deny navigation/execution and emit a typed failure state—never substitute fabricated fallback data | [01 — Input, Auth & Data Scope](references/01-input-auth-and-data-scope.md), [03 — Runtime Risks, Deps & Review](references/03-runtime-risks-deps-and-review.md) |
| **SC14** | **Flag Security-Sensitive Changes in Handoff** | List every change touching auth, secure storage, deep links, TLS/network config, WebViews, or native plugins in the Code Writer handoff (`work-item-contract`) | [03 — Runtime Risks, Deps & Review](references/03-runtime-risks-deps-and-review.md) |

---

## 3. Reference Guides

Load only the reference file needed for the current task:

| Reference | Topics Covered |
|---|---|
| [01 — Input, Deep Links, Auth & Session Scope](references/01-input-auth-and-data-scope.md) | Form input validation & obscuring (`SC1`), deep-link route allow-listing (`SC5`), fail-fast DTO parsing (`SC1`, `SC13`), single-flight `401` token refresh (`SC7`), server authorization (`SC2`), and user/tenant local cache isolation (`SC3`) |
| [02 — Secrets, Secure Storage, PII & Cryptography](references/02-secrets-data-and-crypto.md) | Zero hardcoded secrets & `--dart-define` (`SC6`), Keystore/Keychain secure storage vs. `SharedPreferences` (`SC6`), log/error redaction & UI/task-switcher masking (`SC8`), and `Random.secure()` (`SC12`) |
| [03 — Transport, WebViews, Dependencies & Review Rubric](references/03-runtime-risks-deps-and-review.md) | HTTPS/TLS & certificate validation (`SC9`), WebView sandboxing (`SC5`), local SQL/file safety (`SC4`, `SC10`), native plugin vetting (`SC11`), `rg` audit gates, `SC14` triggers, and `BLOCKER` / `MAJOR` / `MINOR` review rubric |
<!-- {{profile_references}} -->
