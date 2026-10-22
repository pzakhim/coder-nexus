# Output layouts

| Workspace | Layout |
|---|---|
| BE only, FE only, mobile, library | **Flat:** `SKILL.md` + `references/NN-*.md` |
| Fullstack (BE + FE in one repo) | **Branched:** one `SKILL.md` router + `references/shared/`, `references/be/`, `references/fe/` |
| Monorepo, several apps of one kind | Ask: one branched skill at the root, or one flat skill per app |

## Branched layout rules

- `SKILL.md` routes by folder: `<be_dir>` → `references/be/`, `<fe_dir>` → `references/fe/`, with one gate per branch.
- `be/` and `fe/` files cover **only** their branch; rules for both live in `shared/`.
- Same file numbers on both branches for the same topic (e.g. `01`–`07`), branch extras from `08` up — when the suggested shape is kept. If files are merged/split, keep the two branches parallel so an agent finds the same topic in the same place.
- Project-specific rules kept as their own files in `shared/` (BE + FE) or in the branch they belong to.

The layout (flat vs branched) is chosen by workspace type. The file list inside it follows the generator's output table: **Mandatory** content always present, **Suggested** files adapted per [authoring-guide.md](authoring-guide.md).

## Every generated file

- English; real paths and names; shape-only snippets say so.
- Under ~200 lines.
- Ends with `<!-- custom:start -->` / `<!-- custom:end -->`; custom blocks may also appear inside a file and are never touched by sync.
