# Example: Performance Bug Fix

**Scenario**: Product search endpoint takes 8–12 seconds under normal load; profiling shows an N+1 query — for each product in the result set, a separate query fetches its category and tag lists

---

## Root Cause Identification

Applies **identify-bug-root-cause**.

**User reports:**
> “The `/products/search` endpoint is very slow — 8 to 12 seconds for a typical query. Users are complaining and we’ve seen it get worse as the catalog grows.”

**Agent gathers information** — reads `ProductController.java`, `ProductRepository.java`, and runs a query-count diagnostic. Finds: `ProductRepository.findByKeyword()` returns product entities with lazy-loaded `category` and `tags` associations. The serializer accesses those fields for each product, triggering a separate DB query per record.

**Agent asks:**
> 1. Are `category` and `tags` always needed in the search result, or only in certain views?
> 2. Is there an existing benchmark or SLA target for this endpoint?

**User responds:**
> Always needed in the search result. No formal SLA yet, but under 500 ms is expected for a 100-product page.

**Agent confirms root cause:**
> `ProductRepository.findByKeyword()` triggers N+1 queries: one for the product list plus one per product to fetch `category` and `tags`. For 100 results that is 201 queries. The fix is to rewrite the query to use a JOIN FETCH (or equivalent eager-load) so all data is fetched in ≤3 queries.

*User confirms: ✅*

---

## Bug-Fixing Plan

Applies **plan-bug-fix**.

**Root Cause**: `ProductRepository.findByKeyword()` returns product entities with lazy-loaded `category` and `tags` associations; the serializer triggers one additional query per product when accessing those fields

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
