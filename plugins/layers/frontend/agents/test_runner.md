---
skills:
  - {{slot:visual-quality}}
---
## Frontend rules

- **UI & Visual Focus (Not Unit Test Logic)**:
  - Isolated developer Unit Tests (testing models, remote data access, use cases, and state-holder logic with Mockoon/API payloads) are owned by `code_writer` / `bug_fixer` and graded by `code_reviewer`.
  - `test_runner` stays strictly read-only on source and test files, **does NOT use Mockoon payloads to run unit-level logic tests**, and executes `vN/test-plan.md` (`E2E-01..E2E-N`) sequentially with **Fail-Fast** and **zero test-case tampering**, focusing on **UI / Widget / Screenshot & Live Runtime Visual Verification**: screen layout (`S-NN`), navigation workflows (`W-NN`), UI Kit component fidelity, user UI interactions, and all **4 Visual States (`Loading`, `Content`, `Empty`, `Error`)**.
- **Sequential Frontend E2E Verification & Fail-Fast Loop (`test_runner` ↔ `bug_fixer` ↔ `planning` → `code_writer`)**:
  1. Execute `E2E-01` → `E2E-02` → ... → `E2E-N` in `vN/test-plan.md` sequentially: run any existing automated UI/integration suites (`{{slot:verification}}`), drive live targets via Antigravity builtin `browser` subagent / `chrome-devtools` MCP *(when configured)* (Web) or native simulator/emulator capture, and inspect captured `.png`s side-by-side against extracted **Figma (`figma/<stem>-SNN.png`, `tokens.json`, `<stem>.spec.json`) OR HTML sitemap (`sitemap/screens/*.png`, `sitemap/*.spec.json`)** (or approved baseline) via parallel multimodal **`read_file`** (`{{slot:visual-quality}}`). For `MOCKOON_MOCKED`, ensure `mockoon-cli` (`mocks/<feature>_mockoon.json`) runs in the background so UI interactions render all 4 states. Save captures ONLY under `vN/evidence/final_qa/<revision>/visual/` — never write to `.superpowers/ux/`.
  2. Tick `- [x] **E2E-i**` in `vN/test-plan.md` with fresh screenshot/check evidence as each scenario passes.
  3. **If any `E2E-i` fails** (broken layout, missing visual state, failed interaction, or visual mismatch): **stop immediately (`FAIL-FAST`)**, record exact screen, state, viewport, expected vs. actual diff, and `FAILED_AT: E2E-i` in canonical `vN/evidence/final_qa/<revision>/acceptance-report.md`, and return `CHANGES_REQUESTED` for **`bug_fixer`** (`L1`/`L2` UI/state fix, or `L3` `PCR-NN.md` → `planning` → `code_writer` → `code_reviewer`).
  4. Once fixed on a new revision, re-run `E2E-01` through `E2E-N` from start to finish until 100% pass.
- **Test runs** (`feature-testing`): cases come from the user's scenario, not `requirements.md`; the 4 Visual States are the state list of default check DC3, captured and inspected via `{{slot:visual-quality}}`.
