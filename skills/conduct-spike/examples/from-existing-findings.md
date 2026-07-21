# Example: Spike from Existing Investigation Findings

**Scenario**: The user has already done informal investigation on a caching strategy problem and has notes. They want to formalize the findings into ADRs and a solution document without re-doing the investigation.

**Applies**: `define-spike-scope` → `evaluate-solutions-per-area` → `draft-area-adrs` → `compile-solution-doc` (skipping `investigate-per-area`)

**What makes this distinct**: The investigation phase is skipped because the user already has findings. The spike starts from evaluation, demonstrating the "provide pre-existing findings" rule.

---

## Phase 1: Define Spike Scope

### User Input
> "I've already looked into our caching problem. Here's what I found: [pastes notes]. Can you help me turn this into proper ADRs and a solution doc?"

### Assistant Output

*[Assistant reviews the provided notes, then works through scope definition]*

**Spike Goal**: Define a caching strategy for the product catalog service to reduce database load and improve response times.

**Investigation Areas** (derived from user's notes):

| # | Area | Description |
|---|---|---|
| 1 | Cache topology | Where should caches sit in the architecture? (application-level, distributed, CDN) |
| 2 | Cache invalidation strategy | How will cached data stay consistent with the source of truth? |

---

## Phase 2: Investigate Per Area — SKIPPED

*User provided pre-existing investigation findings. Skipping investigation phase per the "pre-existing findings" rule.*

---

## Phase 3: Evaluate Solutions Per Area

*[Based on user's notes, the assistant helps structure and complete the evaluation]*

### Area 1: Cache Topology

| Option | Pros | Cons |
|---|---|---|
| **A: In-memory (Caffeine/Guava)** | Simplest; no network latency; no new infra | Per-instance; cold starts; memory contention with app |
| **B: Redis (ElastiCache)** | Shared cache; persistence; rich data structures | Network hop; new infra cost; operational overhead |
| **C: Two-tier (in-memory + Redis)** | Best latency for hot keys; resilience | Complexity; two sources of staleness; harder to debug |

**Assumed Solution**: Option C (Two-tier) — in-memory Caffeine cache with 30s TTL for ultra-hot keys, backed by Redis cluster for shared cache with 5min TTL.

### Area 2: Cache Invalidation Strategy

| Option | Pros | Cons |
|---|---|---|
| **A: TTL-only** | Simplest; no coordination needed | Stale data window; wasted cache space |
| **B: Write-through** | Always consistent; good for read-heavy workloads | Write latency penalty; cache must be available for writes |
| **C: Cache-aside with CDC invalidation** | Eventual consistency; decoupled; no write penalty | Eventual consistency window; CDC pipeline complexity |

**Assumed Solution**: Option C (Cache-aside with CDC) — services write to DB only; Debezium CDC captures changes and publishes invalidation events to Kafka; cache consumers listen and invalidate affected keys.

---

## Phase 4: Draft ADRs

### ADR-001: Cache Topology for Product Catalog

*[draft-adr skill applied — full ADR produced]*

**Title**: ADR-001: Adopt Two-Tier Caching (In-Memory + Redis) for Product Catalog

**Status**: Draft

**Problem**: The product catalog service experiences 10K reads/second with only 50 writes/second. Database CPU regularly exceeds 80% during peak traffic. A caching layer is needed to reduce database load and improve P99 latency (currently 450ms).

**Decision Drivers**:
- Hard: Must reduce DB CPU below 50%; Must maintain < 100ms P99 for cache hits
- Soft: Prefer solutions that don't require application restarts for cache changes

**Chosen Option**: Two-tier cache: application-level Caffeine (30s TTL) + Redis cluster (5min TTL)

### ADR-002: Cache Invalidation via CDC

*[draft-adr skill applied — full ADR produced]*

**Title**: ADR-002: Use CDC-Based Cache Invalidation for Product Catalog

**Status**: Draft

**Chosen Option**: Cache-aside with Debezium CDC → Kafka → cache invalidation consumers

---

## Phase 5: Compile Solution Doc

*[write-solution-doc skill applied]*

### Final Output Bundle

**Solution Document**: `solution-doc-caching-strategy.md`
- C2 diagram showing Product Catalog Service with Caffeine + Redis, CDC pipeline for invalidation
- Sequence diagrams for read path (cache hit/miss) and write path (DB write → CDC → invalidation)
- API contracts unaffected (caching is transparent to callers)
- RAID: risk of Redis outage, assumption about CDC pipeline reliability

**ADRs**:
- ADR-001: Cache Topology (Two-tier: Caffeine + Redis)
- ADR-002: Cache Invalidation (CDC-based)

### Closing Notes

> Note: This spike skipped the investigation phase because you provided existing findings. If any investigation gaps are discovered during ADR review, you can re-run the investigation phase for specific areas.
