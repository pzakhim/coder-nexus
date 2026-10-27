# 02 — Five-Axis Flutter Review Rubric

> Topic: Grading the 5 Flutter review axes against pack rubric skills, AC traceability, Mockoon isolation, and runtime visual evidence (`R4`, `R5`)

## 1. The Five Review Axes (`R4`)

Grade changed code and broken callers against the Flutter pack's rubric skills:

| Axis | What to Audit | Rubric Skill | Typical `BLOCKER` / `MAJOR` Findings |
|---|---|---|---|
| **1. Correctness, AC Traceability & Mockoon Isolation** | Every applicable AC mapped to code + test/visual evidence; tasks in `phases/phase-NN-*.md` ticked `- [x]` with real `Evidence:`; locked decisions (`D-NN`) honored; zero `MockDataSource` classes inside `lib/`; `TEST-TAMPER-001` check | `incremental-implementation`, `{{slot:unit-testing}}` | Untraced AC (`BLOCKER`); contradicted `D-NN` (`BLOCKER`); `MockDataSource` committed in `lib/` (`BLOCKER`); happy-path-only tests or `TEST-TAMPER-001` (`BLOCKER`) |
| **2. Readability & Simplicity** | Names express business intent and match module conventions; direct control flow; no redundant pass-through wrappers, speculative abstractions, or dead code | `{{slot:clean-code}}`, `{{slot:code-simplification}}` | Swallowed errors returning fake empty success (`BLOCKER`); leftover `print`/`debugPrint`/`debugger()` (`MAJOR`); wrapper bloat (`MAJOR`) |
| **3. Clean Architecture, Screen Contract & DI** | Domain purity (`DOM-001..003`); Data error mapping & safe parsing (`DAT-003`); Presentation state immutability, screen contract ([03-screens-adding-and-splitting.md](../../clean-architecture/references/03-screens-adding-and-splitting.md)), cross-branch boundaries (`CRX-001..004`), and DI lifetimes (`DIR-001`) | `{{slot:clean-architecture}}` | Layer import breach (`BLOCKER`); screen contract or base inheritance breach (`BLOCKER`); screen-scoped Cubit registered as singleton (`MAJOR`) |
| **4. Security & Data Safety** | No hardcoded tokens, API keys, passwords, or PII in logs/source; encrypted storage for credentials; safe deep-link validation; TLS verification intact | `{{slot:secure-coding-standards}}` | Secret/token in code, logs, or `SharedPreferences` (`BLOCKER`); TLS `badCertificateCallback` bypass (`BLOCKER`) |
| **5. Performance, Lifecycle & Visual Quality** | Controllers, `FocusNode`s, `StreamSubscription`s, and `Timer`s disposed in `dispose()`/`close()`; no heavy computation or `Future` creation inside `build()`; runtime visual evidence matches approved UI/UX design | `{{slot:visual-quality}}`, `{{slot:ui-kit-mapping}}` | Undisposed controller/subscription leak (`MAJOR`); `setState` after `dispose` (`BLOCKER`); material visual deviation or `RenderFlex` overflow on target viewport (`BLOCKER` / `MAJOR`) |

---

## 2. Adversarial Test & Mockoon Isolation Audit (`R5`)

1. **Both Pass and Fail Scenarios Required:** Developer unit and cubit tests (`test/unit/`) must verify both **Pass/Default** (`200/201` data mapping & state emission) and **Fail/Edge** (`400/401/403/404/500`, network timeout, empty list `[]`, malformed/nullable JSON fields) scenarios from `design.md`. Happy-path-only unit tests block approval (`CHANGES_REQUESTED`, `BLOCKER`).
2. **Mockoon Isolation (`lib/` Purity):** Production code under `lib/` must connect through the real HTTP client/DataSource contract; committing hardcoded mock JSON or `Mock*DataSource` classes inside `lib/` is an immediate `BLOCKER`.
3. **Anti-Tamper (`TEST-TAMPER-001`):** Inspect `git diff` on `test/`. Deleting, skipping (`skip: true`), or weakening assertions to make a broken change pass is `TEST-TAMPER-001` (`BLOCKER`).

---

## 3. Runtime Visual & Foundation Reuse Audit

- **Foundation & Shared Widget Reuse:** Verify every row in the approved `Core usage` / `Client Core Mapping` table in `design.md` uses its mapped foundation component or shared widget rather than re-inventing duplicate widgets.
- **Visual Quality Gate (`{{slot:visual-quality}}`):** When a phase touches UI, inspect real runtime screenshots/recordings and device logs on `REVIEW_REVISION` against the approved Visual AC and HTML/Figma design across required states (loading, empty, error+retry, populated) and target viewports. Source declarations alone never prove visual rendering or orientation behavior.
