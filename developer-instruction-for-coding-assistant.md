# User Task

- Break down the user task into **small, actionable steps** following TDD principles.
- Order steps logically for **incremental development**: start with unit tests, proceed to implementation, and finish with refactoring.
- Each step should have a **clear, focused scope**, an **expected outcome**, and address **one specific functionality or aspect** at a time.

For each small functionality or aspect, break it down into six structured steps:

1. **Write Small Tests**:
   - Create **focused unit tests** covering a **specific scenario** of this functionality or aspect.
   - Ensure the test cases are minimal and only validate one behavior or condition at a time.

2. **Confirm Small Test Failure**:
   - Run the tests to ensure they fail or cause compilation errors before implementation.
   - This confirms that the tests are valid and that the functionality has not been prematurely implemented.

3. **Implement Small Functionality**:
   - Write **minimal code** sufficient to pass the focused tests.
   - Avoid over-engineering or adding unnecessary features beyond the scope of the current test case.

4. **Verify Small Implementation**:
   - Run the focused tests again to confirm the minimal code passes all test scenarios.
   - Debug and refine as needed, but only within the scope of the current functionality.

5. **Refactor Small Code**:
   - Improve clarity, maintainability, and performance of the focused functionality without changing its behavior.
   - Refactor in small increments, ensuring no new functionality is introduced.

6. **Validate Small Refactoring**:
   - Run the focused tests again to ensure the refactored code still passes all test scenarios.
   - Debug and refine if necessary, keeping changes minimal and focused.

Present the detailed steps before execution. For example:

- **Step 1**: Define the data model for user profiles, including fields like `name`, `email`, and `id`.
- **Step 2**: Write unit tests for data model validation, covering required fields, unique constraints, and edge cases (e.g., invalid email formats, missing fields).
- **Step 3**: Run the tests to confirm they fail or result in compilation errors before implementation.
- **Step 4**: Implement the data model with validation logic based on the tests.
- **Step 5**: Run the tests again to verify the implementation passes all defined tests. Debug and refine as needed.
- **Step 6**: Refactor the data model implementation for clarity and maintainability.
- **Step 7**: Run the tests again after refactoring to ensure the refactored code still passes all tests. Debug and refine if necessary.
- **Step 8**: Set up the database schema and migrations.
- **Step 9**: Write unit tests for the 'create user profile' endpoint, including authentication checks, validation, and error handling (e.g., duplicate emails, missing fields).
- **Step 10**: Run the tests to confirm they fail or result in compilation errors before implementation.
- **Step 11**: Implement the 'create user profile' endpoint with authentication and validation logic.
- **Step 12**: Run the tests again to verify the implementation passes all defined tests. Debug and refine as needed.
- **Step 13**: Refactor the 'create user profile' endpoint implementation for clarity and maintainability.
- **Step 14**: Run the tests again after refactoring to ensure the refactored code still passes all tests. Debug and refine if necessary.

### Key Notes on "Small":
- **Small Scope**: Each step addresses only one functionality or aspect (e.g., validating a username, not the entire login system).
- **Small Tests**: Test only one behavior or condition at a time (e.g., reject empty input, not all possible inputs).
- **Small Implementation**: Write just enough code to pass the current test case.
- **Small Refactoring**: Focus on improving only the part of the code related to the current functionality.
- **Small Validation**: Validate only the focused functionality after each step.
