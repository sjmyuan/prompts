# Example: Refactor — Interface Extraction for Better Testability

**Scenario**: Add interface abstraction and dependency injection to `EventPublisherImpl` for better testability and loose coupling.

---

## Change Classification

Applies **classify-change-type**.

**User request:**
> "We need to make EventPublisherImpl easier to mock in tests. Can we extract an interface and inject it via Spring?"

**Agent classifies** — keywords: "extract interface", "easier to mock" → **Refactor** (structural change, no behavior change).

*User confirms classification: ✅*

---

## Refactor Scope Definition

Applies **define-refactor-scope**.

**Agent asks clarifying questions:**
> 1. Should the interface mirror all public methods of `EventPublisherImpl` or define a subset?
> 2. Are there other implementations of the publisher interface planned (e.g., test-only implementations)?
> 3. Any naming convention for interfaces (e.g., `IEventPublisher` or `EventPublisher`)?

**User responds:**
> Mirror all public methods. Yes, we'll create a mock-friendly test implementation. Use `EventPublisher` (no prefix).

**Agent confirms refactor scope:**
> Extract `EventPublisher` interface from `EventPublisherImpl`. Update `DataImportedHandler` to depend on the interface. Register the interface in Spring configuration. Create a `FakeEventPublisher` for testing. All existing tests must pass unchanged.

*User confirms: ✅*

---

## Refactoring Plan

Applies **plan-refactor**.

**TDD Approach**: Adapted — interface extraction doesn't change behavior; existing tests validate correctness

**Steps:**
- Step 1: Validate Baseline (run tests, linting, type-checking)
- Step 2: Create EventPublisher interface with method signatures
- Step 3: Update EventPublisherImpl to implement the interface
- Step 4: Update DataImportedHandler to depend on interface instead of implementation
- Step 5: Verify existing tests still pass
- Step 6: Update Spring configuration for interface-based dependency injection
- Step 7: Validate Linting, Formatting and Type Checking

## Key Characteristics

- **Complexity**: Simple — interface extraction without behavior change
- **TDD Approach**: Adapted — focus on validation rather than test-first
- **Focus**: Abstraction, dependency injection, testability
- **Testing Strategy**: Rely on existing tests to ensure behavior is preserved
- **Total Steps**: 7
- **Rationale**: Interface extraction doesn't change behavior, so full TDD cycle is not necessary. Existing tests validate that the refactoring is safe.
