# Sources and Attribution

This skill adapts the clean-code standards from the following sources for Python/FastAPI backend services:

## Core and Generator Sources

| Source | Role / Topic | Adaptation |
|---|---|---|
| `src/skill_factory/library/generators/create-clean-code-skill` | Base rules C1–C17, thresholds, naming conventions, self-check flow | Adopted C1–C17 mapped onto Python idioms, ruff/mypy toolchain. |
| `plugins/core/skills/clean-code` | Core rules CC1–CC15, structure-rules checks | Replaced core CC numbering with generator C1–C17; mapped 1-to-1. |
| `plugins/packs/backend/skills/clean-code` (Phase 2 draft) | Python idioms, safe/unsafe patterns | Incorporated into `01-naming`, `02-size-and-structure`, `03-errors-and-logging`, `04-types-constants-comments`. |

## Standards and Upstream Conventions

- **PEP 8**: Style Guide for Python Code (naming, module conventions, indentation).
- **PEP 257**: Docstring Conventions.
- **Ruff**: Modern linter and formatter rules (`F`, `E`, `W`, `C901`, `PLR09xx`, `T10`, `T20`, `B006`).
- **Mypy**: Static type analyzer for Python 3.12+.
- **FastAPI / Pydantic v2**: Dependency injection, lifespan handlers, boundary schemas.
- **SQLAlchemy 2.x async**: Session lifecycle, explicit transactions, exception handling.
