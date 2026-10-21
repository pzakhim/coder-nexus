# 01 — Workflow interview

Huly tickets often describe what the system should do, not how the user moves through it. Ask before drawing. Use `ask_question`, one question per turn, with a recommended option first (skill `grill-me`). Record each answer as `Q-NN → D-NN` in `codebase-notes.md`.

## 1. Read before asking

Read the confirmed goals, the requirements draft, the source inventory (PDF screen specs, images, comments, PO documents), `screen-catalog.md` and the screenshots of the screens involved. Do not ask what a source already answers. Cite the source in the question instead.

## 2. What to settle (only what the sources leave open)

| Topic | Question |
|---|---|
| Actor | Who does this (role), on which device(s)? |
| Entry | Where does it start: which existing screen, menu, button, notification or deep link? |
| Steps | What does the user do at each step, and what does the system show back? |
| Branches | What happens on invalid input, no data, no permission, network error, duplicate action? |
| Exit | Where does the user end up, and what changed (saved, sent, status)? |
| Platforms | Mobile only, or also tablet / web? Any platform-specific step? |
| Existing screens | Which existing screens change, and which stay as they are (context only)? |

## 3. Propose, then confirm

Write the proposal as numbered steps per workflow and ask once:

```
W-01 Count items without PO (serves G-01, G-02)
  1. IS item list — sees PO / Manual source           (S01, CHANGED)
  2. Enter actual received qty — "no PO" warning       (S02, CHANGED)
  3. See excess / shortage result                      (S03, NEW)
  Branch: qty ≤ 0 → error on step 2
```

Options: **Confirm (Recommended)** / **Change steps** / **Split into more workflows**. Only after confirmation, add the rows to `uiux.md` → `## 4. Workflows` and create the screens.

## 4. Keep it bounded

- A workflow that serves no confirmed goal is out of scope. Note it as a non-goal and do not draw it.
- A step that belongs to a blocked stack (for example a .NET agent) stays out of the design.
- If the interview changes a goal or the scope, stop and hand it back to spec_writer (Gate 1 again).
