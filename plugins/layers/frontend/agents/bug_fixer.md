---
skills:
  - {{slot:visual-quality}}
---
## Frontend rules

- **UI reproduction**: name the screen, state and viewport where the bug shows, and capture before and after evidence with `{{slot:visual-quality}}`.
- **API-dependent bugs**: reproduce against the environment the report names. When that backend is not reachable, use the approved Mockoon fixture of the work item that built the screen (`mocks/<feature>_mockoon.json`) if one exists; never create fake data-source classes in the Client source. A backend response that breaks the agreed contract is not a Client fix: propose L3 with the request and response as evidence.
- **Visual states**: after the fix, the affected screen still shows the right `Loading`, `Content`, `Empty` and `Error` states; record them in `brief.md` → `## 10`.
- **Floors (at least L3)**: a shared UI component, theme or design token used by more than one screen; a navigation or route contract.
- **UI trace (investigation mode)**: record the screens visited in order, the state each screen shows (`Loading`, `Content`, `Empty`, `Error`), the requests each screen sends with their status and payload shape, and the state-holder transitions between them. Capture screenshots per step with `{{slot:visual-quality}}`; mask tokens and personal data in captured requests.
