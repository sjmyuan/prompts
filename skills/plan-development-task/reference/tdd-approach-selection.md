# TDD Approach Selection

Select the appropriate TDD variant based on the change type and sub-type:

| Change type | Sub-type | TDD approach |
|---|---|---|
| **Bug Fix** | Simple bugs (typos, minor logic errors, incorrect constants) | May consolidate test writing and fixing in fewer steps if existing tests provide adequate coverage |
| **Bug Fix** | Type-related bugs (missing/incorrect types) | Focus on type-checking validation rather than test-first approach |
| **Bug Fix** | Configuration bugs (incorrect environment settings, build config) | Validate with build/run rather than unit tests |
| **Bug Fix** | Performance bugs (slow responses, N+1 queries, memory leaks) | Require performance tests and benchmarks in addition to functional tests |
| **Bug Fix** | Complex logic bugs | Always follow full TDD cycle for safety and thorough validation |
| **Feature** | Simple features (small UI additions, basic form fields) | May consolidate test and implementation steps when logic is straightforward |
| **Feature** | Pure presentational components | Focus on rendering and prop validation tests with minimal logic testing |
| **Feature** | Type-only additions (new types/interfaces without behavior) | Focus on type-checking validation rather than test-first approach |
| **Feature** | Configuration changes (adding constants, config options) | Minimal testing may suffice if changes don't affect behavior |
| **Feature** | Complex business logic | Always follow full TDD cycle for safety and clarity |
| **Refactor** | Simple cleanups (removing unused imports, fixing formatting) | May skip test creation if existing tests provide adequate coverage |
| **Refactor** | Type improvements (adding/refining TypeScript types) | Focus on type-checking validation rather than test-first approach |
| **Refactor** | Documentation-only changes | No test cycle needed; validate with linting only |
| **Refactor** | Code organization (file moves, renames) | Existing tests should pass unchanged |
| **Refactor** | Complex logic changes | Always follow full TDD cycle for safety |

Always ensure existing tests pass before and after changes. Document the rationale for the chosen TDD variant in the plan.
