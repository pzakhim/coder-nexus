# Base Rules (Generic, Every Workspace)

All rules `DK1`–`DK9` are **mandatory compliance** in every workspace. Each rule goes into the generated skill with the workspace's real facts and its rationale. If a workspace has no RBAC roles or data scopes, `DK3` is satisfied with a one-line `N/A for this workspace` entry rather than dropping the rule. Examples here use neutral names; the generated skill uses the workspace's own.

## 1. Mandatory Domain Knowledge Principles (`DK1`–`DK9`)

| # | Rule | Why | Reference Target |
|---|---|---|---|
| `DK1` | **One term, one meaning.** Each glossary row defines the term in the team's language, its code name(s), a one-line meaning, banned synonyms (`"Avoid saying"`), and a fact label (`VERIFIED`, `CONFIRMED`, or `OPEN`). `"Avoid saying"` is machine-checkable data: `gate-review` spec mode and CLI `rg` checks flag any listed synonym in goals, business rules, acceptance criteria, or scenarios. | Specs and code must name the same concept identically; a listed synonym can be checked deterministically. | `01-glossary-and-ubiquitous-language.md` |
| `DK2` | **Entity cards & lifecycles.** Each business entity documents its owning module, key fields, status values, allowed transitions, forbidden transitions, trigger actor/event, and enforcement location (`file:symbol`). | Status transitions and lifecycle boundaries are where specifications miss edge cases most often. | `02-entities-lifecycles-and-rules.md` |
| `DK3` | **Roles × scopes × actions matrix.** Document which role may perform which action on which data and the condition that limits visible/mutable rows (the data scope), read from permission checks and confirmed by the user. If the workspace has no RBAC roles or data scopes, document a one-line `N/A for this workspace` statement. | Permission and data-scope gaps cause the highest-impact security and authorization defects. | `03-roles-scopes-and-upkeep.md` |
| `DK4` | **Business-rule catalog.** Each domain rule records a stable ID (e.g. `BR-NN` / `DR-NN`), statement, enforcement location (`file:symbol`), source (document, ticket, or user), and fact label. | Planning updates a rule at its single enforcement point and prevents new specs from contradicting existing invariants. | `02-entities-lifecycles-and-rules.md` |
| `DK5` | **Labelled facts, zero invention.** Every entry carries `VERIFIED` (with `file:symbol` or path), `CONFIRMED` (user or approved document), or `OPEN` (unknown — must be asked). An inference is never recorded as a verified or confirmed fact. | An invented domain rule propagates false assumptions into requirements, design, and tests. | `SKILL.md`, `01`–`03` |
| `DK6` | **Link volatile facts.** Counts, customer lists, runtime configuration values, and current versions are linked to their authoritative source file or query, never copied inline. | Copied volatile numbers go stale silently. | `03-roles-scopes-and-upkeep.md` |
| `DK7` | **Same-work-item upkeep.** When a work item changes an entity, lifecycle transition, role, data scope, or business rule, the skill is updated in the same work item and recorded in the upkeep change log. | Domain knowledge must evolve lockstep with the codebase. | `03-roles-scopes-and-upkeep.md` |
| `DK8` | **Zero personal data or secrets.** Examples, glossary rows, and rules never contain real personal data (PII), credentials, tokens, or private customer identifiers. | The skill is committed to version control and shared across agents and developers. | `03-roles-scopes-and-upkeep.md` |
| `DK9` | **Challenge overloaded and fuzzy words.** When the user or a ticket uses an unlisted word, an overloaded word, or a banned synonym from `"Avoid saying"`, name the candidate glossary terms and ask which one (`Q-NN`, one question at a time, recommendation first); record the confirmed answer as `D-NN`. When a statement about behavior contradicts the code, raise a `Q-NN` quoting both. Add resolved terms to the glossary in the same work item (`DK7`). | Fuzzy words hide disagreements between stakeholders; comparing claims against code catches misremembered rules early. | `SKILL.md`, `01-glossary-and-ubiquitous-language.md` |

## 2. Deterministic CLI Verification Gates (`PASS` / `FAIL`)

Automated CLI checks return strictly `PASS` (exit code `0`) or `FAIL` (non-zero exit):

| Gate | Command Pattern | Enforces |
|---|---|---|
| Banned-synonym scan | `rg -n -i "(<avoid_saying_pipe_pattern>)" <spec_paths>` | `DK1`, `DK9` (`PASS` when 0 matches in active specs) |
| Unresolved `OPEN` fact check | `rg -n "\bOPEN\b" .agents/skills/domain-knowledge/` | `DK5`, `DK7` (surfaces unresolved items before Gate 1) |
| Secret & PII hygiene scan | `rg -n "(api_key|secret|password|token|@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})" .agents/skills/domain-knowledge/` | `DK8` (`PASS` when 0 matches) |

## 3. Unified Review Severity Scale (`BLOCKER` / `MAJOR` / `MINOR`)

Reviewers and `gate-review` grade domain-knowledge and specification alignment findings strictly on the 3-tier scale (`shared_contracts/flags_and_statuses.md`):

- **`BLOCKER`**: Invented unlabelled domain facts (`DK5`), real PII/secrets committed in the skill (`DK8`), unchallenged contradiction between spec claims and verified code (`DK9`), or missing/unconfirmed `Role × Scope × Action` matrix for a permission-sensitive change (`DK3`).
- **`MAJOR`**: Banned `"Avoid saying"` synonym used in goals, BR, AC, or scenarios (`DK1`), missing lifecycle transition or enforcement `file:symbol` on an entity card (`DK2`), or uncatalogued business rule modified without updating the skill (`DK4`, `DK7`).
- **`MINOR`**: Copied volatile count/config that should be a link (`DK6`), minor formatting drift in glossary or entity cards, or missing change-log entry when facts are otherwise accurate (`DK7`).
