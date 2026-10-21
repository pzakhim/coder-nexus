# Authoring a workspace skill

How the agent writes the skill a generator produces. The generator supplies knowledge and **suggested** shapes; the agent writes a skill that fits the workspace.

## Mandatory vs suggested

Each generator's `SKILL.md` has an output table with a **Kind** column:

| Kind | What it means | The agent may |
|---|---|---|
| **Mandatory** | Content the user required for this topic (e.g. the 4 slices of clean-architecture) or rules that must never be dropped | Rename headings and reorder inside the file; never drop the content or merge it away |
| **Suggested** | A shape that usually works | Merge, split, rename, skip or add files, when the workspace is better served — and say why in the report |

Templates (`*.tmpl`) are suggestions for **shape**. Each starts with a `<!-- GEN: Why … -->` note: keep the purpose, adapt the structure.

## Write for a smart reader

Generated skills are read by a capable model. Follow these habits (from Anthropic's skill-creator guidance):

- **Explain the why.** Each rule says, in a clause, what goes wrong without it ("repositories never commit — otherwise a use case cannot roll back a multi-step change"). A reason lets the agent handle cases the rule did not foresee.
- **Few hard rules.** Reserve "never/always" for rules that are truly absolute (security, approval gates, data integrity). Everything else is guidance with its reason. A page of capitalised MUSTs is a sign the skill is not explaining enough.
- **Keep it lean.** Remove anything that does not change what the agent does in this workspace. Prefer one real example over three generic ones.
- **Progressive disclosure.** `SKILL.md` = what to do and where to look (aim for < ~150 lines). Details go in `references/`, loaded only when needed. One topic per reference file; branch-specific files for BE/FE.
- **Real over generic.** Real paths, names, commands. If an example is only a shape, say so.
- **Generalise.** Write rules that hold for the next feature too, not just the example you looked at.

## Description (triggering)

The `description` in the frontmatter decides whether the skill is used at all. Models tend to *under*-use skills, so make it slightly pushy:

1. **What it does** in one clause, with the workspace name.
2. **When to use**: the concrete situations, listed — "creating a folder or file", "adding an endpoint", "splitting a long component"…
3. **Trigger words the team actually says**, including their language (e.g. Vietnamese phrases such as "tạo file mới", "tách file", "đặt code ở đâu") when the team writes in it. The skill body stays in English.
4. **Even if** clause for indirect asks: "…even when the user does not mention architecture".
5. Stay under ~1,000 characters; no marketing words.

Step 8 of the [workflow](workflow.md) checks the description against realistic prompts.

## Report what you changed from the template

At the end of generation, list: files merged/split/renamed/added/skipped versus the suggested shape, with one reason each. Mandatory content must be shown as present.
