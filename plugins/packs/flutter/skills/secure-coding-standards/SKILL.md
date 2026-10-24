---
name: secure-coding-standards
description: Mobile & Flutter security standards (OWASP MASVS, secure storage, certificate verification, deep link validation, input sanitization, and PII protection) for iMESPro client applications.
---

# Flutter Secure Coding Standards

This skill defines the security requirements, threat boundaries, and audit rules for Flutter mobile clients within the iMESPro ecosystem. Security findings are graded according to [work-item-contract handoff-and-status section 9](../work-item-contract/references/handoff-and-status.md).

## 1. Security Baseline & Threat Matrix

| Risk Domain | Threat & Vulnerability | Defensive Rule | Severity | Reference |
|---|---|---|---|---|
| **Storage & Secrets** | Hardcoded API keys, signing credentials, or plaintext token storage in `SharedPreferences`. | Store credentials via `LocalStorageService` / secure keychain storage. Never commit secrets; inject via `--dart-define`. | **P1 (Blocker)** | [03-secrets-and-sensitive-data](references/03-secrets-and-sensitive-data.md) |
| **Transport Security** | MitM attacks, disabled SSL verification, cleartext HTTP communication. | Enforce HTTPS via `ApiService(isHttps: true)`. Disallow `badCertificateCallback = true` in production. | **P1 (Blocker)** | [04-stack-risks](references/04-stack-risks.md) |
| **Input & Injection** | Malicious deep links, path traversal, script injection via WebViews or unvalidated inputs. | Sanitize all form inputs with `AppFormField` validators; validate deep link paths and query parameters. | **P1 (Blocker)** | [01-trust-boundaries-and-input](references/01-trust-boundaries-and-input.md) |
| **Auth & Session** | Token reuse after expiration, broken refresh handshake, leaked session state. | Leverage `ApiService.refreshToken` handshake; clear local session on `onRefreshTokenFail`. | **P1 (Blocker)** | [02-authorization-and-data-scope](references/02-authorization-and-data-scope.md) |
| **PII & Data Leakage** | Sensitive customer data or passwords logged in plain text or exposed in task switchers. | Strip tokens from `AppLogger.I`; obscure passwords (`obscureText: true`); mask sensitive account data. | **P1 (Blocker)** | [03-secrets-and-sensitive-data](references/03-secrets-and-sensitive-data.md) |
| **Third-Party Plugins** | Vulnerable, unmaintained, or malicious native Android/iOS dependencies. | Vet packages via `flutter pub outdated`; lock dependency versions; avoid unverified native SDKs. | **P2 (Major)** | [05-dependencies](references/05-dependencies.md) |

## 2. Fast Audit Checklist

Before requesting review for code handling authentication, network transport, or sensitive customer records, verify:

```bash
# 1. Check for hardcoded secrets, passwords, or tokens in source code
git diff | rg -i "(api_key|secret|password|bearer|auth_token)\s*=\s*['\"][A-Za-z0-9_\-]{8,}['\"]"

# 2. Check for disabled SSL verification
git diff | rg -i "badCertificateCallback\s*=\s*\(.*?\)\s*=>\s*true"

# 3. Check for plaintext logging of credentials
git diff | rg -i "AppLogger\..*?(token|password|auth|secret)"
```

See [06-review-triggers](references/06-review-triggers.md) for full review triggers and audit steps.
