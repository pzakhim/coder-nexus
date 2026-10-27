# Boundary Security Checks & Read-Only Verification Catalog

Use this catalog to populate `references/02-security-checks-and-cli-gates.md` (`SR5`–`SR10`). Organize checks by **architectural boundary** tailored to the target workspace's detected language and toolchain. Run CLI scanners **read-only** and only when installed in the workspace.

## 1. Entrypoint, Auth & Session Boundary (`SR3`, `SR10`)

| Look For | How to Verify (Read-Only Trace / `rg` Scan) |
|---|---|
| Missing authentication or role/scope guard on a new/modified endpoint, RPC handler, or stream | Trace route/handler declaration → auth dependency → application service guard call; cross-check every cell in the Authorization Matrix (`01`). |
| Unbounded input / missing strict DTO rejection (mass assignment) | Verify request schemas reject unknown fields and enforce explicit string/list/numeric bounds (`SR5`). |
| Weak token/ticket handling or missing signature verification | Verify JWT/webhook HMAC validation uses constant-time comparison, explicit algorithm allow-lists, and short-lived tickets for realtime/download URLs (`SR10`). |

## 2. Persistence, Query & Cache Boundary (`SR4`, `SR5`)

| Look For | How to Verify (Read-Only Trace / `rg` Scan) |
|---|---|
| Missing tenant/owner scope filter (`IDOR` / cross-tenant data leak) | Inspect every changed database query, repository method, cache key, search index query, and background job payload to confirm `tenant_id` / `owner_id` comes from the verified principal (`SR4`). |
| String-interpolated SQL, shell commands, or unsafe deserialization | Scan changed files with `rg` for raw query string interpolation, `shell=True`, `eval`, `exec`, `pickle`, unsafe `yaml.load`, or unescaped template rendering (`SR5`). |

## 3. Client & UI Boundary (`SR6`)

| Look For | How to Verify (Read-Only Trace / `rg` Scan) |
|---|---|
| Unescaped HTML/DOM injection (XSS) or unvalidated deep-link/redirect targets | Scan changed UI components and route handlers for raw HTML injection sinks and unvalidated redirect query parameters. |
| Plaintext token/secret storage or client-bundled server secrets | Inspect client storage adapters (ensure secure keychain/encrypted storage or `HttpOnly` cookies) and public environment variable prefixes. |
| UI-only authorization checks | Verify every conditional UI button/route is backed by a server-side `403`/`404` check in the Authorization Matrix (`01`). |

## 4. Outbound Network, Webhook & File Boundary (`SR8`)

| Look For | How to Verify (Read-Only Trace / `rg` Scan) |
|---|---|
| Server-Side Request Forgery (SSRF) & missing outbound timeouts | Check every HTTP client call accepting user-influenced URLs/hosts for scheme/domain allow-listing, private CIDR blocking, disabled redirects, and explicit timeouts. |
| Unsafe file upload/download or path traversal | Check `Path.resolve()` containment against base directory, upload byte-size caps, magic-byte/MIME validation, and non-executable object storage keys. |

## 5. Secrets, Logging & Supply-Chain Boundary (`SR7`, `SR9`)

| Look For | How to Verify (Read-Only Trace / `rg` Scan) |
|---|---|
| Hardcoded secrets, tokens, or PII in logs/error responses | Scan diff with `rg` and installed secret scanners (`gitleaks`, `trufflehog`); verify exception handlers return sanitized error codes without stack traces or raw inputs. |
| Vulnerable or unpinned dependencies | Run the workspace's installed dependency auditor (`uv pip audit`, `pip-audit`, `npm audit --omit=dev`, `osv-scanner`, `cargo audit`, etc.) whenever lockfiles change. |
