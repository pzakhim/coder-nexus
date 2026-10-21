# 03 — Review, revisions and approval

## Self-check before showing the user

1. `coder-nexus ux sync`. Open `index.html` and step through every workflow (◀ / ▶) at every confirmed viewport.
2. Switch every state of every screen. Look for overflow, clipped text, missing mock values (orange outline) and wrong kit classes.
3. Compare `CHANGED` screens with the current app screenshots.
4. Check that every `new-component` has a `components/C-NN` file and a row in `uiux.md` → `## 6. New components`.

## Present a revision

Tell the user the revision (`r1`), how to open it (`design-uiux/index.html`), and what to look at: the workflows, the new or changed screens, the new components, and the open points. Ask for specific feedback per screen when possible.

## Feedback loop

- Each round: apply the changes, add a `CHANGELOG.md` entry (`rN → rN+1`: feedback, what changed, screens touched), bump `Revision` in `uiux.md`, run `coder-nexus ux sync`.
- Feedback that changes behavior, rules, scope or goals is a decision: queue it as `Q-NN → D-NN` in `codebase-notes.md` and tell spec_writer. A goal or scope change needs Gate 1 approval again.
- Visual-only feedback (layout, wording, order) stays in the CHANGELOG.

## Approval

Ask for approval of the exact revision: "Approve UI/UX revision r3?". Only an actual user answer approves it. Then fill `uiux.md` → `## 7. Approval` (revision, date, user response) and set `Status: APPROVED`. Any later change starts a new revision that needs approval again.

## After approval

- spec_writer aligns `requirements.md` (Workflows → scenarios and AC) with the approved revision.
- Planning maps each `S-NN` and `C-NN` to the stack's screens, routes and components in `design.md` (`{{slot:ux-kit}}` → kit class to widget).
- After delivery and verification, the coordinator updates `.superpowers/ux/screen-catalog.md` (NEW → EXISTING, latest design, screenshot).
