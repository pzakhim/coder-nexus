# 03 — Review, revisions and approval

## Self-check before showing the user

1. `coder-nexus ux sync`. Open `index.html` and step through every workflow (◀ / ▶) at every confirmed viewport.
2. Switch every state of every screen. Look for overflow, clipped text, missing mock values (orange outline) and wrong kit classes.
3. Press ▶ Play for every workflow that has a walkthrough, at every confirmed viewport ([04_walkthrough.md](04_walkthrough.md)). Every workflow with time-based or automatic behavior, every multi-screen flow and every branch the user asked about has one.
4. Compare `CHANGED` screens with the current app screenshots.
5. Check that every `new-component` has a `components/C-NN` file and a row in `uiux.md` → `## 6. New components`.
6. `coder-nexus ux validate --work-item …` has no ERROR (UX-011 covers walkthrough rows). Optionally `coder-nexus ux record` to attach videos. Before showing the revision set `Status: IN_REVIEW` and run it with `--write-hash`.

## Present a revision

Tell the user the revision (`r1`), how to open it (`design-uiux/index.html`), and what to look at: the workflows, the new or changed screens, the new components, and the open points. Ask for specific feedback per screen when possible. Name the workflows that have a walkthrough and how to play them (▶ Play next to the workflow in `index.html`, or the video from `shots/`), say it is a MOCK simulation, and ask whether each workflow plays as the user expects.

## Feedback loop

- Each round: apply the changes, add a `CHANGELOG.md` entry (`rN → rN+1`: feedback, what changed, screens and walkthroughs touched), bump `Revision` in `uiux.md`, run `coder-nexus ux sync`. A walkthrough change is a revision too.
- Feedback that changes behavior, rules, scope or goals is a decision: queue it as `Q-NN → D-NN` in `codebase-notes.md` and tell spec_writer. A goal or scope change needs Gate 1 approval again.
- Visual-only feedback (layout, wording, order) stays in the CHANGELOG.

## Approval

Ask for approval of the exact revision: "Approve UI/UX revision r3?". Only an actual user answer approves it. Then fill `uiux.md` → `## 7. Approval` (revision, date, user response), set `Status: APPROVED` and run `coder-nexus ux validate --work-item … --write-hash`. The hash covers `uiux.md` (without status and approval fields), screens, components and data; any later change fails UX-010 and starts a new revision that needs approval again.

## After approval

- spec_writer aligns `requirements.md` (Workflows → scenarios and AC) with the approved revision.
- Planning maps each `S-NN` and `C-NN` to the stack's screens, routes and components in `design.md` (`{{slot:ux-kit}}` → kit class to widget).
- After delivery and verification, the coordinator updates `.superpowers/ux/screen-catalog.md` (NEW → EXISTING, latest design, screenshot).
