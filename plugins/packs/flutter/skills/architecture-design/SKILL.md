---
name: architecture-design
description: Flutter Gate 2 architecture design for Flutter / Dart applications - guides the 6-anchor read-only codebase scan, evidence-based architecture_profile resolution, Socratic grilling and D-NN decision locking in codebase-notes.md, the straight-line 7-section technical architecture specification (design.md), Mockoon Trigger & Test Data Table, UI component mapping across 4 visual states, and PHASE-00 readiness. Use when Planning acts as Frontend Tech Lead / Solution Architect for a Flutter work item.
---

# Architecture Design — Flutter / Dart

Used by `planning` acting as **Frontend Tech Lead / Solution Architect**. Core process and statuses come from [work-item-contract](../work-item-contract/SKILL.md), [gate-review](../gate-review/SKILL.md), and [implementation-planning](../implementation-planning/SKILL.md); layer rules from `{{slot:clean-architecture}}`. Profile-specific foundation policies (`imespro`, `external-structured`, `external-standard`) are loaded from the active workspace profile guide.

## 1. Pre-Design & Gate 2 Verification Gates (`PASS` / `FAIL`)

| Gate | Command / MCP Tool | Pass Criteria |
|---|---|---|
| **Developer Toolset Check** | `coder-nexus setup tools --pack flutter --check` | `PASS` (`TOOLS: READY`) |
| **Module Structure Blueprint** | `get_project_structure(scope="module", feature_name="<feature>")` | `PASS` (authoritative target layout retrieved) |
| **UX Error Taxonomy Lookup** | `get_ux_error_patterns` | `PASS` (standard 401/400/timeout/500 patterns retrieved) |
| **Proposal Spec Validator** | `validate_proposal_spec` on `codebase-notes.md` & `design.md` | `PASS` (`valid: true`, 0 `OPEN` `Q-NN`) |

`NOT_RUN`, `BLOCKED`, and `UNVERIFIED` never count as `PASS`.

## 2. Input Contract & 6 Codebase Intelligence Anchors

Before drafting `design.md`, verify `requirements.md` and `codebase-notes.md` are approved at Gate 1 (`G-NN`, `BR-NN`, `AC-NN`, `D-NN` locked), then execute the 6-anchor read-only scan ([01 — Context Scan & Decisions](references/01-context-scan-and-decisions.md)):

```text
Workspace Client Root
├── pubspec.yaml                       ──> 1. Flutter/Dart SDK, state management, router, DI, HTTP client, resolved foundation packages
├── Foundation / Shared Core           ──> 2. Active architecture_profile (company packages, lib/core/ & lib/shared/, or vanilla Flutter)
├── Client Router                      ──> 3. Route table, route arguments, pop return value conventions
├── Client DI Entry                    ──> 4. Service locator / provider wiring, factory vs singleton scopes
├── lib/modules/<feature>/ + shared    ──> 5. Existing module code and shared widgets (lib/commons/widgets/) to reuse first
└── MCP Tool: get_ux_error_patterns    ──> 6. Standard UX error handling patterns (401, 400/422, timeouts, 500)
```

## 3. Mandatory Architecture Design Rules (`AD1`–`AD10`)

| ID | Rule | Reference |
|---|---|---|
| **AD1** | **Evidence-based profile & verified facts:** Resolve `architecture_profile.mode` once from real Client evidence and record every verified path/symbol in `codebase-notes.md` §3. | [01 — Context Scan & Decisions](references/01-context-scan-and-decisions.md) |
| **AD2** | **Scope classification (`INIT` / `EXTEND` / `CORE IMPACT`):** Classify upfront; `EXTEND` preserves the existing module's state and folder conventions (`C11`). | [01 — Context Scan & Decisions](references/01-context-scan-and-decisions.md) |
| **AD3** | **High-leverage `D-NN` decisions only:** Queue `Q-NN` → `D-NN` (1 question at a time via `ask_question`, `(Recommended)` first) only when independently built parts could choose incompatibly. | [01 — Context Scan & Decisions](references/01-context-scan-and-decisions.md) |
| **AD4** | **Minimal directory tree (`get_project_structure`):** Include only the folders under `lib/modules/<feature>/` required by the approved behavior; never create top-level `views/`. | [01 — Context Scan & Decisions](references/01-context-scan-and-decisions.md) |
| **AD5** | **Screen, routing, state & DI contract:** Specify destination screens (`*_screen.dart`) vs child widgets/dialogs, route args/pop results, state transitions, and factory vs singleton DI scopes. | [02 — Screen, State, API & UI](references/02-screen-state-api-and-ui.md) |
| **AD6** | **Backend API & Mockoon strategy (`BE_API_READY` / `MOCKOON_MOCKED` / `NONE`):** Agree with the user on Pass/Default (`200/201`), Empty (`[]`), and Fail (`400/401/403/500`) triggers; zero `MockDataSource` in `lib/`. | [02 — Screen, State, API & UI](references/02-screen-state-api-and-ui.md) |
| **AD7** | **Sequential UI reuse ladder & 4 visual states:** Map every UI need via the reuse ladder, document any justified `Core gap`, and define `Loading`, `Content`, `Empty`, and `Error` states. | [02 — Screen, State, API & UI](references/02-screen-state-api-and-ui.md) |
| **AD8** | **UX error handling & storage policy:** Map `401`, `400/422`, timeout, and `500` behaviors; use encrypted storage (`FlutterSecureStorage`) for tokens and purge caches on logout. | [02 — Screen, State, API & UI](references/02-screen-state-api-and-ui.md) |
| **AD9** | **`PHASE-00` readiness & delivery conventions:** Verify toolset, analyzer baseline, and `mocks/<feature>_mockoon.json` (`[EXECUTE]`) before `PHASE-01`. | [03 — Delivery Gates & Template](references/03-delivery-gates-and-template.md) |
| **AD10** | **One straight locked-in line (`validate_proposal_spec`):** Render `design.md` with 0 `OPEN` `Q-NN`, pass `validate_proposal_spec`, `gate-review`, and `cold-reader-check` before Gate 2 approval. | [03 — Delivery Gates & Template](references/03-delivery-gates-and-template.md) |

## 4. Reference Guides

| Guide | Topic |
|---|---|
| [01 — Context Scan & Decisions](references/01-context-scan-and-decisions.md) | Profile resolution, 6 codebase scans, `INIT`/`EXTEND`/`CORE IMPACT`, `D-NN` decision criteria, and target directory tree |
| [02 — Screen, State, API & UI](references/02-screen-state-api-and-ui.md) | Screen/routing/DI contract, state & domain flow, API/Mockoon strategy, UI component mapping & 4 visual states, and UX error/storage policy |
| [03 — Delivery Gates & Template](references/03-delivery-gates-and-template.md) | `PHASE-00` readiness, Gate 2 verification, downstream delivery conventions, and the copy-ready `design.md` template |
<!-- {{profile_references}} -->
