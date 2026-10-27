# External Standard (Minimalist Flutter) Contracts

> Topic: Idiomatic Flutter SDK / Material 3 usage, Ponytail minimalism, and `shared/widgets/` reuse rules

This reference enforces **C1** (One concept, one place), **C4** (No swallowed errors), **C7** (No magic values), and **C11** (Workspace contracts win) when the workspace profile is **`external-standard`**.

---

## 1. Ponytail Minimalism & Clean Layering (**C1**, **C11**, **C16** — `MAJOR` on violation)

- **No Speculative Base Frameworks**: Do not invent generic `BaseScreen`, `BaseViewModel`, or abstract wrapper hierarchies for a vanilla Flutter project. Add only the layers required by the approved feature (`presentation/`, `domain/`, `data/`).
- **Promote Shared Widgets Only on Real Reuse**: Keep feature widgets private to `lib/modules/<feature>/presentation/widgets/`. Extract a widget to `lib/shared/widgets/` (or `lib/commons/widgets/`) only when **2 or more features** actively import it (**C16**).

---

## 2. Material 3 & Theme Token Discipline (**C7**, **C15** — `MAJOR` / `MINOR` on violation)

- **Theme Tokens Over Magic Values**: Resolve colors and text styles from `Theme.of(context).colorScheme` and `Theme.of(context).textTheme` rather than hardcoding `Color(0xFF...)` or inline `TextStyle` definitions.
- **Idiomatic Flutter Widgets**: Prefer standard Material 3 widgets (`FilledButton`, `OutlinedButton`, `TextFormField`, ` NavigationBar`, `showModalBottomSheet`) with `const` constructors before building custom equivalents.

---

## 3. Explicit Failure Handling & Structured Logging (**C3**, **C4** — `BLOCKER` / `MAJOR` on violation)

- **Typed Failure Mapping**: Convert network/storage exceptions at the repository boundary into explicit Dart 3 sealed classes or typed `Failure` records—never swallow errors with empty `catch (_) {}`.
- **No Debug Leftovers**: Use the project's configured logger (or `dart:developer` `log()` behind the project logger abstraction); never commit `print()` or `debugPrint()`.
