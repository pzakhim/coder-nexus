# 06 - Security Review Triggers

Code changes touching the following areas trigger mandatory security review scrutiny.

## 1. High-Risk Triggers

Reviewers must inspect code thoroughly when a pull request introduces or modifies:
1. **Authentication & Tokens:** Login, registration, token refresh, biometric authentication, session expiry.
2. **Storage of Credentials:** Writing or reading from `LocalStorageService`, `flutter_secure_storage`, or SQLite databases.
3. **Deep Link Handling:** Parsing external URIs, custom schemes, or routing parameters.
4. **Network & SSL Configuration:** Modifying `ApiService`, `HttpClient`, or certificate handling.
5. **WebViews & Third-Party SDKs:** Adding WebViews, analytics SDKs, payment SDKs, or native bridging code.

## 2. Review Checklist

- [ ] Are tokens stored in secure hardware-backed storage?
- [ ] Is HTTPS strictly enforced without `badCertificateCallback` bypasses?
- [ ] Are input parameters sanitized and boundary-checked?
- [ ] Are sensitive fields masked and omitted from `AppLogger.I`?
- [ ] Are deep links strictly validated against an approved route whitelist?
