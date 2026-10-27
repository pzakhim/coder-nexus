# External Structured Core & Design Token Contracts

> Topic: Mandatory reuse of client `lib/core/`, `lib/shared/`, base classes, and design tokens

This reference enforces **C1** (One concept, one place), **C4** (No swallowed errors), **C7** (No magic values), and **C11** (Workspace contracts win) when the workspace profile is **`external-structured`**.

---

## 1. Honor the Client Core Mapping (**C1**, **C11** — `BLOCKER` / `MAJOR` on violation)

- **Reuse Established Client Bases**: Before writing any screen, state holder, repository, or network wrapper under `lib/features/<module>/` (or `lib/modules/<module>/`), check the `Client Core Mapping` table in `design.md` and inspect `lib/core/` and `lib/shared/`.
- **No Competing Base Classes**: Never introduce a second base screen, result wrapper, failure hierarchy, or DI container when the client codebase already has an established pattern with real consumers.
- **No Unapproved iMESPro Imports**: Do not introduce `BaseScreen`, `DataState`, `ApiService`, or `AppLogger` from company templates unless the client repository itself defines those symbols.

---

## 2. Client UI Kit & Theme Token Reuse (**C1**, **C7** — `MAJOR` on violation)

- **Shared Widgets First**: Reuse the client's existing shared buttons, inputs, dialogs, and error/loading states before creating feature-local widgets.
- **Design Tokens**: Reference the client's established theme extensions, color palette, typography, and spacing constants instead of hardcoding `Color(0xFF...)` or raw numeric sizes.

---

## 3. Error Translation & Logging (**C3**, **C4** — `BLOCKER` / `MAJOR` on violation)

- **Boundary Error Mapping**: Map data-source exceptions into the client's established `Result` / `Either` / `Failure` contract at the repository boundary.
- **Client Logger**: Route diagnostic and error logs through the client's configured logger service; never commit `print()` or `debugPrint()`.
