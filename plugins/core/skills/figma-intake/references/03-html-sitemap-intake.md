# Interactive HTML Sitemap Intake (`HTML_SITEMAP_PROVIDED`)

> Topic: Handling single-file interactive HTML UI/UX sitemaps (auto-extracted from Huly or placed manually when oversized), scoping master sitemaps to a single work item, mapping screens (`S-NN`), workflows (`W-NN`), and business rules (`BR-NN`) into `requirements.md`, running Delta Grilling without redundant questions, and isolating unverified technical hints for Gate 2 (`planning`).

Rule **FI-9**.

---

## 1. Obtaining & Extracting the HTML Sitemap (Never Read Raw Multi-MB HTML)

Single-file interactive HTML sitemaps often exceed 30–100 MB because every full-resolution screen image is base64-encoded inside a single script line (`const SCREENS = [...]`). **Never open the raw `.html` file directly with `read_file`.**

### Case A — Auto-Downloaded & Indexed via Huly (`huly_get_task_detail(..., download=True)`)
- When Huly downloads a `.html` attachment up to the auto-download limit (`150 MB`) and detects an interactive sitemap (`SCREENS = [...]`), it automatically extracts into `.superpowers/sources/<ISSUE-ID>/sitemap/`:
  - **Small sitemap (≤ 15 screens)**: extracts `index.json`, `index.md`, and all per-screen files under `screens/` (`<id>_<code>.png`, `<id>_<code>.spec.json`, `<id>_<code>.md`).
  - **Master sitemap (> 15 screens)**: extracts `index.json` and `index.md` (`index_only`) so `spec_writer` can read the full stage/screen catalog first without unpacking unrelated screens.

### Case B — Oversized or External HTML Sitemap (Manual User Drop)
- If Huly reports `status: UNREACHABLE` because the attachment exceeds the `150 MB` auto-download limit (or network download failed), or if the user supplies a local `.html` path:
  1. Surface the exact file name, size/reason, and destination path reported in `source.note` (`.superpowers/sources/<ISSUE-ID>/<filename>`).
  2. Ask the user in **plain session chat text** (open-ended file drop path, not `ask_question`, per `grilling` Law 4) to download/place the HTML file at that exact path or provide its local path.
  3. Once placed, extract the catalog first (`--index-only`) or extract the known in-scope screens directly:
     ```sh
     coder-nexus sitemap extract "<path/to/sitemap.html>" --out "${workspaceFolder}/.superpowers/sources/<ISSUE-ID>/sitemap" --index-only
     ```

---

## 2. Scope Filtering & Split Check for Master Sitemaps

Master HTML sitemaps frequently cover an entire multi-module application (e.g., 8–10 stages and 100+ screens), whereas one work item must stay focused (at most 3 confirmed goals, `REQ-005`).

1. Read `.superpowers/sources/<ISSUE-ID>/sitemap/index.md` (and `index.json` if needed) to inspect the **Stages Overview**, **Stage Bridges**, and **Screen Catalog** (`ID`, `Screen Code`, `Role`, `Title`, `Parents → Children`).
2. Match the Huly ticket description, sub-issues, and user prompt against exact `Stage ID`s or `Screen Code`s (e.g., `M-05`, `M-06`, `BS-03`, `DLG-01`).
   - If the ticket does not name exact screens or spans multiple independent stages/modules, apply the `requirements-elicitation` **Split Check** in the Goal Question to lock which stage/screens belong to this `vN` and defer the rest to **Non-goals** / linked work items.
3. Unpack **only the in-scope screens** (optionally with `--include-neighbors` to inspect parent/child entry and exit points):
   ```sh
   coder-nexus sitemap extract "<path/to/sitemap.html>" \
     --out "${workspaceFolder}/.superpowers/sources/<ISSUE-ID>/sitemap" \
     --stage STAGE_2
   ```
   *(Or filter precisely with `--screens M-05,M-06,BS-03 --include-neighbors`, `--ids H19-H26`, or `--query "<keyword>"`.)*
4. Each unpacked screen produces three lightweight files in `sitemap/screens/`:
   - `<id>_<code>.png` — decoded full-resolution screenshot (inspect with multimodal `read_file`).
   - `<id>_<code>.spec.json` — structured metadata (`viewport`, `parents`, `children`, `overview`, `elements[]` with `pattern_hint`, `behavior`, `business_logic`, and hotspot `bbox`).
   - `<id>_<code>.md` — concise Markdown summary of overview, navigation graph, and UI element logic table.

---

## 3. Mapping Extracted Sitemap Specs into Gate 1 (`requirements.md`)

1. **`## Screens & Visual Sources` (`S-NN`)**:
   - Assign sequential `S-01`, `S-02`... for every in-scope screen (preserve the original `Screen Code` and sitemap `ID` in Screen Name / Notes, e.g., `S-01 | Maintenance Request List (M-05 / H19)`).
   - Use the canonical 5-column table (`Screen ID | Screen Name | Status | Visual Source | Notes`): record `Status` (`NEW` | `CHANGED` | `EXISTING`), the extracted `.png` + `.spec.json` paths under `.superpowers/sources/<ISSUE-ID>/sitemap/screens/`, and viewport (`width×height`) + key controls in `Notes`.
   - Inspect every in-scope `<id>_<code>.png` with multimodal `read_file` alongside `<id>_<code>.md` / `.spec.json` (`FI-2`).
2. **`## Workflows` (`W-NN`, rule `REQ-006`)**:
   - Derive ordered flows directly from the sitemap navigation graph (`parents` → current → `children`) and each screen's `Overview & Action Flow` bullet.
   - Link every `W-NN` to a confirmed `G-NN`, ordered `S-NN` screens, and `AC-NN` scenarios.
3. **Pre-Filling Actors, Business Rules & Scenarios**:
   - Extract actor roles / RBAC notes from `overview` and `elements[*].business_logic` into `## 2. Actors & Permissions`.
   - Distill explicit validation rules, formulas, status transitions, and guard conditions from `elements[*].business_logic` into `## 3. Business Rules (BR-NN)` and `## 4. Behavioral Scenarios & Visual States`, citing the sitemap screen code as source.

---

## 4. Delta Grilling & Separating Technical Hints

Because interactive HTML sitemaps are already rich in UI labels, actions, and business logic, avoid redundant questioning while still closing real engineering gaps:

1. **Delta Grilling (Do Not Re-Ask Explicit Sitemap Rules)**:
   - Do **not** grill the user one by one over element labels, button actions, or business rules already stated clearly in the extracted `<id>_<code>.md` table. Summarize the extracted rules in `DRAFT` `requirements.md` and confirm any low-risk defaults in **one** `grilling` (`modes/batch-confirm.md`) call.
   - Open individual `Q-NN` rows strictly for the **5 real gaps** HTML sitemaps typically leave open:
     1. **Ticket Scope Boundary**: exact in-scope vs. out-of-scope screens/stages when a master sitemap covers more than this ticket.
     2. **Missing Visual States**: screenshots usually show only the `Default / Content` state — confirm `Loading`, `Empty`, and `Error` expectations.
     3. **External API Contract (`BE_API_READY` vs. `MOCKOON_MOCKED`)**: exact endpoints, request/response fields, pagination, and error codes (sitemaps rarely contain complete API schemas).
     4. **Additional Viewports / Orientations**: confirm whether target devices include layouts beyond the sitemap's rendered viewport (e.g., portrait phone vs. landscape tablet).
     5. **Source Conflicts**: any discrepancy between the HTML sitemap, Huly description/comments, and existing codebase behavior.
2. **Isolate Unverified Technical Hints (No Technical Leakage in `requirements.md`)**:
   - Sitemap prose sometimes mentions author-assumed libraries, local storage engines, cache key prefixes, route strings, or UI framework widget names.
   - Keep `requirements.md` in pure business/UX language (`grilling` `modes/spec.md` §3). Move any technical mentions from the HTML sitemap into `codebase-notes.md` (`## 3. Verified Baseline Facts & Cross-Agent Notes`) explicitly labeled **`Unverified spec hint (from HTML sitemap)`** so `planning` verifies them against the real codebase and active architecture profile at Gate 2.

---

## 5. Gate 2 Handoff (`planning` & `{{slot:ui-kit-mapping}}`)

Unlike `FIGMA_PROVIDED`, `HTML_SITEMAP_PROVIDED` has **no** W3C DTCG `tokens.json` or vector node tree:
- `planning` inspects the extracted `<id>_<code>.png` renders (multimodal `read_file`) alongside `<id>_<code>.spec.json` (`viewport`, `elements[*].name`, `pattern_hint`, `behavior`, `bbox`).
- `planning` maps every UI element to the active workspace profile's Design System tokens and reusable components via `{{slot:ui-kit-mapping}}`, treats HTML visual styling as a visual reference aligned to the project's existing tokens (`KIT_OVERRIDE (D-NN)` when snapping to standard kit tokens/widgets), and records any missing component as `C-NN` (`CORE_GAP (D-NN)`) in `design.md` (`## UI/UX mapping`, rule `DESIGN-008`).
- At per-phase / `[REVIEW_CHECKPOINT]` visual review (**`code_reviewer`**) **AND** at `final_qa` visual E2E acceptance (**`test_runner`**) (`{{slot:visual-quality}}`), both roles independently compare revision-bound captured app screenshots side-by-side against the extracted `sitemap/screens/<id>_<code>.png` renders as the Priority 1 visual reference using multimodal `read_file`.
