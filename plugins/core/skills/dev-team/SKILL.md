---
name: dev-team
description: "Coordinate the 7 Coder Nexus delivery agent profiles (Spec Writer, Planning, Code Writer, Code Reviewer, Test Runner, Bug Fixer, Docs Writer) from Gate 1 Huly + Figma/HTML-sitemap intake through architecture design, phased implementation, review, Hybrid E2E QA, and final as-built closure — supporting standard subagent mode (Gates 1-3) and optional Hybrid /swarm peer-to-peer mode (Phases 3-5)."
---

# Dev Team Coordinator

Act as the **Lead Coordinator** for one Client work item (`.superpowers/work-items/<slug>/vN/`). Read the user's request and supplied files (`spec.md`, `<feature>_spec.md`, Figma URLs, HTML sitemaps); Huly is optional and read-only. Inspect the actual Client workspace before assigning work.

Coordinate the **7 specialized agent profiles** in `agents/`:
- **Spec Writer** (`spec_writer`): Gate 1 intake (Huly, Figma/HTML sitemap, codebase) → `requirements.md`, `codebase-notes.md`.
- **Planning** (`planning`): Gate 2 `design.md`, Gate 3 `implementation-plan.md` + `phases/` + `test-plan.md` (`E2E-01..E2E-N`), and `L3` `PCR-NN` change control.
- **Code Writer** (`code_writer`): Single-instance sequential phase implementation (and amended `L3` task implementation).
- **Code Reviewer** (`code_reviewer`): Independent read-only per-phase, `[REVIEW_CHECKPOINT]`, and `L2`/`L3` verification.
- **Test Runner** (`test_runner`): Independent read-only Hybrid E2E `final_qa` (`E2E-01..E2E-N`, Fail-Fast, zero test-case tampering).
- **Bug Fixer** (`bug_fixer`): Resolves `FAILED_AT: E2E-i` defects in `final_qa` via `L1`/`L2` root-cause fixes or `L3` `PCR-NN` escalation.
- **Docs Writer** (`docs_writer`): Single final closure run producing visual `as-built.md` and updating `.superpowers/ux/`.

Read plugin-root `shared_contracts/api_handshake_protocol.md` for API/fixture decisions. Planning records the approved architecture profile once; later roles reuse it. Record each approval with work item, phase, and revision; never re-ask an already matching decision.

---

## Execution Modes (Standard Subagent & Hybrid `/swarm`)

- **Standard Subagent Mode (Default; mandatory for Gate 1–3):**
  - Dispatch ONLY the 7 plugin agents above via Antigravity `invoke_subagent` and continue an active role thread via `send_message`. Never `define_subagent` substitutes, impersonate roles, fake results, or self-approve gates. If an agent fails to start, stop as `BLOCKED — agent <name> failed: <error>`.
  - **Reuse vs Freshness:** Reuse `spec_writer`, `planning`, and `code_writer` across rounds within their phase via `send_message` to keep context warm. Spawn **fresh independent** `code_reviewer` and `test_runner` subagents per verification run so author reasoning never biases review or QA. (Pass 3 cold-reader uses `invoke_subagent`, or a temporary `swarm{action:"add"}` helper if a swarm is already active.)
  - **`ask_question` Ownership (2-Channel Grilling):** Direct `ask_question` belongs ONLY to the active user-facing conversation (Main Chat). When running subagents, Coordinator relays every gate and `Q-NN` in Main Chat: present analysis, visual flow, and options in session chat (`content`), then call 1 short 1-line `ask_question` with `(Recommended)` first. Never require the user to switch subagent threads.
- **Hybrid `/swarm` Mode (Optional for Phase 3–5 only):**
  - **Gates 1–3 always run in Standard / single-thread mode** so interactive grilling and user approval gates stay direct without Coordinator bounce-loop friction.
  - **Phases 3–5 (`/swarm` active):** Coordinator spawns roles just-in-time (`swarm{action:"add"}` for `code-writer`, `code-reviewer`, `test-runner`, `bug-fixer`, `docs-writer`) and kills each worker once its phase/job lands. Peers hand off directly via `@mention`: `@code-writer ↔ @code-reviewer` (clarifications, `READY_FOR_REVIEW`, `CHANGES_REQUESTED`), `@test-runner → @bug-fixer → @test-runner` (`L1`) or `@code-reviewer` (`L2`). Tag `@coordinator` **ONLY** on `APPROVED` phase/checkpoint, `ACCEPTED`, `BLOCKED`, 3-round escalation, or `PCR-NN` user gates.
  - **Workspace / Git Rule (`/swarm`):** For single-writer sequential phases, prefer `workspace:"inherit"` to avoid split-copy visibility drift. Whenever `code-writer` or `bug-fixer` runs in `workspace:"share"`, its commits and `.superpowers/` updates MUST be merged/landed onto the shared branch **before** waking `@code-reviewer` or `@test-runner` on `workspace:"inherit"`.

---

## Two Entry Paths into `dev-team`

- **Path A — Resume After Approved Gate 1 (`READY_FOR_PLANNING` + `BRANCH_READY` — Zero-Re-Ask):** When `vN/` already has Gate 1 approved (`requirements.md`, `codebase-notes.md` with `0 OPEN Q-NN`, `change-impact.md` for `v2+`, and the `git-preflight` branch), skip Phase 1 and start directly at Phase 2 (`planning`) without re-asking any `G-NN`, `BR-NN`, `AC-NN`, `W-NN`, `S-NN`, `C-NN`, or `D-NN`.
- **Path B — Full Entry (Huly / Figma / HTML Sitemap / Non-UI / Escalated L3 Bug):** Start at Phase 1 (`spec_writer`). For an escalated `bug-squad` report (`.superpowers/debug/<bug-slug>/escalation-report.md`, `ESCALATED`), pass it as verified baseline facts (**Zero-Re-Ask** of reproduction, root cause, and blast radius).

---

## Phase 1 — Intake, Goals & Gate 1 (`spec_writer` — Path B)

The Gate 1 flow lives in `spec_writer` §3 (`1A-P` → `1A` → `1A-0` → `1A-G` → `1B` → `1B-O` → `1A-UX` → `1C` → `1D-R` → `1D` → `1E`). Do not restate or reorder it. Spec Writer grills via 2-Channel Grilling (`grilling` Law 4 — analysis in session chat, one short `ask_question` at a time in Main Chat).

Coordinator duties in Phase 1:
1. **Start `spec_writer`** with the request, supplied files, Figma/sitemap inputs, and optional Huly ID (`huly-task-intake`, read-only; downloads in `.superpowers/sources/<ISSUE-ID>/`).
2. **API source** (recorded in `codebase-notes.md`): `BE_API_READY`, `MOCKOON_MOCKED` (`spec_writer` locks business I/O; `planning` designs the mock and `PHASE-00`), or `NO_EXTERNAL_API` (`PHASE-00` pre-ticked `[x] PREPARED (NO_EXTERNAL_API)`). Approved fixtures prove UI/contract checks only; live integration stays pending until checked against a real endpoint.
3. **Visual intake (`1A-UX`):** `spec_writer` runs `figma-intake` (`FIGMA_PROVIDED`, `HTML_SITEMAP_PROVIDED`, `CODEBASE_ONLY`, or `NO_UI_IMPACT`) without generating HTML mockups.
4. **Relay cross-agent questions (`1C`):** Route codebase/architecture queries to `planning` or `code_writer`, which appends evidence to `codebase-notes.md` and stops. Never fabricate answers.
5. **Gate 1:** Accept only after `0 OPEN Q-NN`, 3-pass `gate-review` (`modes/spec.md`; `NOT_RUN` is never `PASS`), explicit user approval of exact revisions (`requirements.md`, `codebase-notes.md`), and branch creation (`1E`). Stop until then.
6. **Verification item (`READY_FOR_VERIFICATION`):** Skip Phases 2–3; invoke `test_runner` on the named revision to write `verification.md`.
7. **Escalated bug:** Pass `escalation-report.md` read-only; `spec_writer` settles job type (`bugfix` vs `feature` with `change-impact.md`).

---

## Phase 2 — Architecture Design & Breakdown (`planning` → Gate 2 & Gate 3)

1. **Step 2A — Codebase Scan & Counter-Review (`grilling` mode `planning`):**
   - Resolve profile via `{{slot:architecture-design}}` and scan target module, router, state, DI, and reuse mapping.
   - **Boundary with `spec_writer`:** `spec_writer` owns business API I/O and screen/workflow UX requirements (from Figma or HTML sitemap via `figma-intake`); `planning` owns data pipeline, state/DI architecture, and `{{slot:architecture-design}}` component mapping.
   - **Hub-and-Spoke Counter-Review:** If `planning` detects a Core Risk/Gap, conflict with `requirements.md`, or multi-option trade-off, it queues `OPEN` `Q-NN` in `codebase-notes.md`. Coordinator relays to `spec_writer` via `send_message` to align 2–3 options (`(Recommended)` first), then follows **2-Channel Grilling** in Main Chat: summarize both technical and business perspectives + trade-offs in session chat (`content`), then call 1 short 1-line `ask_question`. Close `Q-NN → D-NN`, sync `requirements.md` if needed, and write straight-line `design.md`.
2. **Step 2B — API Strategy & Zero Cross-Repo Mutation:** For `MOCKOON_MOCKED`, design mock rules in `design.md` and allocate `PHASE-00` (`[EXECUTE]`). Feature phases call only the real remote data source (never fake data sources in Client source) and never mutate Backend repos or DB schemas.
3. **Step 2C — Gate 2 (`design.md`) & Gate 3 Steps 1–2 (`implementation-planning`):**
   - Write straight-line `design.md` citing `D-NN` (zero `Option A/B`, `Open Questions`, `TBD`), run 3-pass `gate-review` (`modes/design.md`), and obtain explicit user approval at **Gate 2** before planning phases. Keep `codebase-notes.md` permanently across `vN/`. Offer optional `architecture-decision-records` for hard-to-reverse `D-NN`.
   - **Gate 3 Step 1 — High-Level X-Phase Roadmap Lock FIRST:** Present *"Here is the X-phase roadmap"* (`PHASE-00` readiness + `PHASE-01..NN`, brief summary of each phase's deliverable, explicit `Scope in / Scope out`, and the Hybrid E2E strategy choice: live `E2E-01..N` only vs optional local `integration_test/` tasks for `code_writer`) in Channel 1 session chat, then relay 1 short 1-line `ask_question` (`(Recommended)` first) to lock the roadmap direction **before** authoring detailed per-phase specs.
   - **Gate 3 Step 2 — Detail Phases & Adaptive `N` Questions:** After roadmap lock, `planning` authors `implementation-plan.md`, all `phases/phase-NN-*.md` files (`[+]/[M]` files, `Consumes ↔ Produces`, cross-phase conflict check, ordered single-writer tasks, co-located unit tests, context-driven `[REVIEW_CHECKPOINT]` placements), and `test-plan.md` (`E2E-01..E2E-N`), relaying `N` real 2-Channel `ask_question`s (`0, 1, 2...`, recorded as `D-NN`) **only** when a genuine cross-phase conflict, technical trade-off, or risk requires a user decision — skipping mechanical per-phase confirmation stops (`X` ritual popups) whenever a phase is clear.
4. **Step 2D — Gate 3 Step 3: Master Plan Report & Gate 3 Freeze (`implementation-plan.md`, `phases/`, `test-plan.md`):**
   - Run 3-pass `gate-review` (`modes/plan.md`) with `0 OPEN Q-NN`. Present the consolidated Master Plan Report in Channel 1 session chat, then relay 1 short `ask_question`: `(Recommended) Approve Plan & Proceed to Build` (`APPROVED_FOR_BUILD` → `READY_FOR_BUILD`), `Refine Technical Decisions`, or `Modify Business Scope / Requirements` (back to `spec_writer`).

---

## Phase 3 — Sequential Delivery Loop (`code_writer` → `code_reviewer` → Continuation)

Execute ready phases sequentially (`PHASE-00` when `[EXECUTE]`, then `PHASE-01` → `PHASE-02` → ...). `docs_writer` runs **only once at Phase 5** after `ACCEPTED`.

1. **Implementation (`code_writer`):** Assign one phase via `incremental-implementation` (tasks in order, `MATCH`/`CODE_WRONG`/`PLAN_WRONG` triage, co-located unit tests + optional planned `integration_test/`, `{{slot:verification}}`, `{{slot:visual-quality}}` screenshot capture into `evidence/<phase-id>/<REVIEW_REVISION>/visual/`, self `{{slot:bug-hunt}}` & `{{slot:code-simplification}}`, phase commit per `git-preflight`, `writer-handoff.md` with `Visual Artifacts:`). Returns `READY_FOR_REVIEW`, `BLOCKED`, or `NEEDS_CONTEXT`.
2. **Independent Code Review (`code_reviewer`):** Runs `review-workflow` read-only on `BASE_REVISION..REVIEW_REVISION`, re-running commands and performing mandatory multimodal `read_file` visual comparison (`## Visual Comparison`) on every UI phase end and mid-phase `[REVIEW_CHECKPOINT]`, writing `vN/reviews/review_<phase-id>_<REVIEW_REVISION>.md`.
   - `APPROVED` at mid-phase `[REVIEW_CHECKPOINT]` → `code_writer` ticks `- [x]` on the checkpoint and finishes the phase.
   - `APPROVED` at phase end → proceed to Continuation below.
   - `CHANGES_REQUESTED` → back to `code_writer` (`review-resolution`, max **3 rounds** per phase; every fix is a new committed revision).
3. **Phase Continuation Checkpoint:** Keep Gate 1–3, `[REVIEW_CHECKPOINT]`, and per-phase `code_reviewer` `APPROVED` mandatory. Present completed phase results, unit tests, visual provenance, and any `AMENDED` `## Plan change log` rows in session chat, then call 1 short `ask_question` offering: `Continue with named next phase`, `Continue remaining approved phases automatically` (stops only on `[REVIEW_CHECKPOINT]`, `BLOCKED`, `PCR-NN` escalation, 3-round escalation, or before `final_qa`), `Inspect/refine current phase`, or `Pause work item`. When the user has approved continuous execution across approved phases, advance to the next phase after `APPROVED` without an extra modal stop per trivial phase.

### Routing Table (Standard Mode via Coordinator; `/swarm` Peer Handoffs Where Noted)

| Returned | Action |
|---|---|
| `NEEDS_CONTEXT` | Supply the exact missing fact/reference from approved docs or relayed consult, then re-assign. Never re-assign unchanged. |
| `BLOCKED` (env/approval/branch) | Coordinator resolves or asks user; never work around. |
| `BLOCKED` (`PCR-NN`) or `PLAN_CONFLICT` / `SCOPE_CHANGE` row | Coordinator writes `plan-changes/PCR-NN.md` from read-only report rows and invokes `planning` (`change-control`). `AMENDED` → `code_writer` resumes from first affected task (report new log rows at next checkpoint). `ESCALATED` → Coordinator asks user via 2-Channel `ask_question`; re-approve Gate 2 (`DESIGN_CHANGE`) or Gate 1 (`SCOPE_CHANGE`) before resuming. |
| `CHANGES_REQUESTED` (review) | Back to `code_writer` (direct `@code-writer` in `/swarm`). **Cap: 3 rounds per phase** → escalate plan causes via `PCR-NN` to `planning`, else to `@coordinator` / user with both positions. Nobody waives findings. |
| `CHANGES_REQUESTED` (`test_runner`, `FAILED_AT: E2E-i`) | Fail-Fast (zero tampering with `test-plan.md`). Route to **`bug_fixer`** (Mode C; direct `@bug-fixer` in `/swarm`):<br>• **`L1`** (1–2 files inside owning phase Scope / Files, 0 L3 floors): Red-to-Green regression test + fix → `READY_FOR_TEST` → `test_runner` re-runs `E2E-01..E2E-N`. **Cap: max 3 L1 rounds** before mandatory `L3` escalation (matching `bug-squad`).<br>• **`L2`** (multi-file/cross-layer, 0 L3 floors): regression test + fix → `READY_FOR_REVIEW` → `code_reviewer` (`APPROVED`, counts toward owning phase 3-round cap) → `test_runner` re-runs `E2E-01..E2E-N`.<br>• **`L3`** (plan/design/scope flaw, L3 floor hit, or L1 round cap hit): `bug_fixer` writes `plan-changes/PCR-NN.md` (`ESCALATED`) → **`planning`** (`change-control`) amends plan (with user gate if frozen) → **`code_writer`** implements amended task(s) → `code_reviewer` (`APPROVED`) → `test_runner` re-runs `E2E-01..E2E-N`. |
| 3rd `PCR-NN` on same task | Escalate to user via `@coordinator`, whatever its class. |

---

## Phase 4 — Final Hybrid E2E QA & Fail-Fast Loop (`test_runner` ↔ `bug_fixer` ↔ `planning` → `code_writer`)

After the final phase is `APPROVED` (plus any phase marked for intermediate acceptance), invoke **`test_runner` (`final_qa`)** on the exact `APPROVED` revision following `quality-acceptance`:
- **Hybrid E2E & Anti-Tampering:** `test_runner` stays strictly read-only (ticks only `- [x] **E2E-i**` in `test-plan.md`), runs existing local `integration_test/` suites when present, and executes live `E2E-01` → `E2E-N` sequentially via Antigravity `browser` subagent / `chrome-devtools` MCP (web) or native simulator/emulator capture + multimodal `read_file` verification against Figma (`figma/<stem>-SNN.png`) or HTML sitemap (`sitemap/screens/*.png`) renders. Zero scenario weakening or skipping. Report fixture vs live integration separately.
- **Fail-Fast Loop:** On first `E2E-i` `FAIL`, stop immediately, write `vN/evidence/final_qa/<revision>/acceptance-report.md` (`FAILED_AT: E2E-i`), return `CHANGES_REQUESTED`, and follow the `L1` (max 3 rounds before L3) / `L2` / `L3` (`planning` → **`code_writer`** → `code_reviewer` → `test_runner`) routing above. Re-run **`E2E-01` → `E2E-N`** end-to-end on each new revision until 100% pass (`ACCEPTED`). `NOT_RUN`, `BLOCKED`, and `UNVERIFIED` never become `PASS` or `ACCEPTED`.

---

## Phase 5 — Final Handoff & Delivery Closure (`docs_writer`)

Upon `test_runner` returning `ACCEPTED` with `evidence/final_qa/<revision>/acceptance-report.md`:
1. Invoke **`docs_writer` once** (`user-documentation`) to write `vN/as-built.md` (Executive Summary, Mermaid flow diagram, Delivered Code & Component Provenance matching `design.md` reuse mapping, Phase/Review/QA Evidence Ledger, Limitations), update `.superpowers/ux/` (exclusive `docs_writer` ownership), and return `RECORDED`.
2. Mark `UI: N/A` for non-visual items. Keep final user summary strictly synchronized with `as-built.md`.
