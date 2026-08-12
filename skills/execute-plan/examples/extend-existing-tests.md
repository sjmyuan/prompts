# Plan Executor: Extending Existing Tests Example

**Scenario**: A feature step adds new validation rules to an existing validator. The executor applies **place-tests**: locates the existing test class, checks current coverage, extends it — instead of creating a new test file — and skips a redundant test when coverage already exists.

**Applies**: **place-tests**, **execute-step**

## User Request

"Execute the plan to add a max-length rule (50 chars) and an uppercase-ID rule to DataValidator."

## Plan to Execute

1. Add max-length and uppercase-ID rules to DataValidator
2. Add unit tests for the new rules
3. Run lint, formatting and type checks

## Step 2: Add Unit Tests for the New Rules 🔄

Applying **place-tests** before writing any test code.

### Locate existing test homes
`DataValidator` (changed in Step 1) already has a unit-level test file: `test/DataValidatorTest.java` (12 methods, same module).

### Assess existing coverage
Reading `DataValidatorTest.java`:
- `validate_throwsWhenNameTooLong` covers a name-length check but at a different boundary — the new 50-char limit is **partially covered**.
- `validate_acceptsUppercaseId` already asserts an uppercase ID passes — the uppercase-ID rule is **already covered**.

### Decide placement (per test-placement)
- **Max-length rule** → extend `DataValidatorTest.java`: add one method for the 50-char boundary.
- **Uppercase-ID rule** → add nothing; run the existing test instead. A duplicate would add noise.

### Apply
**Files**: Modifying `test/DataValidatorTest.java`
**Implementation**:
```java
@Test
void validate_rejectsNameOverFiftyChars() {
    DataRecord record = new DataRecord("ID-1", "x".repeat(51), BigDecimal.ONE);
    assertThrows(ValidationException.class, () -> validator.validate(record));
}
```

**Validation**: All 13 tests pass — 1 new method + 12 existing (including `validate_acceptsUppercaseId`, which covers the uppercase-ID rule).
**Status**: ✅ Completed

#### Plan Status After Step 2
### Step 1: Add max-length and uppercase-ID rules to DataValidator ✅
### Step 2: Add unit tests for the new rules ✅ (extended `DataValidatorTest.java`; no new file)
### Step 3: Run lint, formatting and type checks ⏳

**Note**: Decision recorded in the plan file — extended the existing `DataValidatorTest.java`; no new test file created; the uppercase-ID rule needed no new test because `validate_acceptsUppercaseId` already covers it.
