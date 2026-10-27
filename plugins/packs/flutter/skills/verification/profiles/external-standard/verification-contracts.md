# External-Standard Flutter Verification Contracts (Standard Flutter & Clean Architecture)

> Topic: Verification rules for `external-standard` Flutter workspaces using standard Flutter SDK widgets, `pub.dev` packages, and Ponytail simplicity.

This reference is auto-injected when `.superpowers/setup.json` sets `"architecture_profile": "external-standard"`.

---

## 1. Pre-Verification Toolchain Gate (`G0`)

- Run `coder-nexus setup tools --pack flutter --check` (`PASS` when `TOOLS: READY`).
- **Never run `coder-nexus setup flutter --check`** and never require external monorepo packages (`app_core`, `app_util`, `app_ui_kit`) or unapproved custom base screen wrappers.

---

## 2. Verifying Clean Architecture & Standard Flutter UI

During `G2` (`flutter analyze`), `G4` (architecture validators), `G5` (`flutter test`), and `G7` (`{{slot:visual-quality}}`), verify:

| Verification Area | Verification Contract (`PASS` vs `FAIL`) |
|---|---|
| **Layer Boundaries (`G4`)** | • `domain/` has zero Flutter UI (`package:flutter/...`) or Data/HTTP (`dio`, `http`) imports.<br>• `lib/modules/<feature>/` contains only the layers required by `design.md` (`data/`, `domain/`, `presentation/`), with zero speculative abstractions or fake `Mock*DataSource` classes in `lib/`. |
| **State & Unit Tests (`G5`)** | • Unit and `bloc_test` / state tests cover model parsing, repository error mapping, and state transitions (`Loading`, `Content`, `Empty`, `Error`). |
| **Standard Flutter UI & 4 Visual States (`G6`–`G7`)** | • Screens use standard `Scaffold` / Material 3 / Cupertino widgets and `Theme.of(context)` tokens cleanly.<br>• Shared widgets appear in `lib/commons/widgets/` only when reused by 2+ features.<br>• All 4 visual states (`Loading`, `Content`, `Empty`, `Error`) are verified via widget/golden tests (`G6`) and runtime visual inspection (`G7`). |
