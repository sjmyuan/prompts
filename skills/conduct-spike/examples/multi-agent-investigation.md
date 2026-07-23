# Example: Multi-Agent Parallel Investigation — Payment Service Migration

**Scenario**: The user wants to conduct a heavy spike with 4 investigation areas on migrating a legacy payment service. The orchestrating agent dispatches investigation and ADR drafting to sub-agents in parallel to reduce wall-clock time.

**Applies**: `define-spike-scope` → `investigate-per-area` (parallel dispatch) → `evaluate-solutions-per-area` → `draft-area-adrs` (parallel dispatch) → `compile-solution-doc`

**What makes this distinct**: This example demonstrates the multi-agent orchestration pattern where the orchestrating agent delegates independent work units to sub-agents that run concurrently, then synthesizes their results. Contrast with `end-to-end-spike.md` where investigation runs sequentially.

---

## Phase 1: Define Spike Scope

### User Input
> "We need to spike migrating our payment processing service from the monolith to microservices. It's a big system — ~200K LOC, three payment types. I want this to go as fast as possible."

### Assistant Output

**Spike Goal**: Determine the target architecture for decomposing the payment monolith into independently deployable services, selecting technologies, and defining a migration strategy.

**Investigation Areas** (4 areas — qualifies for parallel dispatch):

| # | Area | Description |
|---|---|---|
| 1 | Service decomposition boundaries | How should we split the monolith? What are the bounded contexts and service boundaries? |
| 2 | Inter-service communication | How will the new services communicate (sync vs. async, protocol, message format)? |
| 3 | Database decomposition strategy | How do we break up the monolithic database? One DB per service, shared DB with views, or event-driven? |
| 4 | Migration strategy | How do we transition from monolith to microservices with zero downtime? |

> *User confirms the breakdown. The orchestrator notes: 4 areas → will use parallel dispatch for both Phase 2 (investigation) and Phase 4 (ADR drafting).*

---

## Phase 2: Investigate Per Area — PARALLEL DISPATCH

### Orchestrator: Prepare Briefs

The orchestrator prepares 4 self-contained briefs, one per investigation area. Each brief includes the area description, the overall spike goal, and the expected output format.

**Brief 1 — Service Decomposition Boundaries**:
```
Investigate: How should the payment monolith be split into services?
Context: Single Spring Boot app, ~200K LOC. Payment types: CreditCard, BankTransfer, Wallet.
Scope: Identify bounded contexts, current package dependencies, team ownership boundaries.
Expected output: Current state of code organization, domain coupling points, constraints & pain points.
```

**Brief 2 — Inter-service Communication**:
```
Investigate: What communication patterns exist and what will the new services need?
Context: Currently all in-process calls. External integrations use REST, gRPC, and SOAP.
Scope: Map current integration points, assess team familiarity with async patterns.
Expected output: Current communication landscape, constraints, existing infrastructure (message brokers, gateways).
```

**Brief 3 — Database Decomposition Strategy**:
```
Investigate: How is the monolithic database structured and how can it be decomposed?
Context: Single PostgreSQL, ~80 tables. Shared tables across payment types.
Scope: Analyze table ownership, stored procedures, data access patterns.
Expected output: Current database topology, cross-domain table dependencies, constraints & pain points.
```

**Brief 4 — Migration Strategy**:
```
Investigate: What deployment infrastructure exists and what migration patterns are feasible?
Context: Kubernetes on AWS, Kong API Gateway, GitHub Actions CI/CD.
Scope: Assess current deployment pipeline, traffic routing capability, feature flag infrastructure.
Expected output: Current deployment architecture, constraints, migration feasibility assessment.
```

### Orchestrator: Dispatch

> *The orchestrator detects that code-exploration sub-agents are available on the platform. It dispatches all 4 briefs concurrently.*
>
> "Dispatching investigation of 4 areas to sub-agents in parallel for faster completion."

### Sub-Agents Execute Concurrently

*Each sub-agent works independently, exploring the codebase for its assigned area. The sub-agents do not communicate with each other.*

| Sub-agent | Area | Exploration scope | Duration |
|---|---|---|---|
| Agent A | Service decomposition | Package structure, domain imports, class dependencies | Independent |
| Agent B | Inter-service communication | External API calls, circuit breakers, message patterns | Independent |
| Agent C | Database decomposition | Table schemas, stored procedures, cross-table queries | Independent |
| Agent D | Migration strategy | K8s configs, CI/CD pipelines, API gateway routes | Independent |

### Sub-Agent A Returns — Service Decomposition

**Current State**:
- Single Spring Boot app with package-by-layer: `controller/`, `service/`, `repository/`, `domain/`
- Three business domains: CreditCardPayment (40%), BankTransferPayment (30%), WalletPayment (25%), Shared (5%)
- `PaymentOrchestrator` (1200 lines) coordinates all payment types centrally
- Credit card service directly imports bank transfer domain objects (tight coupling)

**Constraints & Pain Points**:
- Full redeploy for any payment type change
- Cannot scale wallet payments independently
- 3 teams step on each other's code

### Sub-Agent B Returns — Inter-service Communication

**Current State**:
- All internal communication is in-process method calls
- External: REST (bank APIs), gRPC (wallet provider), SOAP (legacy acquirer)
- No message broker in ecosystem; no Kafka/RabbitMQ experience on team
- No circuit breaker pattern; external failures propagate to users

**Constraints & Pain Points**:
- Team has no async messaging experience
- SOAP legacy integration must be maintained

### Sub-Agent C Returns — Database Decomposition

**Current State**:
- Single PostgreSQL, ~80 tables
- `transactions`, `accounts`, `audit_log` shared across all payment types
- 12 stored procedures for settlement (2000+ lines)
- No per-payment-type access control

**Constraints & Pain Points**:
- Stored procedures are a migration blocker (heavy logic in DB)
- Cross-payment-type queries in `transactions` table

### Sub-Agent D Returns — Migration Strategy

**Current State**:
- Deployed on Kubernetes (EKS), 3 replicas
- Kong API Gateway routes `/api/payments/*` to monolith
- GitHub Actions CI/CD with canary deployment support
- No feature flags or traffic splitting infrastructure

**Constraints & Pain Points**:
- No traffic splitting at API gateway level
- Canary deployments exist but not tested for routing-based migration

### Orchestrator: Synthesize

> *All 4 sub-agents have returned. The orchestrator reviews findings for cross-area consistency:*
> - Agent A and Agent C both identified tight coupling — consistent
> - Agent B and Agent D both noted lack of infrastructure for gradual migration — aligned
> - No contradictions found across sub-agent outputs
>
> *The orchestrator compiles the synthesized investigation summary and presents it to the user.*

---

## Phase 3: Evaluate Solutions Per Area

*Evaluation is interactive and runs sequentially (not parallelizable). The orchestrator guides the user through each area using the investigation findings collected from sub-agents.*

*[Evaluation proceeds as in the standard end-to-end example — see `examples/end-to-end-spike.md` for the full evaluation dialog.]*

**Assumed Solutions Summary**:

| Area | Assumed Solution |
|---|---|
| Service decomposition | Payment-type services (Wallet, Bank Transfer, Credit Card) |
| Inter-service communication | Hybrid: REST for queries, Kafka events for commands |
| Database decomposition | Database per service, phased by payment type |
| Migration strategy | Strangler Fig, starting with Wallet payments |

---

## Phase 4: Draft ADRs — PARALLEL DISPATCH

### Orchestrator: Prepare Briefs

The orchestrator prepares 4 briefs, each containing one area's evaluation results:

**Brief 1 — ADR for Service Decomposition**:
```
Produce ADR for: Service Decomposition Boundaries
Decision drivers: Must maintain 99.9% SLA; Must not lose data; Prefer alignment with existing teams
Options:
  A: Payment-type services — Pros: clear ownership, independent scaling. Cons: shared lib coupling
  B: Domain-driven services — Pros: cleaner dependencies. Cons: team restructuring
  C: Strangler extraction — Pros: lowest risk. Cons: temporary hybrid complexity
Assumed solution: Option A (Payment-type services)
Load draft-adr skill and produce a complete ADR.
```

*[Similar briefs prepared for areas 2-4]*

### Orchestrator: Dispatch

> *The orchestrator detects suitable sub-agents and dispatches all 4 ADR drafting briefs concurrently.*
>
> "Dispatching ADR drafting for 4 areas to sub-agents in parallel."

### Sub-Agents Execute Concurrently

*Each sub-agent loads the `draft-adr` skill and produces one ADR independently.*

### Sub-Agent Results

**ADR-001**: Payment Service Decomposition (Payment-type services)
**ADR-002**: Inter-service Communication (Hybrid sync/async)
**ADR-003**: Database Decomposition (Database per service)
**ADR-004**: Migration Strategy (Strangler Fig)

### Orchestrator: Synthesize

> *The orchestrator reviews all 4 ADRs for consistency:*
> - ADR-001 assumes payment-type services; ADR-003 assumes DB per service — consistent decomposition strategy
> - ADR-002 assumes Kafka; ADR-004 assumes Strangler Fig with API Gateway routing — complementary, no conflict
> - ADR-004 references ADR-001's service boundaries — cross-reference is correct
>
> *All ADRs are consistent. Presenting to user for review.*

---

## Phase 5: Compile Solution Doc

*The solution document compilation runs sequentially (not parallelizable — it synthesizes all ADRs into one cohesive document).*

*[Solution document produced as in the standard example.]*

### Final Output Bundle

- **Solution Document**: `solution-doc-payment-migration.md` (C4 diagrams, API contracts, RAID, RACI)
- **ADR-001**: Service Decomposition (Payment-type services)
- **ADR-002**: Inter-service Communication (Hybrid sync/async)
- **ADR-003**: Database Decomposition (Database per service)
- **ADR-004**: Migration Strategy (Strangler Fig)

---

## Key Takeaways: Multi-Agent vs. Sequential

| Aspect | Sequential (end-to-end-spike) | Multi-Agent (this example) |
|---|---|---|
| Investigation time | Sum of all areas (4x single-area time) | Max of any single area (~1x) |
| ADR drafting time | Sum of all ADRs (4x single-ADR time) | Max of any single ADR (~1x) |
| Coordination overhead | None | Brief preparation + synthesis |
| Best for | 1-2 areas, simple problems | 3+ areas, heavy codebases |
| Risk | None | Sub-agents may need re-prompting if briefs are incomplete |
