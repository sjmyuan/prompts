# Example: Planning a POC for One ADR Option

**Scenario**: The payment-migration delivery can't pick a cache option from `adr-caching-01-cache-option.md`. The user says: "Plan a POC that builds the Redis option as a standalone feature so we can measure whether it beats in-process."

**Applies**: **plan-poc** → **export-plan**

## 1. Classify + clarify

- Classified: **POC** (an uncertain ADR option needs evidence — a standalone feature, not a snippet).
- Confirmed with the user: option = **Redis**; success criteria = p99 < 50ms @ 2k rps, ≤ 3 new ops dependencies; slice = a full caching layer behind the wallet-service read path.

## 2. Plan (TDD + evaluation step)

```markdown
## Scope Boundary
**In scope**: wallet-service read path + caching layer for the Redis option (`adr-caching-01-cache-option.md`)
**Out of scope**: the in-process option, other ADRs, unrelated modules
**Rule**: no step may change anything beyond **In scope**

1. Prepare Environment — POC branch `poc-adr-caching-01-redis` per repo convention
2. Write focused tests for cache get/set/evict (Redis)
3. Confirm tests fail · implement minimal Redis client + cache facade
4. Refactor + validate + cleanup + quality gate
5. **Evaluation**: run p99 latency benchmark @ 2k rps; count new ops deps — record vs criteria
```

## 3. Export

- `plan.md` marked `type: poc`; `context.md` records success criteria, `adr-caching-01-cache-option.md` references, and the evaluation method. Routes to **execute-plan** (POC mode) and stops at the evaluation report for the orchestrator's decision gate.
