# Mode: Planning (technical options at Gate 2)

Owner: `planning`. Output: one `Q-NN` (`Owner: planning`) → `D-NN` that `design.md` → `## Architectural decision` cites.

## When

During the Gate 2 pre-design loop, after the codebase intelligence scan of `{{slot:architecture-design}}`, when a Core gap, a conflict with the existing architecture, or a choice of architecture, contract or component has more than one viable answer. A choice that one verified fact forces (an existing foundation class, an approved profile) is recorded as a fact, not offered.

Technical options never change business behavior. If an option would change what the user sees, a rule or the scope, send a `Q-NN` to `spec_writer` instead.

## Draft the options

**Small choices** (which existing component, which of two error mappings): draft them yourself with the fields in [SKILL.md](../SKILL.md#2-build-the-options).

**Large choices** (a new module or layer, a cross-layer or external contract, a new seam for testing): draft radically different designs in parallel so the first idea does not anchor the rest.

1. Write one technical brief: the confirmed goals, the relevant `D-NN`, verified facts and file paths, the profile from `{{slot:architecture-design}}`, the dependencies involved, and the constraints any design must meet.
2. Spawn 2-4 fresh **read-only** subagents, each with the brief and one different design constraint, for example:
   - smallest interface: 1-3 entry points carrying the most behavior;
   - optimize the most common caller: the default case is trivial;
   - reuse first: extend what the codebase already has before adding anything;
   - explicit seam: put external dependencies behind a port with a test adapter.
3. Each subagent returns: the interface or contract (signatures, invariants, error modes), a short usage sketch, what it hides, its dependencies, and where it is strong and weak. Subagents write no files and ask the user nothing.
4. Without a subagent tool, draft each design yourself from a blank page, one constraint at a time.

## Compare

Compare the drafts on:

| Criterion | Question |
|---|---|
| Depth | How much behavior does a caller or test get per unit of interface it must learn? |
| Locality | When this feature changes, how many places change with it? |
| Seams | Where can behavior vary or be tested without editing callers? Is a seam backed by two real implementations, or hypothetical? |
| Fit | Does it follow the approved profile and the codebase's existing conventions (`{{slot:clean-architecture}}`)? |
| Reversibility | How costly is it to change the decision later? |

Keep the 2-3 strongest (a hybrid may be one), recommend one, and ask it as one `Q-NN` in plain technical language with one line of trade-off per option.

## After the choice

- `design.md` describes only the chosen design, in one straight line, citing the `D-NN`.
- `Options Considered` holds each presented design with its main trade-off and why it lost.
- A decision that is hard to reverse, surprising and a real trade-off may also be promoted by `architecture-decision-records`; this skill does not write ADRs.
