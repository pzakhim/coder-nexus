# Detecting the workspace's Git setup

Everything here is read-only. Never create branches, commits or tags while detecting.

## Commands

```sh
git branch -a
git tag --sort=-creatordate | head -20
git log --first-parent --format='%h %s' -30 origin/<integration-branch>
git log --merges --format='%h %p %s' -20 origin/main
git for-each-ref --sort=-committerdate --format='%(refname:short)' refs/remotes | head -50
git check-ignore -v .superpowers/work-items/x
```

Squash merges show as single-parent commits with a PR number in the subject; merge commits have two parents.

## Tools that already enforce rules

| Tool | Signal | Use it as |
|---|---|---|
| commitlint | `commitlint.config.*`, `.commitlintrc*`, `@commitlint/*` in `package.json` | The commit-message check: `npx commitlint --from origin/<base> --to HEAD` |
| commitizen | `.cz.toml`, `cz` in `pyproject.toml`, `cz-cli` | Commit prompts; its config names the types |
| husky / lefthook / pre-commit | `.husky/`, `lefthook.yml`, `.pre-commit-config.yaml` | Local hooks; never bypass with `--no-verify` |
| semantic-release | `.releaserc*`, `release.config.*` | Computes the version from commits; the generated skill defers to it |
| release-please | `release-please-config.json`, `.release-please-manifest.json` | Opens release PRs from Conventional Commits |
| changesets | `.changeset/` | Per-package versions in a monorepo (V7 per component) |
| Version sync script | `scripts/*version*`, `Makefile` targets | The single-source-of-truth step (V6) |

When a tool already decides something (for example semantic-release computes the bump), the generated skill states that and links the config instead of restating rules.

## CI and environments

Read the pipeline files for branch and tag filters (`on: push: branches`, `only:`, `rules:`), environment names, and manual approval steps. Record which ref deploys to which environment; ask when the pipeline lives outside the repository.

## Protection

`gh api repos/<owner>/<repo>/branches/<branch>/protection` when `gh` is authenticated and the user agrees; otherwise ask which branches are protected and whether PRs require review.
