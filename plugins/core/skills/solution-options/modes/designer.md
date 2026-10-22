# Mode: Designer (UI flow variants)

Owner: `designer`. Output: one `Q-NN` (`Owner: designer`) → `D-NN` that the `W-NN` steps in `uiux.md` follow; then `ux-mockup` draws the chosen variant.

## When

In the `ux-mockup` workflow interview, after the actor, entry and exit are settled and before any screen is drawn, when the same workflow has more than one materially different shape. One obvious shape is confirmed as part of the proposed `W-NN` steps, not offered as options.

## What counts as a variant

| Topic | Example of real variants |
|---|---|
| Flow shape | One long screen / a step-by-step wizard |
| Where it lives | New screen / a sheet or dialog on the existing screen |
| Feedback | Inline field errors / a summary banner on submit |
| Entry | From the list item / from a toolbar action / from a notification |
| Recovery | Stay on the screen with the input kept / return to the previous step |

Every variant must be buildable from the kit in `{{slot:ux-kit}}`. A variant that needs a new component says so in its costs. Variants never change a business rule, a permission or the scope; such a question goes to `spec_writer`'s queue.

## Describe

Write each variant as labelled steps in the `W-NN` format (`1 <step>→S01, 2 <step>→S01:error`), plus the number of screens and new components, which `G-NN` it serves, and its trade-off for the actor (taps, context switches, error recovery). Ask in words as one `Q-NN`, recommended variant first. Do not draw all variants: drawing is the expensive part and most choices are clear from the steps.

## Hand off to ux-mockup

After the choice, record `D-NN` with the rejected variants in `Options Considered`, then follow `ux-mockup` for the chosen variant only: confirm the `W-NN` steps, draw, review revisions and approval. A variant the user wants to see side by side after the drawings exist is ordinary revision feedback in `CHANGELOG.md`.
