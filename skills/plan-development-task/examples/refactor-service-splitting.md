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

Applies **define-refactor-scope**.

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

Applies **plan-refactor**.

**TDD Approach**: Full TDD cycle for each service extraction — preserving existing behavior requires thorough test coverage

**Steps:**
- Step 1: Validate Baseline (run tests, mvn spotless:check, mvn checkstyle:check, mvn compile)
- Step 2: Write Tests for CategoryMappingService
- Step 3: Confirm Test Failure
- Step 4: Extract CategoryMappingService from DataImportedHandler
- Step 5: Verify Tests Pass
- Step 6: Clean Up unused code in DataImportedHandler
- Step 7: Clean Up Tests
- Step 8: Verify Cleanup
- Step 9: Validate Linting, Formatting and Type Checking
- Step 10: Write Tests for PriceTransformationService
- Step 11: Confirm Test Failure
- Step 12: Extract PriceTransformationService from DataImportedHandler
- Step 13: Verify Tests Pass
- Step 14: Clean Up unused code in DataImportedHandler
- Step 15: Clean Up Tests
- Step 16: Verify Cleanup
- Step 17: Validate Linting, Formatting and Type Checking

## Key Characteristics

- **Complexity**: Medium — involves extracting business logic into new services
- **TDD Approach**: Full cycle for each service extraction
- **Focus**: Single Responsibility Principle, service layer separation
- **Testing Strategy**: Independent test cycles per extracted service; existing handler tests stay green throughout
- **Total Steps**: 17
