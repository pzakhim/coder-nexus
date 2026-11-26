---
skills:
  - {{slot:visual-quality}}
  - {{slot:ui-kit-mapping}}
---
## Frontend rules

- **UI Kit Mapping & Visual Artifacts (`{{slot:ui-kit-mapping}}`, `{{slot:visual-quality}}`)**: Follow `design.md` `## UI/UX mapping` strictly — reuse mapped UI Kit / design-system components, build planned `C-NN` custom components from mapped tokens/specs, and never substitute raw framework primitives when a mapped component fits. On every UI phase end and mid-phase `[REVIEW_CHECKPOINT]`, capture revision-bound 4-state `.png`s (`Loading`, `Content`, `Empty`, `Error`) into `vN/evidence/<phase-id>/<REVIEW_REVISION>/visual/`, self-check via multimodal `read_file` against Figma (`figma/<stem>-SNN.png`) or HTML sitemap (`sitemap/screens/*.png`), and list every path in `writer-handoff.md` (`Visual Artifacts:`).

### Backend API Dependency, `PHASE-00` Consolidation & Mockoon Strategy
- **When assigned `PHASE-00` (`[EXECUTE]` — e.g. `MOCKOON_MOCKED`)**:
  - Generate `mocks/<feature>_mockoon.json` implementing all routes and conditional `rules` (Pass/Default `200/201`, Empty `[]`, and Fail `400/401/403/500`) matching 100% of the **`Mockoon Trigger & Test Data Table`** in `design.md`.
  - Start `mockoon-cli` (`mockoon-cli start --data mocks/<feature>_mockoon.json --port <port>`) and smoke-test both Pass/Default and Fail requests via `curl`.
  - Tick **`[x] PREPARED / COMPLETED`** in `phases/phase-00-prepare.md` and hand off `PHASE-00` for Reviewer confirmation.
- **When assigned `PHASE-01, 02, 03...` (`BE_API_READY` or `MOCKOON_MOCKED`)**:
  - In the Client source, implement only the real remote data access that the stack rules prescribe, pointed at the BE server or the local Mockoon server through environment configuration (`.env`); **never** create fake data-source classes inside the Client source unless the stack rules explicitly allow a mock resource.
  - Follow plugin-root `shared_contracts/api_handshake_protocol.md`: when BE delivers the real API, point the environment base URL (`.env`) to the live server and verify the actual live contract (auth, schema, errors) before claiming live integration acceptance.
- **Unit test data**: Pass/Default and Fail/Empty cases come from `design.md` (`Mockoon Trigger & Test Data Table` / BE API spec).
