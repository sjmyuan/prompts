# Example: Refactor — Split Large Handler into Focused Services

**Scenario**: Split a large `DataImportedHandler` into smaller, focused service classes following Single Responsibility Principle.

---

## Change Classification

Applies **classify-change-type**.

**User request:**
> "DataImportedHandler is getting too big — it handles category mapping, price transformation, and localization all in one class. We want to split it up."

**Agent classifies** — keywords: "split", "refactor without behavior change" → **Refactor** (internal restructuring, no new behavior).

*User confirms classification: ✅*

---

## Refactor Scope Definition

Applies **define-scope** (refactor).

**Agent asks clarifying questions:**
> 1. Should the extracted services be stateless utilities or Spring-managed beans injected into the handler?
> 2. Is the goal for the handler to become a pure orchestrator, or should it retain some logic?
> 3. Are there existing tests for `DataImportedHandler` we must keep green throughout?
> 4. Any naming convention already established for service classes in this package?

**User responds:**
> Spring beans, injected. Pure orchestrator. Yes, existing tests must pass. Follow `<Domain>Service` naming.

**Agent confirms refactor scope:**
> Extract `CategoryMappingService` and `PriceTransformationService` from `DataImportedHandler`. The handler becomes a pure orchestrator delegating to these services. All existing handler tests must remain green. Each extraction keeps tests green; characterization tests are added only where coverage is missing.

*User confirms: ✅*

---

## Refactoring Plan

Applies **plan-refactor**.

### Scope Boundary
**In scope**: `DataImportedHandler` decomposition into `CategoryMappingService` + `PriceTransformationService`, tests
**Out of scope**: behavior change, other handlers
**Rule**: no step may change anything beyond **In scope**

**TDD Approach**: Green-to-green for each service extraction — existing tests stay green throughout; characterization tests added only where coverage is missing

**Steps:**
- Step 1: Prepare Environment (run tests, mvn spotless:check, mvn checkstyle:check, mvn compile)
- Step 2: Confirm existing handler tests cover category mapping; add characterization tests if missing
- Step 3: Extract CategoryMappingService from DataImportedHandler
- Step 4: Verify all tests stay green
- Step 5: Clean Up unused code in DataImportedHandler
- Step 6: Clean Up Tests
- Step 7: Verify Cleanup
- Step 8: Validate Linting, Formatting and Type Checking
- Step 9: Confirm existing handler tests cover price transformation; add characterization tests if missing
- Step 10: Extract PriceTransformationService from DataImportedHandler
- Step 11: Verify all tests stay green
- Step 12: Clean Up unused code in DataImportedHandler
- Step 13: Clean Up Tests
- Step 14: Verify Cleanup
- Step 15: Validate Linting, Formatting and Type Checking

## Key Characteristics

- **Complexity**: Medium — involves extracting business logic into new services
- **TDD Approach**: Green-to-green for each service extraction
- **Focus**: Single Responsibility Principle, service layer separation
- **Testing Strategy**: Existing handler tests stay green throughout; characterization tests added only where coverage is missing
- **Total Steps**: 15
