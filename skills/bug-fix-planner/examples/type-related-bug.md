# Example: Type-Related Bug Fix

**Scenario**: NullPointerException when metadata list is empty in IncomingMessage.DataImported

---

## Root Cause Identification

Applies **identify-bug-root-cause**.

**User reports:**
> “We’re getting a NullPointerException in production when processing records that have no country info attached.”

**Agent gathers information** — reads `DataImportedHandler.java` and `IncomingMessage.java`. Finds: the handler calls `message.getDataImported().getCountryInfos().getFirst()` without checking whether the list is empty.

**Agent asks:**
> 1. Is an empty `countryInfos` list a valid business case, or does it indicate malformed input?
> 2. What should happen when the list is empty — skip processing, use a default, or throw a descriptive error?

**User responds:**
> Valid business case — some records have no country info. When the list is empty, the handler should skip the country mapping step and continue with other transformations.

**Agent confirms root cause:**
> `getCountryInfos().getFirst()` throws `NoSuchElementException` (surfaced as NullPointerException) when the list is empty. The fix is to use `Optional` to safely access the first element and bypass the country mapping step when none is present.

*User confirms: ✅*

---

## Bug-Fixing Plan (Adapted TDD — Focus on Type Safety)

Applies **plan-bug-fix**.

**Root Cause**: Missing null check before calling getFirst() on countryInfos

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
