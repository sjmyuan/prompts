````markdown
# Example: Observability & Deployment Safety Review (New Service Endpoint + DB Migration)

**Scenario**: Review of a PR that adds a new `/api/v1/orders/summary` endpoint backed by a new `order_summary` table, a Flyway migration, and a Redis cache layer.

**Review Focus**: Observability, deployment safety, migration backward-compatibility, and cache correctness.

## Code Review Summary

**Scope**: `feature/order-summary-endpoint` — new REST endpoint, DB migration, and Redis caching
**Focus Areas**: Observability, deployment safety, correctness, security
**Overall Assessment**: Requires two blockers to be addressed before merge; deployment sequence must be documented

---

## Findings

### 🚫 Blockers (Must Fix)

#### DB Migration Is Not Backward-Compatible
- **File**: [db/migration/V20_create_order_summary.sql](db/migration/V20_create_order_summary.sql)
- **Issue**: The migration adds a `NOT NULL` column `summary_status` to `orders` without a default value. If the old app version is still running during a rolling deploy, any `INSERT` from the old code will fail because it does not supply `summary_status`.
- **Impact**: Data loss and 500 errors during the deployment window in any rolling or blue/green deployment strategy.
- **Recommendation**: Add a default value, or split into two migrations (add nullable → backfill → add `NOT NULL` constraint) deployed across two separate releases.

#### Cache Has No Invalidation on Order Update
- **File**: [OrderSummaryService.java](OrderSummaryService.java#L72-L80)
- **Issue**: Summaries are cached in Redis with a 1-hour TTL but there is no `@CacheEvict` on `updateOrder()` or `cancelOrder()`. A cancelled order will appear as active in the summary for up to 60 minutes.
- **Impact**: Users see stale financial data; regulatory and support risk depending on the domain.
- **Recommendation**:
```java
@CacheEvict(value = "orderSummaries", key = "#orderId")
public void updateOrder(String orderId, OrderUpdate update) { ... }

@CacheEvict(value = "orderSummaries", key = "#orderId")
public void cancelOrder(String orderId) { ... }
```

---

### 🔴 Major Issues

#### No Logging on Cache Miss or Slow Query Path
- **File**: [OrderSummaryService.java](OrderSummaryService.java#L55-L68)
- **Issue**: When the cache misses and the DB query runs, there is no log statement and no metric counter. In production it will be impossible to distinguish "cache is working" from "cache is always missing" without querying Redis directly.
- **Impact**: The performance improvement cannot be validated post-deployment; latency regressions will be invisible.
- **Recommendation**:
```java
UserSummary summary = cache.get(orderId);
if (summary == null) {
    log.debug("Cache miss for orderId={}, fetching from DB", orderId);
    meterRegistry.counter("order.summary.cache", "result", "miss").increment();
    summary = repository.findSummaryById(orderId);
    cache.put(orderId, summary);
} else {
    meterRegistry.counter("order.summary.cache", "result", "hit").increment();
}
```

#### New Endpoint Has No Authorization Check
- **File**: [OrderSummaryController.java](OrderSummaryController.java#L28-L35)
- **Issue**: `GET /api/v1/orders/summary` has no `@PreAuthorize` annotation and is not listed in the security config's restricted paths. Any authenticated user can retrieve any other user's order summary by passing a different `orderId`.
- **Impact**: Horizontal privilege escalation — OWASP A01:2021 Broken Access Control.
- **Recommendation**: Add ownership check:
```java
@PreAuthorize("@orderSecurityService.isOwner(#orderId, authentication)")
@GetMapping("/{orderId}/summary")
public ResponseEntity<OrderSummary> getSummary(@PathVariable String orderId) { ... }
```

#### No Deployment Runbook
- **File**: PR description / missing
- **Issue**: This PR requires a specific deployment sequence: migration must run before the new code is deployed. There is no runbook, no PR checklist item, and no note in the README about this prerequisite.
- **Impact**: If a developer deploys app code before running the migration, the new endpoint will throw on every request.
- **Recommendation**: Add a deployment notes section to the PR and to the service README:
```markdown
## Deployment Notes — v2.4.0
1. Run `flyway migrate` against production DB **before** deploying the new application image.
2. Verify `order_summary` table exists and `summary_status` column is populated before routing traffic.
3. Monitor `order.summary.cache` hit/miss counters for the first 30 minutes post-deploy.
```

---

### 🟡 Minor Issues

#### Redis TTL Is Hardcoded
- **File**: [OrderSummaryService.java](OrderSummaryService.java#L72)
- **Issue**: `Duration.ofHours(1)` is hardcoded. Cannot be tuned for different environments without a code change.
- **Recommendation**: Externalize to configuration:
```yaml
# application.yaml
cache:
  order-summary:
    ttl: 1h
```

#### No Test Verifies Migration Is Backward-Compatible
- **File**: Tests missing
- **Issue**: No integration test runs the migration against an empty database and then exercises `INSERT` via the old schema to confirm compatibility.
- **Recommendation**: Add a `@MigrationTest` that verifies the old `INSERT` path succeeds after migration runs.

---

## Positive Highlights
- Flyway versioning is correctly sequenced; no gaps in version numbers.
- Redis cache key design (`"orderSummary::" + orderId`) is clean and avoids namespace collisions with other cache regions.
- The new endpoint follows the existing REST naming and response conventions consistently.

---

## Risks & Assumptions
- Review was based on source code alone; actual rolling deployment behavior depends on the orchestration platform (Kubernetes, ECS, etc.) — verify the deployment strategy handles the migration window correctly.
- Redis failure mode was not verified in code; if Redis is unavailable the cache miss path will fall through to the DB (acceptable), but this was not explicitly tested.

---

## Recommended Next Steps
1. Fix migration backward-compatibility (blocker — prevents safe rolling deploy)
2. Add cache invalidation on order mutations (blocker — stale data risk)
3. Add authorization check to the new endpoint (major — access control gap)
4. Add deployment runbook to the PR and README (major — operational safety)
5. Externalize Redis TTL to configuration (minor — defer if time-constrained)
````
