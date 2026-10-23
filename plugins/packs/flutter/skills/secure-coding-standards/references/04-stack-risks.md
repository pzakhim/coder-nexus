# 04 - Flutter & Mobile Stack Security Risks

Address mobile-specific vulnerabilities and transport security in Flutter applications.

## 1. Network Transport Security & TLS

- **Enforce HTTPS:**
  - All communication with backend APIs and third-party services must use TLS (HTTPS/WSS).
  - `ApiService` enforces `isHttps = true` by default. Never override `isHttps: false` in production builds.
- **Certificate Verification (No SSL Bypasses):**
  - **P1 Blocker:** Any override of `HttpClient.badCertificateCallback` that returns `true` (e.g. `(cert, host, port) => true`) in production code is strictly forbidden.
  - Development proxy debugging configurations must be isolated to DEV flavors and excluded from production builds.

## 2. WebView Sandboxing

If using WebViews (`webview_flutter` or similar):
- **Origin Whitelisting:** Restrict navigation only to trusted domains. Intercept navigation requests and reject external URLs.
- **JavaScript Execution:** Disable JavaScript execution unless explicitly required by the hosted feature.
- **File Access:** Disable file and content access (`allowFileAccess: false`) to prevent local file theft.

## 3. Background Screen Obscuring

For sensitive financial, authentication, or medical views:
- Obscure the application snapshot when the app enters the background (task switcher) using native privacy window flags or overlay screens.
