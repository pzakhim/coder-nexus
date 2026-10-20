---
skills:
  - {{slot:visual-verification}}
---
## Frontend rules

- Confirm the target frontend framework recorded for the Client (the installed stack, or `web-standard`) and keep the UI Kit and Client API safeguards.

### Backend API Dependency, `PHASE-00` Consolidation & Mockoon Strategy
- **When assigned `PHASE-00` (`[EXECUTE]` — e.g. `MOCKOON_MOCKED`)**:
  - Generate `mocks/<feature>_mockoon.json` implementing all routes and conditional `rules` (Pass/Default `200/201`, Empty `[]`, and Fail `400/401/403/500`) matching 100% of the **`Mockoon Trigger & Test Data Table`** in `design.md`.
  - Start `mockoon-cli` (`mockoon-cli start --data mocks/<feature>_mockoon.json --port <port>`) and smoke-test both Pass/Default and Fail requests via `curl`.
  - Tick **`[x] PREPARED / COMPLETED`** in `phases/phase-00-prepare.md` and hand off `PHASE-00` for Reviewer confirmation.
- **When assigned `PHASE-01, 02, 03...` (`BE_API_READY` or `MOCKOON_MOCKED`)**:
  - In the Client source, implement only the real **`RemoteDataSource`** calling `ApiService` (`ApiConfig.domain` pointed to the BE server or local Mockoon server in `.env`); **never** create fake `Mock<Feature>DataSource` classes inside the Client source.
  - Follow the installed plugin's `shared_contracts/api_handshake_protocol.md`: when BE delivers the real API, point `ApiConfig.domain` / `.env` to the live server and verify the actual live contract (auth, schema, errors) before claiming live integration acceptance.
- **Zero cross-repo writes**: NEVER modify Backend repositories, server code, or DB schemas from this agent.
- **Unit test data**: Pass/Default and Fail/Empty cases come from `design.md` (`Mockoon Trigger & Test Data Table` / BE API spec).
- **`PHASE-00` self-verification**: For `PHASE-00` (`[EXECUTE]`), verify `mocks/<feature>_mockoon.json` via `mockoon-cli` and `curl`.
