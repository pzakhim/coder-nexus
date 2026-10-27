# Screen (`S-NN`) & Workflow (`W-NN`) Extraction at Gate 1

> Topic: Running `coder-nexus figma fetch`, classifying `FIGMA_PROVIDED` vs. `CODEBASE_ONLY` (edge-case adjustment) vs. `NO_UI_IMPACT`, reading `<stem>.spec.json` + per-screen `.png`/`.jpg` images, and authoring `## Screens & Visual Sources` and `## Workflows` in `requirements.md`.

Rules **FI-1**, **FI-2**, **FI-3**, **FI-4**, and **FI-5**.

---

## 1. Running Figma Extraction & Checking Source Status (`FI-1`, `FI-2`)

When a Huly ticket (`huly_get_task_detail(..., download=True)`) or user prompt contains one or more Figma URLs:
1. Huly intake automatically fetches every Figma link in the ticket description and comments into `.superpowers/sources/<ISSUE-ID>/figma/`.
2. For user-pasted Figma links not yet downloaded, run:
   ```sh
   coder-nexus figma fetch "<figma-url>" --workspace-path "${workspaceFolder}" --format png
   ```
3. For each fetched link (`<stem>` = node ID with `-`), verify the generated files in `.superpowers/sources/<ISSUE-ID>/figma/`:
   - `tokens.json`: File-level W3C DTCG design tokens (`color`, `typography`, `dimension.radius`, `dimension.spacing`, `shadow`, and `$extensions.com.figma.{components,componentSets}`).
   - `<stem>.spec.json`: Framelink-normalized specification containing `screens[]` (`suggested_id` `S01..SNN`, `image_path`, `bounds`, `layout`, `sections`, `components`, `texts_reading_order`, `interactions`, and recursive `tree` referencing tokens by `{token.path}`).
   - `<stem>.png` and `<stem>-S01.png`, `<stem>-S02.png`...: High-resolution rendered images for the root frame/section and each individual screen.
   - `<stem>.summary.md`: Human-readable Markdown overview.
   - `<stem>.json`: Raw Figma REST API payload (ground truth).

---

## 2. Three Visual Intake Modes (`FI-1`, `FI-3`)

| Mode | When It Applies | Mandatory `spec_writer` Action at Gate 1 |
|---|---|---|
| **`FIGMA_PROVIDED`** | One or more Figma links succeeded (`status: READ`). | Read `<stem>.spec.json` and view every `<stem>-SNN.png` via `view_file`. Extract all screens (`S-NN`) and workflows (`W-NN`) into `requirements.md`. |
| **`CODEBASE_ONLY` (Minor Edge-Case Adjustment)** | PO provided no Figma link because the requirement is a small tweak, validation rule, or edge case on an existing screen. | Locate the existing screen in the codebase, list it as `S01` (`CHANGED`) in `requirements.md` with `Visual Source: CODEBASE_ONLY`, and confirm the exact scope with the user (`Q-NN` $\to$ `D-NN`). |
| **`NO_UI_IMPACT`** | Purely non-visual, data, or background logic change. | Write `No UI impact` with the reason in `requirements.md` (`## 1. Scope & Alignment`) and omit `## Screens & Visual Sources` and `## Workflows`. |

---

## 3. Authoring `## Screens & Visual Sources` & `## Workflows` in `requirements.md` (`FI-4`, `FI-5`)

### A. `## Screens & Visual Sources` Table
Map each screen from `screens[]` in `<stem>.spec.json` (or the existing codebase screen for `CODEBASE_ONLY`):

```markdown
## Screens & Visual Sources

| Screen ID | Screen Name | Kind (`NEW` \| `CHANGED` \| `EXISTING`) | Viewport (`width×height`) | Visual Source (`<stem>.spec.json` / `.png` or Codebase Path) | Key Sections & Controls |
|---|---|---|---|---|---|
| S01 | 01 - Receipt List | CHANGED | 390×844 | `.superpowers/sources/<ID>/figma/2000-1-S01.png` (`node 2000:10`) | Header, Search input, Receipt list, Next button |
| S02 | 02 - Scan Item | NEW | 390×844 | `.superpowers/sources/<ID>/figma/2000-1-S02.png` (`node 2000:20`) | Header, Barcode scan field, Item card, Confirm CTA |
```

### B. `## Workflows` Table (`REQ-006`)
Combine the PO's flow description in Huly with the screen order (`S01` $\to$ `S02`) and prototype `interactions[]` (`navigateTo` in `screens[*].tree`) from `<stem>.spec.json`:

```markdown
## Workflows

| Workflow | Goal | Steps → screens | Scenarios / AC |
|---|---|---|---|
| W-01 | G-01 | 1. Select receipt (`S01`) → 2. Scan item & confirm quantity (`S02`) | `AC-01`, `AC-02` |
```

### C. Cross-Checking Huly vs. Figma (`FI-5`)
Before closing Stage `1B` / `1C`, compare the Huly description/acceptance criteria against `screens[*].texts_reading_order`, `screens[*].components`, and `screens[*].interactions`:
- **Missing fields or buttons**: Huly mentions a field/action absent from the Figma screen (or vice versa) $\to$ queue `Q-NN` (`OPEN`) in `codebase-notes.md`.
- **Missing visual states**: Every `NEW` or `CHANGED` screen requires clear expectations for all 4 visual states (`Default / Content`, `Loading`, `Empty`, `Error`) in `requirements.md` (`## 4. Behavioral Scenarios & Visual States`). If Figma only shows the happy-path `Default` state, confirm whether standard kit `Loading`/`Empty`/`Error` states apply (`Q-NN` $\to$ `D-NN`).
