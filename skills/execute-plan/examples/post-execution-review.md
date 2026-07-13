# Plan Executor: Post-Execution Review and Cleanup Example

**Scenario**: All plan steps are ✅ complete. Demonstrates **review-post-execution** (applying code-reviewer, adding fix steps for findings) and **clean-up-plan** (deleting PLAN.md).

---

## Context

A 5-step refactoring plan has just finished with all steps ✅. The executor now runs the post-execution review.

### Final Plan Status Before Review

```
### Step 1: Create DataValidator class ✅
### Step 2: Move validation logic to DataValidator ✅
### Step 3: Inject validator into DataImportedHandler ✅
### Step 4: Update handler tests ✅
### Step 5: Validate linting, formatting and type checking ✅
```

---

## Post-Execution Review

Applying **code-reviewer** skill on all changed files:
- `domain/validation/DataValidator.java`
- `application/handler/DataImportedHandler.java`
- `test/DataValidatorTest.java`
- `test/DataImportedHandlerTest.java`

### Review Findings

**🔴 Major — Missing null-check in DataValidator**
- `DataValidator.java:L14` — `validateId(record.getId())` is called before `validateNotNull(record)` guards against a null record. If `record` is null, `record.getId()` throws a `NullPointerException` before the null-check runs.
- **Recommendation**: Move `validateNotNull(record)` to be the first call inside `validate()`.

**🟡 Minor — Test only covers happy path**
- `DataValidatorTest.java` has one test for a valid record but no test for null input or invalid ID format.

---

## Adding Fix Steps to PLAN.md

```
### Step 6: Fix null-check ordering in DataValidator ⏳
### Step 7: Add missing null and invalid-input tests for DataValidator ⏳
```

### Step 6: Fix Null-Check Ordering 🔄

**Objective**: Ensure `validateNotNull` runs before any field access.
**Files**: `domain/validation/DataValidator.java`
**Implementation**:
```java
public void validate(DataRecord record) {
    validateNotNull(record);      // ← moved to first
    validateId(record.getId());
    validateName(record.getName());
    validateValue(record.getValue());
}
```
**Validation**: All existing tests still pass.
**Status**: ✅ Completed

#### Plan Status After Step 6
```
### Step 1: Create DataValidator class ✅
### Step 2: Move validation logic to DataValidator ✅
### Step 3: Inject validator into DataImportedHandler ✅
### Step 4: Update handler tests ✅
### Step 5: Validate linting, formatting and type checking ✅
### Step 6: Fix null-check ordering in DataValidator ✅
### Step 7: Add missing null and invalid-input tests for DataValidator ⏳
```

### Step 7: Add Missing Tests 🔄

**Objective**: Cover null input and invalid ID format in `DataValidatorTest`.
**Files**: `test/DataValidatorTest.java`
**Implementation**:
```java
@Test
void validate_throwsWhenRecordIsNull() {
    assertThrows(ValidationException.class, () -> validator.validate(null));
}

@Test
void validate_throwsWhenIdHasInvalidFormat() {
    DataRecord record = new DataRecord("invalid id!", "name", BigDecimal.ONE);
    assertThrows(ValidationException.class, () -> validator.validate(record));
}
```
**Validation**: All 7 tests pass including the 2 new ones.
**Status**: ✅ Completed

---

## Re-Running Code Reviewer

Applying **code-reviewer** on `DataValidator.java` and `DataValidatorTest.java` again.

**Result**: No 🚫 Blockers or 🔴 Major issues remain. Two 🟢 Nits (variable naming preferences) — documented in final summary, not blocking.

---

## Final Summary

All 7 steps completed ✅. Post-execution review resolved 1 🔴 Major issue (null-check ordering) and 1 🟡 Minor (test coverage). Two 🟢 Nits noted for future consideration.

**Cleaned up**: PLAN.md deleted.
