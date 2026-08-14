# Example: Multi-Agent Parallel Investigation — Payment Service Migration

**Scenario**: The user wants to conduct a heavy spike with 4 investigation areas on migrating a legacy payment service. The orchestrating agent dispatches investigation and ADR drafting to sub-agents in parallel to reduce wall-clock time.

**Applies**: `define-spike-scope` → `investigate-per-area` (parallel dispatch) → `compile-findings-doc` → `evaluate-solutions-per-area` → `draft-area-adrs` (parallel dispatch) → `compile-solution-doc`

**What makes this distinct**: This example demonstrates the multi-agent orchestration pattern where the orchestrating agent delegates independent work units to sub-agents that run concurrently, then synthesizes their results. Note that dispatch to sub-agents is the default for **all** spikes — including single-area/single-ADR ones — primarily to preserve the orchestrating agent's context; parallel speed is a secondary benefit (see `reference/multi-agent-orchestration.md`).

---

## Phase 1: Define Spike Scope

*(Scope definition proceeds as in `examples/end-to-end-spike.md` — the same payment service migration problem with 4 investigation areas. See that example for the full scope-definition dialog.)*

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

The orchestrator prepares 4 self-contained briefs, one per investigation area. Each brief includes the area description, the overall spike goal, and the expected output format — and **requires the sub-agent to return a per-area evidence map** (entry points, key code locations with file:line, call chains, evidence verdicts, searched-negatives). No findings doc exists yet, so this first round seeds the evidence map (see `reference/findings-document-guide.md`).

**Brief 1 — Service Decomposition Boundaries**:
```
Investigate: How should the payment monolith be split into services?
Context: Single Spring Boot app, ~200K LOC. Payment types: CreditCard, BankTransfer, Wallet.
Scope: Identify bounded contexts, current package dependencies, team ownership boundaries.
Expected output: Current state of code organization, domain coupling points, constraints & pain points + per-area evidence map.
```

**Brief 2 — Inter-service Communication**:
```
Investigate: What communication patterns exist and what will the new services need?
Context: Currently all in-process calls. External integrations use REST, gRPC, and SOAP.
Scope: Map current integration points, assess team familiarity with async patterns.
Expected output: Current communication landscape, constraints, existing infrastructure (message brokers, gateways) + per-area evidence map.
```

**Brief 3 — Database Decomposition Strategy**:
```
Investigate: How is the monolithic database structured and how can it be decomposed?
Context: Single PostgreSQL, ~80 tables. Shared tables across payment types.
Scope: Analyze table ownership, stored procedures, data access patterns.
Expected output: Current database topology, cross-domain table dependencies, constraints & pain points + per-area evidence map.
```

**Brief 4 — Migration Strategy**:
```
Investigate: What deployment infrastructure exists and what migration patterns are feasible?
Context: Kubernetes on AWS, Kong API Gateway, GitHub Actions CI/CD.
Scope: Assess current deployment pipeline, traffic routing capability, feature flag infrastructure.
Expected output: Current deployment architecture, constraints, migration feasibility assessment + per-area evidence map.
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
>
> *It embeds each returned per-area evidence map into the consolidated findings doc below — `file:line` entry points and key locations annotated inline, plus the Evidence & Verification section (ledger + searched-negatives). See `reference/findings-document-guide.md` for the embedding format.*

---

## Phase 2a: Completion Checkpoint

*[Investigation complete — the orchestrator confirms the result before formalizing findings]*

### Orchestrator

> "All 4 sub-agents have returned and their findings are verified. Is this result sufficient, or should we investigate further before formalizing the findings?"

### User Response

> "It's sufficient — let's formalize. We can prototype the async + routing approach as a follow-up spike later."

### Orchestrator

> "Makes sense. Proceeding to compile findings document from the 4 sub-agent outputs."

---

## Phase 2b: Compile Findings Documents

*[Orchestrator applies compile-findings-doc — producing one consolidated findings document from the synthesized investigation results of all 4 sub-agents]*

### Findings Document: `findings-payment-migration.md`

*[write-solution-doc skill applied to current state]*

**C2 Container Diagram (Current State)**: Monolithic Spring Boot app on Kubernetes → single PostgreSQL, behind Kong API Gateway.

**Current Architecture (synthesized from 4 sub-agent investigations)**:

| Area | Current State | Key Constraint |
|---|---|---|
| Service decomposition | Single app, package-by-layer, 3 intermingled domains | `PaymentOrchestrator` (1200 lines) couples all types |
| Inter-service communication | All in-process calls; external: REST/gRPC/SOAP | No async messaging experience on team |
| Database decomposition | Single PostgreSQL, ~80 tables, shared `transactions`/`accounts` | 12 stored procedures (2000+ lines) are a migration blocker |
| Migration strategy | K8s + Kong API Gateway + GitHub Actions CI/CD | No traffic splitting or feature flags in place |

**Cross-Area Observations**:
- Area 1 (service boundaries) and Area 3 (database): the shared `transactions` table couples payment-type services and database decomposition — both must be addressed together.
- Area 2 (communication) and Area 4 (migration): lack of async messaging and traffic splitting means migration must start with synchronous patterns.

**Raw Data & Metrics**:
- ~200K LOC, ~80 tables, 3 K8s replicas
- 3 external protocols (REST, gRPC, SOAP)
- Team: 3 sub-teams, no Kafka experience

**Evidence & Verification** (per-area evidence maps embedded inline):

**Evidence Ledger**

| Claim / Question | Verdict | Evidence (file:line) | Confidence |
|---|---|---|---|
| Is there a circuit breaker around external calls? | No | `grep "CircuitBreaker\|Resilience4j\|fallback"` across `payment-service` — no matches | Verified (negative) |
| Are all internal calls in-process? | Yes | `service/PaymentOrchestrator.java:88` calls services directly; no internal HTTP client found | Verified |
| Does `transactions` hold all payment types? | Yes | `db/schema.sql:201` — no payment-type discriminator at table level | Verified |
| Can Kong split traffic? | Unknown | `kong/kong.yml:34` — single upstream, no weighted upstreams | Inferred |
| Team has async messaging experience? | N/A | from user conversation, not code | Gap |

**Searched-Negatives**

| Area | Search performed | Result | Next step |
|---|---|---|---|
| Communication | `grep -ri "kafka\|rabbit\|mq"` in `payment-service` | No message broker usage | Prototype async feasibility (direction D2) |
| Migration | `grep -ri "featureflag\|trafficsplit"` in `infra-configs` | None found | Verify Kong weighted-upstream capability in docs |
| Service decomposition | Search for `*Module` / bounded-context markers | None — package-by-layer only | Deep-dive into domain import graph (D1) |

> *Entry points and key locations (`file:line`) also annotate the C2/sequence diagrams above. Findings consolidated from 4 parallel sub-agent investigations. Cross-area consistency verified — no contradictions found. This document is the current-state baseline and evidence home for evaluation.*

---

## Phase 3: Evaluate Solutions Per Area

*(Evaluation proceeds as in `examples/end-to-end-spike.md` — same options and decision drivers. See that example for the full evaluation dialog; here it is dispatched in parallel to ADR-writer sub-agents, one per area, per **evaluate-solutions-per-area**.)*

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
Findings doc: findings-payment-migration.md — Evidence & Verification section (key locations, ledger, coupling) — cite evidence without re-scanning
Load draft-adr skill and produce a complete ADR.
```

*[Similar briefs prepared for areas 2-4 — each includes its area's findings doc (evidence sections).]*

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

## Phase 5: Compile Solution Doc — SINGLE-TASK DISPATCH

*The solution document is a single unit (it synthesizes all ADRs into one cohesive document), so it is dispatched as one task — context preservation, not parallelism.*

*[Orchestrator prepares a brief: business context, findings doc, and the 4 assumed solutions, with instructions to load `write-solution-doc` and produce the target-state document. Dispatched to a solution-doc sub-agent; the orchestrator reviews the result.]*

> "Dispatching solution-doc compilation to a sub-agent."

### Final Output Bundle

- **Findings Document**: `findings-payment-migration.md` (current-state architecture + embedded per-area evidence map: `file:line` key locations, evidence ledger, searched-negatives)
- **Solution Document**: `solution.md` (C4 diagrams, API contracts, RAID, RACI — decision-only, no code references)
- **ADR-001**: Service Decomposition (Payment-type services)
- **ADR-002**: Inter-service Communication (Hybrid sync/async)
- **ADR-003**: Database Decomposition (Database per service)
- **ADR-004**: Migration Strategy (Strangler Fig)

---

## Key Takeaways: Direct vs. Sub-Agent Dispatch

| Aspect | Direct Execution (fallback only) | Sub-Agent Dispatch (default) |
|---|---|---|
| Orchestrator context usage | High — all reading/reasoning stays in the orchestrator's window | Low — work happens in isolated sub-agent contexts |
| Investigation time | Sum of all areas (4x single-area time) | Max of any single area (~1x) when concurrent |
| ADR drafting time | Sum of all ADRs (4x single-ADR time) | Max of any single ADR (~1x) when concurrent |
| Coordination overhead | None | Brief preparation + synthesis |
| Findings/solution-doc compilation | Done in the orchestrator — large writes crowd its context | Single dispatch per doc (one unit) — the write happens in the sub-agent |
| When used | Only when no suitable sub-agent is available | Always — even single-area/single-ADR/single-document spikes |
| Risk | Orchestrator context bloat degrades later synthesis | Sub-agents may need re-prompting if briefs are incomplete |
