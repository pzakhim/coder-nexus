# Coder Nexus for Flutter: user guide

How to use the Flutter multi-agent setup in this project. This file is regenerated on every sync; do not edit it here.

The agents are instructions your host agent (Antigravity, Claude Code, …) follows when you ask it to work. Nothing runs on its own, and **you** approve every gate: no agent approves its own work.

## 1. Which skill to call

You can name the skill, or just describe what you want. `bug-squad`, `debug-investigation` and `feature-testing` also react to Vietnamese wording ("sửa lỗi", "debug chức năng", "test chức năng"); for `dev-team`, naming the skill or giving a ticket ID is the surest way.

| You want to… | Call | Example request |
|---|---|---|
| Build a new feature or change how one works | `dev-team` | "Implement task ABC-12", "Add a settings screen" |
| Fix something that used to work and is now broken | `bug-squad` | "Fix bug: the order list crashes when empty" |
| Understand a bug or a flow, without changing code | `debug-investigation` | "Debug: why does the order list show yesterday's data?", "Trace what happens from page B to C" |
| Run a test scenario you describe | `feature-testing` | "Test function A going from page B to C to D" |

Not sure? A wrong behavior is a bug (`bug-squad`); a wanted change of behavior is a feature (`dev-team`). A check that fails while a feature is being built is handled inside `dev-team`; you do not need to call anything.

## 2. Before you start

1. **Sync**: run **Coder Nexus: Sync Stack to Workspace (Auto-Detect)** from the Command Palette and pick Flutter. It writes `.agents/agents/`, `.agents/plugins/coder-nexus/` (skills, rules, this guide) and `.agents/stack.json`. Re-run it after every extension or CLI update.
2. **Check the setup**: `coder-nexus doctor` (read-only: Huly login and Flutter setup), and `coder-nexus setup flutter --check`. When the project builds on the company packages (`app_core`, `app_util`, `app_ui_kit`), this check must be `READY`; a failed check blocks design and coding.
3. **Optional sources**:
   - Huly tickets: `coder-nexus setup huly` (read-only access). Then a request can be just the ticket ID.
   - Figma: add `FIGMA_TOKEN=…` to `.env`; linked frames are downloaded with `coder-nexus task-detail <ID> --download` or `coder-nexus figma fetch "<frame URL>"`.
   - Keep `.env` in `.gitignore`; credentials never go into Git.
4. **Your own team rules** (optional): skills generated with `skill-factory get …` into `.agents/skills/` override the plugin skills on the same topic.

## 3. Build a feature: `dev-team`

**What to give**: the request in your words, plus whatever you have — a Huly ticket ID, a spec file (`spec.md`, `<feature>_spec.md`), a Figma link or exported screens, and the API source. More input means fewer questions; nothing is invented to fill a gap.

**API source** (you will be asked if it is unclear):

| Value | Means |
|---|---|
| `BE_API_READY` | The real API exists (ticket, Swagger/OpenAPI or a `.md` spec) |
| `MOCKOON_MOCKED` | The API is not ready; a Mockoon mock is planned and prepared in `PHASE-00`; live checks stay pending until the real endpoint is verified |
| `NO_EXTERNAL_API` | The feature calls no API |

**Flow and what you are asked**:

1. **Spec & Figma Intake (Gate 1)** — Spec Writer reads every source, fetches any linked Figma frames (`tokens.json`, `<stem>.spec.json`, `<stem>-SNN.png`), extracts screens (`S-NN`) and UI/UX workflows (`W-NN`) via `figma-intake` (or classifies a no-Figma edge case as `CODEBASE_ONLY` minor adjustment on existing screens or `NO_UI_IMPACT`), asks the goal question first, then drafts `requirements.md` and `codebase-notes.md` and asks the remaining questions **one at a time**. You approve the spec.
2. **Technical design & UI Kit Mapping (Gate 2)** — Planning scans the code, resolves the architecture profile, audits `tokens.json` and `<stem>.spec.json` against the codebase Design System (`app_ui_kit`, `AppColor`, `Text12`–`Text34` in `imespro`) via `ui-kit-mapping`, surfaces any new widget (`C-NN` / `Core gap`), and writes `design.md` (`## UI/UX mapping`). Trade-offs come to you as one question with a recommended option.
3. **Plan (Gate 3)** — Planning splits the work into `PHASE-00` (readiness) and behavior phases with small tasks. You approve the plan.
4. **Build, phase by phase** — Code Writer → Code Reviewer for each phase. After each phase you get a summary and decide whether to continue; Gate 3 does not run all phases at once.
5. **Acceptance & As-Built Record** — Test Runner tests the approved acceptance criteria on the reviewed code and gives a verdict; once `ACCEPTED`, Docs Writer records `as-built.md` once for the feature.

**Where results are**: `.superpowers/work-items/<slug>/vN/` (spec, design, plan, phases, reviews, evidence). The branch is created after Gate 1; agents never merge to `main`, tag or deploy.

## 4. Fix a bug: `bug-squad`

**What to give**: what you see, where it happens, what you expected, and where it was found (DEV / STG / PROD). Steps, screenshots or logs help.

**Flow**:

1. The Bug Fixer **reproduces** the bug first (preferably with a failing test). Not reproduced → `NOT_REPRODUCED`, and you are asked for more information.
2. It finds the root cause and the impact, then proposes a **severity** and a **fix level**. You confirm or change them; no fix starts before that.
   - Severity **S1–S4** (crash/data → cosmetic) only decides the branch: an S1/S2 bug found in production takes the hotfix path.
   - Fix level decides the route:

| Level | When | Route |
|---|---|---|
| **L1 – Quick patch** | One line, one config value or one file in one layer; no shared code | fix → unit test → Test Runner (no code review) |
| **L2 – Local fix** | Inside one feature, possibly across its layers; no API, data or shared-code change | short fixing plan → fix → unit test → **Code Reviewer** → Test Runner |
| **L3 – Escalate** | API contract, schema or data change; more than one screen or a shared component; a business rule or flow change; permissions; unclear root cause | escalation report → `dev-team` (no fix here) |

   Flutter areas that always count as L3: `../app-core`, `../app-util`, `../app-ui-kit`, `BaseScreen` behavior, code under `lib/core/` or `lib/shared/`, route or DI registration. When unsure, the higher level is chosen. Asking to *change* behavior is not a bug: it goes to `dev-team`.
3. The Test Runner reruns the reproduction and regression checks: `VERIFIED_FIXED`, or `STILL_BROKEN` (back to the Bug Fixer; the third time it is escalated).

**Where results are**: `.superpowers/debug/<bug-slug>/` — `brief.md`, `fixing-plan.md` (L2), `reviews/` (L2), `escalation-report.md` (L3), `evidence/`.

## 5. Investigate without fixing: `debug-investigation`

**Two kinds of request**:

- **Bug**: something behaves wrongly and you want to know why.
- **Trace**: you want to see how a feature works at runtime — screens in order, state changes, requests sent. Give a concrete scenario: the screen, the action, the data or account.

**Flow**: the Bug Fixer reproduces the bug or runs the scenario on an emulator or device. If needed it adds **temporary logs** (`debugPrint` / `log` and a temporary `BlocObserver`, every line tagged `DBG-<slug>`), captures the output, then removes every temporary line and proves it (`git status` / `git diff` back to the starting state). A reproduction test written for the investigation is quoted in the report and removed too. **No code change is kept**, nothing is committed, and secrets are masked in logs.

**Result**: `diagnosis.md` — question, scenario, temporary logs used, captured output, findings (root cause or the observed flow), impact, next step. For a bug you are asked whether to fix it now; yes hands the diagnosis to `bug-squad` without repeating the investigation.

**Where results are**: `.superpowers/debug/<slug>/` — `diagnosis.md`, `evidence/`.

## 6. Test a scenario: `feature-testing`

**What to give**: the scenario, in any form — a sentence ("test function A going from page B to C to D"), a list of steps, Given/When/Then, or a file (`.md`, `.txt`, spreadsheet). An optional template is in `skills/work-item-contract/templates/test-scenario.md.tpl`. You will be asked for the target (emulator, device, browser), environment and account if they are missing.

**Flow**:

1. The Test Runner turns your scenario into cases in `test-plan.md` without adding or dropping any.
2. Where you gave no expected result, it applies the **default checks**, labelled `expected inferred`:
   - **DC1** the flow completes; **DC2** no crash or console/log error; **DC3** each screen shows the right state (`Loading`, `Content`, `Empty`, `Error`); **DC4** data is consistent across the steps.
   - It asks you only when a business result cannot be inferred (for example which value is correct).
3. It runs existing automated tests that cover a case and checks every case on the running app, with screenshots and logs as evidence. It **never writes tests or fixes code**; a case with no automated test is listed as a gap.
4. The report gives each case `PASS` / `FAIL` / `BLOCKED` / `NOT_RUN`, the failures with expected vs actual, the gaps, and at the end **suggested cases** it did not run. The run is `COMPLETED` (not the same as "all passed") or `BLOCKED`. For each failure you decide whether to send it to `bug-squad`.

No code review is needed: it tests the current code and records the revision, including uncommitted changes.

**Where results are**: `.superpowers/test-runs/<slug>/` — `scenario.md`, `test-plan.md`, `test-run-report.md`, `evidence/`.

## 7. What lives in `.superpowers/`

| Folder | Created by | Contains |
|---|---|---|
| `work-items/<slug>/vN/` | `dev-team` | Spec (`requirements.md` with `S-NN` & `W-NN`), technical design (`design.md` with `## UI/UX mapping`), plan and phases, reviews, evidence, as-built records. A later change opens `vN+1`. |
| `debug/<slug>/` | `bug-squad`, `debug-investigation` | Bug brief, fixing plan, review reports, escalation report or diagnosis, evidence. |
| `test-runs/<slug>/` | `feature-testing` | Your scenario, the test plan, the report and its evidence. |
| `sources/<ISSUE-ID>/`, `sources/figma/` | `task-detail --download`, `figma fetch` | Downloaded ticket attachments and linked design frames (`tokens.json`, `<stem>.spec.json`, `<stem>-SNN.png`, `<stem>.json`). |
| `ux/` | `docs_writer` | Screen catalog (`.superpowers/ux/screen-catalog.md`) and verified app screenshots. |

These folders belong to your project. `.agents/plugins/coder-nexus/` (including this guide) is replaced on every sync.

**Status**: the bug-fixing, investigation and scenario-testing flows are tested on their contracts and generated agents, but have not yet been run on real project work. Report anything that does not match this guide.
