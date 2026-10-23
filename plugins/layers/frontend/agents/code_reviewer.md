---
skills:
  - {{slot:visual-quality}}
---
## Frontend rules

- Confirm the target frontend framework recorded for the Client (the installed stack, or `web-standard`).

### API Mock Isolation (`PHASE-00` & `PHASE-01+`)
- **When reviewing `PHASE-00` (`[EXECUTE]` — Mockoon preparation phase)**:
  - Do not demand source files or architecture validators when `PHASE-00` only prepares `mocks/<feature>_mockoon.json`.
  - Verify `mocks/<feature>_mockoon.json` matches 100% of the **`Mockoon Trigger & Test Data Table`** in `design.md`: all endpoints, HTTP methods, conditional `rules` for **Pass/Default (`200/201`)**, **Empty (`[]`)**, and **Fail (`400/401/403/500`)**, latency settings, and response JSON structures.
  - Smoke-test via `mockoon-cli` and `curl` for both Pass and Fail triggers, and confirm `phases/phase-00-prepare.md` (and `implementation-plan.md`) is ticked **`[x] PREPARED / COMPLETED`** before approving `PHASE-00` to unlock `PHASE-01, 02, 03...`.
- **When reviewing `PHASE-01, 02, 03...` (`BE_API_READY` or `MOCKOON_MOCKED`)**:
  - Follow plugin-root `shared_contracts/api_handshake_protocol.md`: verify the Client source implements only the real remote data access that the stack rules prescribe, with relative endpoint paths, without fake data-source or repository classes (unless the stack rules explicitly allow a mock resource), hardcoded `localhost` hosts, or production fallbacks.
- **Zero cross-repo mutations**: Verify that no Backend repositories, server code, or database schemas have been touched or modified.
- **Unit test data**: Pass/Default and Fail/Empty payloads come from the `Mockoon Trigger & Test Data Table` or the verified BE API specification; Happy-Path Bias means tests that only assert HTTP 200, complete valid JSON, and success states.
