# 02 - Authorization & Session Management

Mobile clients act on behalf of authenticated users. Session tokens, expired credentials, and permission gates must be managed robustly.

## 1. Token Refresh Handshake with `ApiService`

All HTTP requests in iMESPro flow through `ApiService` from `app_util`.

- **Automatic Token Injection:**
  - `generateAccessToken()` returns the active Bearer token.
- **Single Refresh on 401 Unauthorized:**
  - When an endpoint returns HTTP 401, `ApiService` serializes concurrent requests and executes `refreshToken` exactly once.
  - If refresh succeeds, queued requests retry automatically.
  - If refresh fails, `onRefreshTokenFail` is triggered.
- **Handling `onRefreshTokenFail`:**
  - Must clear stored credentials in `LocalStorageService`.
  - Must navigate the user back to the login screen and reset global user state.
  - Must prevent retry loops.

## 2. Client-Side Authorization vs Server Enforcement

- **UI Gates:**
  - Hide or disable UI buttons/screens when the current user's role lacks permissions (e.g. hiding admin actions from standard operators).
  - This improves UX, but is NOT a security boundary.
- **Server is the SSOT:**
  - The mobile app must anticipate that any action could return HTTP 403 Forbidden or 401 Unauthorized.
  - Display appropriate feedback (`AppDialog.show(..., dialogType: DialogType.error)`) when an unauthorized response occurs.
