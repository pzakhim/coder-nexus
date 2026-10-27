---
name: visual-quality
description: "Launch approved Flutter UI targets (iOS Simulator, Android Emulator, Chrome/Desktop) and headless `golden_screenshot` tests to verify UI visual fidelity across all 4 required states (`Loading`, `Content`, `Empty`, `Error`), viewports, and orientations — grading deviations via the 10-dimension checklist (`BLOCKER` / `MAJOR` / `MINOR`) and recording revision-bound `PASS` / `FAIL` / `BLOCKED` / `NOT_RUN` / `N/A` evidence."
---

# Flutter Visual Quality & Runtime UI Inspection

This skill is `{{slot:visual-quality}}` for the Flutter pack. Open and visually inspect the rendered Flutter UI on the approved target device/simulator and headless golden harness. A clean `flutter analyze` (`G2`), Cubit unit test (`G5`), or flavor build (`G8`) never replaces visual inspection when `UI Impact: Yes`.

## 1. Visual Verification Workflow

1. **Resolve Reference & Preconditions** ([01-references-matrix-and-capture.md](references/01-references-matrix-and-capture.md)):
   - Lock `REVIEW_REVISION`, target platform, flavor, entrypoint (`-t lib/main_<flavor>.dart`), viewports/orientation (`design.md`), and API data provenance (`FE_MOCKOON` vs `BE_LIVE`).
2. **Capture Runtime & Headless Golden States** ([01](references/01-references-matrix-and-capture.md), [02-golden-screenshot-workflow.md](references/02-golden-screenshot-workflow.md)):
   - Exercise and capture all **4 mandatory visual states** (`Loading`, `Content`, `Empty`, `Error`) plus required portrait/landscape orientations and themes.
   - Open and visually inspect every `.png` image and share the images and findings with the coordinator; a saved file path alone is `UNVERIFIED`.
3. **Compare Across 10 Dimensions & Grade** ([03-comparison-checklist-and-verdict.md](references/03-comparison-checklist-and-verdict.md)):
   - Compare side-by-side against extracted Figma per-screen renders (`.superpowers/sources/<ISSUE-ID>/figma/<stem>-SNN.png`) and `design.md` (`## UI/UX mapping`).
   - Grade deviations as `BLOCKER`, `MAJOR`, `MINOR`, or `ACCEPTED (D-NN)` and record per-screen `PASS` / `FAIL` / `BLOCKED` / `NOT_RUN` / `N/A` results.

## 2. Mandatory Rules (`V1`–`V12`)

| ID | Mandatory Rule | Reference |
|---|---|---|
| **V1** | **Compare against an approved reference** (extracted Figma per-screen `.png` renders + `<stem>.spec.json` + `design.md` `## UI/UX mapping` → plan-approved baseline). | [01](references/01-references-matrix-and-capture.md) |
| **V2** | **Like-for-like matrix** (`Screen × State [Loading, Content, Empty, Error] × Viewport × Orientation`). | [01](references/01-references-matrix-and-capture.md) |
| **V3** | **Real runtime target or headless golden capture** saved under `.superpowers/work-items/<slug>/vN/evidence/<phase-id>/<revision>/visual/`. | [01](references/01-references-matrix-and-capture.md), [02](references/02-golden-screenshot-workflow.md) |
| **V4** | **Open and inspect every image** — a file path without visual inspection is `UNVERIFIED`. | [01](references/01-references-matrix-and-capture.md), [02](references/02-golden-screenshot-workflow.md) |
| **V5** | **Preserve API & data provenance** (`FE_MOCKOON` fixture checks vs. `BE_LIVE` integration per `api_handshake_protocol.md`). | [01](references/01-references-matrix-and-capture.md) |
| **V6** | **Judge by the 10 named dimensions**, never personal taste. | [03](references/03-comparison-checklist-and-verdict.md) |
| **V7** | **Grade deviations with `BLOCKER` / `MAJOR` / `MINOR`** (`ACCEPTED (D-NN)` when covered by `D-NN`). | [03](references/03-comparison-checklist-and-verdict.md) |
| **V8** | **Strict golden baseline governance** — `--update-goldens` is for `code_writer` baseline authoring + `code_reviewer` visual sign-off, **never** `test_runner` verification. | [02](references/02-golden-screenshot-workflow.md) |
| **V9** | **Per-screen & per-state evidence table** with exact `REVIEW_REVISION` and `.png` paths. | [03](references/03-comparison-checklist-and-verdict.md) |
| **V10** | **Missing reference, target, or state is never `PASS`** (`BLOCKED` or `NOT_RUN`). | [01](references/01-references-matrix-and-capture.md), [03](references/03-comparison-checklist-and-verdict.md) |
| **V11** | **Zero secrets or PII in screenshots** — use safe test/fixture data and redact credentials. | [01](references/01-references-matrix-and-capture.md) |
| **V12** | **Read-only inspection in Review & Verification** — return `FAIL` → `CHANGES_REQUESTED` on defects; any code change invalidates prior screenshots. | [03](references/03-comparison-checklist-and-verdict.md) |

## 3. Canonical Visual Gate Results (`shared_contracts/flags_and_statuses.md`)

- **`PASS`**: All required screens, 4 states, and viewports were captured, opened, and inspected on `REVIEW_REVISION` with zero `BLOCKER` or unaddressed `MAJOR` deviations.
- **`FAIL`**: Any `BLOCKER` or `MAJOR` visual deviation, `RenderFlex overflowed`, missing state, or golden comparison mismatch (`-> CHANGES_REQUESTED`).
- **`BLOCKED`**: Missing design reference, unavailable simulator/emulator/device, or unreachable data source.
- **`NOT_RUN`**: Required visual state or viewport was not captured.
- **`UNVERIFIED`**: Screenshot path recorded without opening and inspecting the image.
- **`N/A`**: Phase has `UI Impact: No` (record reason; do not launch an emulator just to tick a checkbox).

## 4. Reference Guides

| Topic | Reference File |
|---|---|
| Visual reference hierarchy, Screen × State × Viewport matrix, data provenance, and runtime target capture | [01-references-matrix-and-capture.md](references/01-references-matrix-and-capture.md) |
| Headless 4-state `golden_screenshot` recipe, template, and role boundaries (`code_writer` / `code_reviewer` / `test_runner`) | [02-golden-screenshot-workflow.md](references/02-golden-screenshot-workflow.md) |
| 10-dimension comparison checklist, `BLOCKER` / `MAJOR` / `MINOR` deviation grading, and evidence report table | [03-comparison-checklist-and-verdict.md](references/03-comparison-checklist-and-verdict.md) |
<!-- {{profile_references}} -->
