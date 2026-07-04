# Example: Database Selection for a New Microservice

**Scenario**: The user is building a new order-management microservice and needs to choose a database. They have a clear problem statement and want a structured walkthrough. This example demonstrates all 5 capabilities in sequence (**define-problem** → **define-decision-drivers** → **define-considered-options** → **evaluate-options** → **compile-adr**) with a well-defined starting point.

---

## Capability: define-problem

**User input**:
> We're building a new order-management microservice that will handle ~10K orders/day. We need to pick a database. The service needs to support complex queries on order history, ACID transactions for payment processing, and it'll run on GCP.

**Agent output**:
> Let me restate the problem to make sure I understand:
>
> **Problem Statement**: We need to select a database for a new order-management microservice running on GCP that supports:
> - ~10,000 orders/day (moderate throughput)
> - Complex queries on order history (e.g., filtering by date range, status, customer)
> - ACID transactions for payment processing
> - Deployment on GCP
>
> Does this accurately capture the problem?

**User confirms**: Yes.

---

## Capability: define-decision-drivers

**User input**:
> Main factors: team knows PostgreSQL well, we need to keep infra costs low since we're early-stage, and latency for order lookups should be under 100ms. Also we're on GCP so managed services are preferred.

**Agent output**:
> Here are the decision drivers I've identified. I've separated hard constraints from soft preferences:
>
> **Hard Constraints (must-haves)**:
> 1. ACID transaction support — non-negotiable for payment processing
> 2. Query latency < 100ms for order lookups
> 3. Must run on or integrate cleanly with GCP
>
> **Soft Preferences (nice-to-haves)**:
> 4. Team expertise (PostgreSQL) — reduces ramp-up time
> 5. Low infrastructure cost — early-stage budget constraints
> 6. Managed service — reduces operational overhead
>
> Would you like to reorder or adjust any of these?

**User confirms**: Looks good.

---

## Capability: define-considered-options

**User input**:
> We're thinking Cloud SQL (PostgreSQL), but should we consider others?

**Agent output**:
> Cloud SQL (PostgreSQL) is a solid starting point. Let me brainstorm alternatives across a few dimensions:
>
> - **Do nothing / status quo**: Not applicable — new service
> - **Industry-standard**: Cloud Spanner (global scale, strong consistency), Firestore (serverless NoSQL)
> - **Build vs. buy**: All are managed — no build option here
> - **Incremental vs. big-bang**: We could start simple and migrate later
>
> Here are the options I'd propose for evaluation:
>
> 1. **Cloud SQL for PostgreSQL** — managed relational DB, full SQL, ACID
> 2. **Cloud Spanner** — globally distributed, strong consistency, relational
> 3. **Firestore** — serverless NoSQL document DB, real-time sync
>
> Do these three cover the viable options? Any others to add?

**User confirms**: These three are good.

---

## Capability: evaluate-options

**Evaluating Option 1: Cloud SQL for PostgreSQL**

**User input**:
> Pros: team already knows it, full ACID support, great query flexibility. Cons: might need read replicas at scale, max connections could be a bottleneck.

**Agent output**:
> **Cloud SQL for PostgreSQL — Evaluation**
>
> | Driver | Impact |
> |---|---|
> | ACID transactions ✅ | Full support — satisfies hard constraint #1 |
> | Query latency ✅ | Indexed queries well under 100ms — satisfies #2 |
> | GCP integration ✅ | Native GCP managed service — satisfies #3 |
> | Team expertise ✅ | Team already knows PostgreSQL — satisfies #4 |
> | Cost ⚠️ | Reasonable for moderate load; read replicas add cost — partial on #5 |
> | Managed service ✅ | Fully managed with automatic backups — satisfies #6 |
>
> **Pros**:
> - Good, because team expertise eliminates ramp-up time
> - Good, because full SQL + extensions cover all query patterns
> - Good, because mature ecosystem with tooling and monitoring
>
> **Cons**:
> - Bad, because connection pooling needed at scale (adds operational complexity)
> - Bad, because vertical scaling has an upper bound; read replicas introduce eventual consistency for reads
>
> Does this evaluation look accurate?

**User confirms**: Yes.

**Evaluating Option 2: Cloud Spanner**

**User input**:
> Pros: unlimited scale, strong consistency. Cons: expensive, team doesn't know it, overkill for 10K orders/day.

**Agent output**:
> **Cloud Spanner — Evaluation**
>
> | Driver | Impact |
> |---|---|
> | ACID transactions ✅ | Full support — satisfies #1 |
> | Query latency ✅ | < 10ms typical — satisfies #2 |
> | GCP integration ✅ | Native — satisfies #3 |
> | Team expertise ❌ | No team experience, steep learning curve — fails #4 |
> | Cost ❌ | Minimum ~$600/month even at idle — fails #5 |
> | Managed service ✅ | Fully managed — satisfies #6 |
>
> **Pros**:
> - Good, because unlimited horizontal scaling with no sharding
> - Good, because 99.999% SLA for critical workloads
>
> **Cons**:
> - Bad, because minimum cost is prohibitive for early-stage use
> - Bad, because team has zero experience; significant ramp-up required
> - Bad, because massive overkill for 10K orders/day — 2+ driver misses
>
> Does this evaluation look accurate?

**User confirms**: Yes, Spanner is clearly not the right choice.

**Evaluating Option 3: Firestore**

**User input**:
> Pros: serverless, cheap, real-time. Cons: no joins, limited querying, no native ACID across documents.

**Agent output**:
> **Firestore — Evaluation**
>
> | Driver | Impact |
> |---|---|
> | ACID transactions ❌ | Limited to 25 document groups; no cross-collection transactions — **fails hard constraint #1** |
> | Query latency ✅ | < 100ms typical — satisfies #2 |
> | GCP integration ✅ | Native — satisfies #3 |
> | Team expertise ⚠️ | Some team members have NoSQL experience — partial on #4 |
> | Cost ✅ | Pay-per-use, very low at this scale — satisfies #5 |
> | Managed service ✅ | Serverless, zero ops — satisfies #6 |
>
> **Pros**:
> - Good, because serverless pricing is ideal for early-stage
> - Good, because real-time sync could power live order-tracking features
>
> **Cons**:
> - Bad, because **fails the hard constraint of ACID transactions** — payment processing requires multi-document atomicity
> - Bad, because complex order-history queries (filtering, aggregation) require denormalization and composite indexes
> - Bad, because no JOINs force application-level data assembly
>
> Does this evaluation look accurate?

**User confirms**: Yes. Firestore fails the ACID requirement.

**Agent output (after all options evaluated)**:
> Here's the summary across all three options:
>
> | Driver | Cloud SQL (PG) | Cloud Spanner | Firestore |
> |---|---|---|---|
> | ACID transactions | ✅ | ✅ | ❌ (knock-out) |
> | Query latency < 100ms | ✅ | ✅ | ✅ |
> | GCP integration | ✅ | ✅ | ✅ |
> | Team expertise | ✅ | ❌ | ⚠️ |
> | Low cost | ⚠️ | ❌ | ✅ |
> | Managed service | ✅ | ✅ | ✅ |
>
> Firestore is eliminated by the ACID hard constraint. Cloud Spanner fails on cost and team expertise. Cloud SQL for PostgreSQL satisfies all hard constraints and 3/3 soft preferences.
>
> **Given the evaluations, which option best satisfies the decision drivers?**

**User confirms**: Cloud SQL for PostgreSQL.

---

## Capability: compile-adr

**Agent output**:
> Before I compile the ADR, let me gather metadata:
> - **Title**: What should we call this ADR? (e.g., "Database Selection for Order-Management Service")
> - **Owners**: Who is driving this ADR?
> - **Status**: draft, adopt, declined, or superseded?

**User input**:
> Title: "Database Selection for Order-Management Service", Owners: Alice (Tech Lead), Status: draft.

**Agent loads reference/adr-template.md and produces**:

```markdown
# 2026-07-04-Database-Selection-for-Order-Management-Service

* Status: draft
* Owners: Alice (Tech Lead)
* Date: 2026-07-04

## Context and Problem Statement

We need to select a database for a new order-management microservice running on GCP. The service will handle approximately 10,000 orders per day and must support complex queries on order history (filtering by date range, status, customer) and ACID transactions for payment processing.

## Decision Outcome

Chosen option: "Cloud SQL for PostgreSQL", because it is the only option that satisfies all three hard constraints (ACID transactions, query latency under 100ms, GCP integration) while also meeting all soft preferences — the team already has PostgreSQL expertise, costs are reasonable at the projected scale, and it is a fully managed GCP service.

## Consequences

Adopting Cloud SQL for PostgreSQL gives the team immediate productivity with zero ramp-up time and provides full SQL flexibility for complex order-history queries. The primary risk is that at significantly higher scale (10x+ growth), connection pooling and read replicas will be required, introducing operational complexity.

### Positive Consequences

* Immediate team productivity — everyone already knows PostgreSQL
* Rich SQL + extensions (PostGIS, pg_trgm) cover all current and foreseeable query patterns
* Fully managed with automatic backups, point-in-time recovery, and easy replica creation
* Mature ecosystem with extensive monitoring, tooling, and community support

### Risks

* Connection pooling (e.g., PgBouncer) will be needed if order volume grows significantly — plan for this in the architecture from day one
* Read replicas introduce eventual consistency for read operations — ensure the application layer can tolerate replica lag for non-critical reads
* If the service outgrows Cloud SQL's vertical scaling ceiling, a migration to Cloud Spanner or CockroachDB would be required — but this is unlikely at current projections

### Security

* Cloud SQL supports IAM integration, private IP with VPC, and encryption at rest and in transit
* Ensure customer PII in orders is encrypted at the application layer before storage
* Enable audit logging for all schema changes and sensitive queries

## Decision Drivers

* ACID transaction support (hard constraint — payment processing)
* Query latency < 100ms for order lookups (hard constraint)
* Must run on or integrate cleanly with GCP (hard constraint)
* Team expertise in PostgreSQL (soft preference)
* Low infrastructure cost — early-stage budget constraints (soft preference)
* Managed service to reduce operational overhead (soft preference)

## Considered Options

* Cloud SQL for PostgreSQL
* Cloud Spanner
* Firestore

## Evaluation of the Options

### Cloud SQL for PostgreSQL

Fully managed relational database on GCP. Supports full PostgreSQL with ACID transactions, complex queries with JOINs, and a mature extension ecosystem.

#### Pros

* Good, because team expertise eliminates ramp-up time
* Good, because full SQL + extensions cover all query patterns
* Good, because mature ecosystem with tooling and monitoring

#### Cons

* Bad, because connection pooling needed at scale (adds operational complexity)
* Bad, because vertical scaling has an upper bound; read replicas introduce eventual consistency for reads

### Cloud Spanner

Globally distributed relational database with strong consistency and unlimited horizontal scaling.

#### Pros

* Good, because unlimited horizontal scaling with no sharding
* Good, because 99.999% SLA for critical workloads

#### Cons

* Bad, because minimum cost (~$600/month) is prohibitive for early-stage use
* Bad, because team has zero experience; significant ramp-up required
* Bad, because massive overkill for 10K orders/day

### Firestore

Serverless NoSQL document database with real-time sync and pay-per-use pricing.

#### Pros

* Good, because serverless pricing is ideal for early-stage
* Good, because real-time sync could power live order-tracking features

#### Cons

* Bad, because fails the hard constraint of ACID transactions — payment processing requires multi-document atomicity
* Bad, because complex order-history queries require denormalization and composite indexes
* Bad, because no JOINs force application-level data assembly

## References
```

**Agent output**:
> Here's the completed ADR. Would you like to adjust any section before saving?
