# Canonical Flags, Statuses, and Severities (`coder-nexus`)

Single Source of Truth (SSOT) for all status words, severity levels, verdicts, tool check results, and integration flags across `coder-nexus` agents, core skills, pack skills, and Skill Factory generators.

> **Rule for skill and agent authors**: Never invent ad-hoc status tokens, priority-as-severity scales (`P1`/`P2`/`P3` for code findings), or softened status phrases ("mostly passing", "approved with minor notes"). Always reference and use the exact tokens defined in this file.

---

## 1. Tool & CLI Check Gate Results (`PASS` / `FAIL`)

Automated CLI checks (linter, formatter, static analyzer/type checker, architecture import linter, test runner, security audit, and MCP validators configured by the active stack pack) are **deterministic and binary**:

| Flag | Meaning | Rule |
|---|---|---|
| `PASS` | Command executed on the target revision and exited with `0` | Must include command, working directory, revision, and key output in the evidence row. |
| `FAIL` | Command executed and exited with non-zero (`exit != 0`) | Blocks handoff (`READY_FOR_REVIEW`), review (`APPROVED`), and acceptance (`ACCEPTED`). Must be fixed before proceeding. |
| `BLOCKED` | Tool or environment cannot run due to an external blocker outside the agent's authority | Never counts as `PASS`. Must name the exact blocker. |
| `NOT_RUN` | Check was not executed | Never counts as `PASS`. |
| `UNVERIFIED` | Claim made without an executed command or verifiable evidence row | Treated as a failure to verify; never counts as `PASS`. |

---

## 2. Finding Severity (`BLOCKER` / `MAJOR` / `MINOR`)

A **single unified scale** applies to **every** code finding—whether raised as a behavioral defect (bug-hunt, QA) or as a design/architecture/clean-code/security rule violation (Code Writer self-check, Code Reviewer):

| Severity | Definition | Verdict Impact |
|---|---|---|
| `BLOCKER` | 1. **Behavioral / Security defect**: Data loss/corruption, security vulnerability, crash/hang, or broken acceptance criterion (`AC-NN`).<br>2. **Failed tool gate**: Any required lint, type, format, architecture, or unit test CLI check exiting non-zero.<br>3. **Mandatory design rule violation**: Violation of a core rule in `clean-code`, `clean-architecture`, or `secure-coding-standards` (e.g., pass-through wrapper/alias, swallowed error, mutable module global, exposed internal helper, layer boundary breach). | **Blocks approval** (`CHANGES_REQUESTED`, or `BLOCKED` if `PLAUSIBLE` pending named evidence). |
| `MAJOR` | 1. **Edge-case defect**: Incorrect behavior or resource leak on a realistic edge path (empty state, retry, pagination boundary, slow network).<br>2. **Maintainability risk**: Structural smell or localized complexity not yet caught by CLI linters that degrades readability or testability. | Must be fixed in the same revision when inside the phase's `Scope / Files` and straightforward; if confirmed on an edge path, triggers `CHANGES_REQUESTED`. |
| `MINOR` | Cosmetic polish, naming nuance, or optional refactoring suggestion that does not affect correctness, architecture, or maintainability. | Non-blocking (`Optional`); never blocks `APPROVED`. |

> **Deprecated**: Do **not** use `P1` / `P2` / `P3` to grade code review or clean-code findings. (`P1`–`P3` is reserved strictly for test-case execution priority order in `quality-acceptance` when ordering test runs).

---

## 3. Finding Confidence (`CONFIRMED` / `PLAUSIBLE`)

Used alongside `BLOCKER` / `MAJOR` / `MINOR` during `bug-hunt` and `code-review`:

| Flag | Meaning |
|---|---|
| `CONFIRMED` | Proven end-to-end by code trace, reproduction test, or CLI command output. |
| `PLAUSIBLE` | Concrete failure scenario identified (`given … → when … → then …`), naming the exact check or evidence needed to confirm or refute it. |

---

## 4. Agent Return & Handoff Statuses

| Status Flag | Returned By | Meaning |
|---|---|---|
| `READY_FOR_SPEC` | Designer | UI/UX design package (`design-uiux/`) validated and approved for Spec Writer. |
| `READY_FOR_PLANNING` | Spec Writer | Gate 1 approved (`requirements.md`, `codebase-notes.md`, `change-impact.md` for `v2+`, 0 `OPEN` `Q-NN`). |
| `READY_FOR_VERIFICATION` | Spec Writer | Findings-only / verification item ready for Test Runner (no code phases). |
| `BRANCH_READY` | Spec Writer (`git-preflight`) | Work branch created/switched from the approved base and recorded in `D-NN`. |
| `APPROVED_FOR_BUILD` | Coordinator | User approved Gate 3; specs and plan are frozen. |
| `READY_FOR_BUILD` | Planning | Gate 3 approved; names the next phase for Code Writer to execute. |
| `AMENDED` | Planning | Approved `TASK_DETAIL` plan change (`PCR-NN`) logged; build resumes. |
| `ESCALATED` | Planning / Bug Fixer | Change requires Gate 2 (`DESIGN_CHANGE`), Gate 1 (`SCOPE_CHANGE`), or L3 bug escalation to `dev-team`. |
| `SKIPPED` | Designer / Planning | Step does not apply to this work item `Type`; reason recorded. |
| `READY_FOR_REVIEW` | Code Writer / Docs Writer | All tasks matched (`MATCH`), tool gates `PASS` on a committed revision, `writer-handoff.md` written. |
| `RECORDED` | Docs Writer | Phase or final QA evidence rows recorded in `as-built.md` / `verification.md`. |
| `NEEDS_CONTEXT` | Code Writer | Required input missing from handoff; lists what was checked and what is needed. |
| `BLOCKED` | Any Agent | Cannot proceed without external authority, environment, or `PCR-NN` resolution. |

---

## 5. Review & Acceptance Verdicts

| Verdict Flag | Owner | Meaning |
|---|---|---|
| `APPROVED` | Code Reviewer | Phase revision passes all tool gates and has zero `BLOCKER` (and zero unaddressed in-scope `MAJOR`) findings. |
| `ACCEPTED` | Test Runner | All in-scope `AC-NN` pass acceptance verification on the approved revision. |
| `CHANGES_REQUESTED` | Code Reviewer / Test Runner | One or more `BLOCKER` or `MAJOR` findings/defects require code fixes on a new revision. |
| `BLOCKED` | Code Reviewer / Test Runner | Verification cannot run due to environment, missing artifact, or `PLAUSIBLE` `BLOCKER` awaiting evidence. |

---

## 6. Task Execution, Review Reply & Plan Change Flags

| Category | Flags | Owner & Meaning |
|---|---|---|
| **Task Check Triage** | `MATCH` \| `CODE_WRONG` \| `PLAN_WRONG` | **Code Writer**: Task output matches `Expected` (`MATCH`), implementation is wrong (`CODE_WRONG`), or the plan's expectation contradicts reality (`PLAN_WRONG` → raise `PCR-NN`). |
| **Phase-00 Task Tick** | `[EXECUTE]` → `[x] PREPARED / COMPLETED` | **Planning / Code Writer**: Marks readiness & contract preparation tasks in `phase-00-prepare.md`. |
| **Review Finding Reply** | `FIXED` \| `DISPUTED` \| `RAISED` | **Code Writer** (round 2+): Fixed on new revision (`FIXED`), technical rebuttal with evidence (`DISPUTED`), or escalated as `PCR-NN` (`RAISED`). |
| **Plan Conflict** | `PLAN_CONFLICT` | **Code Reviewer / Test Runner**: Finding where the right fix requires changing the approved plan. |
| **Plan Change Class** | `TASK_DETAIL` \| `DESIGN_CHANGE` \| `SCOPE_CHANGE` | **Planning**: Scope of a `PCR-NN` change request. |

---

## 7. API & Mockoon Integration Mode Flags

Defined in [`api_handshake_protocol.md`](api_handshake_protocol.md):

| Mode Flag | Pack | Meaning |
|---|---|---|
| `FE_MOCKOON` | Frontend pack (FE) | Frontend runs against local Mockoon CLI (`mocks/<feature>_mockoon.json`) simulating Backend APIs. |
| `BE_LIVE` | Frontend pack (FE) / Backend pack (BE) | Frontend connects to live Backend API endpoints after contract alignment. |
| `3RD_PARTY_MOCKOON` | Backend pack (BE) | Backend runs against local Mockoon CLI (`mocks/<provider>_mockoon.json`) simulating outbound 3rd-party APIs (payment, SMS, OAuth, ERP, webhooks). |
| `READY_FOR_INTEGRATION` | Both | Phase-00 contract and mock verification passed (`exit 0`). |

---

## 8. Debug & Bug-Fix Workflow Flags (`defect-resolution` / `debug-investigation`)

| Category | Flags | Meaning |
|---|---|---|
| **Bug Impact Severity** | `S1` \| `S2` \| `S3` \| `S4` | Ticket-level production impact classification at intake (`S1` critical outage → `S4` trivial). |
| **Fix Routing Level** | `L1` \| `L2` \| `L3` | `L1`: single-file localized fix (`bug_fixer` → `test_runner`, no review).<br>`L2`: multi-file/module fix (`bug_fixer` → `code_reviewer` → `test_runner`).<br>`L3`: architectural/spec change needed (escalate to `dev-team`). |
| **Debug Lifecycle Status** | `TRIAGED` \| `NOT_REPRODUCED` \| `DIAGNOSED` \| `VERIFIED_FIXED` \| `STILL_BROKEN` | Status progression for `.superpowers/debug/<bug-slug>/` items. |
