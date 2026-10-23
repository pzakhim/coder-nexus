# Client Cross-Branch Boundary Checklist

Apply the approved profile through [core-package-usage](../../core-package-usage/SKILL.md). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

Inspect the real Client checkout and exact `BASE_REVISION` → `REVIEW_REVISION` diff, including relevant uncommitted changes.

| Rule | Boundary | Evidence | Response |
|---|---|---|---|
| `CRX-001` | No imports of another module's private Presentation | Inspect changed imports under `lib/modules/`. | Use an approved shared widget or public contract. |
| `CRX-002` | No direct use of another module's DataSource, DTO or RepoImpl | Inspect imports of another module's `data/`. | Consume its Domain contract instead. |
| `CRX-003` | Inter-module behavior uses published UseCase or shared contract | Trace DI and consumers for actual dependencies. | Remove private implementation coupling. |
| `CRX-004` | Module DI is anchored in the composition root | Inspect `di.dart` and `lib/modules/modules_di.dart` if changed. | Register the approved module once in the verified boot order. |

Use `git diff --name-only <BASE_REVISION>..<REVIEW_REVISION>`, `git diff --name-only` and `git diff --cached --name-only` to identify the full scope. Run the Client's configured Flutter analyzer. Do not infer cross-file correctness from the Hub's file-level lexical validator.
