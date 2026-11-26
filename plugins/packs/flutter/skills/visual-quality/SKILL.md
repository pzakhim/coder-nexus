---
name: visual-quality
description: "Launch approved Flutter UI targets (iOS Simulator, Android Emulator, Chrome/Desktop) and headless `golden_screenshot` tests to verify UI visual fidelity across all 4 required states (`Loading`, `Content`, `Empty`, `Error`), viewports, and orientations — comparing captured `.png`s side-by-side against Figma (`figma/<stem>-SNN.png`) or HTML sitemap (`sitemap/screens/<id>_<code>.png`) references via multimodal `read_file`, grading deviations via the 10-dimension checklist (`BLOCKER` / `MAJOR` / `MINOR`), and recording revision-bound `PASS` / `FAIL` / `BLOCKED` / `NOT_RUN` / `N/A` evidence."
---

# Flutter Visual Quality & Runtime UI Inspection

This skill is `{{slot:visual-quality}}` for the Flutter pack. Capture rendered Flutter UI on the approved target device/simulator/browser or headless golden harness, and inspect actual `.png` screenshots side-by-side against the approved visual reference via multimodal **`read_file`**. A clean `flutter analyze` (`G2`), Cubit unit test (`G5`), or flavor build (`G8`) never replaces visual inspection when `UI Impact: Yes`.

## 1. Visual Verification Workflow & 3-Role Boundary

1. **Resolve Reference & Preconditions** ([01-references-matrix-and-capture.md](references/01-references-matrix-and-capture.md)):
   - Lock `REVIEW_REVISION`, target platform, flavor, entrypoint (`-t lib/main_<flavor>.dart`), viewports/orientation (`design.md`), and API data provenance (`FE_MOCKOON` vs `BE_LIVE`).
2. **Capture Runtime & Headless Golden States** ([01](references/01-references-matrix-and-capture.md), [02-golden-screenshot-workflow.md](references/02-golden-screenshot-workflow.md)):
   - Exercise and capture all **4 mandatory visual states** (`Loading`, `Content`, `Empty`, `Error`) plus required portrait/landscape orientations and themes.
   - Load every reference `.png` and captured `.png` in parallel with Antigravity multimodal **`read_file`** for side-by-side visual comparison; a saved file path without `read_file` inspection is `UNVERIFIED`.
3. **Compare Across 10 Dimensions & Grade** ([03-comparison-checklist-and-verdict.md](references/03-comparison-checklist-and-verdict.md)):
   - Compare side-by-side against extracted Figma per-screen renders (`.superpowers/sources/<ISSUE-ID>/figma/<stem>-SNN.png` + `tokens.json` + `<stem>.spec.json`) OR extracted HTML sitemap renders (`.superpowers/sources/<ISSUE-ID>/sitemap/screens/<id>_<code>.png` + `sitemap/screens/<id>_<code>.spec.json`) and `design.md` (`## UI/UX mapping`).
   - Grade deviations as `BLOCKER`, `MAJOR`, `MINOR`, or `ACCEPTED (D-NN)` and record per-screen `PASS` / `FAIL` / `BLOCKED` / `NOT_RUN` / `N/A` results.

| Role | Scope & Capture Responsibility | Artifact Path & Output |
|---|---|---|
| **`code_writer`** | Captures revision-bound 4-state `.png`s (headless `golden_screenshot --update-goldens` when configured, or simulator/Chrome capture) and self-checks via `read_file` | Writes `vN/evidence/<phase-id>/<REVIEW_REVISION>/visual/*.png` and lists every path in `writer-handoff.md` (`Visual Artifacts:`) |
| **`code_reviewer`** | Read-only per-phase & `[REVIEW_CHECKPOINT]` visual gate; loads actual `.png`s side-by-side against Figma OR HTML sitemap PNGs via parallel `read_file`, grades 10-dimension checklist + `design.md` `## UI/UX mapping` | Writes `## Visual Comparison` in `vN/reviews/review_<phase-id>_<REVIEW_REVISION>.md`; never edits code or captures goldens |
| **`test_runner`** | Independent `final_qa` live runtime capture & 4-state verification (`E2E-01..N`); runs goldens strictly **without** `--update-goldens`; inspects side-by-side via `read_file` | Writes ONLY to `vN/evidence/final_qa/<revision>/visual/` and `acceptance-report.md` (never writes `.superpowers/ux/` — owned solely by `docs_writer`) |

## 2. Mandatory Rules (`V1`–`V12`)

| ID | Mandatory Rule | Reference |
|---|---|---|
| **V1** | **Compare against an approved reference** (`FIGMA_PROVIDED`: `figma/<stem>-SNN.png` + `tokens.json` + `<stem>.spec.json`; `HTML_SITEMAP_PROVIDED`: `sitemap/screens/<id>_<code>.png` + `sitemap/*.spec.json`; + `design.md` `## UI/UX mapping` → `CODEBASE_ONLY` baseline). | [01](references/01-references-matrix-and-capture.md) |
| **V2** | **Like-for-like matrix** (`Screen × State [Loading, Content, Empty, Error] × Viewport × Orientation`). | [01](references/01-references-matrix-and-capture.md) |
| **V3** | **Real runtime target or headless golden capture** saved under `vN/evidence/<phase-id>/<REVIEW_REVISION>/visual/` (`code_writer`) or `vN/evidence/final_qa/<revision>/visual/` (`test_runner`). | [01](references/01-references-matrix-and-capture.md), [02](references/02-golden-screenshot-workflow.md) |
| **V4** | **Multimodal `read_file` side-by-side inspection** — load reference `.png` and captured `.png` in parallel via `read_file`; a file path without `read_file` inspection is `UNVERIFIED`. | [01](references/01-references-matrix-and-capture.md), [02](references/02-golden-screenshot-workflow.md) |
| **V5** | **Preserve API & data provenance** (`FE_MOCKOON` fixture checks vs. `BE_LIVE` integration per `api_handshake_protocol.md`). | [01](references/01-references-matrix-and-capture.md) |
| **V6** | **Judge by the 10 named dimensions**, never personal taste. | [03](references/03-comparison-checklist-and-verdict.md) |
| **V7** | **Grade deviations with `BLOCKER` / `MAJOR` / `MINOR`** (`ACCEPTED (D-NN)` when covered by `D-NN`). | [03](references/03-comparison-checklist-and-verdict.md) |
| **V8** | **Strict golden baseline governance** — `--update-goldens` is for `code_writer` baseline authoring + `code_reviewer` visual sign-off, **never** `test_runner` verification. | [02](references/02-golden-screenshot-workflow.md) |
| **V9** | **Per-screen & per-state evidence table** with exact `REVIEW_REVISION` and `.png` paths (`## Visual Comparison` in review report; `acceptance-report.md` in `final_qa`). | [03](references/03-comparison-checklist-and-verdict.md) |
| **V10** | **Missing reference, target, or state is never `PASS`** (`BLOCKED` or `NOT_RUN`). | [01](references/01-references-matrix-and-capture.md), [03](references/03-comparison-checklist-and-verdict.md) |
| **V11** | **Zero secrets or PII in screenshots** — use safe test/fixture data and redact credentials. | [01](references/01-references-matrix-and-capture.md) |
| **V12** | **Read-only inspection in Review & Verification** — per-phase `FAIL` returns `CHANGES_REQUESTED` to `code_writer`; `final_qa` `FAIL` routes to `bug_fixer` Mode C. Any code change invalidates prior screenshots. | [03](references/03-comparison-checklist-and-verdict.md) |

## 3. Canonical Visual Gate Results (`shared_contracts/flags_and_statuses.md`)

- **`PASS`**: All required screens, 4 states, and viewports were captured, loaded side-by-side via multimodal `read_file`, and verified on `REVIEW_REVISION` with zero `BLOCKER` or unaddressed `MAJOR` deviations.
- **`FAIL`**: Any `BLOCKER` or `MAJOR` visual deviation, `RenderFlex overflowed`, missing state, or golden comparison mismatch (`-> CHANGES_REQUESTED`).
- **`BLOCKED`**: Missing design reference, unavailable simulator/emulator/browser target, or unreachable data source.
- **`NOT_RUN`**: Required visual state or viewport was not captured.
- **`UNVERIFIED`**: Screenshot path recorded without multimodal `read_file` inspection.
- **`N/A`**: Phase has `UI Impact: No` (record reason; do not launch an emulator just to tick a checkbox).

## 4. Reference Guides

| Topic | Reference File |
|---|---|
| Visual reference hierarchy (Figma & HTML sitemap), Screen × State × Viewport matrix, data provenance, Hybrid E2E target driving/capture, and 3-role evidence paths | [01-references-matrix-and-capture.md](references/01-references-matrix-and-capture.md) |
| Headless 4-state `golden_screenshot` recipe, template, and strict 3-role boundaries (`code_writer` / `code_reviewer` / `test_runner`) | [02-golden-screenshot-workflow.md](references/02-golden-screenshot-workflow.md) |
| 10-dimension comparison checklist via parallel `read_file`, `BLOCKER` / `MAJOR` / `MINOR` deviation grading, and verdict routing | [03-comparison-checklist-and-verdict.md](references/03-comparison-checklist-and-verdict.md) |
<!-- {{profile_references}} -->
