# Five-Axis Code Review Rubric

Apply the approved profile through [core-usage](../../core-usage/SKILL.md). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

Review the approved feature version, phase and exact code revision before issuing a verdict.

## 1. Correctness and AC coverage

- Trace every applicable AC in `docs/features/<module>/<feature>/vN/requirements.md` and the linked phase to code and revision-bound evidence.
- Check relevant error, timeout, auth, empty, validation and recovery paths; do not require irrelevant states.
- Preserve the real DataSource → Repository → UseCase → state → UI contract where the behavior uses those layers. Do not hide required-data errors with fake empty values.
- Audit `test/` changes. Deleting, disabling or weakening assertions to make a defect pass is `TEST-TAMPER-001` and fails review. A legitimate test correction must match approved AC and receive review; a changed AC returns to its approval gate.

## 2. Readability and simplicity

- Use names that express business intent and the module's existing file/class conventions.
- Remove redundant wrappers, speculative abstractions and unrelated boilerplate.
- Keep control flow direct and functions focused; do not impose an arbitrary reuse count or line limit.

## 3. Clean Architecture and DI

- Domain stays independent of Flutter, Data and Presentation (`DOM-001..003`).
- DataSource and RepoImpl follow the verified `BaseDataSource`, `DataState<T>`, `tryCatch`/`tryCatchAsync` and parsing contracts (`DAT-001..003`).
- Presentation keeps state and side effects in their intended places; new state follows the Client's existing convention (sibling module), and existing modules keep theirs (`PRE-001..004`).
- Each affected screen follows `presentation/screens/*_screen.dart`, the verified Client `BaseScreen`/`BaseScreenState`, metadata/layout and router contract. Confirm dialog/widget exemptions from the real UI role (`PRE-005..006`, module naming). A missing active base API is `BLOCKED`.
- Check cross-module boundaries (`CRX-001..004`) and DI lifetimes (`DIR-001`) only where affected. A scoped UI-only phase does not require empty Domain/Data/DI files.

## 4. Security and data safety

- No embedded tokens, passwords, keys, fake service responses or sensitive logs.
- Verify input handling, safe parsing and masking of sensitive fields where applicable.
- Use the Client's logging abstraction rather than uncontrolled `print()`.

## 5. Performance and lifecycle

- Dispose controllers, focus nodes, subscriptions and other owned resources in the responsible lifecycle.
- Avoid expensive work in `build()` and unnecessary rebuilds; use `const`, `buildWhen` and `listenWhen` when they solve an observed issue.
- Compare visual evidence on the same revision with approved Visual AC; a material mismatch is `FAILED`.
