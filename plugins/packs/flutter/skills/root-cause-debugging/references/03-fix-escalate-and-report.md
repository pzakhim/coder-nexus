# 03 — Root-Cause Fix, Escalation, Report & Review (Flutter / Dart)

Rules **D6**, **D7**, **D8**, **D9**, **D10**, **D11**, **D12**, and **D14**.

---

## 1. Root-Cause Fix & Red-to-Green Regression Prevention (`D7`, `D8`, `D9`)

1. **Regression Test First (`D8`, `{{slot:unit-testing}}`):** Convert the minimized reproduction into a permanent test at the owning seam:
   - JSON parsing / null coercion / mapping bug → `Model` / `Mapper` unit test (`test/modules/<feature>/data/models/`).
   - Business validation or error propagation bug → `UseCase` / `Repository` unit test (`test/modules/<feature>/domain/` or `data/`).
   - Missing error state, loading hang, or duplicate emission → `blocTest` `Cubit` test (`test/modules/<feature>/presentation/cubit/`).
   - Layout overflow or widget interaction bug → `testWidgets` test.
   Run it **red** first and verify it fails for the exact reported reason.
2. **Smallest Fix at the Owning Layer (`D7`, `{{slot:clean-architecture}}`):** Fix the defect at the layer that owns the invariant inside the task's **Scope / Files** (e.g., fix null parsing in `Model.fromJson` rather than scattering `?? ''` across widgets; fix flex constraints rather than shrinking font sizes). Check the diff for sibling bugs (`D6`). Do not bundle unrelated refactoring.
3. **Prove Red → Green → Undo-Red → Green:** Run the regression test (`PASS`), temporarily undo only the production fix to verify the test fails (`FAIL`), restore the fix, and re-run (`PASS`). Record both runs as evidence rows.
4. **Full Verification & Cleanup (`D11`):** Re-run the original reproduction, `flutter test test/modules/<feature>/`, `dart format --output=none --set-exit-if-changed lib test`, `flutter analyze`, and verify `rg -n "DEBUG-|print\(|debugPrint\(|debugger\(" lib test` returns 0 matches (`PASS`).

### Never Green-Wash (`D9` — Automatic `BLOCKER`)

| Forbidden Shortcut | Why It Is Forbidden |
|---|---|
| Editing, deleting, `skip: true`, weakening a test assertion, or regenerating broken goldens to pass | Hides the defect and destroys the guard that caught it (wrong spec → `change-control`) |
| Empty or blanket `try { ... } catch (_) {}` swallowing exceptions | Converts a reproducible failure into a silent broken UI state (`{{slot:clean-code}}` `C4`) |
| Hardcoded mock/fallback business records in production code | Fabricates success while the real data pipeline remains broken |
| Unchecked `dynamic`, `as Any`, `// ignore:`, or `// ignore_for_file:` | Disables sound null-safety and static analyzer checks across the file |
| Adding `Future.delayed(...)` to mask async race conditions or lifecycle bugs | Leaves the race condition in production on slower devices |
| Editing or copying code from read-only foundation packages (`../app-*`) into the client | Violates workspace boundary rules (`AGENTS.md` §5) |

---

## 2. Environment (`BLOCKED`) vs. Code & Escalation (`D10`, `D12`)

Never patch client code to work around a broken environment or live backend contract breach:

| Environment / Upstream Sign | Diagnostic Check | Report Action |
|---|---|---|
| Sibling foundation packages (`../app-*`) or `pubspec.lock` unresolved | `coder-nexus setup flutter --check` / `flutter pub get --offline` | `BLOCKED` — workspace package setup failed |
| Missing `.env` or environment config file required at startup | Check file/key existence (names only, never print secret values) | `BLOCKED` — missing workspace `.env` configuration |
| Live backend returns `500` or violates approved API schema | Capture redacted status and response structure | `BLOCKED` — backend API contract breach (escalate with payload proof) |
|Defect reproduces inside a read-only foundation package (`../app_core`, `../app_util`, `../app_ui_kit`) or pinned 3P plugin | Prove with a minimal reproduction test at the package boundary | `BLOCKED` — upstream package defect (record Core gap / escalate) |
| Stale generated files (`*.g.dart`, `*.freezed.dart`) after a model edit in scope | Run `dart run build_runner build --delete-conflicting-outputs` | Re-run tests after regeneration; if build_runner is broken outside scope → `BLOCKED` |

- **3-Attempt Time-Box (`D12`):** After **3 failed fix attempts** (where the reproduction still fails), **stop immediately**. Return `BLOCKED` with the Debug Report block below showing `Root cause: unknown`, the 3 ruled-out hypotheses, and missing evidence.
- **Back to the Gate (`change-control`):** Stop and escalate if the fix requires:
  - Editing files outside the task's **Scope / Files** (`TASK_DETAIL`)
  - Changing an approved `design.md` (`## UI/UX mapping`) / Figma layout spec, API contract, `pubspec.yaml` dependency, or layer boundary (`DESIGN_CHANGE`)
  - Changing user-visible behavior or approved Acceptance Criteria (`SCOPE_CHANGE`)

---

## 3. Hand-Off Debug Report Format (`D14`)

Include this block in the Code Writer / Bug Fixer hand-off (or `FIXED` finding response) with redacted outputs (`<REDACTED>`):

```text
Symptom:      <what failed and where; reported by task check / reviewer / bug-hunt / tester / user>
Triage:       CODE_WRONG (task <id>, Expected: <...>)
Reproduction: flutter test <file>_test.dart --plain-name "<name>" @ <revision> -> exit 1 (<key output>)
Root cause:   <exact defect at lib/modules/<feature>/<file>.dart:<line> and why it occurred>
Fix:          <what changed at which owning layer and why>
Regression:   <test/..._test.dart ("<name>")> -> FAIL (exit 1) with fix undone, PASS (exit 0) with fix
Evidence:     <rows per evidence-standard: regression red/green, module suite, dart format, flutter analyze>
Ruled out:    H2 (<why>), H3 (<why>)
Debug tags:   rg -n "DEBUG-|print\(|debugPrint\(|debugger\(" lib test -> 0 matches (PASS)
```

---

## 4. Review Severity (`BLOCKER` / `MAJOR` / `MINOR`)

Code Reviewers grade debugging fixes on the unified 3-tier scale (`shared_contracts/flags_and_statuses.md` §2):

| Severity | Finding | Review Verdict Impact |
|---|---|---|
| `BLOCKER` | Any green-washing (`D9`); missing Red-to-Green regression test (`D8`) where a seam exists; leftover `[DEBUG-xxxx]`, `print()`, `debugPrint()`, or `debugger()` (`D11`); editing/copying read-only foundation package code; unapproved contract/design/dependency change (`D12`); any check `FAIL`s | `CHANGES_REQUESTED` (blocks approval) |
| `MAJOR` | Symptom patched in the widget (`?? ''`, magic offset) instead of the owning mapper/state/layout layer (`D6`, `D7`); sibling bug in the same diff left unfixed (`D6`); missing or incomplete Debug Report block (`D14`) | Must be fixed in the same phase scope |
| `MINOR` | Minor regression test description or report formatting improvement | Optional (never blocks approval) |
