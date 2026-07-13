# plan-bug-fix

1. **Validate Baseline**: Run existing tests, linting, and type-checking to ensure the codebase is in a clean state before bug fixing begins.
2. Break down the identified bug root cause into specific, independently testable issues.
3. Map out dependencies between issues to establish an efficient bug-fixing sequence.
4. **Consolidate Steps**: Group related issues together when they share context or can be tested together, reducing the total step count while maintaining clarity.
5. Load **reference/tdd-approach-selection.md** to select the appropriate TDD variant for each issue. Document the rationale.
6. Create a detailed step-by-step bug-fixing plan. For each issue, include the following steps:
   1. **Write Focused Tests**: Create precise unit tests targeting the specific bug issue, ensuring comprehensive coverage of all scenarios, edge cases, and invalid inputs.
   2. **Confirm Test Failure**: Execute the tests to verify they fail initially, validating that the tests correctly identify the current code behavior before fixing begins.
   3. **Fix Code**: Modify the minimum amount of code necessary to pass the tests while addressing the bug, avoiding over-engineering or introducing unrelated changes.
   4. **Verify Fix**: Re-run all tests to confirm the fix works successfully. Debug and refine as necessary to ensure correctness.
   5. **Clean Up Unused Code**: Remove any obsolete or redundant code that is no longer needed after the bug fix.
   6. **Clean Up Tests**: Update or remove tests that are no longer relevant due to the bug fix, ensuring the test suite remains accurate and effective.
   7. **Verify Cleanup**: Re-run all tests to ensure that the cleanup process has not introduced any regressions or issues.
   8. **Validate Linting, Formatting and Type Checking**: Run linting, formatting and type checking tools to ensure code quality and adherence to coding standards.
7. **Validate Plan Quality**: Load **reference/plan-quality-checklist.md** and verify — every identified issue has a corresponding fix step, the selected TDD variant is documented with rationale, dependencies between issues are correctly ordered, and the total step count does not exceed 20. Confirm that all verification checkpoints (Confirm Test Failure, Verify Fix, Verify Cleanup) are included for each issue.
8. Summarize the complete plan to the user.
