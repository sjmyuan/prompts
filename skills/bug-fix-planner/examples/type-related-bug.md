# Example: Type-Related Bug Fix

**Scenario**: NullPointerException when metadata list is empty in IncomingMessage.DataImported

**Root Cause**: Missing null check before calling getFirst() on countryInfos

**Bug-Fixing Plan** (Adapted TDD - Focus on validation):

## Steps

- **Step 1**: Validate Baseline
- **Step 2**: Add validation test for empty countryInfos list
- **Step 3**: Confirm Test Failure
- **Step 4**: Update DataImportedHandler to use Optional<MetadataInfo> and handle empty list
- **Step 5**: Verify existing tests still pass
- **Step 6**: Run Checkstyle and fix any issues
- **Step 7**: Validate Quality

## Key Characteristics

- **Complexity**: Simple
- **Approach**: Adapted TDD with focus on null safety
- **Focus**: Type safety using Optional and proper null handling
- **Rationale for Adaptation**: Null-safety bugs benefit from using Java Optional patterns and validation tests. Existing tests provide adequate functional coverage.
