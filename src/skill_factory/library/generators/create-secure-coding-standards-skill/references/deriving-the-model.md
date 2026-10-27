# Deriving the Workspace Security Model & Risk Taxonomy

Stack-neutral guide for discovering a workspace's real security architecture and mapping `SC1`–`SC14` onto concrete safe-vs-unsafe patterns and deterministic `rg` checks.

---

## 1. Security Model Discovery (For `01-input-auth-and-data-scope.md`)

Inspect the existing codebase, architecture documentation, and configuration before authoring the skill. Never invent a parallel authentication or authorization scheme.

| Dimension | What to Discover & Document |
|---|---|
| **Trust Boundaries (`SC1`, `SC5`)** | Every entry point where external data enters the process: network endpoints/handlers, UI forms, deep links/navigation URIs, webhooks, queue consumers, file imports, and external provider responses — along with the validator/schema boundary for each |
| **Authentication & Session Lifecycle (`SC7`)** | How identity is established, verified, refreshed, and terminated (token/session validation helper, single-flight refresh hook, and credential wipe on logout/expiry) |
| **Authorization Model (`SC2`)** | Roles, permissions/capabilities, where object-level guards execute (application/use-case layer), and the rule that UI visibility gates are UX only |
| **Data Scopes (`SC3`)** | Active isolation dimensions (tenant, owner/user, environment, release state), how the scope identifier travels from the authenticated context into queries/caches/storage keys, and what an unscoped leak looks like |
| **Fail-Closed Error Contract (`SC13`)** | How validation, auth, and upstream failures are denied without returning permissive defaults or fabricated fallback records |

---

## 2. Secrets, Sensitive Data & Cryptography Discovery (For `02-secrets-data-and-crypto.md`)

| Dimension | What to Discover & Document |
|---|---|
| **Secrets & Configuration (`SC6`)** | Typed configuration loader or compile-time injection mechanism, hardware-backed/encrypted credential store, `.gitignore` rules for environment files, and secret rotation policy |
| **Sensitive Data & PII Redaction (`SC8`)** | What constitutes sensitive data/PII in the domain, structured logger redaction rules, generic client-facing error envelopes, and UI masking/background screen protection |
| **Cryptographic Primitives (`SC12`)** | Vetted libraries used for password/secret hashing, authenticated encryption, constant-time comparison, and cryptographic random token generation |

---

## 3. Runtime Risk Taxonomy & `rg` Audit Patterns (For `03-runtime-risks-deps-and-review.md`)

Map each runtime risk category onto the workspace's **Unsafe Pattern** vs. **Safe Pattern** using real project helpers:

| Risk Category | Universal Unsafe Pattern | Universal Safe Pattern |
|---|---|---|
| **Query / Command Injection (`SC4`)** | Interpolating or concatenating input strings into queries, shell commands, or dynamic evaluation | Parameterized queries/bound parameters; argument arrays without shell invocation; allow-listed sort/filter identifiers |
| **Path Traversal & File Handling (`SC4`, `SC10`)** | Joining user-supplied filenames directly into filesystem paths; unbounded file reads into memory | Enforcing byte-size caps, content-type sniffing, generated filenames, and canonical path containment checks |
| **Output & Navigation Injection (`SC5`)** | Rendering raw untrusted markup or navigating/redirecting to unvalidated external URIs | Context-aware auto-escaping or explicit sanitization; strict route/domain allow-listing for redirects and deep links |
| **Transport & Outbound Calls (`SC9`)** | Disabling TLS certificate verification; calling user-supplied URLs without host/IP checks or timeouts | Enforcing verified HTTPS/TLS, outbound host + global-IP allow-lists (SSRF guard), explicit timeouts, and disabled redirects |
| **Supply-Chain Dependencies (`SC11`)** | Unpinned dependency ranges, unreviewed native/runtime permissions, or un-audited advisory alerts | Locked dependency versions, automated advisory audits, and permission review on every added package |

### Designing Deterministic `rg` Security Audits (`PASS` / `FAIL`)
In the generated skill's Gate table (`SKILL.md`) and `03-runtime-risks-deps-and-review.md`, define concrete `rg -n` commands tailored to the workspace's language that scan source files for:
1. Hardcoded credentials, API keys, or tokens (`SC6`).
2. Disabled TLS/certificate verification or cleartext `http://` endpoints (`SC9`).
3. String-interpolated queries, shell execution, or unsafe deserialization/eval (`SC4`).
4. Logging of tokens, passwords, or authorization headers (`SC8`).
5. Unencrypted storage of session tokens or sensitive credentials (`SC6`).
