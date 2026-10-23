# 01 - When to Simplify & Scope Discipline

Simplification improves readability, maintainability, and runtime performance without altering behavior.

## 1. When to Simplify

- **During Implementation:** When writing new widgets, use `app_ui_kit` components directly instead of assembling primitive `Container`s.
- **During Self-Check:** Review the newly written code for helper methods, deeply nested layouts, and repetitive null checks before requesting review.
- **During Review:** Reviewers flag unnecessary boilerplate, non-const widgets, and reinvented components.

## 2. Scope Discipline (Zero Drive-by Refactoring)

- **Rule:** Simplify **only** files touched as part of the current phase task.
- Do not refactor untouched legacy files or screens outside the task scope.
- If you notice heavy technical debt outside the task scope, record it as a Concern in the task handoff instead of modifying the file.
