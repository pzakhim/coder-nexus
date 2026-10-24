---
skills:
  - {{slot:visual-quality}}
---
## Frontend rules

- **UI & Visual Focus (Not Unit Test Logic)**:
  - Isolated developer Unit Tests (testing models, remote data access, use cases, and state-holder logic with Mockoon/API payloads) are owned by `code_writer` and already graded by `code_reviewer`.
  - `test_runner` **does NOT use Mockoon payloads to run unit-level logic tests**. Instead, `test_runner` focuses strictly on **UI / Widget / Screenshot & Runtime Visual Verification**: screen layout, UI Kit component fidelity, user UI interactions, and the **4 Visual States (`Loading`, `Content`, `Empty`, `Error`)**.
- **Test runs** (`feature-testing`): cases come from the user's scenario, not from `requirements.md`; the 4 Visual States are the state list of default check DC3, and each step is captured with `{{slot:visual-quality}}`.
- **UI test-case matrix sources**: `requirements.md` (BDD Scenarios, Workflows, 4 Visual States, and Acceptance Criteria table), `design.md` (UI State Matrix, Component Mapping and UI/UX mapping) and, when it exists, the approved `design-uiux/` revision (screens × states × confirmed viewports).
- **In-Scope UI & Functional Verification**: Verify observable UI behavior for every BDD scenario and every AC-NN using executable widget/UI tests, reviewed screenshot comparisons, and runtime visual checks. When running runtime visual verification on a `MOCKOON_MOCKED` feature, ensure `mockoon-cli` (`mocks/<feature>_mockoon.json` prepared in `PHASE-00`) is running in the background so UI interactions render the required visual states.
- Run targeted widget/integration tests on the reviewed tree (for a test run, the recorded current revision). Unit test logic has already been verified by `code_reviewer`; focus on user acceptance and visual fidelity.
