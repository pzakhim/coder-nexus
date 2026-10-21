# 04 — Walkthrough (auto-playing workflows)

Static screens cannot show what happens over time: a scan that saves by itself, a mode that turns off 15 seconds after the last scan, a field that resets. A walkthrough is a short script in `uiux.md` that `index.html` plays like a video (▶ Play): a fake cursor taps, text is typed or scanned, states switch, a countdown runs, and a caption says what happens.

It is a **scripted simulation labelled "Mô phỏng — MOCK"**. It shows the confirmed behavior to the reviewer; it does not prove app logic and is not a test.

## When

| Workflow | Walkthrough |
|---|---|
| Time-based or automatic behavior (auto-save, countdown, timeout, auto-reset, auto-submit) | Required |
| Multi-screen flow | Required |
| Error or empty branch the user asked about | Required, in that workflow's walkthrough |
| Single-screen visual change | Optional |

`coder-nexus ux validate` warns (UX-011) when a screen note describes timing (`15 giây`, `auto-save`, `countdown`, …) and its workflow has no walkthrough at Status `IN_REVIEW`.

## Rules

- **One walkthrough per workflow**, covering the happy path and its main unhappy branch.
- **Mirror the confirmed steps 1:1.** The `#` column is the `W-NN` step number (the label in the Workflows Steps column, e.g. `2` of `1→S01, 2→S02`). Several rows may belong to one step. Do not script behavior the workflow does not contain. Anything new you notice while scripting (an unclear timeout, a missing branch) is a `Q-NN` for spec_writer, not a silent addition.
- **Stable targets.** Rows point at elements by `data-ux-target="<name>"`: kebab-case, named after what the element is (`lpn-field`, `ng-toggle`, `save-button`), unchanged across revisions. A CSS selector works only as a fallback and gets a warning.
- **MOCK values.** Scanned and typed values come from `data/mock-data.js`: write the literal MOCK value or `@path` (e.g. `@lpns[0]`), which the screen reads from `window.MOCK`. Never real codes or personal data.
- **Real durations.** A `timer` shows the real duration (`15s`). Playback may be faster (Wait (ms) or the 2× speed) and the badge says so; never shorten the number on screen.
- **Captions** are in the user's language, one short line "what the user does → what the app does", citing AC / `D-NN` where it helps: `Quét LPN → app tự lưu OK (AC-01)`.

## Grammar (`uiux.md` → `## 8. Walkthrough`)

| Workflow | # | Screen | State | Action | Target | Value | Wait (ms) | Caption |
|---|---|---|---|---|---|---|---|---|
| W-01 | 1 | S01 | default | show | | | 800 | Thủ kho mở màn Quét LPN |
| W-01 | 1 | | ok | scan | lpn-field | @lpns[0] | 1200 | Quét LPN → app tự lưu OK (AC-01) |
| W-01 | 2 | | ng | tap | ng-toggle | | 600 | Bấm Chế độ NG → app bật chế độ NG |
| W-01 | 2 | | | scan | lpn-field | @lpns[1] | 600 | Quét LPN lỗi → ghi NG |
| W-01 | 2 | | | timer | ng-banner | 15s | 3000 | 15 giây sau lần quét cuối… (D-03) |
| W-01 | 2 | | default | show | | | 1500 | → app tự về chế độ OK |

| Action | Needs | Plays |
|---|---|---|
| `show` | Screen (State, default `default`) | Opens the screen in that state |
| `tap` | Target | Cursor moves to the element, ripple. Links are not followed: the next row shows the result |
| `type` | Target, Value | Cursor to the field, text typed character by character |
| `scan` | Target, Value | Field flashes green, the whole value appears at once |
| `wait` | Wait (ms) | Pause |
| `timer` | Value (real duration, `15s` / `500ms`), optional Target to highlight | Countdown badge; playback takes Wait (ms) if set, else the real duration |
| `caption` | Caption | Shows the caption only |

- An empty **Screen** continues on the previous row's screen.
- **State** on a `show` row is the state to open; on any other row it is the state the screen switches to **after** the action (the app's reaction). A Target must be drawn in the state on screen when the row starts.
- **Wait (ms)** is the pause after the row (default about 0.9 s).

## Self-check

1. `coder-nexus ux sync --work-item …` (prints the number of walkthroughs).
2. Open `index.html`, press ▶ Play for every workflow at every confirmed viewport; use ⏭ Step to check row by row and 1×–2× for speed.
3. `coder-nexus ux validate --work-item …`: no UX-011 error (unknown workflow, step, screen, state or target; target not in the active state; missing value or duration).
4. Optional: `coder-nexus ux record --work-item … [--workflow W-01] [--viewport mobile]` writes `design-uiux/shots/<W-NN>-<viewport>.webm` (git-ignored). It needs Playwright in the environment; if the command says it is missing, ask the user before installing anything, or skip the video.

## Presenting

- Tell the user which workflows have a walkthrough and how to play it (open `index.html`, ▶ Play next to the workflow), or share the recorded video.
- Ask for approval of the flow per workflow ("W-01 plays as you expect?"), together with the screens.
- A walkthrough change is a revision like any other: `CHANGELOG.md` entry, `Revision` bump, `ux sync`, and a new content hash when presenting.
