# 02 — Screen rules

## Markup contract (the validator and `index.html` rely on it)

| Markup | Meaning |
|---|---|
| `<main class="screen" data-screen="S02" data-steps="W-01#2" data-catalog="wms.is-items.receive">` | One screen; which workflow steps it serves; its stable catalog slug |
| `<section … data-state="default">`, `loading`, `empty`, `error`, `disabled`, `success`, or a named state | One block per state, inside the screen |
| `<a href="S03-result.html" data-next>` | The action that moves to the next step |
| `class="new-component" data-name="No-PO warning"` | Not in the kit; also drawn in `components/C-NN` |
| `data-mock="items[1].name"` | Value from `data/mock-data.js` |
| `<div class="note" data-ref="AC-02, D-05">` | Design note linked to AC / decision / source |
| `data-ux-target="lpn-field"` | Stable name a walkthrough row points at (kebab-case, what the element is; keep it across revisions). Put it on every element a walkthrough taps, types or scans into, in each state where it appears |

## States

| Screen type | Required states |
|---|---|
| List / data view | default, loading, empty, error |
| Form / input | default, error (validation); add `disabled` / `submitting` when the action can be blocked or slow |
| Result / confirmation | default; error if the action can fail |
| Dialog / bottom sheet | Draw it as a state of the screen that opens it (`app-overlay` + `app-dialog` / `app-bottomsheet`) |

Time-based or automatic behavior (auto-save, countdown, auto-reset) is drawn as the states before and after, plus a `.note` with the real duration and the trigger ("tắt sau 15 giây kể từ lần quét cuối"); the walkthrough plays the change ([04_walkthrough.md](04_walkthrough.md)).

States that do not apply are left out, with a `.note` saying why when a reviewer would expect them. For a list or data screen the note must name the state ("No empty state: …"); `coder-nexus ux validate` then reports a warning instead of an error.

## Composition

- Build from kit classes: `app-appbar`, `app-content`, `app-button`, `app-formfield`, `app-search`, `app-dropdown`, `app-datepicker`, `app-card`, `app-list` + `app-list-item`, `app-badge`, `app-chip`, `app-banner`, `app-nodata`, `app-loading`, `app-shimmer`, `app-overlay` + `app-dialog` / `app-bottomsheet`, `app-bottomnav`, `app-footer`; layout helpers `stack`, `row`, `cols md-2/md-3`, `centered`, `muted`, `small`.
- Use the kit's colors through classes or `var(--c-…)`. Never hard-code a new color or font.
- Text is real and in the app's language (Vietnamese UI → Vietnamese copy), including error and empty messages.
- Mobile first. For tablet and web use `cols md-2` or `.centered`; mark platform-only differences with a `.note`.
- `CHANGED` screens start from the current screen (screenshot or last approved design) and change only what the work item needs. Show what changed with a `.note`.
- `EXISTING` screens appear only as context (entry or exit of a workflow), unchanged.

## New components (`components/C-NN-<slug>.html`)

Draw the component alone, in each of its states, with a `.note` for its behavior (tap, disabled, validation, data it shows) and why the kit cannot do it. Planning estimates and implements it from this file.
