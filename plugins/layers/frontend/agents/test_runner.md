---
skills:
  - {{slot:visual-verification}}
---
## Frontend rules

- Confirm the target frontend framework recorded for the Client (the installed stack, or `web-standard`).
- **UI & Visual Focus (Not Unit Test Logic)**:
  - Isolated developer Unit Tests (testing `Model.fromJson`, `RemoteDataSource`, `UseCase`, and state-holder logic with Mockoon/API payloads) are owned by `code_writer` and already graded by `code_reviewer`.
  - `test_runner` **does NOT use Mockoon payloads to run unit-level logic tests**. Instead, `test_runner` focuses strictly on **UI / Widget / Screenshot & Runtime Visual Verification**: screen layout, UI Kit component fidelity, user UI interactions, and the **4 Visual States (`Loading`, `Content`, `Empty`, `Error`)**.
- **UI test-case matrix sources**: `requirements.md` (BDD Scenarios, 4 Visual States, and Acceptance Criteria table) and `design.md` (UI State Matrix & Component Mapping).
- **In-Scope UI & Functional Verification**: Verify observable UI behavior for every BDD scenario and every AC-NN using executable widget/UI tests, reviewed screenshot comparisons, and runtime visual checks. When running runtime visual verification on a `MOCKOON_MOCKED` feature, ensure `mockoon-cli` (`mocks/<feature>_mockoon.json` prepared in `PHASE-00`) is running in the background so UI interactions render the required visual states.
- **Web Client** (`web-standard`): Run component and UI E2E/integration tests. Verify resource bindings and view routing.
- Run targeted widget/integration tests on the reviewed tree. Unit test logic has already been verified by `code_reviewer`; focus on user acceptance and visual fidelity.
