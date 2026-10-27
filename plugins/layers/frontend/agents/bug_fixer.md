---
skills:
  - {{slot:visual-quality}}
---
## Frontend rules

- **UI reproduction**: name the screen, state and viewport where the bug shows, and capture before and after evidence with `{{slot:visual-quality}}`.
- **Runtime Browser, Console & Network Inspection**:
  - When reproducing or tracing a UI/Web bug on a browser target, use `chrome-devtools` MCP (`list_console_messages`, `get_console_message`, `list_network_requests`, `get_network_request`, `take_screenshot`, `take_snapshot`) to capture live console errors/stack traces, inspect failing HTTP 4xx/5xx requests and payloads, and snapshot DOM/UI state.
  - Use `coder-nexus` `get_ux_error_patterns` to verify whether a visual or interaction defect stems from a known UX anti-pattern.
- **API-dependent bugs**: reproduce against the environment the report names. When that backend is not reachable, use the approved Mockoon fixture of the work item that built the screen (`mocks/<feature>_mockoon.json`) if one exists; never create fake data-source classes in the Client source. A backend response that breaks the agreed contract is not a Client fix: propose L3 with the request and response as evidence.
- **Visual states**: after the fix, the affected screen still shows the right `Loading`, `Content`, `Empty` and `Error` states; record them in `brief.md` → `## 10`.
- **Floors (at least L3)**: a shared UI component, theme or design token used by more than one screen; a navigation or route contract.
- **UI trace (investigation mode)**: record the screens visited in order, the state each screen shows (`Loading`, `Content`, `Empty`, `Error`), the requests each screen sends with their status and payload shape, and the state-holder transitions between them. Capture screenshots per step with `{{slot:visual-quality}}`; mask tokens and personal data in captured requests.
