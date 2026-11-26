# External-Standard Visual Quality Contracts (Material 3 / Cupertino)

> Topic: Visual fidelity verification for `external-standard` Flutter workspaces using standard Material 3 / Cupertino widgets and `ThemeData` tokens.

This reference is auto-injected when `.superpowers/setup.json` sets `"architecture_profile": "external-standard"`.

---

## 1. Verifying Standard Flutter UI & 4 Visual States

During runtime visual inspection (`01-references-matrix-and-capture.md`) and golden review (`02-golden-screenshot-workflow.md`), compare the rendered UI side-by-side via multimodal `read_file` against `design.md` (`## UI/UX mapping`) and extracted Figma per-screen `.png` renders (`.superpowers/sources/<ISSUE-ID>/figma/<stem>-SNN.png`) OR extracted HTML sitemap renders (`.superpowers/sources/<ISSUE-ID>/sitemap/screens/<id>_<code>.png` + `*.spec.json`):

| Verification Area | Visual Check (`BLOCKER` on violation) |
|---|---|
| **Standard Material 3 / Cupertino Widgets** | Verify idiomatic use of `AppBar`, `FilledButton` / `OutlinedButton` / `TextButton`, `TextFormField`, `AlertDialog`, `NavigationBar`, `Card`, and `ListTile` styled via `Theme.of(context)`. |
| **4 Mandatory Visual States (`Loading`, `Content`, `Empty`, `Error`)** | Confirm all 4 states render cleanly on the target viewport(s) without `RenderFlex overflowed` stripes, clipped text, or keyboard/safe-area overlap. |
| **No Company Kit Assumptions** | Never require `app_ui_kit` or `BaseScreen` in an `external-standard` workspace. |
