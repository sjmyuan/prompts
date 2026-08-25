# Example: Spike from Existing Investigation Findings

**Scenario**: The user has already done informal investigation on a caching strategy problem and has notes. They want to formalize the findings into ADRs and a solution document without re-doing the investigation.

**Applies**: `define-spike-scope` → `compile-findings-doc` → `draft-problem-adrs` (option evaluation via `draft-adr`) → `compile-solution-doc` (skipping `investigate-per-area`; compile-findings-doc formalizes the provided findings)

**What makes this distinct**: Investigation is skipped because the user already has findings. The spike starts from ADR drafting (evaluation included), demonstrating the "provide pre-existing findings" rule.

---

## Define Spike Scope

### User Input
> "I've already looked into our caching problem. Here's what I found: [pastes notes]. Can you help me turn this into proper ADRs and a solution doc?"

### Assistant Output

*(Reviews the provided notes, then works through scope definition)*

**Spike Goal**: Define a caching strategy for the product catalog service to reduce database load and improve response times.

**Areas and problems** (derived from the user's notes, recorded in `scope.md`):

| # | Area | Problem ("How to …?") |
|---|---|---|
| 1 | Cache topology | How to position caches in the architecture? (application-level, distributed, CDN) |
| 2 | Cache invalidation strategy | How to keep cached data consistent with the source of truth? |

---

## Investigate Per Area — SKIPPED

*User provided pre-existing investigation findings. Skipping investigation per the "pre-existing findings" rule.*

---

## Compile Findings Document

*(compile-findings-doc applied to formalize the user's pre-existing investigation notes)*

### Findings Document: `findings-caching-strategy.md`

*(write-solution-doc applied to current state, seeded with the user's provided findings)*

**C2 Container Diagram (Current State)**: Product Catalog Service → PostgreSQL (no caching layer). 10K reads/sec, 50 writes/sec. DB CPU regularly exceeds 80%.

**Current Architecture Summary** (formalized from user's notes):
- Product Catalog Service queries PostgreSQL directly for all read operations
- No caching layer exists at any tier (application, distributed, or CDN)
- Database CPU exceeds 80% during peak traffic; P99 latency is 450ms
- Read-to-write ratio: 200:1 (10K reads/sec vs. 50 writes/sec)
- The service is the single source of truth for product data
- No existing Redis/ElastiCache infrastructure in the organization

**Constraints & Pain Points**:
- Database is the scaling bottleneck — cannot handle projected 2x traffic growth
- P99 latency of 450ms is above the 100ms target for cache hits
- Any caching solution must not increase write latency (already acceptable at ~50ms)
- No existing cache infrastructure — any solution requires new operational investment

**Raw Data & Metrics**:
- 10K reads/sec, 50 writes/sec (200:1 ratio)
- DB CPU: 80%+ during peak
- P99 latency: 450ms (target: <100ms for cache hits)
- Write latency: ~50ms (acceptable)

> *Findings formalized from your pre-existing notes. This document is the current-state baseline. Evaluation will compare solution options against these constraints. No re-investigation was needed.*

---

## Draft Problem ADRs — Evaluate + Draft

*(Per problem, an ADR-writer sub-agent runs the full `draft-adr` flow — drivers → options → **evaluate-options** → compile-adr — interactively with the user, seeded from the provided notes. The evaluation tables below are the evaluate stage of each drafting session.)*

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

### ADR: Cache topology — position caches

*(draft-adr applied — full ADR produced; saved as `adr-cache-topology-01-position-caches.md`)*

**Title**: Adopt Two-Tier Caching (In-Memory + Redis) for Product Catalog

**Status**: Draft

**Problem**: The product catalog service experiences 10K reads/second with only 50 writes/second. Database CPU regularly exceeds 80% during peak traffic. A caching layer is needed to reduce database load and improve P99 latency (currently 450ms).

**Decision Drivers**:
- Hard: Must reduce DB CPU below 50%; Must maintain < 100ms P99 for cache hits
- Soft: Prefer solutions that don't require application restarts for cache changes

**Chosen Option**: Two-tier cache: application-level Caffeine (30s TTL) + Redis cluster (5min TTL)

### ADR: Cache invalidation — keep cached data consistent

*(draft-adr applied — full ADR produced; saved as `adr-cache-invalidation-01-invalidate-cached-data.md`)*

**Title**: Use CDC-Based Cache Invalidation for Product Catalog

**Status**: Draft

**Chosen Option**: Cache-aside with Debezium CDC → Kafka → cache invalidation consumers

---

## Compile Solution Doc

*(write-solution-doc applied)*

### Final Output Bundle

**Solution Document**: `solution.md`
- C2 diagram showing Product Catalog Service with Caffeine + Redis, CDC pipeline for invalidation
- Sequence diagrams for read path (cache hit/miss) and write path (DB write → CDC → invalidation)
- API contracts unaffected (caching is transparent to callers)
- RAID: risk of Redis outage, assumption about CDC pipeline reliability

**ADRs** (one per problem, area-prefixed in `adrs/`, mirrored grouped by area in `solution.md`):
- `adr-cache-topology-01-position-caches.md` — Two-tier (Caffeine + Redis)
- `adr-cache-invalidation-01-invalidate-cached-data.md` — CDC-based

### Wrap-Up (conversation level — not written into any artifact)

> This spike skipped the investigation because you provided existing findings. If any investigation gaps are discovered during ADR review, we can re-run the investigation for specific areas.
