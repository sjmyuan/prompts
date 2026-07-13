# plan-refactor

1. **Validate Baseline**: Run existing tests, linting, and type-checking to ensure the codebase is in a clean state before refactoring begins.
2. Break down the refactor request into specific, measurable objectives and clearly defined constraints.
3. Identify and map dependencies between objectives to establish an efficient and logical refactoring sequence.
4. **Consolidate Steps**: Group related objectives together when they share context or can be tested together, reducing the total step count while maintaining clarity.
5. Load **reference/tdd-approach-selection.md** to select the appropriate TDD variant for each objective. Document the rationale.
6. Create a detailed step-by-step refactor plan. For each objective, include the following steps:
   1. **Write Focused Tests**: Create precise unit tests targeting the specific refactoring objective, ensuring comprehensive coverage of all scenarios, edge cases, and invalid inputs.
   2. **Confirm Test Failure**: Execute the tests to verify they fail initially, validating that the tests correctly identify the current code behavior before refactoring begins.
   3. **Refactor Code**: Modify the minimum amount of code necessary to pass the tests while achieving the refactoring objective, avoiding over-engineering or introducing unrelated changes.
   4. **Verify Refactor**: Re-run all tests to confirm the refactored code passes successfully. Debug and refine as necessary to ensure correctness.
   5. **Clean Up Unused Code**: Remove any obsolete or redundant code that is no longer needed after the refactor.
   6. **Clean Up Tests**: Update or remove tests that are no longer relevant due to the refactor, ensuring the test suite remains accurate and effective.
   7. **Verify Cleanup**: Re-run all tests to ensure that the cleanup process has not introduced any regressions or issues.
   8. **Validate Linting, Formatting and Type Checking**: Run linting, formatting and type checking tools to ensure code quality and adherence to coding standards.
7. Ensure the total number of steps in the plan is manageable and does not exceed 20 steps.
8. **Validate Plan Quality**: Load **reference/plan-quality-checklist.md** and verify — every objective has tests defined, dependency ordering is correct, step count ≤ 20, and TDD variants are documented. Revise any failing items before presenting to the user.
9. Summarize the complete plan to the user.
