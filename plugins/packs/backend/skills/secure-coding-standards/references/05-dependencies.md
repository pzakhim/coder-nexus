# 05 — Dependencies

Why: every dependency is code you run without reading it (SC11).

- Add a package only when a few lines of code or an existing dependency cannot do the job; give the reason in the handoff. Reason: fewer packages, fewer advisories.
- Adding or upgrading a dependency in `pyproject.toml` needs the approval the workspace's `AGENTS.md` requires; when unsure, ask through `change-control`. Reason: the dependency set is a design decision, not a task detail.
- Versions are pinned through the lockfile (`uv.lock` or `poetry.lock`), and the lockfile diff is part of the change. Check it matches: `uv lock --check` (or `poetry check --lock`).
- Before adding, check advisories with `uv run pip-audit` and avoid packages without an active maintainer or recent release. An advisory without a fixed version goes into the handoff's Concerns with the affected code path, for the reviewer to grade.
- Upgrades: read the changelog, one package per change unless the lockfile forces a group. Reason: a mixed upgrade hides which package broke.
- Security-sensitive packages (auth, JWT, crypto, parsers, HTTP clients) are always a review trigger ([06](06-review-triggers.md)).

`pip-audit` needs network access; when it cannot run, record `NOT_RUN` with the reason.
