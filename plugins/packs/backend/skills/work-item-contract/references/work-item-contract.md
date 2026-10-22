# Backend Work Item Contract

- `requirements.md` and `codebase-notes.md` (authored by `spec_writer` via `grilling`; `brief.md` supported for small phase-free items) must declare:
  - **Technical Scope (`requirements.md` & `codebase-notes.md`)**: Target service, database tables affected, external APIs, `Scope in` / `Scope out`.
  - **API Endpoints**: Methods, paths, authentication/RBAC requirements, and `BR-NN` business rules citing `D-NN`.
  - **Question Queue & Decision Log (`codebase-notes.md`)**: Zero `OPEN` `Q-NN` rows before Gate 1 or Gate 2 approval; every confirmed user choice and considered option recorded in `## 1. Decision Log (D-NN)`.
  - **Handshake status**: Reference to `api_contract.json` if consumed by Frontend.
  - **Permanent Retention**: `codebase-notes.md` is retained throughout the entire `vN/` lifecycle.
