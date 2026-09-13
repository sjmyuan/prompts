# TDD Guardrails

Rules that stop a plan from quietly abandoning test-first. Loaded by the classification, scope, and quality-check steps.

## Iron Law

```
NO BEHAVIOR CHANGE WITHOUT A FAILING TEST FIRST
```

Applies to bug fixes, features, and behavior-changing refactors.

- Streamlined (fewer, consolidated steps) is allowed when a test is still written first and watched to fail.
- Skipping test creation is allowed only for non-behavioral changes — config values with no logic, type-only additions, docs. Record the justification in `context.md`.

## Rationalizations to Reject

| Excuse | Reality |
|---|---|
| "Too simple to test" | Simple code breaks; the test takes seconds |
| "I'll test after" | Tests written after pass immediately — they prove nothing and cover only what you remembered |
| "Tests after achieve the same goals" | Tests-after answer "what does this do?"; tests-first answer "what should this do?" |
| "Already manually tested" | Manual testing is ad-hoc: no record, no re-run, easy to miss cases |
| "Deleting X hours is wasteful" | Sunk cost — the choice is a trusted rewrite vs. untrusted code |
| "Need to explore first" | Explore, throw the exploration away, start with TDD |
| "TDD will slow me down" | TDD catches bugs before commit; shortcuts mean debugging in production |
| "Existing code has no tests" | Add tests for the existing code you are about to change |
| "Skip TDD just this once" | Stop — this is rationalization |

## Red Flags — Stop and Rewrite the Plan

- A test step follows its implementation step
- "Write tests" and "implement" merged for a behavioral change
- A test is expected to pass the first time it runs
- No step watches a test fail before the fix or implementation
- Cleanup removes tests without replacement coverage
- A streamlined variant chosen for a change that alters behavior

## Testability Is a Design Signal

Hard-to-test work is a design smell. Surface it during scope definition and route to a refactor first.

| Planning symptom | Design signal | Action |
|---|---|---|
| Don't know how to test it | Unclear interface | Write the wished-for API first; plan a refactor |
| Test setup is huge | Too many dependencies | Extract or inject dependencies (refactor first) |
| Must mock everything | Tight coupling | Apply **plan-refactor** before **plan-feature-implementation** |
| Test too complicated | Design too complicated | Simplify the interface before implementing |
