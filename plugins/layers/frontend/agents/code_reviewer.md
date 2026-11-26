---
skills:
  - {{slot:visual-quality}}
  - {{slot:ui-kit-mapping}}
---
## Frontend rules

### Frontend Visual & UI Kit Audit (Mandatory on UI Phases & `[REVIEW_CHECKPOINT]`)
- Enforce `design.md` **`## UI/UX mapping`** via `{{slot:ui-kit-mapping}}`: confirm mapped UI Kit / design-system components are reused (no unauthorized raw primitive substitutions) and custom `C-NN` components / `Core gap` items match the approved token and node specifications.
- On **every UI phase end AND mid-phase `[REVIEW_CHECKPOINT]`**, verify `writer-handoff.md` (`Visual Artifacts:`) lists revision-bound 4-state `.png`s (`Loading`, `Content`, `Empty`, `Error`), load captured `.png`s side-by-side against extracted **Figma (`figma/<stem>-SNN.png`, `tokens.json`, `<stem>.spec.json`) OR HTML sitemap (`sitemap/screens/<id>_<code>.png`, `sitemap/*.spec.json`)** via parallel multimodal **`read_file`** (`{{slot:visual-quality}}`), and record findings in **`## Visual Comparison`**.

### API Mock Isolation (`PHASE-00` & `PHASE-01+`)
- **When reviewing `PHASE-00` (`[EXECUTE]` — Mockoon preparation phase)**:
  - Do not demand source files or architecture validators when `PHASE-00` only prepares `mocks/<feature>_mockoon.json`.
  - Verify `mocks/<feature>_mockoon.json` matches 100% of the **`Mockoon Trigger & Test Data Table`** in `design.md`: all endpoints, HTTP methods, conditional `rules` for **Pass/Default (`200/201`)**, **Empty (`[]`)**, and **Fail (`400/401/403/500`)**, latency settings, and response JSON structures.
  - Smoke-test via `mockoon-cli` and `curl` for both Pass and Fail triggers, and confirm `phases/phase-00-prepare.md` (and `implementation-plan.md`) is ticked **`[x] PREPARED / COMPLETED`** before approving `PHASE-00` to unlock `PHASE-01, 02, 03...`.
- **When reviewing `PHASE-01, 02, 03...` (`BE_API_READY` or `MOCKOON_MOCKED`)**:
  - Follow plugin-root `shared_contracts/api_handshake_protocol.md`: verify the Client source implements only the real remote data access that the stack rules prescribe, with relative endpoint paths, without fake data-source or repository classes (unless the stack rules explicitly allow a mock resource), hardcoded `localhost` hosts, or production fallbacks.
- **Unit test data**: Pass/Default and Fail/Empty payloads come from the `Mockoon Trigger & Test Data Table` or the verified BE API specification; Happy-Path Bias means tests that only assert HTTP 200, complete valid JSON, and success states.
