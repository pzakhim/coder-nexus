## Flutter rules

- **Source and test folders**: `lib/` and `test/`.
- **Sequential Flutter E2E Verification Ladder (`test-plan.md` `E2E-01..E2E-N` — Fail-Fast)**:
  - Execute `E2E-01` → `E2E-02` → ... → `E2E-N` in `vN/test-plan.md` sequentially, one scenario at a time, adapting the harness per `{{slot:verification}}` and `{{slot:visual-quality}}` for the resolved `architecture_profile.mode`:
    1. **Rung 1 — Static & Widget/Integration Test Suite**: Run actual Client `flutter analyze` and targeted `flutter test` widget/UI/integration suites on the reviewed revision.
    2. **Rung 2 — Runtime Visual & Workflow Execution (`S-NN` & `W-NN`)**: Launch the real Client target (with `mockoon-cli` running when `MOCKOON_MOCKED` or against the live backend when `BE_API_READY`), walk through each `E2E-i` screen flow, and verify all **4 Visual States (`Loading`, `Content`, `Empty`, `Error`)**.
    3. **Rung 3 — Profile & UI Kit Invariants**: Under `imespro`, verify `BaseScreen` route observer and responsive layout hooks, `ListViewPaging` auto-load and pull-to-refresh, and `app_ui_kit` widget interactions; under `external-standard`, Cubit/BLoC is not required.
    4. **Rung 4 — Golden Screenshot & Figma `<stem>-SNN.png` Fidelity**: When an approved golden test and reviewed baseline already exist, run the comparison **without `--update-goldens`** (`--update-goldens` during verification is a `BLOCKER` violation). Compare captured runtime screens against extracted Figma `<stem>-SNN.png` renders when present.
  - **Fail-Fast & Handoff (`test_runner` ↔ `bug_fixer` ↔ `planning`)**:
    - Tick `- [x] **E2E-i**` in `vN/test-plan.md` with fresh `flutter test` / runtime screenshot evidence as each scenario passes.
    - If any `E2E-i` fails, **stop immediately (`FAIL-FAST`)**, never alter `test-plan.md` or update golden baselines, record `FAILED_AT: E2E-i` in `vN/evidence/final_qa/<revision>/acceptance-report.md`, and return `CHANGES_REQUESTED` so the coordinator invokes **`bug_fixer`** (`L1`/`L2` Flutter fix or `L3` `PCR-NN.md` escalation to **`planning`**).
    - Once fixed, re-run `E2E-01` through `E2E-N` from start to finish until 100% pass.
