## Frontend rules

- **API ownership**: `spec_writer` checks whether BE API exists (`BE_API_READY`), requires **Mockoon** (`MOCKOON_MOCKED`), or no external API is needed (`NONE`), and defines business Input/Output in `requirements.md` and `codebase-notes.md`. `planning` writes the API contract into `design.md` (Huly context stays in `codebase-notes.md`), plans **`PHASE-00` (`phases/phase-00-prepare.md`)** as readiness only, agrees with the user on **Pass/Default vs. Fail test data** (`Mockoon Trigger & Test Data Table`) when Mockoon is used, and designs the **FE integration architecture & Data Pipeline** (the stack's remote data access, models, repositories, use cases and DI as the stack rules define them — never creating fake data-source classes inside the Client source unless the stack rules explicitly allow a mock resource).
- **UI & Design System ownership**: `spec_writer` defines screen contents, UX flows (from Figma `.md`), and 4 visual state expectations. `planning` maps each UI need to exact widget/class names, records any `Core gap`, and specifies screen base, `Router`, and state contracts.
- **Web Standard Client** (TODO — not yet maintained): Organize tasks into API service -> state management -> reusable components -> view routing.
- **Step 1A frontend scans**: include `get_ux_error_patterns`. **If `MOCKOON_MOCKED`**: Propose and confirm with the user via `ask_question` the exact test data conventions — what input/payload represents **Pass / Default (`200/201`)**, what input triggers **Fail (`400/401/403/500`)**, and what input triggers **Empty (`[]`)** — so both Mockoon rules and developer Unit Tests share an agreed contract.
- **`design.md` frontend sections**:
  - **Screen, Routing & DI Contract**: Specify screen base inheritance, route arguments, pop return value, and DI scopes.
  - **Backend API Integration & Mockoon Design**:
    - **If `BE_API_READY`**: Consolidate all BE endpoints, methods, headers, request/response schemas, whether each endpoint has been verified/probed, and whether it matches the user-supplied API specification.
    - **If `MOCKOON_MOCKED`**: Record the **`Mockoon Trigger & Test Data Table`** (mapping each Pass/Default, Empty, and Fail scenario to its input trigger, Mockoon rule, HTTP status/latency, and JSON body) and the `mocks/<feature>_mockoon.json` design per the stack's API mocking strategy reference.
    - **If No External API (`NONE`)**: Omit the external API section.
  - **Core Usage, UI Mapping & 4 Visual States**: Fill the exact widget/class mapping table according to the resolved profile; specify all 4 visual states (Loading, Content, Empty, Error).
  - **UX Error Handling & Storage**: Apply `get_ux_error_patterns` and local cache policies.
- **`PHASE-00` modes**:
  1. **When `MOCKOON_MOCKED` (`[EXECUTE]`)**: `PHASE-00` contains executable tasks for `code_writer` to create `mocks/<feature>_mockoon.json` (implementing all Pass/Default, Empty, and Fail rules from the `Mockoon Trigger & Test Data Table`), start `mockoon-cli`, verify via `curl`, and pass `code_reviewer` inspection, then tick **`[x] PREPARED / COMPLETED`**.
  2. **When `BE_API_READY` (`[INFO_NOTE]` or `[EXECUTE]` if live probe needed)**: Link the BE API section of `design.md` from `PHASE-00` and list what is verified; do not copy it.
- **Technical Refinement** may adjust mock fixtures.
