# Convention Discovery, Naming Taxonomy & Self-Check Mapping

Stack-neutral guide for discovering a workspace's naming conventions and mapping `C1`–`C17` into deterministic CLI gates and `rg` audits.

---

## 1. Universal Naming Taxonomy (For `01-structure-naming-and-types.md`)

Sample 10–20 real files, types, and functions across the workspace's architectural layers before proposing the naming table. When existing code is consistent, codify what is already used; where drift exists, propose one canonical rule and record the drift.

| Symbol Category | What to Specify in `01-structure-naming-and-types.md` | Universal Anti-Patterns |
|---|---|---|
| **File / Module** | Case style (`snake_case`, `kebab-case`, etc.) and role suffix/prefix convention per layer. | Generic buckets (`utils`, `helpers`, `common`, `misc`, `manager`). |
| **Type / Class / Contract** | Case style (`PascalCase`) and role naming for domain entities, use cases, ports/interfaces, DTOs/models, state holders, and errors. | Ambiguous `*Manager`, `*Processor`, `*Data`, or arbitrary interface prefixes not used by the language standard. |
| **Function / Method** | Case style and verb-first convention (`create_`, `fetch_`, `validate_`, `map_`). | Vague verbs (`process`, `handle`, `doWork`, `executeData`). |
| **Boolean** | Predicate prefix (`is`, `has`, `can`, `should`). | Double-negative names (`isNotDisabled`, `disableNoCache`). |
| **Variable / Parameter** | Domain noun with explicit unit or semantic role (`timeoutSeconds`, `retryCount`, `tenantId`). | Single-letter names outside short loops, or generic `data`, `info`, `tmp`, `val`, `obj`. |
| **Constant / Enumeration** | Workspace constant casing (`UPPER_SNAKE_CASE` or language-idiomatic `lowerCamelCase` const) and typed enum convention. | Magic numbers or raw string literals scattered across logic. |
| **Private / Internal Symbol** | Language-native file/module-private visibility mechanism (leading `_`, unexported identifier, or `private` keyword). | Exporting single-file helpers as public symbols (**C16**). |
| **Test Case** | Behavior-and-condition naming pattern (`<unit>_<scenario>_<expectedResult>`). | Numbered or meaningless test names (`test1`, `testSuccess`). |

### Universal Domain Glossary Rules
- Use the workspace's domain glossary terms verbatim—never maintain two synonyms for the same domain concept in code.
- Never use temporal or position-based prefixes (`new_`, `old_`, `legacy_`, `v2_`) as permanent symbol names.

---

## 2. Deterministic Self-Check & `rg` Audit Framework (For `03-self-check-and-review.md`)

Inspect the workspace's configuration files, CI pipelines, and task scripts to populate the 5 standard verification gates. List only tools installed in the workspace (or approved by the user during Step 4).

### The 5 Standard Verification Gates

| Gate Category | Purpose | Outcome |
|---|---|---|
| **1. Formatter** | Verifies canonical code formatting across touched files without mutating files in check mode. | `exit 0` = `PASS`, `exit != 0` = `FAIL` |
| **2. Static Linter & Complexity Analyzer** | Enforces unused-code removal (**C2**), cyclomatic complexity and size limits (**C6**), and language lint rules. | `exit 0` = `PASS`, `exit != 0` = `FAIL` |
| **3. Static Type Checker** | Verifies full static type annotations and null/type soundness (**C9**). | `exit 0` = `PASS`, `exit != 0` = `FAIL` |
| **4. Pattern & Structure Audit (`rg`)** | Scans changed files with `ripgrep` (`rg -n`) for rules not covered by the static linter. | Zero unapproved violations = `PASS` |
| **5. Unit Test Runner** | Runs unit tests covering the modified modules (**C14**). | `exit 0` = `PASS`, `exit != 0` = `FAIL` |

### Mapping Rules to Automated Checks & `rg` Audits

| Rule | Verification Mechanism |
|---|---|
| **C2 (No dead code)** | Static linter unused-import / unused-symbol rules + `rg -n "TODO|FIXME"` on changed files. |
| **C3 (No debug leftovers)** | Static linter print/debugger rules + `rg -n "<language_debug_print_or_breakpoint_pattern>" <changed_files>`. |
| **C4 (No swallowed errors)** | `rg -n "<broad_or_empty_catch_pattern>" <changed_files>` to verify every catch block translates, chains, or logs the error. |
| **C6 (Size thresholds)** | Complexity/size linter metrics or line-count check on changed files. |
| **C9 (Full static types)** | Strict type-checker gate + `rg -n "<untyped_escape_or_ignore_directive>" <changed_files>`. |
| **C15 (Module-level purity)** | Inspect top-level declarations in changed files via `rg` to confirm no mutable runtime state is defined at module scope. |
| **C16 (Helper locality)** | For each new non-private helper (`rg -l "<symbol_name>" <src_dir>`), verify at least 2 files import it; reject new `utils`/`helpers`/`common` files. |
| **C17 (Explicit export surface)** | Scan package entry/barrel files with `rg` for wildcard re-exports, and verify every newly exported symbol has an external consumer. |
