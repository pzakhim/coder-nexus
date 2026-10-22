# Base rules (generic, every workspace)

Each rule goes into the generated skill with the workspace's real API facts **and its reason**, or is marked "not adopted" with a reason. The handshake evidence policy of Coder Nexus (`shared_contracts/api_handshake_protocol.md`) always applies.

| # | Rule | Why | Goes into |
|---|---|---|---|
| AP1 | **Contract first, one source of truth.** The contract (an OpenAPI/schema file or the API section of `design.md`) is written and approved before code; code, clients and mocks follow it. | Backend and clients never guess each other. | SKILL, 01 |
| AP2 | **Naming.** Resource and path style, HTTP methods (or RPC verbs), field casing, plurals, IDs and dates as the workspace already does them. | A consistent API is learnable. | 01 |
| AP3 | **Response and error shape.** One success envelope (or none), one error shape: code, message, field errors, correlation ID, translation key if used; status-code usage. | Clients handle errors in one place. | 01 |
| AP4 | **Lists.** One pagination style (page/size or cursor), filter and sort parameters, total counts, limits. | Every list screen and client reuses one pattern. | 02 |
| AP5 | **Auth and data scopes per endpoint.** Who may call it and which rows it may return or change, matching `domain-knowledge`; enforcement follows `secure-coding-standards`. | An endpoint is the easiest way to leak data outside a scope. | 03 |
| AP6 | **Compatibility.** Adding optional fields and endpoints is safe; removing, renaming or changing meaning is breaking: it needs a compatible path (new field, new version), a deprecation note and the version bump defined by `git-workflow`. | Clients already installed keep working. | 04 |
| AP7 | **Clients and mocks follow the contract.** Generated clients or one shared wrapper; mocks (Mockoon, MSW, WireMock…) built from the contract and updated with it. | A mock that drifts hides integration defects. | 05 |
| AP8 | **Safe mutations.** Idempotency keys or natural idempotency where clients retry; timeouts and retry rules; no side effects on `GET`. | Retries over a weak network must not duplicate data. | 01, 05 |
| AP9 | **Fixture success is not live success.** Evidence states whether it ran against a mock or the real endpoint, per the handshake protocol. | Honest integration status. | 05, SKILL |

**Never "not adopted":** AP1, AP6, AP9.
