# 06 — Review severity

Reviewers grade violations on the rule-violation scale defined in [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md).

## Severity mapping

| Level | Criteria | Review outcome |
|---|---|---|
| **P1** | Violation of mandatory rules: pass-through wrapper (C1), compatibility alias (C1), dead/debug code (C2, C3), swallowed error (C4), broken contract (C11), skipped self-check (C14), mutable module global (C15), exposed internal helper (C16), or wildcard export (C17). | `CHANGES_REQUESTED` (blocks review approval). |
| **P2** | Maintainability or clarity risk: vague name (C5), function/file exceeding size threshold (C6), magic literal value (C7), missing type annotation (C9), drive-by edit outside scope (C10), hidden import side-effect (C12). | Finding recorded; must be addressed if inside task scope and straightforward; does not block review alone. |
| **P3** | Suggestion or documentation polish: redundant docstring (C8), mutable internal structure where frozen would be cleaner (C13). | Optional improvement; never blocks review. |

## Defect vs Rule Violation

- If a violation produces an incorrect result, data corruption, runtime crash, or security vulnerability, it is graded as a **Defect** on the `BLOCKER` / `MAJOR` / `MINOR` scale of `[handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md)`.
- Pure craft and maintainability issues that execute correctly are graded on the `P1` / `P2` / `P3` scale above.
- Reviewers evaluate only code modified in the current task or phase diff. Pre-existing legacy debt outside the diff is reported as an informational note, never a blocker.
