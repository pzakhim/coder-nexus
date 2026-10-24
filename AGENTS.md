# AGENTS.md — AIFactory-Coder

Instructions for agents working in this **Hub repository**. Treat current code, tests, and the [plugin manifest](plugins/core/bundle_manifest.json) as implementation evidence.

## 1. Responsibility and boundaries

- **Coder Nexus / AIFactory-Coder (Hub):** Python MCP server in `src/coder_nexus/`, read-only Huly adapter, read-only Figma frame extraction (`src/coder_nexus/figma/`), Clean Architecture references and validators, UI/UX design tooling (`src/coder_nexus/ux/`: HTML kit, `design-uiux/` scaffolding and the UX-001…UX-012 validator), the `core-package-usage` skill that routes agents to the iMESPro packages (`app_core`, `app_util`, `app_ui_kit`), plugin sources split into stack-neutral `plugins/core/`, shared `plugins/layers/`, stack packs in `plugins/packs/<stack>/` (two packs: Flutter, maintained, and Backend, preview until Phase 2; a projection and a workspace hold exactly one pack; composed by `coder_nexus.plugin_build`; see the [installation guide](docs/guides/installation.md#how-a-projection-is-built)), shared handshake contracts in `plugins/shared_contracts/`, an initial VS Code plugin-sync extension, and the Skill Factory (`src/skill_factory/`, `skill-factory list | get`): generators a workspace copies into `.agents/skills/` and owns, overriding fixed pack skills of the same topic (see [skill-factory guide](docs/guides/skill-factory.md)). Use `uv` for Python commands.
- **Antigravity Flutter Client (separate workspace):** owns its `.env`, resolved package dependencies, approved feature documents under `docs/features/<module>/<feature>/vN/`, implementation under `lib/`, tests, and revision-bound evidence. The iMESPro packages live next to the Client (`../app-core`, `../app-util`, `../app-ui-kit`); `coder-nexus setup flutter --check` proves they are resolved.
- **Huly:** a source of real task details and acceptance criteria. Hub Huly operations are read-only. A real user request can also supply requirements when no Huly task exists.

Do not describe the agent profiles as an autonomous code generator. They are host-executed instructions with explicit approvals and verification gates. Figma extraction is read-only and limited to one linked frame per call (`coder-nexus figma fetch`, `task-detail --download`): a PNG render, the raw node JSON and a summary of what that JSON contains, tested against mocked API responses in `tests/test_figma.py` and fetched once from the real Figma API (IMES-1235 frame `1150:10051`) on 2026-10-21. Do not claim design-to-code generation, full-file or prototype extraction, full Flutter logic coverage, or feature E2E acceptance without evidence.

## 2. Read before changing code

1. Read [README.md](README.md) and [docs/guides](docs/guides/) for current capability and acceptance status.
2. Inspect actual source, tests, plugin agent/skill contracts, and the target Client when a change crosses the Hub–Client boundary. Do not treat template imports, paths, or old examples as verified Client APIs.
3. Check `git status` and preserve unrelated or pre-existing user changes. Keep Markdown links clickable and repository-relative where possible.

## 3. Implementation rules

- Follow the **Ponytail** approach: solve the current problem with the smallest clear change; avoid unused layers, speculative abstractions, and duplicated Kit widgets.
- Manage Python with `uv`. Keep MCP lookups and validators free of Client writes. Catalog search/spec lookup must remain read-only.
- For Flutter work, use the `core-package-usage` skill: pass `coder-nexus setup flutter --check`, read `../app-*/guidance/GUIDE.md`, then decide per need. Reuse a core API or `app_ui_kit` widget when its GUIDE "Use when" fits, even if styling differs from a supplied design; ask when several fit. Otherwise write the simplest Client code under `lib/modules/<feature>/` (shared folder only when two or more modules need it) and record a Core gap in `design.md`. A failed setup gate is a blocker.
- Keep Domain independent of Flutter and Data implementations; use the real Client's Data, Presentation, routing, state, and DI conventions. Add only the layers required by the approved behavior.
- For feature work, honor the three actual user approval gates for requirements, design, and plan. Code Writer implements one ready phase; Reviewer inspects the same revision; Test Runner supplies independent evidence. Neither a validator result nor an agent may self-approve a gate. `NOT_RUN`, `BLOCKED`, and `UNVERIFIED` are not `PASS`.
- Report exact checks and their limits.

## 4. Ask before changing

- Dependencies in `pyproject.toml`.
- Public schemas, signatures, or behavior of the existing MCP tools, including the original five core tools.
- The Component Registry schema.

## 5. Prohibited actions

- Do not store Huly, Figma, or developer credentials in this repository or Git. Credential persistence belongs to the Client workspace `.env` and must remain untracked.
- Do not implement Huly create, update, or delete operations.
- Do not fabricate business records, mock design/task data, or hardcoded fallback data to make a missing source look successful. Fail explicitly when required evidence is unavailable.
- Do not edit, copy, or rewrite `app_core` / `app_util` / `app_ui_kit` code into the Client, invent a package API, or mark an unrun analyzer, test, build, or visual check as passed.

## 6. Current verification boundary

The Hub currently exposes **9 MCP tools** (the `flutter_ui_kit` catalog tools were removed on 2026-10-13; `validate_ux_design` was added on 2026-10-21) and the plugin ships **8 shared agent profiles** (5 delivery roles plus Designer, Docs Writer and Bug Fixer) composed with one stack pack per workspace: Flutter (maintained) or Backend (preview until Phase 2). Projections are single-stack (`workspace-flutter`, `workspace-backend`, `global-flutter`, `global-backend`); installing a different pack needs `--replace` and switches the workspace instead of merging. The Frappe UI pack was removed in 3.2.0. The Hub suite passed **368/368 tests** on 2026-10-24. The UI/UX designer flow (workflow interview → HTML design → approval → requirements/design mapping → visual comparison) is contract- and validator-tested only; it has **not** been piloted on a real ticket. The same holds for the bug-fixing flow (`defect-resolution` → `bug_fixer` → `test_runner` for L1, with `code_reviewer` in between for L2, or an L3 escalation to `dev-team`): its contract and rendered agents are tested, but it has **not** run on a real bug. The same holds for the two entry skills built on the same agents: `debug-investigation` (Bug Fixer observes only, temporary logs removed) and `feature-testing` (Test Runner runs a user's scenario, read-only). The example Client resolved a pinned Kit package, passed analysis and an import probe, and passed its two existing Flutter tests on 2026-10-07. A real approved feature replay through specification, code, review, runtime visual inspection, and acceptance testing has **not** run. Keep that distinction in code review and documentation.

## 7. Release and tagging protocol

Automated testing, `.vsix` packaging, Open VSX publication (`IMP-AIFactory.coder-nexus`), and GitHub Release generation are managed by [`.github/workflows/release.yml`](.github/workflows/release.yml).

- **Single Source of Truth (SSOT):** The version is synchronized between [`plugins/core/bundle_manifest.json`](plugins/core/bundle_manifest.json) (`plugin_version`) and [`package.json`](package.json) (`version`) via [`scripts/sync_version.py`](scripts/sync_version.py). Tests dynamically assert compatibility across manifest and package metadata; never re-introduce hardcoded version strings into test suites.
- **Branch model (Git Flow):**
  - `develop` is integration. `release/X.Y.Z` is the frozen release candidate. `main` plus tag `vX.Y.Z` is released.
  - Work branches start from `develop`: `feature/`, `fix/`, `refactor/`, `perf/`, `chore/`, named `<type>/<ticket>-<short-description>`. Hotfixes start from `main` as `hotfix/<ticket>-<short-description>`.
  - Never commit directly on `develop`, `release/*` or `main`. Keep at most one active `release/*`.
- **Decide what a push includes:**
  - On every push request, inspect `git status --short --branch`, the current branch and upstream, the working diff, and the commits ahead of the target remote branch.
  - Stage only files belonging to the requested work with `git add -- <paths>`. Inspect `git diff --cached` and `git diff --cached --check` before committing.
  - Preserve unrelated modified and untracked files, credentials, generated files, and other agents' work. Do not push unrelated existing commits without the user's authorization.
  - An agent may push its own work branch. Merging or pushing into `develop`, `release/*` or `main`, and deleting a remote branch, each need the user's explicit approval for that action.
  - Do not use `git add .`, `git push --all`, or `git push --tags`.
- **Merge strategy:**
  - Squash a work branch into `develop`, and a `fix/` into the active `release/*`.
  - Use a merge commit for `release/*` → `main` and `hotfix/*` → `main`; never squash a release.
  - Do not cherry-pick to promote code between lines. Cherry-pick only as a deliberate, stated backport.
  - Never force-push `develop`, `release/*` or `main`.
- **Decide whether to tag:**
  - Any pushed `v*` tag runs the release workflow, which publishes to Open VSX and GitHub. Treat it as a production release.
  - Tag only a merge commit on `main`, and only after the user approves that release. A routine push carries no tag.
  - A documentation or CI-only fix after an existing release does not retroactively change that tag. Do not move or reuse a published tag; fix forward with the next version.
  - If the scope or release readiness is uncertain, finish the reviewable changes and ask before publishing a release.
- **For a release:**
  1. Check the latest local and remote tags (`git tag --sort=-v:refname` and `git ls-remote --tags origin`) and propose the next semver version from the commits since the last tag. Confirm that the target tag does not exist on either side. The user decides the version.
  2. Cut `release/X.Y.Z` from `develop` (approval). On the release branch, run `python3 scripts/sync_version.py <new_version>` (release notes are generated on the GitHub Release) and refresh only the authorized Client workspace projection. Do not install globally when the user requested workspace-only installation. Only fixes land on the release branch, and each fix is also brought back to `develop`.
  3. Run `uv run pytest -q` and any checks required by the change on the release tip.
  4. Check that `git log release/X.Y.Z..main` is empty, so every hotfix on `main` is in the release.
  5. Merge `release/X.Y.Z` into `main` with `git merge --no-ff` (approval). Check that `git diff release/X.Y.Z <merge-commit>` is empty.
  6. Create an **annotated** tag on that merge commit with `git tag -a vX.Y.Z -m "Coder Nexus vX.Y.Z"`. Push `main` and **that exact tag** together with `git push --atomic origin main refs/tags/vX.Y.Z` (approval). Do not push unrelated local tags. If the remote rejects the push, resolve the rejection and revalidate; do not force-push or retag a published version.
  7. Check the tag-triggered [release workflow](.github/workflows/release.yml), the Open VSX version, and the GitHub Release with its `.vsix` asset. A pushed tag or packaged local VSIX alone does not prove publication. If a later step fails after Open VSX succeeded, repair and retry that release; do not create a new version merely to bypass a duplicate publication error.
  8. Merge `main` back into `develop` and delete `release/X.Y.Z` locally and on the remote (approval).
- **For a hotfix:** branch `hotfix/*` from `main`, test it, then merge it into `main` with a merge commit and tag a PATCH version as in release steps 5–7 (approval). Bring the same change into the active `release/*` (when it contains the affected code) and into `develop`.

## 8. Where a skill belongs: core, pack, or Skill Factory

`plugins/core/` is the **shared handshake layer**, like `plugins/shared_contracts/`. It holds only what one role hands to another, so every pack reads the same copy unchanged:

| Touchpoint | Core owns |
|---|---|
| specs → plan | requirements and design gates, decision records |
| plan → coder | plan/task contract, change control |
| coder → review | hand-off format, finding severity and verdict (`work-item-contract` handoff-and-status §9), evidence standard |
| tester → `requirements.md` | acceptance-criteria traceability, test report and verdict vocabulary |

Decide placement with two questions:

1. **Does another role consume it as an input or output contract?** → core, stack-neutral, one copy.
2. **Are the rules common but each stack writes its own body?** (clean-code, secure-coding-standards, code-simplification, unit-testing, root-cause-debugging, bug-hunt, code-review, clean-architecture…) → **not core**. The common rules live in the Skill Factory generator (`src/skill_factory/library/generators/create-*/`, its own `references/base-rules.md`); each pack holds the generated skill in a slot and records the generator version in `pack.json` → `generated_from`; a workspace may override it in `.agents/skills/<name>/`.

Anything that is neither belongs to a single pack only.

- Core agents and skills reach stack knowledge through `{{slot:<name>}}` (registered in [`plugins/core/slots.json`](plugins/core/slots.json)), never by a pack skill path.
- Do not keep "base rules" in core for generators to read; a generator owns its base rules.
- Current state: in 3.2.0, the 6 stack skills (`clean-code`, `secure-coding-standards`, `code-simplification`, `unit-testing`, `root-cause-debugging`, `bug-hunt`) live entirely in pack slots and are generated per stack from Skill Factory generators; they have been removed from `plugins/core/skills/`.
