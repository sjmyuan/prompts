# Example: End-to-End Spike — Payment Service Migration

**Scenario**: The user wants to spike migrating a legacy payment processing service from a monolithic architecture to microservices. The spike should produce ADRs for each key decision problem (grouped by area) and a consolidated solution document.

**Applies**: All capabilities in sequence — `define-spike-scope` → `investigate-per-area` → `compile-findings-doc` → `evaluate-problem-solutions` → `draft-problem-adrs` → `compile-solution-doc`

**What makes this distinct**: Full multi-area brownfield spike demonstrating the complete 5-phase workflow end to end (see `examples/multi-agent-investigation.md` for the parallel-dispatch variant).

---

## Phase 1: Define Spike Scope

### User Input
> "We need to spike migrating our payment processing service from the monolith to microservices. It handles credit card, bank transfer, and wallet payments. Currently it's a single Spring Boot app with ~200K LOC."

### Assistant Output (after clarification)

**Spike Goal**: Determine the target architecture for decomposing the payment monolith into independently deployable services, selecting technologies, and defining a migration strategy.

**Areas and problems** (each problem → one ADR, recorded in `scope.md`):

| # | Area | Problems ("How to …?") |
|---|---|---|
| 1 | Service decomposition boundaries | How to split the monolith? What are the bounded contexts and service boundaries? |
| 2 | Inter-service communication | How to handle service-to-service communication (sync vs. async, protocol, message format)? |
| 3 | Database decomposition strategy | How to break up the monolithic database? · How to migrate the schema safely? |
| 4 | Migration strategy | How to transition from monolith to microservices with zero downtime? Strangler fig, parallel run, or big-bang? |

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

### Assistant → User

> "Investigation complete — is this sufficient, or should we investigate further before formalizing?"
> User: "It's sufficient — let's formalize. We can dig into the orchestrator call graph after the first round of ADRs."

---

## Phase 2b: Compile Findings Documents

*[compile-findings-doc applied — producing one consolidated findings document for 4 tightly-coupled areas]*

### Findings Document: `findings-payment-migration.md`

*[write-solution-doc skill applied to current state, adapted with constraints & pain points replacing RAID/RACI]*

**C2 Container Diagram (Current State)**: Single Spring Boot monolith → PostgreSQL database, with all payment types sharing the same app and DB.

**Current Architecture Summary**: monolithic Spring Boot app (~200K LOC), package-by-layer, three intermingled domains coordinated by `PaymentOrchestrator` (1200 lines); all communication in-process; single PostgreSQL (~80 tables) with `transactions`/`accounts`/`audit_log` as cross-domain hotspots; 12 settlement stored procedures (2000+ lines); deployed on Kubernetes (3 replicas) behind Kong API Gateway; no message broker, feature flags, or traffic splitting.

**Constraints & Raw Data**: full redeploy for any payment-type change; wallet cannot scale; three teams contend on the same code; no circuit breaker; no async experience; SOAP legacy must be maintained · ~200K LOC · ~80 tables · 12 stored procedures · 3 replicas · 3 protocols (REST, gRPC, SOAP).

> *Findings = current-state baseline; evaluation compares options against it; ADRs cite its evidence; the solution doc evolves these diagrams as-is → to-be.*

---

## Phase 3: Evaluate Problem Solutions

*(Evaluation dispatched per problem to an ADR-writer sub-agent per **evaluate-problem-solutions** — a whole area's problems share one brief when evidence is shared; the `draft-adr` evaluate chain below ran interactively with the user inside the sub-agent session.)*

### Area 1: Service Decomposition — problem: How to split the monolith?

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A: Payment-type services** | One per payment type + shared lib | Clear ownership; independent scaling | Shared-lib coupling; duplicated concerns |
| **B: Domain-driven services** | Initiation, Processing, Settlement, Reconciliation | Aligned with business process | More services; team restructuring |
| **C: Strangler extraction** | Extract one payment type at a time | Lowest risk; incremental | Temporary hybrid complexity |

**Assumed Solution**: Option A (Payment-type services) — aligns with existing team structure, minimizes organizational change, and allows independent scaling.

### Area 2: Inter-service Communication

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A: Synchronous REST** | Services call via REST | Simple; team familiar | Tight coupling; cascading failures |
| **B: Async events (Kafka)** | Event streams | Loose coupling; resilience | Learning curve; eventual consistency |
| **C: Hybrid** | REST for queries, events for commands | Best of both worlds | More infra; two patterns |

**Assumed Solution**: Option C (Hybrid) — synchronous REST for real-time payment status queries, async Kafka events for payment processing commands and settlement.

### Area 3: Database Decomposition Strategy

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A: Database per service** | Each service owns its DB | True decoupling; independent scaling | Complex migration; hard cross-service queries |
| **B: Shared DB + views** | Schema-level separation via views | Simpler migration; SQL preserved | Not true decoupling |
| **C: Event-driven sync** | DB per service, CDC events | Eventual consistency + audit trail | Complex to operate |

**Assumed Solution**: Option A (Database per service) — phased implementation starting with the least-coupled payment type (Wallet), using the Strangler Fig pattern.

**Second problem — How to migrate the schema safely?** (→ `adr-database-02-schema-migration.md`): Options — (A) expand-contract migrations shipped with each service (**chosen**), (B) central schema-migration tool (single choke point), (C) shared DB with views during transition (deferred). **Assumed solution**: Option A.

### Area 4: Migration Strategy

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A: Strangler Fig** | Incrementally replace parts | Low risk; reversible; incremental value | Takes longer; routing complexity |
| **B: Parallel run** | Run old and new side by side | Highest correctness confidence | Double operational cost |
| **C: Big-bang cutover** | Build everything, switch at once | Clean cut; no transition complexity | High risk; no rollback |

**Assumed Solution**: Option A (Strangler Fig) — extract Wallet payments first (simplest domain), then Bank Transfer, then Credit Card. Use API Gateway for traffic routing.

---

## Phase 4: Draft Problem ADRs

### ADR: Service decomposition — split the monolith

*[draft-adr skill applied — full ADR produced; saved as `adr-service-decomposition-01-split-monolith.md`, tagged `Area: Service decomposition`]*

**Title**: Decompose Payment Monolith into Payment-Type Microservices

**Status**: Draft

**Problem**: The payment monolith couples three independent payment domains, preventing independent deployment and scaling, and causing team contention.

**Decision Drivers**:
- Hard: Must maintain existing SLA (99.9% uptime); Must not lose payment data during migration
- Soft: Prefer alignment with existing team structure; Prefer incremental migration

**Considered Options**: (A) Payment-type services, (B) Domain-driven services, (C) Strangler extraction

**Chosen Option**: A — Payment-type services (Wallet, Bank Transfer, Credit Card) with a shared utility library

**Consequences**: (+) independent deploy/scale per payment type; (+) incremental Strangler extraction; (−) shared lib coupling risk — version and treat as an API; (−) duplicated cross-cutting concerns (auth, logging).

---

## Phase 5: Compile Solution Doc

*[write-solution-doc skill applied]*

### Final Output Bundle

**Solution Document**: `solution.md`
- Business context: migrate payment monolith to microservices
- C2 Container Diagram: API Gateway → Wallet, Bank Transfer, Credit Card services, each with own DB; Kafka event bus
- C3 Component + Sequence Diagrams: per service (as-is → to-be), payment initiation/settlement/migration flows
- API Contracts: REST endpoints for queries, Kafka topic schemas for events
- RAID: risks (data consistency), assumptions (Kafka adoption), issues (SOAP legacy)
- RACI: ownership per service and cross-cutting concerns

**ADRs** (one per problem, area-prefixed in `adrs/`):
- `adr-service-decomposition-01-split-monolith.md` — Payment-type services
- `adr-communication-01-service-communication.md` — Hybrid sync/async
- `adr-database-01-break-up-database.md` — Database per service
- `adr-database-02-schema-migration.md` — Expand-contract migrations
- `adr-migration-01-zero-downtime-migration.md` — Strangler Fig

### Wrap-Up (conversation level — not written into any artifact)

> All five assumed solutions are adopted into the solution doc, mirrored **grouped by area** per `scope.md`. If an ADR decision changes during review, the corresponding area section is rewritten in place. Artifacts version together in `spikes/payment-migration/` — scope map at the root, ADRs in `adrs/` (area-prefixed), solution doc at the root, findings in `docs/` (see `examples/spike-artifact-layout.md`).
