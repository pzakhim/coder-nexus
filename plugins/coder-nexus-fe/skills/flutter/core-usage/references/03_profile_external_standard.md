# Profile 3: External Standard (Vanilla / Minimalist)

Use only after Planning records this profile from actual Client evidence. Shared directories must have real consumers; empty folders do not select a profile. Downstream roles reuse the approved selection.


This profile activates when working on an **External Flutter Client** that has neither the iMESPro `app-*` packages nor an established, pre-existing core/shared framework (e.g. greenfield projects, simple apps, or vanilla Flutter repositories).

---

## 1. Activation Criteria

A project qualifies for **Profile 3 (External-Standard)** if:
1. The approved Client profile does not use company foundations; unrelated neighboring folders are irrelevant. Preserve an explicit approved selection and follow `core-usage` for evidence-based resolution.
2. The workspace lacks established shared base abstractions or central design system libraries.

---

## 2. Core Philosophy: Ponytail Minimalism & YAGNI

Under Profile 3, agents are liberated to create clean, standard implementations, but MUST adhere to the **Ponytail Approach**:
- **Solve the current problem with the smallest clear change.**
- **Standard Library & Framework First:** Prefer standard Flutter widgets (`StatefulWidget`, `StatelessWidget`, `ElevatedButton`, `TextFormField`, `CircularProgressIndicator`) over heavy custom frameworks.
- **YAGNI (You Aren't Gonna Need It):** Never build a speculative `lib/core/` or complex architectural wrappers "just in case" future features might need them.

---

## 3. Implementation Rules

### A. Feature-First Clean Architecture
Use only the layers needed by the approved behavior. This optional layout illustrates a complete flow; do not scaffold empty folders, pass-through use cases, Cubit or DI solely to match it:
```text
lib/modules/<feature>/
├── domain/
│   ├── entities/       # Pure Dart business objects
│   ├── repositories/   # Abstract contracts
│   └── usecases/       # Focused single-responsibility operations
├── data/
│   ├── models/         # Data transfer objects & JSON mappers
│   ├── datasources/    # Remote or local data fetching
│   └── repositories/   # Implementation of domain repository contracts
└── presentation/
    ├── bloc/ (or cubit/) # State management
    ├── screens/          # Screen destinations (Stateful/StatelessWidget)
    └── widgets/          # Feature-specific reusable UI components
```

### B. UI & Component Rules
- Build custom UI components directly under `lib/modules/<feature>/presentation/widgets/`.
- If an existing standard community package is already in `pubspec.yaml` (e.g. `flutter_bloc`, `dio`, `http`), utilize it cleanly without creating redundant wrappers.
- If two or more distinct features eventually require the exact same utility or component, promote it to a shared folder (e.g. `lib/commons/`) with clear documentation.

---

## 4. Role Playbook

1. **Planning (Tech Lead):**
   - Keep `design.md` lean.
   - Specify standard Flutter widget trees, only the state management needed by the behavior, and verified API contracts.
   - Do not require `BaseScreen` or iMESPro specific bases.
2. **Code Writer:**
   - Full right to construct clean, idiomatic Flutter widgets and business logic.
   - Write readable, maintainable, and testable code without unnecessary boilerplate.
3. **Code Reviewer:**
   - Review code for simplicity, clarity, layer boundaries, and null safety.
   - Ensure no unnecessary dependencies or over-engineered abstractions were introduced.
4. **Test Runner:**
   - Run standard Flutter widget tests and integration tests directly against the implemented screens and widgets.
