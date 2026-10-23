# 03 — Review Definition of Done (DoD) and Developer Testing

Use a screenshot-comparison harness only when approved and already available, or when its dependency addition is explicitly approved. Screenshot-comparison evidence supplements required runtime checks; it never proves live integration. Follow `{{slot:visual-quality}}` and the shared handshake evidence policy. The concrete stack commands and tools for this DoD are in `{{slot:verification}}` and `{{slot:unit-testing}}`.


Guide for Verification and DoD design in `implementation-plan.md`.

## 1. Tech Lead's Definition of Done for Code Review
The Planning Agent establishes the technical quality gates that `code_writer` must pass before requesting review:
- **Static Analysis Gate**: the stack's analyzer runs on affected files with 0 warnings, 0 errors, and 0 linter violations.
- **Developer Unit Tests**:
  - Entity & Mapper unit tests: Verify transformation logic and null-safety.
  - UseCase unit tests: Verify delegation to Repository with mock parameters.
  - State-holder unit tests: Verify the expected sequence of state emissions with the stack's state test tooling.
- **Screen Visual Review Gate (Mandatory for Screen Phases)**:
  - If a phase creates or modifies a Screen (`UI Impact: Yes`):
    - `code_writer` authors a screenshot test with the stack's approved harness covering the 4 visual states (Default, Loading, Empty, Error).
    - `code_writer` generates reviewed baseline `.png` artifacts with the harness's baseline command.
    - `code_reviewer` inspects the rendered `.png` images against `design.md` and the approved profile’s design-system guidance to verify visual fidelity, layout integrity, touch targets, and contrast before approving the phase.

## 2. Distinction between Developer Testing and QA Testing
- **Planning owns Developer Review DoD**: Specifies unit and state tests required from Coder before submitting to Reviewer.
- **Test Runner owns Independent QA Testing**: Test Runner designs test cases independently based on `requirements.md` and BDD scenarios. Planning does NOT dictate QA verification.
