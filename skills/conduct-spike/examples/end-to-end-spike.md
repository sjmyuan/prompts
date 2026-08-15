# Example: End-to-End Spike — Payment Service Migration

**Scenario**: The user wants to spike migrating a legacy payment processing service from a monolithic architecture to microservices. The spike should produce ADRs for each key decision area and a consolidated solution document.

**Applies**: All capabilities in sequence — `define-spike-scope` → `investigate-per-area` → `compile-findings-doc` → `evaluate-solutions-per-area` → `draft-area-adrs` → `compile-solution-doc`

**What makes this distinct**: This is a full multi-area spike on a brownfield system with complex dependencies, demonstrating the complete 5-phase workflow. It runs investigation, ADR drafting, and findings/solution-doc compilation directly in the orchestrating agent to keep the walkthrough readable; in practice these steps dispatch to sub-agents whenever available — including for single tasks — to preserve the orchestrating agent's context (see `reference/multi-agent-orchestration.md` and `examples/multi-agent-investigation.md`).

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

**Current State**: package-by-layer (`controller/`, `service/`, `repository/`, `domain/`); three intermingled domains — CreditCardPayment (40%), BankTransferPayment (30%), WalletPayment (25%), Shared (5%); `PaymentOrchestrator` (1200 lines) coordinates all payment types; credit card service imports bank-transfer domain objects.
**Constraints & Pain Points**: whole-app redeploy on any payment-type change; wallet cannot scale independently; 3 teams step on each other's code.

### Areas 2–4 (same pattern, abbreviated)

*[investigate-code skill applied per area]*

| Area | Current State | Key Constraint |
|---|---|---|
| 2. Inter-service communication | All in-process calls; external REST/gRPC/SOAP; no broker; no circuit breaker | No async experience; SOAP must be maintained |
| 3. Database decomposition | Single PostgreSQL ~80 tables; `transactions`/`accounts`/`audit_log` shared; 12 settlement stored procedures (2000+ lines) | No per-type access control |
| 4. Migration strategy | K8s (3 replicas); Kong routes `/api/payments/*`; GitHub Actions canary CI/CD | No feature flags or traffic splitting |

---

## Phase 2a: Completion Checkpoint

*[Investigation complete — the assistant confirms the result before formalizing findings]*

### Assistant

> "Investigation complete. Is this result sufficient, or should we investigate further before formalizing the findings?"

### User Response

> "It's sufficient for now — let's formalize. We can dig into the orchestrator call graph and monitoring after the first round of ADRs."

### Assistant

> "Got it. Proceeding to compile findings document."

---

## Phase 2b: Compile Findings Documents

*[compile-findings-doc applied — producing one consolidated findings document for 4 tightly-coupled areas]*

### Findings Document: `findings-payment-migration.md`

*[write-solution-doc skill applied to current state, adapted with constraints & pain points replacing RAID/RACI]*

**C2 Container Diagram (Current State)**: Single Spring Boot monolith → PostgreSQL database, with all payment types sharing the same app and DB.

**Current Architecture Summary**: monolithic Spring Boot app (~200K LOC), package-by-layer, three intermingled domains coordinated by `PaymentOrchestrator` (1200 lines); all communication in-process; single PostgreSQL (~80 tables) with `transactions`/`accounts`/`audit_log` as cross-domain hotspots; 12 settlement stored procedures (2000+ lines); deployed on Kubernetes (3 replicas) behind Kong API Gateway; no message broker, feature flags, or traffic splitting.

**Constraints & Pain Points**: full redeploy for any payment-type change; wallet cannot scale independently; three teams contend on the same code; no circuit breaker; no async experience; SOAP legacy must be maintained; canaries untested for routing migration.

**Raw Data & Metrics**: ~200K LOC · ~80 tables · 12 stored procedures · 3 replicas · 3 protocols (REST, gRPC, SOAP).

> *The findings document now serves as the current-state baseline. Evaluation will compare solution options against this baseline. ADRs will cite specific sections for evidence. The solution document will evolve these diagrams from as-is → to-be.*

---

## Phase 3: Evaluate Solutions Per Area

*(Evaluation dispatched to an ADR-writer sub-agent per **evaluate-solutions-per-area** — the `draft-adr` evaluate chain below ran interactively with the user inside the sub-agent session.)*

### Area 1: Service Decomposition Boundaries

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A: Payment-type services** | One service per payment type + shared lib | Clear ownership; independent scaling | Shared-lib coupling; duplicated cross-cutting concerns |
| **B: Domain-driven services** | Payment Initiation, Processing, Settlement, Reconciliation | Aligned with business process; cleaner deps | More services; team restructuring |
| **C: Strangler extraction** | Extract one payment type at a time | Lowest risk; incremental | Temporary hybrid complexity |

**Assumed Solution**: Option A (Payment-type services) — aligns with existing team structure, minimizes organizational change, and allows independent scaling.

### Area 2: Inter-service Communication

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A: Synchronous REST** | Services call each other via REST APIs | Simple; team familiar | Tight coupling; cascading failures |
| **B: Async events (Kafka)** | Services communicate via event streams | Loose coupling; resilience | Team learning curve; eventual consistency |
| **C: Hybrid** | REST for queries, events for commands | Best of both worlds | More infra; two patterns to maintain |

**Assumed Solution**: Option C (Hybrid) — synchronous REST for real-time payment status queries, async Kafka events for payment processing commands and settlement.

### Area 3: Database Decomposition Strategy

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A: Database per service** | Each service owns its own database | True decoupling; independent scaling | Complex migration; hard cross-service queries |
| **B: Shared DB + views** | One physical DB, schema-level separation via views | Simpler migration; existing SQL preserved | Not true decoupling; schema coupling remains |
| **C: Event-driven sync** | DB per service, synchronized via CDC events | Eventual consistency with audit trail | Complex to operate; eventual consistency |

**Assumed Solution**: Option A (Database per service) — phased implementation starting with the least-coupled payment type (Wallet), using the Strangler Fig pattern.

### Area 4: Migration Strategy

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A: Strangler Fig** | Incrementally replace monolith parts with new services | Low risk; reversible; incremental value | Takes longer; routing complexity during transition |
| **B: Parallel run** | Run old and new systems side by side, compare results | Highest confidence in correctness | Double operational cost; complex comparison |
| **C: Big-bang cutover** | Build everything, switch in one go | Clean cut; no transitional complexity | High risk; no rollback on failure |

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

**Solution Document**: `solution.md`
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

### Wrap-Up (conversation level — not written into any artifact)

> The solution document adopts the assumed solutions from all four ADRs. If any ADR decision changes during team review, the corresponding section of the solution document is rewritten in place. All artifacts are version-controlled together in the spike folder — `spikes/payment-migration/` — with the ADRs in `adrs/`, the solution doc (`solution.md`) and change summary at the root, and findings docs in `docs/` (see `examples/spike-artifact-layout.md`).
