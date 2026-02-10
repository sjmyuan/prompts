# Example: Simple Logic Bug Fix

**Scenario**: DataImportedHandler sends incorrect data ID to message publisher

**Root Cause**: Using transformed ID instead of original ID in the outgoing message

**Bug-Fixing Plan**:

## Steps

- **Step 1**: Validate Baseline (run tests, Spotless, Checkstyle)
- **Step 2**: Write Tests for correct ID handling in DataImportedHandler
- **Step 3**: Confirm Test Failure
- **Step 4**: Fix ID mapping logic in DataImportedHandler
- **Step 5**: Verify Tests Pass
- **Step 6**: Clean Up Unused Code
- **Step 7**: Clean Up Tests
- **Step 8**: Verify Cleanup
- **Step 9**: Validate Quality (mvn spotless:check, Checkstyle)

## Key Characteristics

- **Complexity**: Simple
- **Approach**: Full TDD cycle
- **Focus**: Logic correctness and data mapping
- **Test Coverage**: ID transformation scenarios and edge cases
