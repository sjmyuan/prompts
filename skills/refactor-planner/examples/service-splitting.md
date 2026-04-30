# Service Splitting Example

## Objective
Split large DataImportedHandler into smaller, focused service classes following Single Responsibility Principle

---

## Refactor Request Definition

Applies **define-refactor-request**.

**User request:**
> "DataImportedHandler is getting too big — it handles category mapping, price transformation, and localization all in one class. We want to split it up."

**Agent asks clarifying questions:**
> 1. Should the extracted services be stateless utilities or Spring-managed beans injected into the handler?
> 2. Is the goal for the handler to become a pure orchestrator, or should it retain some logic?
> 3. Are there existing tests for `DataImportedHandler` we must keep green throughout?
> 4. Any naming convention already established for service classes in this package?

**User responds:**
> Spring beans, injected. Pure orchestrator. Yes, existing tests must pass. Follow `<Domain>Service` naming.

**Agent confirms refactor scope:**
> Extract `CategoryMappingService` and `PriceTransformationService` from `DataImportedHandler`. The handler becomes a pure orchestrator delegating to these services. All existing handler tests must remain green. Each extraction follows a full TDD cycle.

*User confirms: ✅*

---

## Refactoring Plan

### Steps
- Step 1: Validate Baseline (run tests, mvn spotless:check, Checkstyle)
- Step 2: Write Tests for CategoryMappingService
- Step 3: Confirm Test Failure
- Step 4: Extract CategoryMappingService from DataImportedHandler
- Step 5: Verify Tests Pass
- Step 6: Clean Up unused code in DataImportedHandler
- Step 7: Clean Up Tests
- Step 8: Verify Cleanup
- Step 9: Validate Quality (mvn spotless:check, Checkstyle)
- Step 10: Write Tests for PriceTransformationService
- Step 11: Confirm Test Failure
- Step 12: Extract PriceTransformationService from DataImportedHandler
- Step 13: Verify Tests Pass
- Step 14: Clean Up unused code in DataImportedHandler
- Step 15: Clean Up Tests
- Step 16: Verify Cleanup
- Step 17: Validate Quality (mvn spotless:check, Checkstyle)

## Key Characteristics

- **Complexity**: Medium - involves extracting business logic into new services
- **TDD Approach**: Full cycle for each service extraction (Steps 2–9, then 10–17)
- **Focus**: Single Responsibility Principle, service layer separation
- **Testing Strategy**: Independent test cycles per extracted service; existing handler tests stay green throughout
