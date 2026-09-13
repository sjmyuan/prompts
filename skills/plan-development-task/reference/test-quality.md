# Test Quality

Rules that keep planned tests honest. Loaded by the "Write Focused Tests" step and the plan-quality checklist.

A test exists to catch a specific break. Two principles govern everything:

1. Every test names the break it catches.
2. Every test exercises the real thing.

## Principle 1: Name the Break

Before writing the test body, answer: **what production change should make this test fail — and is that change a bug or a decision?**

| Check | Rule |
|---|---|
| Names a break | A test earns its place by catching a wrong branch, missing side effect, wrong argument, boundary case, or broken contract |
| Independent expectation | Derive expected values from literals or hand-checked fixtures — never from the code under test |
| No mirror assertion | An expectation computed by the same builder as the result is always true; replace it with a literal |
| No change detector | If only intentional decisions can fail the test (a constant's value, exact message wording, private structure), it fires on redesign and sleeps through bugs |
| Behavior, not text | Asserting that a file contains an exact line proves only that the source is the source; run the artifact and assert outputs, side effects, or exit codes |
| Your boundary, not the framework | Test the contract your code makes; upstream mechanics are their maintainers' tests |

### Gate Function

```
BEFORE writing the test body:
  Name the production change that would make this test fail.

  Cannot name one            → redesign around an observable behavior
  "The source text changed"  → run the artifact and assert its effects
  Only intentional decisions → change detector; test the behavior that depends on the decision

  Confirm the expected value is derived without the code under test.
  IF it reuses the code's logic or helpers:
    Replace it with a literal or hand-checked fixture
```

## Principle 2: Exercise the Real Thing

| Rule | Detail |
|---|---|
| Mock earns no assertions | A mock assertion passes when the mock is present and fails when it is absent — it says nothing about the component; unmock it or delete the assertion |
| Mock at the right level | Learn every side effect of the real method; mock only the slow or external operation and keep what the test depends on real |
| Make doubles specific | When arguments, call counts, or ordering are part of the contract, assert them; give each branch (success, error, malformed) its own fixture |
| Mirror real data completely | Mock the complete structure as it exists in reality — all documented fields — not just the ones the test reads |
| Production classes carry production methods only | Cleanup that only tests need lives in test utilities, never as a method on the production class |
| Prefer real components | When mock setup outgrows the test logic, switch to an integration test with real components |

### Gate Function

```
BEFORE adding a mock or test helper:
  List the real method's side effects; keep the ones the test depends on real.
  Mock responses mirror the complete real structure.
  A method only tests call lives in test utilities, not production.
  About to assert on the mock itself? Unmock it or delete the assertion.
```

## The Mutation Check

Before finishing, mentally mutate the production code; at least one test should fail for each realistic mutation:

| Mutation | Caught? |
|---|---|
| Wrong constant or argument | |
| Wrong branch handler | |
| Missing state change or side effect | |
| Empty or default return | |
| Missing validation for zero, empty, nil, unauthorized, or malformed input | |

A mutation nothing catches marks the behavior as unprotected — or the test as tautological.

## Warning Signs

- Setup and assertion share the same object, guaranteeing equality
- The test can fail only through a crash or a missing selector
- The test fails on every intentional change, never on accidental breakage
- Expected values are hidden behind loops, builders, or helpers
- The test greps source text
- The test would still matter if only the framework remained
- An assertion checks a mock, or fails if you remove the mock
- A method is called only from test files
- Mock setup is more than half the test, or you cannot explain why the mock is needed
