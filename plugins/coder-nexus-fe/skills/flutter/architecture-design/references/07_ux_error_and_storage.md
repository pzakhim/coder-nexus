# 07 — UX Error Handling and Storage Policy

Apply the approved profile through [core-usage](../../core-usage/SKILL.md). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

Guide for Section 7 of `design.md`: **UX Error Handling & Storage Policy**.

## Purpose
Establishes standardized application-wide exception handling behaviors using `get_ux_error_patterns` and defines local persistence and cache invalidation policies.

## 1. UX Error Patterns & Behavioral Taxonomy
Inspect `get_ux_error_patterns` for standard application error handling patterns:
- **401 Unauthorized / Token Expired**:
  - Interceptor intercepts 401 $\to$ Attempts silent token refresh.
  - If refresh fails $\to$ Emits global auth event to navigate to Login screen, preserving redirect target.
- **400 / 422 Validation Error**:
  - Server validation errors mapped to field-level helper text or inline banner.
- **Network Timeout / No Internet (SocketException)**:
  - Show non-blocking SnackBar/Toast with `Retry` action or full-screen `ErrorView` if initial load failed.
- **500 Server Error**:
  - Show friendly generic error message; log detail to diagnostic logger (never display raw stack trace to user).

## 2. Storage & Cache Invalidation Policy
- **Local Persistence Technology**:
  - Secure Tokens / Credentials: MUST use `FlutterSecureStorage` (encrypted).
  - User Preferences / Key-Value: `SharedPreferences`.
  - Offline Domain Cache (if applicable): `Hive` or `Isar`.
- **Cache Invalidation Lifecycle**:
  - On user logout: Call `clearCache()` to purge feature-specific cached files/data.
  - On pull-to-refresh: Force remote fetch bypassing local cache.

## Output Format
```markdown
## 7. UX Error Handling & Storage Policy

### A. UX Error Patterns Matrix
| Error Type / Code | Trigger Condition | Presentation Behavior | Recovery Action |
|---|---|---|---|
| `AUTH_401` | Session expired | Emit global auth failure | Auto-redirect to Login |
| `NETWORK_TIMEOUT` | Request > 15s | SnackBar "Connection lost" | Show "Retry" action button |
| `VALIDATION_400` | Invalid input payload | Inline field errorText | Highlight problematic input |
| `SERVER_500` | Unhandled backend failure | Generic modal error dialog | Log error ID, contact support |

### B. Storage & Cache Policy
- **Storage Engine**: `FlutterSecureStorage` for auth token; `SharedPreferences` for filter preferences.
- **Invalidation Hook**: Purge on `AuthLogoutEvent` or pull-to-refresh force reload.
```
