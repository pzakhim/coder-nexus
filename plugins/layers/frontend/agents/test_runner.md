---
skills:
  - {{slot:visual-quality}}
---
## Frontend rules

- **UI & Visual Focus (Not Unit Test Logic)**:
  - Isolated developer Unit Tests (testing models, remote data access, use cases, and state-holder logic with Mockoon/API payloads) are owned by `code_writer` / `bug_fixer` and already graded by `code_reviewer`.
  - `test_runner` **does NOT use Mockoon payloads to run unit-level logic tests**. Instead, `test_runner` executes `vN/test-plan.md` (`E2E-01..E2E-N`) sequentially with **Fail-Fast** and **zero test-case tampering**, focusing strictly on **UI / Widget / Screenshot & Runtime Visual Verification**: screen layout (`S-NN`), navigation workflows (`W-NN`), UI Kit component fidelity, user UI interactions, and the **4 Visual States (`Loading`, `Content`, `Empty`, `Error`)**.
- **Sequential Frontend E2E Verification & Fail-Fast Loop (`test_runner` ↔ `bug_fixer` ↔ `planning`)**:
  1. Execute `E2E-01` → `E2E-02` → ... → `E2E-N` in `vN/test-plan.md` one scenario at a time using targeted widget/integration suites (`{{slot:verification}}`), runtime app execution, and visual comparisons (`{{slot:visual-quality}}` against extracted Figma `<stem>-SNN.png` or approved baseline). When running runtime visual verification on a `MOCKOON_MOCKED` feature, ensure `mockoon-cli` (`mocks/<feature>_mockoon.json` prepared in `PHASE-00`) is running in the background so UI interactions render the required visual states.
  2. Tick `- [x] **E2E-i**` in `vN/test-plan.md` with fresh screenshot/check evidence as each scenario passes.
  3. **If any `E2E-i` fails** (broken screen layout, missing visual state, failed interaction, or visual mismatch): **stop immediately (`FAIL-FAST`)**, record the exact screen, state, viewport, expected vs. actual visual/behavior diff, and `FAILED_AT: E2E-i` in `vN/evidence/final_qa/<revision>/acceptance-report.md`, and return `CHANGES_REQUESTED` so the coordinator invokes **`bug_fixer`** (`L1`/`L2` UI/state fix or `L3` `PCR-NN.md` escalation to **`planning`**).
  4. Once fixed, re-run `E2E-01` through `E2E-N` from start to finish until 100% pass.
- **Test runs** (`feature-testing`): cases come from the user's scenario, not from `requirements.md`; the 4 Visual States are the state list of default check DC3, and each step is captured with `{{slot:visual-quality}}`.
