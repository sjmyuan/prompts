````markdown
# Example: Branch Diff Review

**Scenario**: User asks to review changes between `main` and `feature/order-discount`, or supplies only one branch to diff against the current checkout.

---

## Workflow

### Step 1 – Identify branches

**One branch supplied**:
> "Review my branch `feature/order-discount`"

```bash
# Determine current branch
git rev-parse --abbrev-ref HEAD
# → main

# Get full diff
git diff main...feature/order-discount
```

**Two branches supplied**:
> "Review the diff between `release/1.2` and `feature/order-discount`"

```bash
git diff release/1.2...feature/order-discount
```

---

### Step 2 – Summarize changed files before diving in

```
Changed files (feature/order-discount vs main):
  M  src/order/OrderService.java          (+82 / -14)
  M  src/order/dto/OrderRequest.java      (+12 / -2)
  A  src/discount/DiscountCalculator.java (+120 / -0)
  M  src/discount/DiscountRepository.java (+18 / -5)
  M  tests/order/OrderServiceTest.java    (+95 / -8)

Total: +327 / -29 across 5 files
```

---

### Step 3 – Conduct the review

## Code Review Summary

**Scope**: `feature/order-discount` vs `main` — adds discount calculation to the order flow  
**Focus Areas**: Correctness, security, performance, test coverage  
**Overall Assessment**: Close to merge-ready; one security issue and one race condition must be addressed first

---

## Findings

### 🚫 Blockers (Must Fix)

#### Discount Code Not Sanitized Before Database Query
- **File**: [DiscountCalculator.java](DiscountCalculator.java#L44-L48)
- **Issue**: `discountCode` from the request is interpolated directly into a JPQL string instead of using a parameterized query.
- **Impact**: SQL/JPQL injection — an attacker can exfiltrate or corrupt the `discounts` table.
- **Recommendation**:
```java
// Before (unsafe)
String jpql = "FROM Discount WHERE code = '" + discountCode + "'";

// After (safe)
TypedQuery<Discount> query = em.createQuery(
    "FROM Discount WHERE code = :code", Discount.class);
query.setParameter("code", discountCode);
```

---

### 🔴 Major Issues

#### Race Condition in Discount Usage Counter
- **File**: [DiscountRepository.java](DiscountRepository.java#L62-L70)
- **Issue**: `usageCount` is read, incremented, and saved in separate steps without pessimistic locking. Under concurrent requests the counter can be under-incremented and a single-use discount may be applied multiple times.
- **Impact**: Financial loss from discount over-redemption under load.
- **Recommendation**: Use `@Lock(LockModeType.PESSIMISTIC_WRITE)` on the repository method, or an atomic SQL `UPDATE discount SET usage_count = usage_count + 1 WHERE id = :id AND usage_count < max_usage`.

#### Missing Test for Expired Discount
- **File**: [OrderServiceTest.java](OrderServiceTest.java#L140)
- **Issue**: Tests cover valid and invalid discount codes but no test verifies that an expired discount is rejected.
- **Impact**: Regression risk — expiry logic could silently break in a future refactor.
- **Recommendation**: Add:
```java
@Test
void shouldRejectExpiredDiscountCode() {
    Discount expired = buildDiscount("SAVE10", LocalDate.now().minusDays(1));
    when(discountRepository.findByCode("SAVE10")).thenReturn(Optional.of(expired));
    assertThrows(DiscountExpiredException.class,
        () -> orderService.applyDiscount(buildOrder(), "SAVE10"));
}
```

---

### 🟡 Minor Issues

#### `OrderRequest` Accepts Negative Quantity
- **File**: [OrderRequest.java](OrderRequest.java#L18)
- **Issue**: `quantity` field has no `@Min(1)` constraint; a value of `-1` passes validation.
- **Recommendation**: Add `@Min(value = 1, message = "Quantity must be at least 1")`.

#### `DiscountCalculator` Silently Returns 0 for Unknown Strategy
- **File**: [DiscountCalculator.java](DiscountCalculator.java#L80-L84)
- **Issue**: The `switch` default branch returns `BigDecimal.ZERO` without logging or throwing, making misconfigured discount types invisible.
- **Recommendation**: Log a warning or throw an `UnsupportedDiscountTypeException`.

---

### 🟢 Nits / Suggestions

- `applyDiscount()` in `OrderService.java` could be extracted to a private helper to reduce method length (currently 45 lines).
- Constant `0.0` on line 33 of `DiscountCalculator.java` could be named `NO_DISCOUNT` for readability.

---

## Positive Highlights
- New `DiscountCalculator` is well-structured with clear single responsibility.
- Test coverage is thorough for the happy path and covers several edge cases already.
- `OrderRequest` DTO cleanly separates concerns from the domain entity.

---

## Risks & Assumptions
- Assumes discount codes are case-insensitive — no normalization observed; verify DB collation matches.
- Distributed lock may be needed if the service runs with multiple replicas (see race condition finding).

---

## Recommended Next Steps
1. Fix JPQL injection (blocker — required before merge)
2. Add pessimistic lock on usage counter (major — required before merge)
3. Add expired-discount test (major — required before merge)
4. Add `@Min(1)` to `OrderRequest.quantity` (minor)
5. Handle unknown discount strategy explicitly (minor)

---

## Key Review Characteristics

- **Review Type**: Branch diff (`main` → `feature/order-discount`)
- **Diff obtained via**: `git diff main...feature/order-discount` (or MCP service)
- **Files reviewed**: 5 (327 lines added, 29 removed)
- **Severity Distribution**: 1 blocker, 2 major, 2 minor, 2 nits
- **Action Required**: Fix security and concurrency issues before merge
````
