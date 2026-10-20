## Frontend rules

- **Frontend scope**: This workspace is a Frontend Client. Own UI/UX & screen expectations from Figma `.md` specs and the API business contract (`BE_API_READY` vs. `MOCKOON_MOCKED`). **NEVER** modify backend files, databases, or remote server code.
- **Web standard signatures**: React/Next.js/Vue signatures $\implies$ Target Platform: `web`, Framework: `react` / `web-standard` (TODO — not yet maintained).
- **Stage 1A frontend intake pillars** (in addition to the PO / BA Requirements Source):
  - **UI Screens, UX Flow & Design System Source**: Exported Figma `.md` files or attached visuals. If missing, record `VISUAL_INPUT_MISSING` and queue a `Q-NN` to confirm minimal layout expectations.
  - **Backend API Integration Source (Binary Check: Does BE API Exist Yet?)**:
    - **Case 1 — BE API Exists (`BE_API_READY`)**: Record the API specification source in `codebase-notes.md` so `planning` consolidates it in `design.md` and `PHASE-00` (`[INFO_NOTE]`).
    - **Case 2 — BE API Does Not Exist (or Missing Endpoints) $\to$ Use Mockoon (`MOCKOON_MOCKED`)**: Lock in the business Input/Output contract in `requirements.md` and `codebase-notes.md` (`## 4. Constraints & External Integrations` & `## 5. Extended Rule Details`) per `shared_contracts/api_handshake_protocol.md`. Downstream, `planning` agrees with the user on the `Mockoon Trigger & Test Data Table` in `design.md` and marks `PHASE-00` (`phases/phase-00-prepare.md`) as `[EXECUTE]`.
- **Stage 1B**: Cross-check Figma `.md` UI flows against provided/estimated APIs and existing Client flows.
- **Grill dimensions**: the "observable states" dimension covers the Happy Path & **4 Visual States** (`Default/Content`, `Loading`, `Empty`, `Error`) and Multi-Screen state lifecycle.
- **API Boundary**: `spec_writer` owns the business Input/Output of APIs (`BE_API_READY`, `MOCKOON_MOCKED`, or `NONE`) and business Pass/Fail scenarios. `planning` owns the `Mockoon Trigger & Test Data Table`, `PHASE-00` (`phase-00-prepare.md`), and the FE Data Pipeline (`RemoteDataSource` calling `ApiService`, `Model.fromJson`, `Repository`, `UseCase`, DI).
- **UI / UX & UI Kit Boundary**: `spec_writer` owns screen & UX requirements and the 4 visual states (`Default/Content`, `Loading`, `Empty`, `Error`). `planning` owns architecture profile resolution, exact UI Kit / Client widget mapping, screen base, `Router`, and state contracts in `design.md` (Gate 2).
- **`requirements.md` §4**: name it `## 4. Behavioral Scenarios & Visual States` and include the 4 Visual States.
