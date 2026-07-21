# Example: Single-Area Spike — Database Choice for New Service

**Scenario**: The user wants to spike the choice of database for a new analytics service. Since this is a greenfield service with a single clear decision, it's a single-area spike.

**Applies**: All capabilities — `define-spike-scope` → `investigate-per-area` → `evaluate-solutions-per-area` → `draft-area-adrs` → `compile-solution-doc`

**What makes this distinct**: Single investigation area with greenfield context (no existing implementation to investigate). Demonstrates the workflow still applies in full but with a lighter touch.

---

## Phase 1: Define Spike Scope

### User Input
> "We're building a new analytics service that needs to ingest clickstream events and support real-time dashboards. I need to decide what database to use."

### Assistant Output (after clarification)

**Spike Goal**: Select the optimal database for a clickstream analytics service supporting high-throughput writes and real-time dashboard queries.

**Investigation Areas**:

| # | Area | Description |
|---|---|---|
| 1 | Database selection | Which database (or combination) best supports the write throughput, query patterns, and operational constraints of the analytics service? |

---

## Phase 2: Investigate Per Area

### Area 1: Database Selection

*[investigate-code skill applied — adapted for greenfield]*

**Current State**: No existing analytics service. However, the organization has:
- PostgreSQL for all relational workloads (team has deep expertise)
- Elasticsearch used by the search team for log indexing
- No existing ClickHouse, Druid, or other OLAP database experience
- Infrastructure runs on AWS (EKS); team prefers managed services

**Constraints**:
- Expected write throughput: 50K events/second peak
- Query patterns: time-series aggregations, funnel analysis, real-time counters
- Retention: raw events for 30 days, aggregated data for 2 years
- Team size: 4 backend engineers, no dedicated DBA

**Relevant patterns from org**: All existing services use PostgreSQL via JPA/Hibernate. DevOps team manages infrastructure via Terraform.

---

## Phase 3: Evaluate Solutions Per Area

### Area 1: Database Selection

| Option | Pros | Cons |
|---|---|---|
| **A: PostgreSQL + materialized views** | Team already knows it; no new infra; Good enough for moderate scale | Write throughput ceiling; materialized view refresh lag; not purpose-built for OLAP |
| **B: ClickHouse (self-hosted on EKS)** | Purpose-built for analytics; excellent write & query performance; columnar storage | New technology for team; operational burden; no managed AWS offering |
| **C: Apache Druid (self-hosted)** | Real-time ingestion; pre-aggregation; good for time-series | Complex architecture (multiple node types); heavy ops; steep learning curve |
| **D: Amazon Timestream (managed)** | Fully managed; serverless; designed for time-series; AWS-native | Vendor lock-in; limited query flexibility compared to SQL; relatively new service |
| **E: ClickHouse Cloud (managed)** | Managed ClickHouse; AWS integration; purpose-built OLAP; SQL-compatible | New vendor relationship; cost at scale uncertain; team still needs ClickHouse knowledge |

**Decision Drivers**:
- Hard: Must handle 50K writes/sec; Must support SQL-like queries for dashboard team; Must fit within existing AWS infrastructure
- Soft: Prefer managed service to reduce ops burden; Prefer technology with organizational learning overlap

**Assumed Solution**: Option E (ClickHouse Cloud) — managed, purpose-built for analytics, SQL-compatible, integrates with AWS. Trade-off is a new vendor and technology learning curve, but the managed aspect reduces operational risk.

---

## Phase 4: Draft ADR

### ADR-001: Database Selection for Analytics Service

*[draft-adr skill applied]*

**Title**: ADR-001: Select ClickHouse Cloud as the Database for the Analytics Service

**Status**: Draft

**Problem**: The new analytics service requires a database capable of ingesting 50K events/second and supporting real-time dashboard queries with SQL-like semantics. The team's existing PostgreSQL expertise is insufficient for the expected write throughput and query patterns.

**Decision Drivers**:
- Hard: 50K writes/sec peak throughput; SQL-compatible query interface; AWS-native deployment
- Soft: Managed service preferred; Learning curve manageable for 4-person team

**Considered Options**: PostgreSQL (status quo), self-hosted ClickHouse, Apache Druid, Amazon Timestream, ClickHouse Cloud

**Chosen Option**: ClickHouse Cloud — managed service providing purpose-built OLAP capabilities with SQL compatibility and AWS integration. The managed aspect mitigates the team's lack of ClickHouse operations experience.

**Consequences**:
- (+) Purpose-built for the workload; no throughput ceiling concerns
- (+) Managed service eliminates operational burden of self-hosting
- (+) SQL interface minimizes dashboard team migration effort
- (-) New technology for the team; training and ramp-up required
- (-) New vendor relationship; cost monitoring needed at scale
- (-) Different query patterns than PostgreSQL; team must adapt from ORM-based access

---

## Phase 5: Compile Solution Doc

*[write-solution-doc skill applied]*

### Final Output Bundle

**Solution Document**: `solution-doc-analytics-database.md`
- Business context: new analytics service for clickstream data
- C2 Container Diagram: API Gateway → Analytics Ingestion Service → ClickHouse Cloud; Dashboard Service → ClickHouse Cloud; with PostgreSQL for service metadata
- C3 Component Diagram: Analytics Ingestion Service (Ingest Controller → Batch Processor → ClickHouse Writer)
- Sequence Diagrams: event ingestion flow, dashboard query flow
- API Contracts: ingestion endpoint (POST /events), query endpoint (GET /analytics)
- RAID Analysis: risk around ClickHouse learning curve, assumption about 50K/sec estimate, dependency on ClickHouse Cloud SLA

**ADR**:
- ADR-001: Database Selection for Analytics Service (ClickHouse Cloud)

### Closing Notes

> This is a single-area spike. The solution document is simpler than a multi-area spike but still provides C4 diagrams, API contracts, and RAID analysis for the new service. If additional decisions arise during implementation (e.g., schema design, partitioning strategy), they can be addressed in follow-up ADRs.
