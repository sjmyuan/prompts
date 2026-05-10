# Review Dimensions Reference

Reference checklist for **all 8 review dimensions**. Apply every relevant ✓ item from each dimension when conducting a code review.

1. **Correctness & Robustness**:
   - ✓ Logic errors and edge cases (null/undefined, empty collections, boundary values)
   - ✓ Error handling (try/catch coverage, error propagation, user-facing messages)
   - ✓ Input validation (type checking, range validation, sanitization)
   - ✓ State consistency (race conditions, concurrent access, state transitions)
   - ✓ Async/Promise handling (proper awaiting, error catching, cancellation)
   - ✓ Backward compatibility (API changes, data migration, deprecated features)

2. **Maintainability**:
   - ✓ Code clarity (self-documenting code, complex logic explained)
   - ✓ Naming (descriptive, consistent, follows conventions)
   - ✓ Function/component cohesion (single responsibility, appropriate size)
   - ✓ Code duplication (DRY principle, extraction opportunities)
   - ✓ Modularity (separation of concerns, loose coupling)
   - ✓ Project conventions (style guide, architectural patterns)

3. **Performance & Resources**:
   - ✓ Algorithmic complexity (O(n²) → O(n log n) opportunities)
   - ✓ Database optimization (N+1 queries, missing indexes, inefficient JOINs)
   - ✓ Performance hotspots (loops, database queries, network calls)
   - ✓ Rendering efficiency (unnecessary re-renders, memoization)
   - ✓ I/O patterns (batch operations, connection pooling)
   - ✓ Caching strategies (when to cache, invalidation logic, cache stampede risks)
   - ✓ Memory management (unbounded collections, memory leaks, resource cleanup)
   - ✓ Benchmark validation (performance test coverage for optimization claims)
   - ✓ Scalability (concurrent users, large datasets)

4. **Security & Privacy**:
   - ✓ Injection vulnerabilities (SQL, XSS, command injection)
   - ✓ Authentication/authorization (proper checks, token handling)
   - ✓ Secrets management (no hardcoded credentials, secure storage)
   - ✓ Dependency risks (outdated packages, known vulnerabilities)
   - ✓ Unsafe defaults (overly permissive access, insecure configurations)
   - ✓ Data privacy (PII handling, logging sensitive data)

5. **APIs, Contracts & Types**:
   - ✓ Public interface design (intuitive, consistent, minimal surface area)
   - ✓ Schema/type changes (breaking changes flagged, versioning)
   - ✓ Type safety (TypeScript strictness, avoiding `any`)
   - ✓ Error handling contracts (documented error conditions)
   - ✓ Safe failure modes (graceful degradation, fallbacks)

6. **Tests**:
   - ✓ Coverage of critical paths (happy path + edge cases + errors)
   - ✓ Regression coverage (tests for fixed bugs)
   - ✓ Test determinism (no flaky tests, proper mocking)
   - ✓ Test readability (clear AAA structure, descriptive names)
   - ✓ Alignment with requirements (tests verify actual requirements)
   - ✓ Test infrastructure: if the project has **no test coverage at all**, flag as 🔴 Major — recommend establishing a test baseline before merging production code

7. **Architecture**:
   - ✓ Modularity (clear boundaries, appropriate abstractions)
   - ✓ Extensibility (easy to add features without major refactors)
   - ✓ Alignment with project goals (fits existing patterns and vision)
   - ✓ Technical debt (quick fixes that need follow-up noted)

8. **Inconsistencies** *(treat existing code as potentially wrong — do NOT assume it is the correct baseline)*:
   - ✓ Naming style clashes (e.g., `camelCase` vs `snake_case`, `get` prefix vs none)
   - ✓ Pattern clashes (e.g., callbacks vs Promises vs async/await; class-based vs functional components)
   - ✓ API usage clashes (e.g., two different libraries doing the same job, two different ways to call the same API)
   - ✓ Error-handling style clashes (e.g., exceptions vs result objects vs error callbacks)
   - ✓ Structural clashes (e.g., flat vs nested directory layout, co-located vs separated test files)
   - ✓ Config/constant definition clashes (e.g., inline magic numbers vs named constants, scattered config vs centralized)

   **For every inconsistency found**:
   - Show **both** variants with concrete file/line references
   - Explain the trade-offs of each without declaring a winner
   - Explicitly ask the user (or note in the review) which variant should be the canonical one
   - Do **not** recommend "align with existing code" unless the existing code is clearly the established, intentional pattern
