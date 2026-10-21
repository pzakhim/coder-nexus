---
name: ux-mockup
description: Design a work item's UI/UX as static HTML screens drawn with the project's real UI kit — workflow interview, screens per step with states, mobile/tablet/web viewports, revisions and user approval — in `.superpowers/work-items/<slug>/vN/design-uiux/`.
---

# UX mockup (UI/UX design in HTML)

Every change the user can see gets a UI/UX design the user approves before technical design and planning. The approved revision is the Visual AC: implementation is later checked against it at the same viewport.

## Model

**Goal** `G-NN` (why; from `requirements.md`) ← **Workflow** `W-NN` (user-confirmed ordered steps) → **Step** → **Screen** `S-NN` (static HTML, with its states).

- Goals only keep the work on topic. They are checked per workflow, not per screen.
- A screen belongs to at least one workflow step. A screen in no workflow is extra, or a step is missing.
- Each workflow becomes Given/When/Then scenarios and AC in `requirements.md`.

## Files

```
.superpowers/
├── ux/                        # shared, committed — never holds designs
│   ├── design-system.json     # design source ({{slot:ux-kit}}), decision D-NN
│   ├── viewports.json         # mobile / tablet / web sizes, decision D-NN
│   ├── kit/                   # generated: kit.css, kit.js, viewports.js, components.html, fonts/
│   ├── screen-catalog.md      # every known screen of the app → latest approved design
│   └── current/               # screenshots of the running app
└── work-items/<slug>/vN/design-uiux/     # only when the work item has UI impact; committed
    ├── uiux.md                # APPROVAL DOC — source of truth for workflows and screens
    ├── index.html             # open this: workflows, device frame, viewport/state/notes switches
    ├── screens/S01-<slug>.html
    ├── components/C01-<slug>.html
    ├── data/flows.js          # generated from uiux.md by `coder-nexus ux sync`
    ├── data/mock-data.js      # window.MOCK — MOCK data only
    ├── assets/  CHANGELOG.md
    └── shots/                 # generated screenshots (git-ignored)
```

## Commands (run in the Client workspace)

| Step | Command |
|---|---|
| Design source + kit | `coder-nexus ux extract --project .` ({{slot:ux-kit}}) |
| Viewports (ask once per project) | `coder-nexus ux viewports --project .` then `--platforms mobile,tablet --mobile 390x844 --tablet 820x1180 --decision D-NN` |
| Create the folder | `coder-nexus ux new --work-item .superpowers/work-items/<slug>/vN --title "<feature>"` |
| Add a screen | `coder-nexus ux screen --work-item … --id S02 --slug receive-qty --title "…" --steps W-01#2 --kind CHANGED --catalog wms.is-items.receive [--states default,error]` |
| Add a new component | `coder-nexus ux component --work-item … --id C01 --slug no-po-warning --title "…" --used-in S02` |
| Rebuild `index.html` data | `coder-nexus ux sync --work-item …` (after every edit of `uiux.md`) |
| Check the design (UX-001…UX-010) | `coder-nexus ux validate --work-item …` (MCP `validate_ux_design`); add `--write-hash` when presenting or approving a revision |

The commands create files with the correct relative paths to the kit and add rows to `uiux.md`. Edit the generated files; do not move them.

## Process

1. **Decide whether a design is needed** — see the designer agent's "When you are called" (no UI impact / existing visual / one-screen change). A fetched design-tool export in `.superpowers/sources/<ISSUE-ID>/` (status `READ`) counts as an existing visual: cite its file in `uiux.md` and in screen notes. A source marked `NOT_PROVIDED` or `UNREACHABLE` is missing input, not a design.
2. **Workflow interview** — [references/01_workflow_interview.md](references/01_workflow_interview.md). The user confirms `W-NN` and its steps before any screen is drawn.
3. **Viewports and design source** — confirmed once per project and recorded as `D-NN`.
4. **Screens and components** — [references/02_screen_rules.md](references/02_screen_rules.md).
5. **Review, revisions, approval** — [references/03_revisions_and_approval.md](references/03_revisions_and_approval.md).

## Rules

- Only kit classes from `kit/components.html`. Anything else is `class="new-component" data-name="…"` plus a `components/C-NN` file explaining why the kit cannot do it.
- Every screen has the states its steps need (see screen rules). A list or data screen has at least default, loading, empty and error.
- Notes (`.note data-ref="AC-02, D-05"`) explain decisions and link to AC, `D-NN` or the Huly source. Do not hide decisions in notes; record them in `codebase-notes.md`.
- Mock data lives in `data/mock-data.js`, bound with `data-mock`. It is realistic in shape and clearly MOCK.
- HTML is a behavior and layout contract, not pixel-perfect: animations, complex gestures and heavy charts are sketched and noted as such.
- `uiux.md` is the source of truth. `index.html` reads `data/flows.js`, generated from it by `coder-nexus ux sync`.
