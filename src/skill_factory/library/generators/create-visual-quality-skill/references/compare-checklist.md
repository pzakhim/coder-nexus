# Comparison checklist

Starting points for `03-compare-checklist.md`; the generated file names the workspace's tokens, components and UI standards.

| Dimension | Check | Blocking example |
|---|---|---|
| **Layout & hierarchy** | Regions in the approved order (e.g. KPI strip → control bar → primary surface → inspector); grid and widths | Primary action or main surface missing/moved |
| **Spacing & alignment** | Spacing scale, alignment to the grid, consistent gaps | Overlapping or clipped elements |
| **Typography** | Font family, sizes/weights per level, truncation rules | Wrong heading level breaking hierarchy, truncated key data |
| **Color & tokens** | Colors come from design tokens; semantic colors (success/warning/danger) used as defined | Hard-coded color that breaks theme/contrast; wrong semantic color (danger shown as success) |
| **Components** | Shared UI components used (modal, select, empty state, toast) instead of custom copies | Custom modal without focus trap; inconsistent button styles for the same action |
| **Icons** | The workspace's icon set and sizes; no emoji if the standard forbids them | Icon meaning differs from the design |
| **UI states** | Loading (no layout jump), empty (no data vs no match), error + retry, populated, forbidden | Missing error or empty state |
| **Responsiveness** | Target viewports: no horizontal scroll, readable at each size | Content cut off or unusable at a target viewport |
| **Copy** | Labels and messages as specified, language consistent | Copy that changes meaning |
| **Accessibility basics** | Contrast, visible focus, keyboard operation of modals and menus, alt text | Unreadable contrast, keyboard trap |

## Deviation line

`<screen>/<state>@<viewport>: <dimension> — expected <reference detail>, actual <observed> — blocking | minor — <reason>`
