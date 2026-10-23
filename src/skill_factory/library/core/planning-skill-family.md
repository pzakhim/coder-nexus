# The Spec & Planning skill family

Rules shared by the Planning Package generators (Spec Writer and Planning roles). Factory skills live in `.agents/skills/` and are owned by the workspace (see [workflow.md](workflow.md) Step 0).

## Generic generators, specific skills

A generator is written for **every** workspace. It names the *kind* of information to find and *how* to find it; it never assumes a domain (no warehouses, invoices, patients or tenants as if every project had them). The generated skill holds the workspace's real entities, roles, data scopes, ticket IDs and commands, found in the repository and confirmed by the user.

| In the generator (same for every workspace) | In the generated skill (one workspace) |
|---|---|
| "Find the columns or conditions that limit who sees which data" | "Rows are filtered by `<real column>`; role `<real role>` sees only …" |
| "List the entities that have a status and how it changes" | "`<Real entity>`: Draft → Approved → …" |
| Examples with neutral names (`Order`, `ABC-123`, `<scope>`), marked as illustrations | Examples taken from the workspace's own code, tickets and approved specs |

If a category does not exist in the workspace (no data scopes, no translations, no external consumers), the generated skill says so in one line instead of inventing content.

## The fixed pack keeps the process

Coder Nexus' fixed skills own the process; workspace skills add content inside it and never weaken it.

| Fixed pack owns (never changed by a workspace skill) | Workspace skill adds |
|---|---|
| Gates 1/2/3; `grilling` (draft first, confirm every inference, Q-NN → D-NN, one question at a time, 0 open questions); `requirements-elicitation` (sources, job type, G-NN, non-goals) | Domain words, entities, roles × scopes, business rules |
| `work-item-contract`: folder/file contract and templates `requirements.md`, `codebase-notes.md`, `design.md`, `implementation-plan.md`, phase files, `change-impact.md` | Question bank, mandatory edge cases, AC style, vague words, change deltas |
| `gate-review` (validators first, mode checklist, severities, findings → Q-NN); `cold-reader-check`; `solution-options` (2–3 options → D-NN) | Workspace review questions for `gate-review` spec mode, synonyms to avoid |
| Validators (`validate_proposal_spec`, `validate_plan_slices`, `validate_ux_design`) and the sections they check | Phase order, task shape, real check commands, PHASE-00 items |
| PHASE-00, AC → phase coverage, vertical behavior slices | API conventions, impact tracing and regression selection |

A workspace skill that would drop a gate, rename a validated section or replace a `grilling` law is wrong; adapt the content instead.

## Ownership

| Skill (`.agents/skills/<name>/`) | Answers | Used by | Adds to fixed skill |
|---|---|---|---|
| `domain-knowledge` | What the words mean, which entities exist and how their status changes, who may do what on which data, where each business rule lives | Spec Writer, Designer, Planning, Quality Engineer, Code Reviewer | `grilling`, `requirements-elicitation`, `gate-review` (synonyms to avoid) |
| `requirements-specification` | Where requirements come from, what to ask, which edge cases are mandatory, how BR, AC and change deltas are written, what the Gate 1 review asks | Spec Writer | `grilling`, `requirements-elicitation`, `gate-review` spec mode, `requirements.md` template (`work-item-contract`) |
| `change-impact-analysis` | What a change to existing behavior touches, with evidence, and which regression tests follow | Spec Writer, Planning, Code Reviewer | `change-impact.md` template (`work-item-contract`) |
| `implementation-planning` | Phase order inside a behavior, task shape, real checks, PHASE-00 items, Definition of Done | Planning | `implementation-planning` |
| `api-contract-design` | API naming, response and error shape, pagination, auth and scopes, compatibility, how clients consume and mock | Planning, Code Writer, Code Reviewer | `{{slot:architecture-design}}` API section, backend `api-contract-design` |

**Who wins on conflict:** approved decisions (`D-NN`) and the approved documents of the work item win over every skill for that item. Then `domain-knowledge` wins on meaning (terms, entities, scopes); `api-contract-design` wins on API shape; `implementation-planning` wins on task order; `requirements-specification` owns the delta vocabulary (ADDED / MODIFIED / REMOVED) that `change-impact-analysis` fills with evidence. Cross-family: `git-workflow` owns branches and versions; `clean-architecture` owns where files go; `secure-coding-standards` owns how authorization is enforced; `quality-planning` owns test cases (it receives the regression list from `change-impact-analysis`).

## Shared vocabulary

| ID | Meaning | Defined in |
|---|---|---|
| `G-NN` | Confirmed outcome goal | `requirements.md` → Goals |
| `BR-NN` | Business rule | `requirements.md` |
| `AC-NN` | Acceptance criterion | `requirements.md` |
| `W-NN` / `S-NN` / `C-NN` | Workflow / screen / component of an approved UI design | `design-uiux/uiux.md` |
| `Q-NN` → `D-NN` | Open question → user-confirmed decision | `codebase-notes.md` |
| `PHASE-NN` | Approved plan phase | `implementation-plan.md` |
| ADDED / MODIFIED / REMOVED | Delta kind of an affected BR or AC in a change (`vN` of built behavior) | `change-impact.md` → AC delta, written as Add / Change / Remove (unaffected: Keep) |

Rule IDs inside generators use their own prefixes (`DK`, `RS`, `CX`, `IP`, `AP`) so they never collide with these.

## Linking

- Refer to siblings by path: `.agents/skills/<name>/SKILL.md`. If a sibling does not exist yet, write "not set up in this workspace".
- Fullstack: link the branch file when it exists (`references/be/…`, `references/fe/…`, see [layouts.md](layouts.md)).
- Coder Nexus fixed skills are base inputs for generators (P1), never runtime links from a workspace skill.

## Facts and their labels

| Label | Means |
|---|---|
| `VERIFIED` | Read from the repository; the path (and symbol) is given |
| `CONFIRMED` | Stated by the user at the gate or in an approved document |
| `OPEN` | Not known yet; listed so the next work item asks it |

Never write an inferred rule as `VERIFIED` or `CONFIRMED`. Volatile facts (counts, customer lists, current versions) are linked to their source instead of copied.
