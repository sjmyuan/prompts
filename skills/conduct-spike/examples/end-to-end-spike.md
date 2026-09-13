# Example: End-to-End Spike — Payment Service Migration

**Scenario**: The user wants to spike migrating a legacy payment processing service from a monolith to microservices, producing ADRs per decision problem and a consolidated solution document.

**Applies**: All capabilities in sequence — `define-spike-scope` → `investigate-per-area` → `compile-findings-doc` → `draft-problem-adrs` (option evaluation via `draft-adr`) → `compile-solution-doc`

**What makes this distinct**: Full multi-area brownfield spike, end to end (see `examples/multi-agent-investigation.md` for the parallel-dispatch variant).

---

## Define Spike Scope

### User Input
> "We need to spike migrating our payment processing service from the monolith to microservices. It handles credit card, bank transfer, and wallet payments. Currently it's a single Spring Boot app with ~200K LOC."

### Assistant Output (after clarification)

**Spike Goal**: Determine the target architecture for decomposing the payment monolith into independently deployable services, selecting technologies, and defining a migration strategy.

**Areas and problems** (each problem → one ADR, recorded in `scope.md`):

| # | Area | Problems ("How to …?") |
|---|---|---|
| 1 | Service decomposition boundaries | How to split the monolith? |
| 2 | Inter-service communication | How to handle service-to-service communication? |
| 3 | Database decomposition strategy | How to break up the monolithic database? · How to migrate the schema safely? |
| 4 | Migration strategy | How to transition with zero downtime? |

---

## Investigate Per Area

*(investigate-code applied per area; evidence maps recorded)*

| Area | Current State | Key Constraint |
|---|---|---|
| 1. Service decomposition | Package-by-layer; CreditCard 40% / BankTransfer 30% / Wallet 25%; `PaymentOrchestrator` (1200 lines) couples all types | Redeploy on any change; wallet can't scale; 3 teams contend |
| 2. Inter-service communication | All in-process; external REST/gRPC/SOAP; no broker; no circuit breaker | No async experience; SOAP must stay |
| 3. Database decomposition | Single PostgreSQL ~80 tables; `transactions`/`accounts`/`audit_log` shared; 12 settlement stored procedures (2000+ lines) | No per-type access control; procs block decomposition |
| 4. Migration strategy | K8s (3 replicas); Kong routes `/api/payments/*`; GitHub Actions canary CI/CD | No feature flags or traffic splitting |

### Completion Checkpoint

> "Investigation complete — is this sufficient, or should we investigate further before formalizing?"
> User: "It's sufficient — let's formalize. We can dig into the orchestrator call graph after the first round of ADRs."

---

## Compile Findings Documents

*(one findings doc per area, always: `docs/findings-<area>.md`; four areas → four docs, compiled concurrently, each embedding its area's evidence map inline.)*

| Findings doc | Current Architecture Summary | Constraints & Pain Points |
|---|---|---|
| `findings-service-decomposition.md` | Monolithic Spring Boot app (~200K LOC), package-by-layer; `PaymentOrchestrator` (1200 lines) couples all types | Redeploy on any change; wallet can't scale; 3 teams contend |
| `findings-communication.md` | All calls in-process; external REST/gRPC/SOAP; no broker; no circuit breaker | No async experience; SOAP must be maintained |
| `findings-database.md` | Single PostgreSQL (~80 tables); `transactions`/`accounts`/`audit_log` shared; 12 settlement procedures | No per-type access control; procedures block decomposition |
| `findings-migration.md` | K8s (3 replicas) behind Kong; GitHub Actions canary CI/CD; routes `/api/payments/*` | No feature flags or traffic splitting |

**Cross-area constraints**: `findings-database.md` ↔ `findings-service-decomposition.md` (shared tables); `findings-communication.md` ↔ `findings-migration.md` (no async/traffic-split infra → migration starts synchronous).

> *Findings = current-state baseline per area; ADRs cite their area's doc; the solution doc evolves these diagrams as-is → to-be.*

---

## Draft Problem ADRs — Evaluate + Draft

*(Per problem, an `adr-writer` sub-agent runs the `draft-adr` flow headlessly from the drivers and findings carried in the brief; the orchestrator confirms each proposed chosen option. A whole area's problems share one brief when evidence is shared.)*

| Area → Problem | Options evaluated | Chosen Option |
|---|---|---|
| Service decomposition → split the monolith | A payment-type services · B domain-driven services · C strangler extraction | A — payment-type services + shared lib |
| Communication → service communication | A synchronous REST · B async events (Kafka) · C hybrid | C — REST for queries, Kafka for commands |
| Database → break up the database | A DB per service · B shared DB + views · C event-driven sync | A — DB per service, phased from Wallet |
| Database → migrate the schema safely | A expand-contract · B central tool · C shared DB + views | A — expand-contract migrations |
| Migration → zero-downtime migration | A strangler fig · B parallel run · C big-bang | A — strangler fig, Wallet first |

**ADR output** (`adrs/`, each tagged with its `Area:`): `adr-service-decomposition-01-split-monolith.md`, `adr-communication-01-service-communication.md`, `adr-database-01-break-up-database.md`, `adr-database-02-schema-migration.md`, `adr-migration-01-zero-downtime-migration.md`.

Example — `adr-service-decomposition-01-split-monolith.md`:
- **Title**: Decompose Payment Monolith into Payment-Type Microservices
- **Status**: Draft
- **Problem**: The monolith couples three independent payment domains, preventing independent deployment and scaling.
- **Decision Drivers**: Hard — maintain 99.9% SLA; no payment-data loss. Soft — align with existing teams; prefer incremental.
- **Chosen Option**: A — payment-type services (Wallet, Bank Transfer, Credit Card) with a shared utility library.
- **Consequences**: (+) independent deploy/scale; (+) incremental strangler extraction; (−) shared-lib coupling risk; (−) duplicated cross-cutting concerns.

---

## Compile Solution Doc

*(write-solution-doc applied — target-state, decision-only, ADR decisions grouped by area.)*

**Solution Document**: `solution.md`
- C2: API Gateway → Wallet, Bank Transfer, Credit Card services, each with own DB; Kafka event bus
- C3 + sequence diagrams per service (as-is → to-be); payment initiation/settlement/migration flows
- API contracts: REST endpoints for queries, Kafka topic schemas for events
- RAID: risks (data consistency), assumptions (Kafka adoption), issues (SOAP legacy); RACI per service

**Final bundle**: `scope.md` · `adrs/` (5 area-prefixed ADRs) · `solution.md` · `docs/findings-<area>.md` (4).

### Wrap-Up (conversation level — not written into any artifact)

> All five chosen options are adopted into the solution doc, mirrored **grouped by area** per `scope.md`. If an ADR decision changes during review, the corresponding area section is rewritten in place. Artifacts version together in `spikes/payment-migration/` (see `examples/spike-artifact-layout.md`).
