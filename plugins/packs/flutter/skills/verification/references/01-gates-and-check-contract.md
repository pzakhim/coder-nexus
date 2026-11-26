# Flutter Gates and Client Check Contract (`G0`–`G8`)

> Topic: Detailed execution order, exit-code and output rules for `G0`–`G8`, API handshake data provenance (`FE_MOCKOON` vs `BE_LIVE`), screen/route verification, and revision invalidation.

Read plugin-root `shared_contracts/api_handshake_protocol.md` and `shared_contracts/flags_and_statuses.md`. Take commands and targets from `.superpowers/work-items/<slug>/vN/` (`implementation-plan.md`, `phases/phase-XX-<slug>.md`, or `brief.md` for small phase-free items; `docs/features/<module>/<feature>/vN/` applies only to legacy historical items).

---

## 1. Preconditions Before Running Verification

1. **Explicit Revisions**: `BASE_REVISION` and `REVIEW_REVISION` are recorded (`git rev-parse HEAD`), and `git status --short` is clean (no untracked or unstaged drift outside the reviewed scope).
2. **Gate Approvals**: Gate 1 (`requirements.md`), Gate 2 (`design.md`), and Gate 3 (`implementation-plan.md`) approvals cover their current revisions, and `phases/phase-00-prepare.md` is ticked **`[x] PREPARED / COMPLETED`** (or **`[x] PREPARED (INFO_READY)`**).
3. **Review Gate Prerequisite (for `test_runner`)**:
   - **`dev-team` features & `L2` bug fixes**: Code Reviewer verdict on `REVIEW_REVISION` must be `APPROVED` (if `CHANGES_REQUESTED`, return to `code_writer`/`bug_fixer`; if `BLOCKED`, remain `BLOCKED`).
   - **`L1` bug fixes (`bug-squad`)**: Bypass `code_reviewer` per the `bug-squad` L1 route (`bug_fixer → test_runner` directly on the fix revision).
   - **`feature-testing`**: No code review prerequisite; records the current revision directly.
4. **Workspace Configuration Match**: Prefix (`fvm flutter` vs `flutter`), working directory, flavor, entrypoint (`-t lib/main_<flavor>.dart`), and target device come from real workspace files (`.fvmrc`, `pubspec.yaml`, `.vscode/launch.json`).

---

## 2. Gate Execution Order and Interpretation (`G0`–`G8`)

Execute applicable gates in dependency order. Every gate row records: **Claim**, **Command (+ `cwd`)**, **Revision**, **Exit Code**, **Key Output / Artifact Path**, and **Result** (`PASS` | `FAIL` | `BLOCKED` | `NOT_RUN` | `UNVERIFIED`, or `N/A` for `G7` when `UI Impact: No`).

| Gate | Command (`fvm` prefix when `.fvmrc` exists) | `PASS` Criteria | `FAIL` / `BLOCKED` / `NOT_RUN` Criteria |
|---|---|---|---|
| **G0: Tools Check** | `coder-nexus setup tools --pack flutter --check` | Exit `0`, reports `TOOLS: READY` | Missing CLI tool → install via `coder-nexus setup tools --pack flutter -y` or record `BLOCKED` |
| **G1: Code Generation** | `dart run build_runner build --delete-conflicting-outputs` | Exit `0`, generated `*.g.dart` / `*.freezed.dart` match committed tree | Non-zero exit or uncommitted diff after generation → `FAIL` |
| **G2: Static Analyzer** | `flutter analyze` (narrow module path during task; full workspace or module at phase end) | Exit `0`, `No issues found!` (`0 errors, 0 warnings`) | Any analyzer error/warning/info lint in scope → `FAIL`; SDK/pub cache broken → `BLOCKED` |
| **G3: Code Metrics** | `dart run dart_code_linter:metrics analyze lib` *(when configured)* | Exit `0`, `0` complexity/metrics violations in touched files (`N/A` if not configured) | Metrics threshold breach or lint violation → `FAIL` |
| **G4: Architecture Validators** | MCP `validate_architecture_code` & `validate_module_architecture` | `PASS` with `0` layer or module structure violations | Cross-layer import (`domain` → `data`/`presentation`), `Mock*DataSource` in `lib/`, or bad folder layout → `FAIL` |
| **G5: Unit, Widget & Optional `integration_test/`** | `flutter test test/modules/<feature>/` (+ `flutter test integration_test/<feature>_e2e_test.dart` when present) | Exit `0`, `All tests passed!`, all phase test IDs executed (`0 skipped` on required ACs) | Test failure → `FAIL`; `0` tests collected or required AC test skipped → `NOT_RUN` |
| **G6: Golden Comparison** | `flutter test <golden_test_path>` | Exit `0` against Reviewer-approved baseline `.png` files | Pixel mismatch → `FAIL`; running `--update-goldens` during verification is forbidden (`FAIL`) |
| **G7: Live E2E & Runtime Visual Check** | `{{slot:visual-quality}}` live `E2E-01..N` (`browser` subagent / `chrome-devtools` MCP on Web; simulator/emulator on native) + multimodal `read_file` side-by-side comparison | All 4 states (`Loading`, `Content`, `Empty`, `Error`) independently captured, inspected side-by-side via `read_file` against Figma or HTML sitemap renders with 0 `BLOCKER`/`MAJOR` defects | Overflow, broken state, or missing state → `FAIL`; target device or Mockoon unavailable → `BLOCKED`; `UI Impact: No` → `N/A` (with reason) |
| **G8: Flavor Build** | `flutter build <apk\|ios\|macos\|web> --flavor <flavor> -t <entrypoint>` | Exit `0`, artifact built cleanly | Compile/linking failure → `FAIL`; missing signing/SDK toolchain → `BLOCKED` |

- **Non-substitutability rule**: Hub lexical validation (`G4`) does not replace the Dart analyzer (`G2`); Cubit unit tests (`G5`) do not prove rendered widget semantics; a clean build (`G8`) does not replace runtime UI inspection (`G7`).

---

## 3. Data Provenance & API Handshake Rules (`FE_MOCKOON` vs `BE_LIVE`)

Per `shared_contracts/api_handshake_protocol.md`:
1. **Contract-Derived Fixtures (`FE_MOCKOON`)**:
   - When `design.md` (`D-NN`) specifies `MOCKOON_MOCKED` (`FE_MOCKOON`), start `mockoon-cli start --data mocks/<feature>_mockoon.json --port <port>` in the background before running `G7` runtime visual checks.
   - Record fixture provenance (`mocks/<feature>_mockoon.json`) and contract revision explicitly in the report.
   - Fixture-backed `PASS` applies **only** to its labeled UI/contract check.
2. **Live Integration (`BE_LIVE`)**:
   - Any acceptance criterion requiring live Backend integration remains `BLOCKED` or `NOT_RUN` until exercised against the real endpoint (`BE_LIVE`). Fixture screenshots or Mockoon responses never prove live backend persistence or close a live integration handshake.
3. **No Fabricated Fallbacks**:
   - Never fabricate business records, Huly task data, fake `Mock*DataSource` classes in `lib/`, or hardcoded `catch (_) => []` success fallbacks.

---

## 4. Screen, Routing & Responsive Contract Verification

- For any created or modified Screen (`presentation/screens/*_screen.dart`), verify:
  1. The active `architecture_profile` base-screen contract (see the injected profile reference in `SKILL.md`) and route registration resolve cleanly under `flutter analyze` (`G2`).
  2. When the approved requirements/design specify analytics/screen tracking or portrait/landscape responsiveness, collect observable tracking evidence and portrait/landscape screenshot evidence on the target device (`G7`).
  3. A class declaration or lexical check alone without analyzer + runtime verification is **`UNVERIFIED`**.
- Dialogs, bottom sheets, and child widgets under `presentation/widgets/` do not use full-page screen wrappers.

---

## 5. Revision Invalidation & Routing

Compare `git rev-parse HEAD` and `git status --short` against `REVIEW_REVISION` before every gate:
- If production code (`lib/`), test code (`test/`, `integration_test/`), generated files (`*.g.dart`), `pubspec.yaml` / `pubspec.lock`, flavor configuration, or assets change after `REVIEW_REVISION`, all affected review, test, build, and visual evidence is **stale**.
- **Failure & re-verification routing**:
  - **Per-phase review failure**: return to `code_writer` (`incremental-implementation`) on a new revision → re-run `{{slot:code-review}}`.
  - **`final_qa` acceptance/visual failure**: route `CHANGES_REQUESTED` to **`bug_fixer` Mode C** (not `incremental-implementation`), then re-verify on the fixed revision (`L1` bypasses `code_reviewer` directly to `test_runner`; `L2` / multi-layer fixes pass `{{slot:code-review}}` before `test_runner`).
  - **`bug-squad` `L1` fix**: `bug_fixer → test_runner` directly (`code_reviewer` bypassed); **`L2` fix**: `bug_fixer → code_reviewer → test_runner`.
