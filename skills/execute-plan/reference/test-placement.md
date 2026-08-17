# Test Placement

Before writing any test code for a step, decide where tests belong — check existing coverage first, then extend existing tests when possible; create a new file only when no natural home exists.

| Situation | Action |
|---|---|
| Behavior already covered by an existing test | Run it; add nothing unless an assertion is wrong or missing |
| Changed class/module has an existing test file | Add new test methods there (extend) |
| New behavior is a variant/edge case of an existing scenario | Add a method or parameterized case to the covering test |
| New class/component with no existing test home | Create a new test file mirroring the class (e.g., `XTest` for `X`) |
| New test is a different level than the natural existing file (unit vs integration) | Create a file at the right level |
| Existing test file is unfocused or bloated (mixed concerns) | Create a new focused test file |

Reuse the existing test's fixtures and mocks instead of duplicating setup. Extending an existing test file is a test-only change for this plan's own tests — within the **Scope Boundary**'s Minor exceptions. Record the placement decision in the plan file's step notes.
