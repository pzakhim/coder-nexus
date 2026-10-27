# 10-Dimension Comparison Checklist, Deviation Grading, and Verdict

> Topic: 10-dimension visual comparison rubric against extracted Figma per-screen `.png` renders and `design.md` (`## UI/UX mapping`), unified `BLOCKER` / `MAJOR` / `MINOR` deviation grading, and per-screen evidence reporting.

Rules **V6**, **V7**, **V9**, **V10**, and **V12**.

---

## 1. Comparing Against the Approved Visual Reference (`V6`, `V7`)

For each screen (`S-NN`) and each required state (`Loading`, `Content`, `Empty`, `Error`), open the approved visual reference (`.superpowers/sources/<ISSUE-ID>/figma/<stem>-SNN.png` + `design.md` `## UI/UX mapping`, or pre-change baseline for `CODEBASE_ONLY` minor adjustments) side-by-side with the captured Flutter `.png` screenshot at the target viewport and evaluate all **10 dimensions**:

| # | Dimension | What to Inspect | `BLOCKER` (`FAIL`) | `MAJOR` (`FAIL`) / `MINOR` |
|---|---|---|---|---|
| **1** | **Layout & Hierarchy** | Screen regions appear in approved order (`app bar` → `header/search` → `primary list/form` → `bottom action bar`); column layout matches viewport | Missing/reordered region or overlapping surfaces | `MAJOR`: tablet landscape rendered as stretched single column instead of 2-column |
| **2** | **Spacing & Alignment** | Padding, margins, and item spacing follow the design scale; consistent edge and baseline alignment | Yellow/black `RenderFlex overflowed` stripes, clipped widgets, or colliding controls | `MINOR`: 2–4dp non-destructive spacing variance |
| **3** | **Typography** | Font family, size/weight hierarchy, and multi-line wrapping/ellipsis on long strings | Truncated critical data (amounts, status, IDs) or broken heading hierarchy | `MAJOR`: missing `maxLines`/`TextOverflow` causing text wrap to break card layout |
| **4** | **Color & Tokens** | Surface, text, border, and semantic colors (`success`, `warning`, `danger`) use approved theme tokens | Hardcoded `Color(0x...)` breaking theme/contrast; destructive action styled as primary/success | `MINOR`: subtle shade difference inherent to the UI kit widget |
| **5** | **Shared / Kit Components** | Approved design-system / UI kit widgets used per `design.md` (`Core usage` / `Client Core Mapping`) | Custom/raw widget built where an approved kit component fits without a recorded `Core gap` (`D-NN`) | `MAJOR`: wrong kit variant (e.g. primary button instead of outline/secondary) |
| **6** | **Icons & Media** | Approved icon set, sizes, aspect ratios, and image shimmer/placeholder fallbacks | Missing icon, broken asset (`Unable to load asset`), or wrong icon meaning | `MINOR`: minor icon size difference |
| **7** | **4 Mandatory UI States** | `Loading`, `Content`, `Empty`, and `Error` (with retry/recovery) all rendered and verified; entered form input preserved on recoverable error | Any of the 4 states missing, blank, or crashing | `MAJOR`: loading state causes jarring layout jump or loses user input on error |
| **8** | **Responsiveness & Safe Area** | Confirmed viewports (`design.md`), portrait/landscape orientation, notch/status-bar/home-bar safe areas, soft keyboard inset | Action button or input hidden behind notch, home indicator, or soft keyboard | `MAJOR`: horizontal overflow on target viewport |
| **9** | **Copy & Localization** | Exact labels, placeholders, units, and error messages from `requirements.md` / `design.md` | Raw localization keys displayed (`order.title_key`) or copy that changes meaning | `MINOR`: minor punctuation nuance |
| **10** | **Accessibility Basics** | Touch targets (`>= 48x48dp` Android / `>= 44x44pt` iOS), text contrast (`>= 4.5:1`), text-scale resilience | Unreadable contrast or untappable control (`< 36dp`) | `MAJOR`: touch target below `48x48dp` / `44x44pt` |

- **Kit Styling & `D-NN` Precedence**: When an approved UI kit component's built-in styling differs cosmetically from a raw Figma frame (`KIT_OVERRIDE (D-NN)`), Kit styling wins — record the difference as `ACCEPTED (D-NN)` rather than `FAIL`.

---

## 2. Deviation Format & Per-Screen Visual Evidence Table (`V9`)

Record each visual deviation using the canonical format:
```text
<screen>/<state>@<viewport>: [<dimension>] expected <reference detail>, observed <actual detail> — BLOCKER | MAJOR | MINOR | ACCEPTED (D-NN) — <reason>
```

Include the per-screen visual verification table in the review or verification report:

| Screen (`S-NN`) | State (`Loading` \| `Content` \| `Empty` \| `Error`) | Viewport & Orientation | Data Mode (`FE_MOCKOON` \| `BE_LIVE`) | Visual Reference | Screenshot Artifact Path | Deviations (`BLOCKER` / `MAJOR` / `MINOR` / `ACCEPTED`) | Result (`PASS` \| `FAIL` \| `BLOCKED` \| `NOT_RUN`) |
|---|---|---|---|---|---|---|---|
| `S-01` | `Loading` | `mobile (390x844, portrait)` | `FE_MOCKOON` | `design.md` (`S-01` Loading state) | `evidence/PHASE-01/<sha>/visual/S-01_loading.png` | `0` | `PASS` |
| `S-01` | `Content` | `mobile (390x844, portrait)` | `FE_MOCKOON` | `.superpowers/sources/IMES-1235/figma/work-orders-S01.png` | `evidence/PHASE-01/<sha>/visual/S-01_content.png` | `0 (ACCEPTED D-02)` | `PASS` |
| `S-01` | `Empty` | `mobile (390x844, portrait)` | `FE_MOCKOON` | `design.md` (`S-01` Empty state) | `evidence/PHASE-01/<sha>/visual/S-01_empty.png` | `0` | `PASS` |
| `S-01` | `Error` | `mobile (390x844, portrait)` | `FE_MOCKOON` | `design.md` (`S-01` Error state) | `evidence/PHASE-01/<sha>/visual/S-01_error.png` | `1 BLOCKER: retry button clipped` | `FAIL` |

---

## 3. Visual Gate Verdict & Revision Invalidation (`V10`, `V12`)

- **`PASS`**: Every required screen, state (`Loading`, `Content`, `Empty`, `Error`), and viewport has been captured, opened, and visually inspected on `REVIEW_REVISION` with `0 BLOCKER` and `0` unaddressed `MAJOR` deviations.
- **`FAIL`**: Any `BLOCKER` or `MAJOR` deviation, `RenderFlex overflowed`, missing state, or golden comparison failure → return `CHANGES_REQUESTED` to `incremental-implementation`.
- **`BLOCKED`**: Required visual reference, target device/emulator, or data source is unavailable.
- **`NOT_RUN`**: Required state or viewport was not attempted.
- **`UNVERIFIED`**: Screenshot path cited without opening and inspecting the image (or claiming screen tracking from a screenshot alone without log evidence).
- **`N/A`**: Phase has `UI Impact: No` with recorded reason.
- **Revision Invalidation**: Any code, widget, asset, or theme fix creates a new revision and invalidates prior visual and golden evidence for the affected screens.
