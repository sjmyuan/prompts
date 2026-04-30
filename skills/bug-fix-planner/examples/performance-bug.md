# Example: Performance Bug Fix

**Scenario**: Product search endpoint takes 8–12 seconds under normal load; profiling shows an N+1 query — for each product in the result set, a separate query fetches its category and tag lists

**Root Cause**: `ProductRepository.findByKeyword()` returns product entities with lazy-loaded `category` and `tags` associations; the serializer triggers one additional query per product when accessing those fields

**Bug-Fixing Plan**:

## Steps

- **Step 1**: Validate Baseline (run existing tests, linting, type-checking; capture current p99 latency with a benchmark)
- **Step 2**: Write performance test that asserts the endpoint completes within 500 ms for a 100-product result and issues no more than 3 database queries total
- **Step 3**: Confirm Test Failure — run benchmark to verify the test fails under current implementation
- **Step 4**: Fix Code — rewrite the repository query to use a JOIN FETCH (or equivalent eager-load) for `category` and `tags`; add a query-count assertion using a SQL counter interceptor
- **Step 5**: Verify Fix — re-run the performance test and all existing repository tests
- **Step 6**: Write regression test for the N+1 pattern (assert query count ≤ 3 for variable result sizes)
- **Step 7**: Confirm regression test passes
- **Step 8**: Clean Up Unused Code — remove any ad-hoc caching workarounds that were masking the underlying issue
- **Step 9**: Clean Up Tests — remove tests that asserted the old lazy-load behavior
- **Step 10**: Verify Cleanup
- **Step 11**: Validate Linting, Formatting and Type Checking

## Key Characteristics

- **Complexity**: Complex (requires profiling, query analysis, and benchmark validation)
- **Approach**: Full TDD cycle extended with performance benchmarks — write a performance test first, then fix, then add a query-count regression test
- **Focus**: Query efficiency, N+1 elimination, and measurable latency improvement
- **Test Coverage**: Latency under load, database query count, correctness of returned data after query refactor
- **Rationale for Extension**: Performance bugs require both a failing benchmark (to confirm the bug is measurable) and a query-count assertion (to prevent regression). Standard correctness tests alone cannot verify the fix.
