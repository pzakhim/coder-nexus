# 01 — Workflow interview

Huly tickets often describe what the system should do, not how the user moves through it. Ask before drawing. Use `ask_question`, one question per turn, with a recommended option first (skill `grill-me`). Record each answer as `Q-NN → D-NN` in `codebase-notes.md`.

## 1. Read before asking

Read the confirmed goals, the requirements draft, the source inventory (PDF screen specs, images, comments, PO documents), `screen-catalog.md` and the screenshots of the screens involved. Read `codebase-notes.md` → Question Queue and Decision Log too. Do not ask what a source or a `D-NN` already answers; cite it instead. Ask the rows with `Owner: designer`; route business-rule, permission or API questions back to spec_writer's queue.

## 2. What to settle (only what the sources leave open)

| Topic | Question |
|---|---|
| Actor | Who does this (role), on which device(s)? |
| Entry | Where does it start: which existing screen, menu, button, notification or deep link? |
| Steps | What does the user do at each step, and what does the system show back? |
| Branches | What happens on invalid input, no data, no permission, network error, duplicate action? |
| Exit | Where does the user end up, and what changed (saved, sent, status)? |
| Platforms | Asked **once per project**, not per work item — see §2.1. Per work item only: any platform-specific step? |
| Existing screens | Which existing screens change, and which stay as they are (context only)? |

### 2.1 Platforms, sizes and orientation (once per project)

Run `coder-nexus ux viewports --project .` first. If it says confirmed with orientations, do not ask again. Otherwise ask **one** `ask_question` that settles all three, recommended option first, pre-filled from the sources (a design-tool frame size, screenshots, the device the ticket names):

```
Thiết bị và hướng màn hình cho dự án (hỏi một lần):
  Platforms:   mobile · tablet · web            (Recommended: <what the app ships on>)
  Size:        mobile 360x800 · 390x844 · 412x915
               tablet 768x1024 · 820x1180 · 800x1280
               web    1280x800 · 1440x900 · 1920x1080
  Orientation: per platform — portrait · landscape · portrait + landscape
               (Recommended: mobile portrait, web landscape, tablet = what the source shows)
```

Recommend landscape (or both) only when a source shows it, for example a landscape design frame or a mounted terminal. Save the answer as `D-NN` and run `coder-nexus ux viewports --project . --platforms mobile,tablet --mobile 390x844 --tablet 820x1180 --orientations mobile=portrait,tablet=portrait+landscape --decision D-NN`. The first orientation listed is the default in the viewer; the reviewer rotates with ⟲ when a platform allows both. UX-009 blocks review until the orientations are confirmed.

### 2.2 One workflow per user-visible scenario

Each scenario the user can reach and would want to watch is its own `W-NN`, so it is listed in the `index.html` sidebar and can be played on its own. A login feature, for example:

| Workflow | Title | Steps |
|---|---|---|
| W-01 | Đăng nhập thành công | `1 Nhập tài khoản→S01, 2 Vào trang chủ→S02` |
| W-02 | Sai mật khẩu | `1 Nhập sai mật khẩu→S01, 2 Báo lỗi→S01:error` |
| W-03 | Quên mật khẩu | `1 Bấm "Quên mật khẩu"→S01, 2 Nhập email→S03, 3 Đã gửi link→S03:sent` |
| W-04 | Tài khoản bị khoá | `1 Đăng nhập→S01, 2 Thông báo bị khoá→S01:locked` |

- A small error branch (an inline field error that clears itself) may stay inside its workflow as a screen state plus walkthrough rows; anything the user asks about, or that changes screens, gets its own `W-NN`.
- Every `W-NN` maps to its Given/When/Then scenario and AC in `requirements.md` → `## Workflows` (REQ-006), one to one.
- Screens are shared between scenario workflows; draw a screen once and give it every state the scenarios need.

### 2.3 Steps column

`## 4. Workflows` → Steps lists `<n> <label>→<screen>[:<state>]`, comma separated: `1 Chọn NG→S01, 2 Quét LPN→S01:scan` (also `1. Chọn NG → S01`). The label is what the user does in that step and is shown in the sidebar as `n · label` with the screen id as a tag; `:state` opens the screen in that state (UX-004 checks it exists). The old `1→S01, 2→S02` stays valid, but write labels whenever two steps share a screen. Labels must not contain `,` or `|`.

## 3. Propose, then confirm

Write the proposal as numbered steps per workflow and ask once:

```
W-01 Count items without PO (serves G-01, G-02)
  1. IS item list — sees PO / Manual source           (S01, CHANGED)
  2. Enter actual received qty — "no PO" warning       (S02, CHANGED)
  3. See excess / shortage result                      (S03, NEW)
  Branch: qty ≤ 0 → error on step 2 (state)
W-02 Count items without PO — over the limit (serves G-01)
  1. Enter qty above the PO limit                      (S02)
  2. Blocked with "over limit" message                 (S02:over-limit)
```

Options: **Confirm (Recommended)** / **Change steps** / **Split into more workflows**. Only after confirmation, add the rows to `uiux.md` → `## 4. Workflows` and create the screens.

## 4. Keep it bounded

- A workflow that serves no confirmed goal is out of scope. Note it as a non-goal and do not draw it.
- A step that belongs to a blocked stack (for example a .NET agent) stays out of the design.
- If the interview changes a goal or the scope, stop and hand it back to spec_writer (Gate 1 again).
