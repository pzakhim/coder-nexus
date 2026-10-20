---
name: code-simplification
description: Simplifies recently changed Dart or Flutter code while preserving exact behavior. Use after implementation and targeted checks pass, or when review identifies concrete unnecessary complexity.
---

# Flutter Code Simplification

Simplify only the changed scope and only when the result is easier to understand.

1. Understand callers, side effects, error paths, lifecycle and tests before editing.
2. Identify a concrete issue: deep nesting, misleading names, duplication, dead code, or an abstraction that adds no current value.
3. Make one focused simplification. Preserve inputs, outputs, ordering, state transitions, error behavior, accessibility behavior and performance constraints.
4. Do not change tests to make the simplification pass. Do not remove checks, error mapping, DI boundaries or package contracts.
5. Re-run formatter/analyzer and affected tests. If behavior or public contracts change, stop treating the work as simplification and return to the relevant approval gate.

Skip this skill when code is already clear. Record unrelated cleanup as a separate task rather than expanding the current diff.
