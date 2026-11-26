# Hybrid E2E Acceptance Verification and `acceptance-report.md` Template

> Topic: Test Runner strictly read-only Hybrid E2E verification (optional local `integration_test/` regression + live `E2E-01..N` UI driving and independent 4-state visual capture via multimodal `read_file`), and the copy-ready `acceptance-report.md` template.

When `test_runner` runs at `final_qa` after Code Reviewer `APPROVED` (or during `feature-testing` / `L1`–`L2` bug verification), it executes an independent verification pass on `REVIEW_REVISION` without modifying any production code, test files (`test/` or `integration_test/`), or golden baselines.

---

## 1. Hybrid E2E & Independent Acceptance Verification Flow (`test_runner`)

1. **Lock Environment & Revision Provenance**:
   - Record Client workspace path, Hub revision, installed plugin version, Flutter/FVM version, `BASE_REVISION`, `REVIEW_REVISION`, Gate 1–3 approval references (or `L1` bug-fix reference), and `git status --short`.
2. **Build the Sequential E2E & Acceptance Matrix (`E2E-01 → E2E-N`, Fail-Fast)**:
   - Derive `E2E-01..N` cases from `requirements.md` (`## Workflows` `W-NN`, 4 Visual States, `AC-NN` table), `design.md` (`## UI/UX mapping`, Mockoon Trigger Table), and `test-plan.md`.
   - Isolated unit tests (`G5`) were already audited in Code Review; `test_runner` focuses on **automated regression (`G5`/`G6`), optional local `integration_test/` execution, and independent live `E2E-01..N` + 4-state visual capture (`G7`)**.
3. **Execute Automated Gates & Optional Local `integration_test/` (Hybrid E2E — Part 1)**:
   - Confirm analyzer (`G2`) and metrics (`G3` *(when configured)*) match `REVIEW_REVISION`; re-run if stale.
   - Run targeted widget/unit tests (`G5`), golden screenshot comparison (`G6` via standard `flutter test`, **never** `--update-goldens`), and the required flavor build (`G8`).
   - **Optional Local `integration_test/`**: If `integration_test/<feature>_e2e_test.dart` exists in the repo (authored by `code_writer` when approved in Gate 3 plan or requested by the user), run `flutter test integration_test/<feature>_e2e_test.dart` (with `-d <device>` when targeting a simulator, emulator, or Chrome) as automated E2E regression. **`test_runner` never writes or edits `integration_test/` files itself.**
4. **Execute Live E2E (`E2E-01..N`) & Independent 4-State Visual Capture (`G7`, Hybrid E2E — Part 2)**:
   - When `FE_MOCKOON` (`MOCKOON_MOCKED`) is active, verify `mockoon-cli` from `PHASE-00` is running and serving `mocks/<feature>_mockoon.json`.
   - **Mandatory Independent Capture**: `test_runner` **must always** capture fresh runtime screenshots on `REVIEW_REVISION` into `.superpowers/work-items/<slug>/vN/evidence/final_qa/<review-revision>/visual/` — **never skip capture by reusing `code_writer` or `code_reviewer` screenshots**, and **never write to `.superpowers/ux/`** (owned exclusively by `docs_writer`).
   - **Concrete Target Driving & Capture Commands (`test_runner`, strictly read-only)**:
     - **Flutter Web / Chrome**: Launch with `flutter run -d chrome --flavor <flavor> -t <entrypoint>` (or `flutter run -d web-server --web-port <port>`), then drive UI flows and capture evidence using Antigravity's builtin **`browser` subagent** or **`chrome-devtools` MCP** (`navigate_page`, `click`, `fill`, `take_screenshot`, `list_console_messages`, `list_network_requests`).
     - **iOS Simulator**: `xcrun simctl boot <device-id>` → `flutter run -d <device-id> --flavor <flavor> -t <entrypoint>`; drive via deep links (`xcrun simctl openurl <device-id> <uri>`), Mockoon triggers, or existing `integration_test/` driver; capture via `xcrun simctl io <device-id> screenshot <artifact-path>.png`.
     - **Android Emulator**: `flutter emulators --launch <emulator-id>` → `flutter run -d <serial> --flavor <flavor> -t <entrypoint>`; drive via `adb -s <serial> shell input tap/text/keyevent`, deep links (`adb -s <serial> shell am start -a android.intent.action.VIEW -d <uri>`), or existing `integration_test/` driver; capture via `adb -s <serial> exec-out screencap -p > <artifact-path>.png`.
     - **macOS / Desktop**: `flutter run -d macos --flavor <flavor> -t <entrypoint>`; drive via existing `integration_test/` driver or window interaction; capture via `screencapture -x <artifact-path>.png`.
   - **Multimodal Visual Verification**: Load every captured 4-state `.png` (`Loading`, `Content`, `Empty`, `Error`) in parallel with its approved visual reference — Figma (`.superpowers/sources/<ISSUE-ID>/figma/<stem>-SNN.png`) OR HTML sitemap (`.superpowers/sources/<ISSUE-ID>/sitemap/screens/<id>_<code>.png`) — using Antigravity's multimodal **`read_file`** tool (`{{slot:visual-quality}}`). A file path without `read_file` inspection is `UNVERIFIED`.
5. **Write `acceptance-report.md` & Return Verdict**:
   - Save `.superpowers/work-items/<slug>/vN/evidence/final_qa/<review-revision>/acceptance-report.md` using the template in §2.
   - Return the canonical Test Runner verdict (`shared_contracts/flags_and_statuses.md` §5):
     - **`ACCEPTED`**: Every required `AC-NN`, `E2E-01..N`, and gate (`G0`–`G8`) has `PASS` evidence on `REVIEW_REVISION`.
     - **`CHANGES_REQUESTED`**: Any gate, `E2E-NN`, or visual check resulted in `FAIL`. Route **`final_qa` failures to `bug_fixer` Mode C** (not `incremental-implementation`).
     - **`BLOCKED`**: Environment, missing device/emulator/browser, unreachable required live endpoint (`BE_LIVE`), or missing credential prevented a required check (`BLOCKED` / `NOT_RUN`).

---

## 2. Flutter Acceptance Report Template (Copy-Ready)

Save to `.superpowers/work-items/<slug>/vN/evidence/final_qa/<review-revision>/acceptance-report.md`:

```markdown
# Flutter Acceptance Report

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
| E2E Driver / Mode | `{{E2E_MODE}}` <!-- Live E2E (browser/chrome-devtools/simctl/adb) + optional integration_test/ --> |
| Working tree (`git status --short`) | `{{GIT_STATUS}}` |

## 2. Executed Gates (`G0`–`G8`)

Planned checks: {{PLANNED_CHECKS}}. Every required gate without current-revision proof is `NOT_RUN` or `BLOCKED`.

| Gate | Command / Observation | CWD | Exit Code | Result (`PASS` \| `FAIL` \| `BLOCKED` \| `NOT_RUN` \| `N/A`) | Evidence / Output |
|---|---|---|---:|---|---|
| G0 Tools check | `coder-nexus setup tools --pack flutter --check` | `{{WORKSPACE_PATH}}` | 0 | `PASS` | `TOOLS: READY` |
| G2 Static analysis | `flutter analyze` | `{{WORKSPACE_PATH}}` | 0 | `PASS` | `No issues found!` |
| G3 Code metrics *(when configured)* | `dart run dart_code_linter:metrics analyze lib` | `{{WORKSPACE_PATH}}` | 0 | `PASS` | `0 violations` |
| G4 Architecture | `validate_architecture_code` & `validate_module_architecture` | `{{WORKSPACE_PATH}}` | 0 | `PASS` | `PASS` |
| G5 Unit & Widget tests | `flutter test test/modules/<feature>/` | `{{WORKSPACE_PATH}}` | 0 | `PASS` | `<N> passed` |
| G5b Optional `integration_test/` | `flutter test integration_test/<feature>_e2e_test.dart` | `{{WORKSPACE_PATH}}` | 0 | `PASS` / `N/A` | Automated E2E regression |
| G6 Golden comparison | `flutter test <golden_test_path>` (no `--update-goldens`) | `{{WORKSPACE_PATH}}` | 0 | `PASS` | Baseline matched |
| G7 Live E2E & Runtime Visual | `{{slot:visual-quality}}` (4 states, independent capture + `read_file`) | `{{WORKSPACE_PATH}}` | 0 | `PASS` | Visual table below |
| G8 Flavor build | `flutter build <target> --flavor <flavor> -t <entrypoint>` | `{{WORKSPACE_PATH}}` | 0 | `PASS` | Artifact built |

## 3. Hybrid E2E & Acceptance Test-Case Matrix (`E2E-01..N`)

| E2E / AC ID | Scenario | Check Scope (`FE_MOCKOON` UI/Contract vs `BE_LIVE` Integration) | Data Source / Fixture + Contract Revision | Expected Result | Target / Capture Path | Result (`PASS` \| `FAIL` \| `BLOCKED` \| `NOT_RUN`) | Evidence |
|---|---|---|---|---|---|---|---|
| `E2E-01` / `AC-01` | {{SCENARIO}} | {{CHECK_SCOPE}} | {{DATA_SOURCE}} | {{EXPECTED_RESULT}} | `evidence/final_qa/{{REVIEW_REVISION}}/visual/...` | {{RESULT}} | {{EVIDENCE}} |

> Fixture-backed `PASS` (`FE_MOCKOON`) applies only to its labeled UI/contract check. Required `BE_LIVE` integration rows remain `BLOCKED` / `NOT_RUN` until exercised against the live endpoint.

## 4. Acceptance Criteria Traceability

| AC ID | Implementation File(s) | Observable Check | Evidence | Result (`PASS` \| `FAIL` \| `BLOCKED` \| `NOT_RUN`) | Limitation / Note |
|---|---|---|---|---|---|
| {{AC_ID}} | `{{IMPL_PATH}}` | {{OBSERVABLE_CHECK}} | {{EVIDENCE}} | {{RESULT}} | {{LIMITATION}} |

## 5. Independent Runtime Visual Verification (`G7`)

- **UI impact:** `{{UI_IMPACT}}` <!-- Yes | No -->
- **Visual Reference Source:** `{{VISUAL_SOURCE}}` <!-- FIGMA_PROVIDED | HTML_SITEMAP_PROVIDED | CODEBASE_ONLY -->
- **Required visual states (`Loading`, `Content`, `Empty`, `Error`):** {{REQUIRED_STATES}}
- **Independent capture directory:** `.superpowers/work-items/<slug>/vN/evidence/final_qa/{{REVIEW_REVISION}}/visual/`
- **Multimodal `read_file` side-by-side comparison summary:** {{SCREENSHOT_REVIEW_AND_PRESENTATION}}
- **Golden baseline & comparison (`G6`, no `--update-goldens`):** {{GOLDEN_BASELINE_AND_RESULT_OR_NA}}
- **Visual Gate Result:** `{{VISUAL_RESULT}}` <!-- PASS | FAIL | BLOCKED | NOT_RUN | N/A -->

## 6. Handoff

{{HANDOFF}}

> Any code, test, asset, or config modification after this report invalidates affected rows. `final_qa` failures (`CHANGES_REQUESTED`) route to `bug_fixer` Mode C and require re-verification on the new revision.
```
