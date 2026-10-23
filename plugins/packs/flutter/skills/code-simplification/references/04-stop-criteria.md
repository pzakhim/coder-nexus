# 04 - Stop Criteria

Know when to stop simplifying to avoid over-engineering.

## 1. Stop Simplifying When:

1. **Readability Decreases:** If collapsing three lines into a complex nested higher-order fold makes the code harder to read for colleagues, stop.
2. **Behavioral Invariants are at Risk:** If a widget refactoring introduces potential subtle animation timing changes or layout jumps, stop.
3. **Abstraction Inversion:** Do not create generic wrapper widgets for one-off layouts. Two similar widgets are better than one leaky abstraction.
4. **Out of Task Scope:** Never simplify code in unrelated features or legacy modules.
