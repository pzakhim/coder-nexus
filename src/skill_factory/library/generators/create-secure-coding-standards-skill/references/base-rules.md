# Base Security Rules (`SC1`–`SC14` — Universal, Stack-Agnostic)

Secure-by-default rules applied while writing and reviewing code across any language, runtime, or architecture. Every rule (`SC1`–`SC14`) is **mandatory compliance** when authoring code (no per-rule `P1`/`P2`/`P3` severity column).

---

## 1. Core Security Rules (`SC1`–`SC14` — Mandatory Compliance)

| ID | Principle | Mandatory Contract | Why It Matters | Target Reference |
|---|---|---|---|---|
| **SC1** | **Validate Untrusted Input at the Boundary** | Validate schema, types, allow-lists, lengths, numeric bounds, and collection sizes at every external entry point; forbid unknown fields and server-owned fields in client inputs; reject invalid input rather than guessing or repairing | Every injection, overflow, and mass-assignment exploit starts with unchecked input | `SKILL`, `01` |
| **SC2** | **Authorize Every Operation per Object** | Enforce object-level and capability-level authorization in the authoritative business layer (deny by default); UI hiding or client-side checks are UX only, never security boundaries | Broken object-level access control is the most frequent and damaging application vulnerability | `SKILL`, `01` |
| **SC3** | **Isolate Data Scopes Explicitly** | Pass and enforce the active data scope (tenant, owner/user, environment, release state) on every query, mutation, local cache key, file path, background job, and event; never rely on an implicit global default scope | A single unscoped query or cache key leaks another user's or tenant's data | `SKILL`, `01` |
| **SC4** | **Prevent Injection Across All Interpreters** | Use parameterized queries/bound statements, argument arrays without shell invocation, resolved path containment checks, and safe schema-validated parsers; never concatenate untrusted input into queries, commands, paths, or dynamic code execution | Injection turns untrusted data into executable instructions | `SKILL`, `03` |
| **SC5** | **Encode Output & Validate Redirects/Navigation** | Rely on context-aware auto-escaping or an explicit sanitizer for untrusted markup; validate redirect URLs and deep-link route targets against an explicit allow-list | Unescaped output and unchecked redirects enable script injection and phishing | `SKILL`, `01`, `03` |
| **SC6** | **Keep Secrets Out of Source, Bundles & Logs** | Load credentials and keys exclusively from typed environment/secret stores or hardware-backed secure storage; never hardcode secrets in source, assets, fixtures, migrations, or client bundles; rotate any exposed secret immediately | Leaked secrets in Git history, logs, or mobile/web binaries cannot be un-leaked | `SKILL`, `02` |
| **SC7** | **Use Verified Authentication & Session Lifecycles** | Use the workspace's vetted authentication flow, pinned token algorithms/claims, single-flight token refresh, and complete credential wipe on logout or refresh failure; never invent custom token formats or disable signature checks | Homemade authentication and stale session state lead directly to account takeover | `SKILL`, `01` |
| **SC8** | **Redact Sensitive Data & PII from Logs, Caches & Errors** | Log correlation/request IDs and non-sensitive operational context only; never log tokens, passwords, raw auth headers, or unmasked PII, and never expose stack traces or internal driver errors to end users | Logs, crash reports, and error responses have broader readership and longer retention than primary storage | `SKILL`, `02` |
| **SC9** | **Enforce Transport Security & Guard Outbound Calls** | Require verified TLS/HTTPS without certificate-validation bypasses in production; validate user-influenced URLs against host/IP allow-lists (SSRF protection), enforce explicit timeouts, and disable unsafe redirects | Cleartext transport, TLS bypasses, and unchecked URLs expose traffic and internal networks | `SKILL`, `03` |
| **SC10** | **Handle Files & External Payloads Defensively** | Enforce strict byte-size caps, content-type verification, generated storage filenames, and sandboxed/non-executable storage locations; fail explicitly on malformed files without fabricating fallback records | Unbounded or unsanitized file handling causes memory exhaustion, path traversal, and code execution | `SKILL`, `03` |
| **SC11** | **Vet Dependencies & Lock Supply Chain** | Add third-party packages only when justified; pin versions in the lockfile, audit for known advisories, and verify native/runtime permissions before adoption | Every third-party dependency executes with the application's privileges | `SKILL`, `03` |
| **SC12** | **Use Vetted Cryptography & Cryptographic Randomness** | Use standard, platform-vetted cryptographic primitives (e.g., adaptive password hashing, authenticated encryption, constant-time secret comparison, and CSPRNG for tokens/nonces); never use non-cryptographic PRNGs or obsolete hashes for security | Subtle cryptographic flaws are invisible in functional testing until exploited | `SKILL`, `02` |
| **SC13** | **Fail Closed on Security & Validation Errors** | When input validation, token verification, permission checks, or security dependencies fail, deny the operation and surface a typed error; never fall back to permissive defaults, empty success lists, or unauthenticated access | Attackers actively target error and exception paths to bypass guards | `SKILL`, `01`, `03` |
| **SC14** | **Flag Security-Sensitive Changes in Handoff** | Explicitly list any diff touching authentication, authorization guards, data scopes, secrets, cryptography, file/URL handling, TLS/CORS config, or dependencies in the Code Writer handoff for focused review | Reviewers catch subtle boundary bugs when security-relevant touchpoints are surfaced explicitly | `SKILL`, `03` |

> **Non-negotiable core:** `SC1`, `SC2`, `SC3`, `SC4`, `SC6`, and `SC13` apply to every workspace without exception (for single-tenant applications, `SC3` applies to user/owner and environment scopes).

---

## 2. Deterministic Gate & Review Severity Contract

1. **Deterministic Security Tool Gates (`PASS` / `FAIL`):**
   - Security linters, dependency vulnerability scanners, lockfile checks, and `rg` anti-pattern audits report strictly **`PASS`** or **`FAIL`** (or `NOT_RUN` with an explicit environment blocker reason—never `PASS` when unrun).
2. **Code Review Finding Severity (`BLOCKER` / `MAJOR` / `MINOR`):**
   - **`BLOCKER`:** Exploitable or direct violation of a core security boundary — missing auth/scope enforcement (`SC2`, `SC3`), injection vector (`SC4`), hardcoded secret or plaintext credential storage (`SC6`), TLS verification bypass (`SC9`), or fail-open exception handling (`SC13`).
   - **`MAJOR`:** Missing input bounds or unknown-field rejection (`SC1`), sensitive data/PII in logs or user error bodies (`SC8`), missing outbound timeout/redirect restriction (`SC9`), unbounded file read (`SC10`), or unvetted/unlocked dependency change (`SC11`).
   - **`MINOR`:** Defense-in-depth hardening or missing handoff trigger note (`SC14`) where the runtime guard itself is already in place.
