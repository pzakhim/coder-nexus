# Visual Acceptance Verification and Report Template

> Topic: Test Runner UI and acceptance test-case matrix construction, 4-state runtime and golden verification rules, and the copy-ready `verification_report.md` template.

When `test_runner` runs after Code Reviewer `APPROVED` (or during `feature-testing` / `L1`–`L2` bug verification), it executes an independent verification pass on `REVIEW_REVISION` without modifying any code, tests, or golden baselines.

---

## 1. Independent UI & Acceptance Verification Flow (`test_runner`)

1. **Lock Environment & Revision Provenance**:
   - Record Client workspace path, Hub revision, installed plugin version, Flutter/FVM version, `BASE_REVISION`, `REVIEW_REVISION`, Gate 1–3 approval references, and `git status --short`.
2. **Build the UI & Acceptance Test-Case Matrix**:
   - Derive test cases directly from `requirements.md` (BDD scenarios, 4 Visual States, `AC-NN` table), `design.md` (UI State Matrix, Component Mapping, Mockoon Trigger Table), and `brief.md` (Scope In / Out-of-Scope).
   - Isolated developer unit tests (`G5`) were already verified during Code Review; `test_runner` does **not** use Mockoon HTTP payloads to run unit-level Dart logic tests.
   - `test_runner` focuses on **UI / Widget / Golden Comparison (`G6`) & Runtime Visual Verification (`G7`)** plus end-to-end acceptance across the 4 visual states (`Loading`, `Content`, `Empty`, `Error`).
3. **Execute Gates in Dependency Order**:
   - Verify whether Code Reviewer's analyzer (`G2`) and metrics (`G3`) evidence matches `REVIEW_REVISION`; re-run if stale.
   - Run targeted widget/UI tests (`G5`), golden screenshot comparison (`G6` via standard `flutter test`, **never** `--update-goldens`), and the required flavor build (`G8`).
4. **Execute Runtime Visual Verification (`G7` — `{{slot:visual-quality}}`)**:
   - When `FE_MOCKOON` (`MOCKOON_MOCKED`) is active, verify `mockoon-cli` from `PHASE-00` is running and serving `mocks/<feature>_mockoon.json`.
   - Reuse prior visual evidence only when `REVIEW_REVISION`, platform, target device, flavor, route, data source mode, and all 4 required visual states match 100%.
   - Open and inspect every captured screenshot (`Loading`, `Content`, `Empty`, `Error`) and present the images and findings to the coordinator. A file path alone is `UNVERIFIED`.
5. **Write the Verification Report & Return Verdict**:
   - Save `.superpowers/work-items/<slug>/vN/evidence/<phase-id>/<review-revision>/verification_report.md` using the template in §2.
   - Return the canonical Test Runner verdict (`shared_contracts/flags_and_statuses.md` §5):
     - **`ACCEPTED`**: Every required `AC-NN` and gate (`G0`–`G8`) has `PASS` evidence on `REVIEW_REVISION`.
     - **`CHANGES_REQUESTED`**: Any gate or `AC-NN` check resulted in `FAIL`. Hand off to `incremental-implementation`.
     - **`BLOCKED`**: Environment, missing device/emulator, unreachable required live endpoint (`BE_LIVE`), or missing credential prevented a required check (`BLOCKED` / `NOT_RUN`).

---

## 2. Flutter Verification Report Template (Copy-Ready)

Save to `.superpowers/work-items/<slug>/vN/evidence/<phase-id>/<review-revision>/verification_report.md`:

```markdown
# Flutter Verification Report

> **Task:** {{TASK_ID}} — {{TASK_TITLE}}
> **Base revision:** `{{BASE_REVISION}}`
> **Review revision:** `{{REVIEW_REVISION}}`
> **Review report:** `{{REVIEW_REPORT_PATH}}`
> **Acceptance verdict:** `{{VERDICT}}` <!-- ACCEPTED | CHANGES_REQUESTED | BLOCKED -->
> **Overall gate result:** `{{OVERALL_GATE_RESULT}}` <!-- PASS | FAIL | BLOCKED | NOT_RUN -->
> **Approved document revisions:** {{APPROVED_DOCUMENT_REVISIONS}}
> **Gate 1–3 approval references:** {{ACTUAL_APPROVAL_REFERENCES}}
> **Uncommitted scope reviewed:** {{UNCOMMITTED_SCOPE}}

## 1. Environment

| Item | Evidence |
|---|---|
| Client workspace | `{{WORKSPACE_PATH}}` |
| Architecture profile | `{{ARCHITECTURE_PROFILE}}` <!-- imespro | external-structured | external-standard --> |
| Hub source revision | `{{HUB_REVISION}}` |
| Installed plugin version | `{{PLUGIN_VERSION}}` |
| Flutter / FVM version | `{{FLUTTER_VERSION}}` |
| Platform / Target device | `{{PLATFORM_DEVICE}}` |
| Flavor / Entrypoint | `{{FLAVOR_ENTRYPOINT}}` |
| API Integration mode | `{{API_MODE}}` <!-- FE_MOCKOON | BE_LIVE | NONE --> |
| Working tree (`git status --short`) | `{{GIT_STATUS}}` |

## 2. Executed Gates (`G0`–`G8`)

Planned checks: {{PLANNED_CHECKS}}. Every required gate without current-revision proof is `NOT_RUN` or `BLOCKED`.

| Gate | Command / Observation | CWD | Exit Code | Result (`PASS` \| `FAIL` \| `BLOCKED` \| `NOT_RUN`) | Evidence / Output |
|---|---|---|---:|---|---|
| G0 Tools check | `coder-nexus setup tools --pack flutter --check` | `{{WORKSPACE_PATH}}` | 0 | `PASS` | `TOOLS: READY` |
| G2 Static analysis | `flutter analyze` | `{{WORKSPACE_PATH}}` | 0 | `PASS` | `No issues found!` |
| G3 Code metrics | `dart run dart_code_linter:metrics analyze lib` | `{{WORKSPACE_PATH}}` | 0 | `PASS` | `0 violations` |
| G4 Architecture | `validate_architecture_code` & `validate_module_architecture` | `{{WORKSPACE_PATH}}` | 0 | `PASS` | `PASS` |
| G5 Unit & Widget tests | `flutter test test/modules/<feature>/` | `{{WORKSPACE_PATH}}` | 0 | `PASS` | `<N> passed` |
| G6 Golden comparison | `flutter test <golden_test_path>` | `{{WORKSPACE_PATH}}` | 0 | `PASS` | Baseline matched |
| G7 Runtime visual | `{{slot:visual-quality}}` (4 states) | `{{WORKSPACE_PATH}}` | 0 | `PASS` | Screenshots inspected |
| G8 Flavor build | `flutter build <target> --flavor <flavor> -t <entrypoint>` | `{{WORKSPACE_PATH}}` | 0 | `PASS` | Artifact built |

## 3. UI & Acceptance Test-Case Matrix

| AC ID | Scenario | Check Scope (`FE_MOCKOON` UI/Contract vs `BE_LIVE` Integration) | Data Source / Fixture + Contract Revision | Expected Result | Test Path / Target State | Result (`PASS` \| `FAIL` \| `BLOCKED` \| `NOT_RUN`) | Evidence |
|---|---|---|---|---|---|---|---|
| {{AC_ID}} | {{SCENARIO}} | {{CHECK_SCOPE}} | {{DATA_SOURCE}} | {{EXPECTED_RESULT}} | {{TARGET_STATE}} | {{RESULT}} | {{EVIDENCE}} |

> Fixture-backed `PASS` (`FE_MOCKOON`) applies only to its labeled UI/contract check. Required `BE_LIVE` integration rows remain `BLOCKED` / `NOT_RUN` until exercised against the live endpoint.

## 4. Acceptance Criteria Traceability

| AC ID | Implementation File(s) | Observable Check | Evidence | Result (`PASS` \| `FAIL` \| `BLOCKED` \| `NOT_RUN`) | Limitation / Note |
|---|---|---|---|---|---|
| {{AC_ID}} | `{{IMPL_PATH}}` | {{OBSERVABLE_CHECK}} | {{EVIDENCE}} | {{RESULT}} | {{LIMITATION}} |

## 5. Runtime Visual Verification (`G7`)

- **UI impact:** `{{UI_IMPACT}}` <!-- Yes | No -->
- **Required visual states (`Loading`, `Content`, `Empty`, `Error`):** {{REQUIRED_STATES}}
- **Visual report / screenshot artifacts:** {{VISUAL_EVIDENCE}}
- **Human/Agent screenshot inspection summary:** {{SCREENSHOT_REVIEW_AND_PRESENTATION}}
- **Golden baseline & comparison (`G6`):** {{GOLDEN_BASELINE_AND_RESULT_OR_NA}}
- **Visual Gate Result:** `{{VISUAL_RESULT}}` <!-- PASS | FAIL | BLOCKED | NOT_RUN | N/A -->

## 6. Handoff

{{HANDOFF}}

> Any code, test, asset, or config modification after this report invalidates affected rows and requires re-running `{{slot:code-review}}` and `{{slot:verification}}` on the new revision.
```
