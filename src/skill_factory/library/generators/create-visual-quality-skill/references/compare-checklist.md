# 10-Dimension Visual Comparison Checklist & Deviation Grading

Starting point for `references/03-comparison-checklist-and-verdict.md`. All deviations are graded on the unified 3-tier scale (`BLOCKER` / `MAJOR` / `MINOR` — `shared_contracts/flags_and_statuses.md` §2), or marked `ACCEPTED (D-NN)` when explicitly covered by an approved architectural/design decision.

## 1. The 10 Visual Comparison Dimensions

| # | Dimension | What to Verify | `BLOCKER` Example (`FAIL`) | `MAJOR` / `MINOR` Example |
|---|---|---|---|---|
| **1** | **Layout & Hierarchy** | Regions appear in the approved order (app bar, header/KPI strip, primary content, sticky footer/actions); grid and column proportions match reference | Primary action or main content region missing, reordered, or overlapping | `MAJOR`: secondary card misaligned on tablet grid |
| **2** | **Spacing & Alignment** | Padding, margins, and inter-item gaps follow the design token scale; consistent baseline and edge alignment | Render overflow (`RenderFlex overflowed`), clipped widgets, or colliding controls | `MINOR`: 2–4px non-destructive padding variance |
| **3** | **Typography** | Font family, size/weight hierarchy, line height, and ellipsis/wrapping behavior on long strings | Wrong heading hierarchy or truncated key business data (amounts, status, IDs) | `MAJOR`: missing `maxLines`/`overflow` causing text wrap to break row height |
| **4** | **Color & Tokens** | Surface, text, border, and semantic colors (`success`, `warning`, `danger`) use approved design tokens in light/dark themes | Hardcoded color breaking dark mode or contrast; danger action styled as primary/success | `MINOR`: subtle border shade difference covered by kit defaults |
| **5** | **Shared Components** | Approved UI kit / shared design-system components used instead of raw/home-grown copies | Custom button/input/dialog replacing a mandated UI kit component without a `Core gap` (`D-NN`) | `MAJOR`: wrong kit variant (e.g., primary instead of outline) |
| **6** | **Icons & Media** | Approved icon set, sizes, aspect ratios, and placeholder/shimmer fallbacks | Wrong icon conveying opposite meaning; broken image asset | `MINOR`: icon size off by 2dp |
| **7** | **4 Mandatory UI States** | `Loading` (spinner/skeleton without layout jump), `Content` (populated), `Empty` (illustration + message), `Error` (clear message + retry/recovery) | Any of the 4 states missing, blank, or crashing | `MAJOR`: loading state causes jarring layout shift |
| **8** | **Responsiveness & Safe Area** | Confirmed viewports (`.superpowers/ux/viewports.json`), portrait/landscape orientation, notch/status-bar/home-indicator safe areas, keyboard inset | Content hidden behind notch, home bar, or soft keyboard; stretched phone layout on tablet landscape where 2-column is required | `MAJOR`: horizontal scroll or cramped layout on small screen |
| **9** | **Copy & Localization** | Exact labels, units, currency/date formatting, and error messages from `requirements.md` / `design.md` | Raw translation keys shown on screen, or copy that changes business meaning | `MINOR`: minor punctuation difference |
| **10** | **Accessibility Basics** | Touch targets (`>= 48x48dp` Android / `>= 44x44pt` iOS), text contrast (`>= 4.5:1`), focus order, text-scaling resilience | Unreadable contrast or untappable control (`< 36dp`) | `MAJOR`: touch target slightly below `48x48dp` on secondary action |

---

## 2. Standard Deviation Line Format

```text
<screen>/<state>@<viewport>: [<dimension>] expected <reference detail>, observed <actual detail> — BLOCKER | MAJOR | MINOR | ACCEPTED (D-NN) — <reason>
```
