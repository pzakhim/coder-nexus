# External Providers: Sandboxes and Labelled Stubs

Orientation for `references/02-test-data-accounts-and-stubs.md` (`E7`).

## 1. Order of Preference

1. **Provider sandbox / test mode** (test API keys, dedicated sandbox tenant, non-billable test project).
2. **Stub at the network edge** — an HTTP/RPC mock server that the application calls via configuration/env URL override, keeping application source code untouched.
3. **Unavailable without sandbox or stub** → mark affected test cases **`BLOCKED`** (never fabricate a `PASS`).

## 2. Network-Edge Stub Options

| Category / Tool | Best Fit | Notes |
|---|---|---|
| **Workspace fake/mock server** | Existing mock service in the repo | Always prefer the workspace's existing fake server first |
| **Mockoon (CLI)** | HTTP/REST JSON APIs | Version the environment file with the work item; `mockoon-cli start --data <file>` |
| **WireMock** | HTTP APIs needing request matching and fault injection | Supports deterministic delays, timeouts, and status overrides |
| **Prism** | OpenAPI-specified external services | Serves contract-validated responses directly from the OpenAPI spec |
| **Browser/Client network interceptor** | Client-only UI state tests | Use only when testing isolated UI states that do not claim backend integration |

## 3. Mandatory Stub Scenarios

Provide deterministic scenarios as required by the test plan:
- **Success (`2xx`)**
- **Validation / client error (`4xx`)**
- **Authentication / permission failure (`401` / `403`)**
- **Upstream server error (`5xx`)**
- **Timeout / slow response**
- **Malformed payload**

## 4. Mandatory Labelling (`stubbed: <provider>`)

Every test result executed against a stub must carry `stubbed: <provider>` in the environment record and test report. A stubbed `PASS` proves the application's contract handling, not live provider integration; explicitly list which cases still require verification against the real provider sandbox.
