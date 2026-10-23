# Mode: questionnaire — knowledge held by a third party

Use with [SKILL.md](../SKILL.md) when the user cannot answer a row and names someone who can (PO, BA, backend owner, customer, operations). The questionnaire is a document the user sends; the agent never sends it.

## 1. When

- The user replies "I don't know, ask X", or a source is `UNREACHABLE` and its owner is known.
- The rows stay `OPEN` in `## 0. Question Queue` while the questionnaire is out, so the gate stays closed (NOTES-003). Keep asking the rows that do not depend on them.

## 2. Ask the user only about the send

Two short questions the user can always answer, one per turn:
1. **Recipient**: role, expertise, relation to the project. It sets the tone and how much context the document must carry.
2. **What is needed back**: the exact `Q-NN` rows to include. Do not add rows the user did not pick.

## 3. Write it

Write `questionnaire-<topic>.md` in the version folder (`.superpowers/work-items/<slug>/vN/`) and give the user its path.

| Part | Content |
|---|---|
| Purpose | The decision riding on the answers, in one or two lines. |
| From / To / Use | The user, the recipient, and that answers go into the work item's decision log after review. |
| Context | One paragraph a newcomer can answer from. No internal IDs without a plain-language name. |
| How to answer | Deadline and rough effort. "I don't know" and partial answers are welcome. |
| Questions by theme | Most important first. One idea per question, an empty answer line under it, a one-line "why it matters" only where it could be misread. Map each question to its `Q-NN` with an HTML comment (`<!-- Q-12 -->`). |
| Anything else | A closing catch-all. |

Write it in the recipient's language and vocabulary, not the agent's.

## 4. When answers come back

1. Read the answers as source data, not as decisions; record cited facts in `## 3` with the questionnaire as the source.
2. Present each answer that decides a row to the user through the normal one-question flow, recommended option = the recipient's answer.
3. Only after the user confirms does `Q-NN` close as `CLOSED -> D-NN` (`(user choice)` or `(default accepted)` as in SKILL §3). Reason: the recipient informs; the user decides what the work item commits to.
4. Answers that conflict with a locked `D-NN` reopen it (SKILL §3).
