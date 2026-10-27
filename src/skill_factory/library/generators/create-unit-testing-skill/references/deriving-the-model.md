# Deriving the Unit Testing Model from a Workspace

Stack-neutral guide for discovering a workspace's test runner, directory tree, per-layer test matrix, doubles strategy, and CLI commands before authoring `.agents/skills/unit-testing/`.

---

## 1. Discovering the Test Setup (`EXTEND` vs `INIT`)

Inspect the workspace before proposing conventions:
- **Existing project (`EXTEND`):** The workspace's installed test runner, async plugin, mocking/faking library, directory layout, fixture files, and naming patterns always win. Document any legacy drift so new tests follow one clean standard without doing out-of-scope renames.
- **Greenfield project (`INIT`):** Propose the idiomatic test runner, directory tree mirroring source modules, and port-fake conventions for the stack.

| Discovery Target | How to Inspect |
|---|---|
| **Runner & Plugins** | Read dependency manifests and test configuration files for the test runner, async plugin, coverage plugin, and test-ordering plugin |
| **Directory Tree** | List test directories and compare against source directories to see how paths mirror modules (`├──`/`└──`) |
| **Doubles & Fixtures** | Search existing test helpers, shared fixture modules, builder functions, and port fakes/mocks |
| **Naming Convention** | Sample 10–20 existing test function/method names to identify the pattern (e.g., behavior + condition + expected result) |

---

## 2. Mapping Required Cases by Architectural Layer (For `01-test-matrix-and-structure.md`)

Map the workspace's architectural layers (from `clean-architecture` if present, otherwise its real source folders) into a per-layer unit test matrix. Every layer row must specify:
1. **Layer / Subject** and **Example Path**
2. **Boundary Doubled** (`none` for pure logic/models/mappers; port fakes or boundary mocks for use cases/services/controllers/state holders/adapters)
3. **Required Cases:**
   - **Pass/Default:** Valid inputs produce the expected return value, state transition, or port call, asserted field-by-field against literal design values.
   - **Handled Fail:** Each validation failure, not-found error, authorization/ownership refusal, state conflict, or upstream dependency error raises/emits the exact domain error or failure state without committing side effects.
   - **Empty / Edge:** Empty collections, `null`/missing optional fields, boundary numbers (`0`, `1`, max cap, negative), malformed payloads, and time/locale edge cases.
4. **What Is Not Unit-Tested Here:** Real database queries/migrations, live HTTP/gRPC endpoints, and pixel rendering (explicitly routed to integration, contract, or visual verification).

---

## 3. Doubles Hierarchy & Test Quality (For `02-doubles-fixtures-and-quality.md`)

Establish the workspace's test double hierarchy in strict order of preference:
1. **Real** collaborators for pure domain objects, value objects, policies, and mappers.
2. **Hand-written Fakes** (or typed interface mocks where idiomatic) at port boundaries owned by the application, preserving the port's exact contract and error types.
3. **Transport / Edge Stubs** at external HTTP/SDK boundaries.
4. **Never Doubled:** The subject under test (`U5`), authorization/ownership guards (`U6`), or real database sessions inside unit tests (`U4`, `U6`).

Include 2–3 concise, copy-pasteable code patterns in the workspace's actual language and test framework showing:
- Testing a use case / application service with a port fake/mock (both success and failure/rollback paths).
- Testing a schema / model / mapper with valid and boundary/malformed inputs.
- Testing a controller / router or presentation state machine (`Cubit` / `Bloc` / store) with boundary overrides.

---

## 4. CLI Commands & Red-to-Green Evidence (For `03-execution-boundaries-and-review.md`)

Verify that every command listed in the generated skill exists in the workspace and returns a deterministic exit code (`exit 0` = `PASS`, `exit != 0` = `FAIL`):

| Command Category | Purpose |
|---|---|
| **Focused Single Test** | Run one test function/case during the Red → Green loop (`U12`, `U14`) |
| **Collection / Verbose Check** | Prove the new test ID was collected and actually executed (not skipped or deselected) |
| **Module Test File** | Run all unit tests for the touched module after completing a task |
| **Full Unit Suite** | Run the entire unit test suite at phase end before hand-off |
| **Static Checks on Tests** | Run the workspace formatter, linter, and type checker on test files as well as production files |
