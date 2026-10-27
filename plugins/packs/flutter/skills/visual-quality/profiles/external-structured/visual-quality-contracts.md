# External-Structured Visual Quality Contracts (`lib/shared/`, `Client Core Mapping`)

> Topic: Visual fidelity verification for `external-structured` Flutter workspaces using project-internal `lib/shared/` design-system components and theme tokens.

This reference is auto-injected when `.superpowers/setup.json` sets `"architecture_profile": "external-structured"`.

---

## 1. Verifying Client Design System & Theme Fidelity

During runtime visual inspection (`01-references-matrix-and-capture.md`) and golden review (`02-golden-screenshot-workflow.md`), verify the rendered UI against `design.md` (`Client Core Mapping` and `## UI/UX mapping` tables) and extracted Figma per-screen `.png` renders:

| Verification Area | Visual Check (`BLOCKER` on violation) |
|---|---|
| **Shared Components (`lib/shared/` / `lib/commons/widgets/`)** | Verify that buttons, inputs, dialogs, app bars, and state views reuse the project's shared components listed in `Client Core Mapping` rather than introducing duplicate one-off widgets. |
| **Theme Tokens (`ThemeData` / `ThemeExtension`)** | Verify colors, typography, border radii, and elevations match the project's `ThemeData` / `ColorScheme` across required themes (light/dark). |
| **4 Mandatory Visual States** | Inspect `Loading`, `Content`, `Empty`, and `Error` states using the project's established loading/empty/error widgets, ensuring zero `RenderFlex overflowed` stripes and proper safe-area padding. |
