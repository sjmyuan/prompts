# plan-feature-implementation

1. **Validate Baseline**: Run existing tests, linting, and type-checking to ensure the codebase is in a clean state before implementation begins.
2. Break down high-level software requirements into specific, independently testable functionalities.
3. Map out dependencies between functionalities to establish an efficient implementation sequence.
4. **Consolidate Steps**: Group related functionalities together when they share context or can be tested together, reducing the total step count while maintaining clarity.
5. Load **reference/tdd-approach-selection.md** to select the appropriate TDD variant for each functionality. Document the rationale.
6. Create a detailed step-by-step implementation plan. For each functionality, include the following steps:
   1. **Write Focused Tests**: Create precise unit tests for a single functionality, task or requirement, ensuring coverage of all possible scenarios, edge cases, and invalid inputs.
   2. **Confirm Test Failure**: Execute the tests to verify they fail initially, confirming their validity before implementation begins.
   3. **Implement Minimal Code**: Write the simplest code required to pass the tests, avoiding over-engineering or adding features not directly related to the current test cases.
   4. **Verify Implementation**: Re-run the tests to confirm that the implemented code passes all test cases successfully. Debug and refine as necessary.
   5. **Refactor**: Improve the code's structure, readability, and performance while maintaining functionality, ensuring no tests break during the process.
   6. **Validate Refactoring**: Run the tests again after refactoring to ensure the updated code still passes all test cases without introducing regressions.
   7. **Clean Up Unused Code**: Remove any obsolete or redundant code that is no longer needed after implementation.
   8. **Clean Up Tests**: Update or remove tests that are no longer relevant, ensuring the test suite remains accurate and effective.
   9. **Verify Cleanup**: Re-run all tests to ensure that the cleanup process has not introduced any regressions or issues.
   10. **Validate Linting, Formatting and Type Checking**: Run linting, formatting and type checking tools to ensure code quality and adherence to coding standards.
7. Ensure the total number of steps in the plan is manageable and does not exceed 25 steps. The full TDD cycle can generate up to 10 steps per functionality; use consolidation strategies to reduce this where appropriate.
8. **Validate Plan Quality**: Load **reference/plan-quality-checklist.md** and verify — every functionality has tests defined, dependency ordering is correct, step count ≤ 25, and TDD variants are documented. Revise any failing items before presenting to the user.
9. Summarize the complete plan to the user.
