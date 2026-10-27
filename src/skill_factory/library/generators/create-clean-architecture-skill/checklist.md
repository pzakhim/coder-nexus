# Checklist — clean-architecture

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Folder tree was confirmed by the user before any workspace file was written
- [ ] Every rule A1–A10 is adopted, adapted to a workspace contract, cited as enforced by an automated gate, or "not adopted" with a stated reason; A1, A2, A3, A5, A6, A7, A8, A10 are adopted
- [ ] Confirmed tree uses real workspace directory and module names (no generic placeholder paths)
- [ ] Dependency matrix in `02-dependencies-di-and-contracts.md` covers every layer in `01-layout-and-layer-roles.md` and includes deterministic CLI / `rg` boundary check commands (`PASS` / `FAIL`)
- [ ] DI composition order, unit-of-work/state ownership, and import/startup purity match the workspace's real runtime contracts
- [ ] `03-adding-splitting-and-review.md` links to `clean-code` (`01-structure-naming-and-types.md`) for size thresholds instead of repeating numbers, and forbids pass-through wrappers/re-export shims (`clean-code` C1, C17)
- [ ] Reviewer findings use the unified `BLOCKER` / `MAJOR` / `MINOR` scale (`shared_contracts/flags_and_statuses.md` §2)
- [ ] `01-layout-and-layer-roles.md`, `02-dependencies-di-and-contracts.md`, and `03-adding-splitting-and-review.md` present in `references/`
