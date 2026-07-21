# Example: End-to-End Spike — Payment Service Migration

**Scenario**: The user wants to spike migrating a legacy payment processing service from a monolithic architecture to microservices. The spike should produce ADRs for each key decision area and a consolidated solution document.

**Applies**: All capabilities in sequence — `define-spike-scope` → `investigate-per-area` → `evaluate-solutions-per-area` → `draft-area-adrs` → `compile-solution-doc`

**What makes this distinct**: This is a full multi-area spike on a brownfield system with complex dependencies, demonstrating the complete 5-phase workflow.

---

## Phase 1: Define Spike Scope

### User Input
> "We need to spike migrating our payment processing service from the monolith to microservices. It handles credit card, bank transfer, and wallet payments. Currently it's a single Spring Boot app with ~200K LOC."

### Assistant Output (after clarification)

**Spike Goal**: Determine the target architecture for decomposing the payment monolith into independently deployable services, selecting technologies, and defining a migration strategy.

**Investigation Areas**:

| # | Area | Description |
|---|---|---|
| 1 | Service decomposition boundaries | How should we split the monolith? What are the bounded contexts and service boundaries? |
| 2 | Inter-service communication | How will the new services communicate (sync vs. async, protocol, message format)? |
| 3 | Database decomposition strategy | How do we break up the monolithic database? One DB per service, shared DB with views, or event-driven? |
| 4 | Migration strategy | How do we transition from monolith to microservices with zero downtime? Strangler fig, parallel run, or big-bang? |

---

## Phase 2: Investigate Per Area

### Area 1: Service Decomposition Boundaries

*[investigate-code skill applied]*

**Current State**:
- Single Spring Boot app with package-by-layer structure: `controller/`, `service/`, `repository/`, `domain/`
- Three main business domains identifiable in code: CreditCardPayment (40% of code), BankTransferPayment (30%), WalletPayment (25%), Shared utilities (5%)
- Domain packages are intermingled — credit card service directly imports bank transfer domain objects
- `PaymentOrchestrator` class (1200 lines) coordinates all payment types in one place

**Constraints & Pain Points**:
- Deployment: whole app redeploys when any payment type changes
- Scaling: cannot scale wallet payments independently during peak hours
- Team ownership: 3 teams work on different payment types but step on each other's code

### Area 2: Inter-service Communication

*[investigate-code skill applied]*

**Current State**:
- All communication is in-process method calls; no service boundaries exist yet
- External integrations use: REST (to bank APIs), gRPC (to wallet provider), SOAP (legacy acquirer)
- No message broker in the current ecosystem; team has no Kafka/RabbitMQ experience
- Circuit breaker pattern not used; external call failures propagate directly to users

### Area 3: Database Decomposition Strategy

*[investigate-code skill applied]*

**Current State**:
- Single PostgreSQL database, ~80 tables
- Payment types share `transactions`, `accounts`, and `audit_log` tables
- Stored procedures for settlement logic (2000+ lines across 12 procedures)
- No database-level access control per payment type; any service can query any table

### Area 4: Migration Strategy

*[investigate-code skill applied]*

**Current State**:
- Monolith deployed on Kubernetes with 3 replicas
- API Gateway (Kong) already routes `/api/payments/*` to the monolith
- CI/CD pipeline in GitHub Actions; canary deployments supported
- No feature flags or traffic splitting infrastructure currently in place

---

## Phase 3: Evaluate Solutions Per Area

### Area 1: Service Decomposition Boundaries

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A: Payment-type services** | One service per payment type + shared lib | Clear ownership per team; independent scaling | Shared lib coupling; cross-cutting concerns duplicated |
| **B: Domain-driven services** | Payment Initiation, Payment Processing, Settlement, Reconciliation | Aligned with business process; cleaner dependencies | More services; team restructuring needed |
| **C: Strangler extraction** | Extract one payment type at a time, leaving rest in monolith | Lowest risk; incremental | Temporary hybrid complexity |

**Assumed Solution**: Option A (Payment-type services) — aligns with existing team structure, minimizes organizational change, and allows independent scaling.

### Area 2: Inter-service Communication

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A: Synchronous REST** | Services call each other via REST APIs | Simple; team familiar | Tight coupling; cascading failures |
| **B: Async events (Kafka)** | Services communicate via event streams | Loose coupling; resilience | Team learning curve; eventual consistency complexity |
| **C: Hybrid** | REST for queries, events for commands | Best of both worlds | More infrastructure; two patterns to maintain |

**Assumed Solution**: Option C (Hybrid) — synchronous REST for real-time payment status queries, async Kafka events for payment processing commands and settlement.

### Area 3: Database Decomposition Strategy

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A: Database per service** | Each service owns its own database | True decoupling; independent scaling | Complex data migration; cross-service queries hard |
| **B: Shared DB + views** | One physical DB, schema-level separation with views | Simpler migration; existing SQL preserved | Not true decoupling; schema coupling remains |
| **C: Event-driven sync** | DB per service, synchronized via CDC events | Eventual consistency with audit trail | Complex to operate; eventual consistency |

**Assumed Solution**: Option A (Database per service) — phased implementation starting with the least-coupled payment type (Wallet), using the Strangler Fig pattern.

### Area 4: Migration Strategy

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A: Strangler Fig** | Incrementally replace monolith parts with new services | Low risk; reversible; incremental value | Takes longer; routing complexity during transition |
| **B: Parallel run** | Run old and new systems side by side, compare results | Highest confidence in correctness | Double operational cost; comparison logic complex |
| **C: Big-bang cutover** | Build everything, switch in one go | Clean cut; no transitional complexity | High risk; no rollback if something fails |

**Assumed Solution**: Option A (Strangler Fig) — extract Wallet payments first (simplest domain), then Bank Transfer, then Credit Card. Use API Gateway for traffic routing.

---

## Phase 4: Draft ADRs

### ADR 001: Payment Service Decomposition

*[draft-adr skill applied — full ADR produced]*

**Title**: ADR-001: Decompose Payment Monolith into Payment-Type Microservices

**Status**: Draft

**Problem**: The payment monolith couples three independent payment domains, preventing independent deployment and scaling, and causing team contention.

**Decision Drivers**:
- Hard: Must maintain existing SLA (99.9% uptime); Must not lose payment data during migration
- Soft: Prefer alignment with existing team structure; Prefer incremental migration

**Considered Options**: (A) Payment-type services, (B) Domain-driven services, (C) Strangler extraction

**Chosen Option**: A — Payment-type services (Wallet, Bank Transfer, Credit Card) with a shared utility library

**Consequences**:
- (+) Each team independently deploys and scales their payment type
- (+) Incremental extraction possible via Strangler Fig
- (-) Shared lib creates coupling risk; must be versioned and treated as an API
- (-) Cross-cutting concerns (auth, logging) may be duplicated across services

---

### ADR 002-004 (summarized)

Similar structured ADRs produced for communication strategy (ADR-002: Hybrid sync/async), database decomposition (ADR-003: Database per service), and migration strategy (ADR-004: Strangler Fig).

---

## Phase 5: Compile Solution Doc

*[write-solution-doc skill applied]*

### Final Output Bundle

**Solution Document**: `solution-doc-payment-migration.md`
- Business context: migrate payment monolith to microservices
- C2 Container Diagram: API Gateway → Wallet Service, Bank Transfer Service, Credit Card Service, each with own DB; Kafka event bus
- C3 Component Diagrams: per service (e.g., Wallet Service: Controller → Service → Repository → Wallet DB)
- Sequence Diagrams: payment initiation flow, settlement flow, migration toggle flow
- API Contracts: REST endpoints for queries, Kafka topic schemas for events
- RAID Analysis: risks around data consistency, assumptions about Kafka adoption, issues with SOAP legacy integration
- RACI Matrix: ownership per service and cross-cutting concerns

**ADRs**:
- ADR-001: Payment Service Decomposition (Payment-type services)
- ADR-002: Inter-service Communication (Hybrid sync/async)
- ADR-003: Database Decomposition (Database per service)
- ADR-004: Migration Strategy (Strangler Fig)

### Closing Notes

> The solution document adopts the assumed solutions from all four ADRs. If any ADR decision changes during team review, update the corresponding section in the solution document. All artifacts should be version-controlled in `docs/architecture/decisions/` and `docs/architecture/solutions/`.
