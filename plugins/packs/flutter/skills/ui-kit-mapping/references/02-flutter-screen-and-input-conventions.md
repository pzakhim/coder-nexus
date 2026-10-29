# Flutter Screen Layout, Viewport, and Hardware Input Conventions

> Topic: Translating Figma `screens[i].tree` (`layout`, `bounds`) into Flutter responsive scaffolds, viewport and orientation rules, numeric keyboards, and hardware barcode/RFID scanner conventions.

Rules **K2**, **K4**, **K5**, and **K6**.

---

## 1. Translating Figma `layout` Tree, `textMeta`, & Screen Anatomy to Flutter (`K6`)

Each node in `<stem>.spec.json` → `screens[i].tree` includes a normalized `layout` object (`mode: "row" | "column" | "none"`, `gap`, `padding`, `alignItems`, `justifyContent`, `sizing`, `positioning`, `constraints`, `scrollDirection`, `scrollBehavior`, `minMax`), `repeatCount`, and `textMeta` on `TEXT` nodes:

| `<stem>.spec.json` Property | Flutter Layout / Widget Idiom |
|---|---|
| `layout.positioning == "absolute"` + `layout.constraints` (`horizontal`, `vertical`) | `Stack` + `Positioned` / `Align` for floating badges, overlays, or pinned floating action buttons |
| `layout.scrollBehavior == "fixed" \| "sticky"` | Pinned `AppBar`, `Scaffold.bottomNavigationBar` / sticky bottom `SafeArea` CTA bar, or `SliverPersistentHeader` |
| `layout.scrollDirection` (`"vertical" \| "horizontal" \| "both"`) + `repeatCount >= 3` | `ListView.builder` / profile's paginated list widget (`list` pattern in `<!-- {{profile_references}} -->`) / `SingleChildScrollView` |
| `layout.minMax` (`minWidth`, `maxWidth`, `minHeight`, `maxHeight`) | `ConstrainedBox(constraints: BoxConstraints(...))` or responsive `LayoutBuilder` breakpoints |
| `textMeta.maxLines` + `textMeta.truncation == "ellipsis"` | `Text(..., maxLines: N, overflow: TextOverflow.ellipsis)` (combined with `Expanded` / `Flexible` in `Row`s) |

- **Top-Level Screen Scaffold**:
  - Map the top header section to the profile's AppBar widget → scrollable body (`SingleChildScrollView` / `ListView.builder` / profile paging list) → sticky bottom action bar (`SafeArea` bottom bar) or inline content CTA → bottom navigation only on top-level shell screens.
- **Auto-Layout (`mode: "row" | "column"`)**:
  - Map `mode: "column"` to `Column` / `ListView` and `mode: "row"` to `Row` / `Wrap`, translating `gap` into `SizedBox(height/width: ...)` or list separator spacing and `padding` into `EdgeInsets`.
  - When a child node has `sizing.horizontal: "fill"` or `sizing.vertical: "fill"`, wrap appropriately in `Expanded` or `Flexible` and guard text nodes with `maxLines` + `TextOverflow.ellipsis` (`textMeta`) to prevent `RenderFlex overflowed` errors.
- **Tablet & Web Adaptive Layouts**:
  - Inspect `screens[i].bounds` (`width` × `height`).
  - Never stretch a single-column mobile form (`~375–430` width) across a tablet (`>= 768` width) or desktop (`>= 1024` width) viewport without constraints or a 2-column split (master list + detail pane, or scan input pane + live tally pane).
- **Ignore Captured OS Chrome**:
  - Figma frames often include decorative iOS/Android status bars (time, battery, Wi-Fi), home indicators, or mock virtual keyboards at the top/bottom of the frame. **Never build custom widgets for OS status bars, home indicators, or virtual keyboards** — Flutter `Scaffold` and `SafeArea` handle system insets natively.

---

## 2. Viewport & Orientation Resolution from Figma `bounds` (`K2`, `K6`)

Determine target platforms, viewport dimensions, and orientations from `screens[i].bounds` in `<stem>.spec.json` and the Huly ticket context:

| Figma Screen `bounds` (`width` × `height`) | Inferred Target Viewport & Orientation | Flutter Layout Requirement |
|---|---|---|
| `~360–430` × `~780–932` (`width < height`) | `mobile` (`portrait`) | Standard mobile portrait layout |
| `~744–1024` × `~1024–1366` (`width < height`) | `tablet` (`portrait`) | Tablet portrait layout (responsive grid / constrained max-width) |
| `~1024–1366` × `~744–1024` (`width > height`) | `tablet` (`landscape`) | Mounted warehouse terminal / packing station / tablet scanner kiosk layout (2-column split so operators act without vertical scrolling) |
| `>= 1280` × `>= 800` (`width > height`) | `desktop` / `web` | Desktop / Web multi-pane layout |

- If a Huly ticket requires both mobile and tablet/landscape support (or if the active profile's screen base class provides tablet/landscape builders) but Figma only supplies one viewport, queue a `Q-NN` (`Owner: planning`) to confirm the secondary orientation layout and record `D-NN`.

---

## 3. Specialized Flutter Input & Hardware Scanner Conventions (`K6`)

| Input / Hardware Need | How It Appears in Figma (`<stem>.spec.json` & `.png`) | Flutter Target Mapping (`design.md` & Implementation) |
|---|---|---|
| **Numeric Entry** (quantities, weights, PINs, prices, lot counts) | Input field with numeric label/unit (`Qty`, `Kg`, `Price`, `0.00`) or numeric keypad overlay in Figma | `keyboardType: TextInputType.number` (or `TextInputType.numberWithOptions(decimal: true)`) + `FilteringTextInputFormatter` |
| **Hardware Barcode / RFID Scanners** (Zebra/Honeywell handhelds, ring scanners) | Scan input field or barcode icon in warehouse/MES flows. Hardware scanners emit rapid keyboard input into the focused field ending with `Enter`/`Tab` — **never build a camera viewfinder screen unless the requirement explicitly specifies device camera scanning** | `FocusNode` retention + `onFieldSubmitted` / hardware key listener triggering the state holder's scan handler |
| **Dialog / Bottom Sheet States** | Separate Figma frame (`FRAME`) or overlay group showing confirmation/filter modal | Triggered via `BlocListener` (one-shot side effect) calling the profile's dialog or bottom-sheet API |
