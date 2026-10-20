# 03 — Review Definition of Done (DoD) and Developer Testing

Use a golden harness only when approved and already available, or when its dependency addition is explicitly approved. Golden evidence supplements required runtime checks; it never proves live integration. Follow `visual-verification` and the shared handshake evidence policy.


Guide for Verification and DoD design in `implement-plan.md`.

## 1. Tech Lead's Definition of Done for Code Review
The Planning Agent establishes the technical quality gates that `code_writer` must pass before requesting review:
- **Static Analysis Gate**: `flutter analyze` runs on affected files with 0 warnings, 0 errors, and 0 linter violations.
- **Developer Unit Tests**:
  - Entity & Mapper unit tests: Verify transformation logic and null-safety.
  - UseCase unit tests: Verify delegation to Repository with mock parameters.
  - Cubit / Bloc unit tests: Verify expected stream of state emissions using `bloc_test`.
- **Screen Visual Review Gate (Mandatory for Screen Phases)**:
  - If a phase creates or modifies a Screen (`UI Impact: Yes`):
    - `code_writer` authors a Golden Test using `golden_screenshot` covering the 4 visual states (Default, Loading, Empty, Error).
    - `code_writer` generates baseline `.png` artifacts via `flutter test --update-goldens`.
    - `code_reviewer` inspects the rendered `.png` images against `design.md` and the approved profile’s design-system guidance (iMESPro: `app_ui_kit` GUIDE) to verify visual fidelity, layout integrity, touch targets, and contrast before approving the phase.

## 2. Distinction between Developer Testing and QA Testing
- **Planning owns Developer Review DoD**: Specifies unit and state tests required from Coder before submitting to Reviewer.
- **Test Runner owns Independent QA Testing**: Test Runner designs test cases independently based on `requirements.md` and BDD scenarios. Planning does NOT dictate QA verification.
