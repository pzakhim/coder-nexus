# 02 - Behavior Safety & Invariant Protection

Every simplification must preserve identical runtime behavior and layout fidelity.

## 1. Safety Invariants

1. **Pixel-Perfect UI Stability:**
   - Replacing custom widgets with `app_ui_kit` must preserve padding, alignment, and interactive tap targets.
   - Do not change visual layout without consulting the UI/UX specification.
2. **State & Lifecycle Invariants:**
   - Replacing `StatefulWidget` with `StatelessWidget` is only safe if the state was genuinely unused or completely managed by a Cubit.
   - Retain `SingleTickerProviderStateMixin` or controllers if local animations depend on them.
3. **Sound Null Safety Guarantees:**
   - Replacing verbose null checks with `?.` and `??` must retain the exact fallback values expected by downstream logic.

## 2. Verification Protocol

- Run unit tests before making structural simplifications.
- Make the simplification edit.
- Re-run `flutter test` to ensure zero regressions in logic or state transitions.
