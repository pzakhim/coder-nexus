# External providers: sandboxes and stubs

## Order of preference

1. **Provider sandbox / test mode** (payment test keys, ERP test instance, LLM with a test project).
2. **Stub at the network edge** — a mock server the app calls instead of the provider (configured by URL/env), so application code is unchanged.
3. **Not testable here** → the affected cases are `BLOCKED` (never fabricated success).

## Stub tools

| Tool | Fits | Notes |
|---|---|---|
| Mockoon (CLI) | HTTP APIs, quick JSON scenarios | Environment file versioned with the work item; `mockoon-cli start --data <file>` |
| WireMock | HTTP APIs with request matching and faults | Supports delays/timeouts for failure cases |
| Prism | OpenAPI-described providers | Mocks from the spec |
| MSW | Frontend-only mocking in the browser | Only for UI cases that do not need the real backend |
| Workspace-specific fake server | Whatever the workspace already has | Prefer it |

## Scenarios a stub must offer

Success · validation error · auth error · server error · timeout/slow response · malformed response — as the plan requires.

## Labelling

Every result produced against a stub carries `stubbed: <provider>` in the evidence. A stubbed PASS proves the application's handling, not the provider integration; say which cases still need the real provider.
