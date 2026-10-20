---
name: clean-code
description: Applies readable, maintainable Dart and Flutter coding practices within an approved task scope. Use while implementing or reviewing Flutter code; project and Senior contracts take precedence over generic clean-code preferences.
---

# Flutter Clean Code

Improve clarity without changing the approved architecture or inventing new abstractions.

- Follow the Client workspace's naming, state, error, DI, routing, and formatting conventions.
- Use intention-revealing names, focused functions/classes, explicit control flow, immutable state, and visible side effects.
- Prefer existing utilities and direct code. Extract shared behavior only when current duplication or ownership justifies it.
- Preserve `DataState`/`ErrorEntity`, nullability, lifecycle, and package contracts. Generic advice such as “always throw” or “never return null” does not override verified project contracts.
- Keep comments for non-obvious reasons and external constraints; express ordinary behavior in code.
- Do not broaden file scope, modernize adjacent code, add dependencies, or weaken validation/error handling.
- Run formatter/analyzer and the task's targeted tests before claiming completion.

Use `flutter-code-simplification` only when working behavior remains harder to understand than necessary.
