# Screen (`S-NN`) & Workflow (`W-NN`) Extraction at Gate 1

> Topic: Running `coder-nexus figma fetch`, classifying `FIGMA_PROVIDED` vs. `HTML_SITEMAP_PROVIDED` vs. `CODEBASE_ONLY` (edge-case adjustment) vs. `NO_UI_IMPACT`, reading `<stem>.spec.json` + per-screen `.png`/`.jpg` images via multimodal `read_file`, and authoring `## Screens & Visual Sources` and `## Workflows` in `requirements.md`.

Rules **FI-1**, **FI-2**, **FI-3**, **FI-4**, and **FI-5**.

---

## 1. Running Figma Extraction & Checking Source Status (`FI-1`, `FI-2`)

When a Huly ticket (`huly_get_task_detail(..., download=True)`) or user prompt contains one or more Figma URLs:
1. Huly intake automatically fetches every Figma link in the ticket description and comments into `.superpowers/sources/<ISSUE-ID>/figma/`.
2. For user-pasted Figma links not yet downloaded, run:
   ```sh
   coder-nexus figma fetch "<figma-url>" --workspace-path "${workspaceFolder}" --format png [--export-icons]
   ```
   - Passing `--export-icons` batch-exports pure-vector `ICON` subtrees to `.superpowers/sources/<ISSUE-ID>/figma/icons/*.svg` and records their paths in `icon_svg_paths`.
3. For each fetched link (`<stem>` = node ID with `-`), verify the generated files in `.superpowers/sources/<ISSUE-ID>/figma/`:
   - `tokens.json`: File-level W3C DTCG design tokens (`color`, `typography`, `dimension.radius`, `dimension.spacing`, `shadow`, and `$extensions.com.figma.{components,componentSets}`).
   - `<stem>.spec.json`: Framelink-normalized specification containing `screens[]` (`suggested_id` `S01..SNN`, `image_path`, `bounds`, `layout`, `sections`, `components` with `pattern_hint`, `texts_reading_order`, `interactions`, and recursive `tree` referencing tokens by `{token.path}` with `patternHint`, `repeatCount`/`repeatedSamples`, and advanced `layout`/`textMeta`), `design_tokens.component_catalog` (with `pattern_hint`), and `icon_svg_paths` (when `--export-icons` is enabled).
   - `<stem>.png` and `<stem>-S01.png`, `<stem>-S02.png`...: High-resolution rendered images for the root frame/section and each individual screen.
   - `icons/*.svg` (optional, when `--export-icons` is used): Exported SVG assets for pure-vector `ICON` subtrees, indexed in `icon_svg_paths`.
   - `<stem>.summary.md`: Human-readable Markdown overview.
   - `<stem>.json`: Raw Figma REST API payload (ground truth).

---

## 2. Four Visual Intake Modes (`FI-1`, `FI-3`, `FI-9`)

| Mode | When It Applies | Mandatory `spec_writer` Action at Gate 1 |
|---|---|---|
| **`FIGMA_PROVIDED`** | One or more Figma links succeeded (`status: READ`). | Read `<stem>.spec.json` and inspect every `<stem>-SNN.png` via multimodal `read_file`. Extract all screens (`S-01`..`S-NN`) and workflows (`W-NN`) into `requirements.md`. |
| **`HTML_SITEMAP_PROVIDED`** | PO supplied an interactive HTML sitemap (`status: READ`, auto-extracted or manually placed). | Follow [03-html-sitemap-intake.md](03-html-sitemap-intake.md): read `sitemap/index.md`, unpack only in-scope screens via `coder-nexus sitemap extract`, inspect every `sitemap/screens/<id>_<code>.png` via multimodal `read_file` alongside `*.spec.json` / `*.md`, and apply Delta Grilling. |
| **`CODEBASE_ONLY` (Minor Edge-Case Adjustment)** | PO provided no Figma or HTML sitemap because the requirement is a small tweak, validation rule, or edge case on an existing screen. | Locate the existing screen in the codebase, list it as `S-01` (`CHANGED`) in `requirements.md` with `Visual Source: CODEBASE_ONLY` (+ codebase path), and confirm the exact scope with the user (`Q-NN` $\to$ `D-NN`). |
| **`NO_UI_IMPACT`** | Purely non-visual, data, or background logic change. | Write `No UI impact` with the reason in `requirements.md` (`## 1. Scope & Alignment`) and omit `## Screens & Visual Sources` and `## Workflows`. |

---

## 3. Authoring `## Screens & Visual Sources` & `## Workflows` in `requirements.md` (`FI-4`, `FI-5`)

### A. `## Screens & Visual Sources` Table
Map each screen from `screens[]` in `<stem>.spec.json` (normalizing `suggested_id` `S01..SNN` to canonical `S-01..S-NN`), `sitemap/screens/` (`HTML_SITEMAP_PROVIDED`), or the existing codebase screen (`CODEBASE_ONLY`), using the exact canonical 5-column schema from [`requirements.md.tpl`](../../work-item-contract/templates/requirements.md.tpl):

```markdown
## Screens & Visual Sources

| Screen ID | Screen Name | Status (`NEW` \| `CHANGED` \| `EXISTING`) | Visual Source (`Figma` / `HTML Sitemap` `.spec.json` + `.png` \| `Codebase path`) | Notes |
|---|---|---|---|---|
| S-01 | 01 - Receipt List | CHANGED | `.superpowers/sources/<ID>/figma/2000-1-S01.png` (`2000-1.spec.json`, `node 2000:10`) | 390×844; Header, Search input, Receipt list, Next button |
| S-02 | 02 - Scan Item | NEW | `.superpowers/sources/<ID>/figma/2000-1-S02.png` (`2000-1.spec.json`, `node 2000:20`) | 390×844; Header, Barcode scan field, Item card, Confirm CTA |
```

### B. `## Workflows` Table (`REQ-006`)
Combine the PO's flow description in Huly with the screen order (`S-01` $\to$ `S-02`) and prototype `interactions[]` (`navigateTo` in `screens[*].tree`) from `<stem>.spec.json`:

```markdown
## Workflows

| Workflow | Goal | Steps → screens | Scenarios / AC |
|---|---|---|---|
| W-01 | G-01 | 1. Select receipt (`S-01`) → 2. Scan item & confirm quantity (`S-02`) | `AC-01`, `AC-02` |
```

### C. Accelerating Gate 1 Control & List Identification (`patternHint` & `repeatCount`)
When reading `screens[]` in `<stem>.spec.json` to populate the `Notes` column (key sections & controls) and behavioral scenarios:
- **Canonical UI Pattern Hinting (`patternHint` / `pattern_hint`)**: Every `INSTANCE`/`COMPONENT` node in `screens[*].tree` (`component.patternHint`), `screens[*].components` (`pattern_hint`), and `design_tokens.component_catalog` (`pattern_hint`) carries a deterministic pattern classification (`appbar`, `button`, `formfield`, `search`, `dropdown`, `datepicker`, `dialog`, `bottomsheet`, `bottomnav`, `badge`, `nodata`, `loading`, `list`, `card`, `chip`, `banner`, or `custom`) to accelerate Gate 1 control identification.
- **Repeating List/Table Deduplication (`repeatCount` & `repeatedSamples`)**: Contiguous runs of $\ge 3$ structurally identical children in `screens[*].tree` are collapsed into the first child with `"repeatCount": N` and `"repeatedSamples": [...]` (sample text/variant payloads from the collapsed siblings), while `screens[*].texts_reading_order` and `screens[*].components` retain 100% of items. `spec_writer` uses `repeatCount` + `repeatedSamples` to recognize dynamic or paginated lists and tables at Gate 1 without drowning in repetitive JSON nodes.

### D. Cross-Checking Huly vs. Figma (`FI-5`)
Before closing Stage `1B` / `1C`, compare the Huly description/acceptance criteria against `screens[*].texts_reading_order`, `screens[*].components`, and `screens[*].interactions`:
- **Missing fields or buttons**: Huly mentions a field/action absent from the Figma screen (or vice versa) $\to$ queue `Q-NN` (`OPEN`) in `codebase-notes.md`.
- **Missing visual states**: Every `NEW` or `CHANGED` screen requires clear expectations for all 4 visual states (`Default / Content`, `Loading`, `Empty`, `Error`) in `requirements.md` (`## 4. Behavioral Scenarios & Visual States`). If Figma only shows the happy-path `Default` state, confirm whether standard kit `Loading`/`Empty`/`Error` states apply (`Q-NN` $\to$ `D-NN`).
