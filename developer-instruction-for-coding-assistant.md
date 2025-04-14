## User Task  

- Break down the user task into small, actionable steps following TDD principles.  
- Order steps logically for incremental development: start with unit tests, proceed to implementation, and finish with refactoring.  
- Each step should have a clear scope, expected outcome, and focus on one functionality or aspect.  

For each functionality or aspect, follow these six steps:  
1. **Write Tests**: Develop comprehensive unit tests covering all scenarios (happy path, edge cases, error handling).  
2. **Confirm Test Failure**: Run the tests to ensure they fail or cause compilation errors before implementation, validating the tests.  
3. **Implement Functionality**: Write minimal code sufficient to pass the tests.  
4. **Verify Implementation**: Run the tests again to confirm the code passes all tests, debugging and refining as needed.  
5. **Refactor Code**: Improve clarity, maintainability, and performance without changing behavior.  
6. **Validate Refactoring**: Run the tests again to ensure the refactored code still passes all tests, debugging and refining if necessary.  

Present the detailed steps before execution. For example:

   - **Step 1**: Define the data model for user profiles, including fields like `name`, `email`, and `id`.
   - **Step 2**: Write unit tests for data model validation, covering required fields, unique constraints, and edge cases (e.g., invalid email formats, missing fields).
   - **Step 3**: Confirm tests fail or result in compilation errors before implementation.
   - **Step 4**: Implement the data model with validation logic based on the tests.  
   - **Step 5**: Verify implementation by running tests, debugging and refining as needed.
   - **Step 6**: Refactor the data model implementation for clarity and maintainability.  
   - **Step 7**: Validate refactoring by running tests again, debugging and refining if necessary.
   - **Step 8**: Set up the database schema and migrations.
   - **Step 9**: Write unit tests for the 'create user profile' endpoint, including authentication checks, validation, and error handling (e.g., duplicate emails, missing fields).
   - **Step 10**: Confirm tests fail or result in compilation errors before implementation.
   - **Step 11**: Implement the 'create user profile' endpoint with authentication and validation logic.
   - **Step 12**: Verify implementation by running tests, debugging and refining as needed.
   - **Step 13**: Refactor the 'create user profile' endpoint implementation for clarity and maintainability.
   - **Step 14**: Validate refactoring by running tests again, debugging and refining if necessary.