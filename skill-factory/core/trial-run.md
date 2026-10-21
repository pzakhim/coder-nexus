# Trial run (does the skill help?)

After generating a skill, check that it changes what an agent does on **real work in this workspace**. Inspired by the eval loop of Anthropic's skill-creator, kept light: no scripts, no benchmark files.

## 1. Pick 2–3 realistic tasks

Tasks a teammate would really ask, taken from the workspace (open issues, the current plan, recent commits, long files). Each generator lists task ideas for its topic. Show the tasks to the user and let them add or swap one.

Good: "Add an endpoint to list release history for a change set", "Split `docs-list-view.tsx`", "Implement task 2.1 of phase 02".
Too simple (the skill will not matter): "Read file X", "Rename a variable".

## 2. Run with and without the skill — on paper

For each task, ask **two subagents in parallel** (Agent tool) to produce a **plan, not code**: the File Action Tree (`[+] [~] [-] [=]`), where each piece goes, which checks they would run, and the order of work.

- **With skill:** told to read `.agents/skills/<name>/SKILL.md` first.
- **Baseline:** same prompt, told not to read that skill.

Both are **read-only**: they must not edit files, run migrations, install packages or commit. If the user wants a real run, do it only in a temporary git worktree they approve, and discard it afterwards.

## 3. Compare

For each task, judge the two plans against the skill's own rules:

| Check | Question |
|---|---|
| Placement | Did files land where the skill says? |
| Boundaries | Any import/dependency the skill forbids? |
| Process | Were the skill's steps and checks followed (gates, task loop, evidence)? |
| Workspace fit | Real names/commands used, or generic guesses? |
| Difference | Is the with-skill plan actually better than the baseline? Where? |

Also read **how** the with-skill agent got there: if it wasted effort on a part of the skill, that part is unclear or unnecessary.

## 4. Improve and repeat

- Fix what the comparison shows: unclear rule → explain the why; ignored file → better pointer from `SKILL.md`; same helper rewritten by every run → write it once into the skill.
- Generalise; do not patch only for the trial task.
- Rerun the failing task. Stop when the with-skill plans follow the skill and beat the baseline, or the user is satisfied, or changes stop helping.

## 5. Report

Per task: one line for with-skill vs baseline, the main difference, and what was changed in the skill because of it. Keep the trial tasks in the generated skill's custom block only if the user wants them for later re-checks.
