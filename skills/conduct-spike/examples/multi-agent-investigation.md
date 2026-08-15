# Example: Multi-Agent Parallel Investigation — Payment Service Migration

**Scenario**: The user wants to conduct a heavy spike with 4 investigation areas on migrating a legacy payment service. The orchestrating agent dispatches investigation and ADR drafting to sub-agents in parallel to reduce wall-clock time.

**Applies**: `define-spike-scope` → `investigate-per-area` (parallel dispatch) → `compile-findings-doc` → `evaluate-solutions-per-area` → `draft-area-adrs` (parallel dispatch) → `compile-solution-doc`

**What makes this distinct**: Demonstrates parallel sub-agent orchestration — the orchestrator delegates independent work units concurrently, then synthesizes. Dispatch is the default for **all** spikes (even single-area) to preserve the orchestrating agent's context; parallel speed is secondary (see `reference/multi-agent-orchestration.md`).

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

The orchestrator prepares 4 self-contained briefs, one per area — area description, spike goal, expected output — each **requiring a per-area evidence map** (entry points, `file:line` key locations, call chains, verdicts, searched-negatives). No findings doc exists yet, so this round seeds the evidence map (see `reference/findings-document-guide.md`).

| Brief | Investigate | Scope | Expected output |
|---|---|---|---|
| 1 — Service decomposition | How to split the monolith? | Bounded contexts, package deps, ownership | Current org, coupling, constraints + evidence map |
| 2 — Inter-service communication | What patterns exist / needed? | Integration points, async familiarity | Comm landscape, constraints, infra + evidence map |
| 3 — Database decomposition | How is the DB structured / decomposable? | Table ownership, stored procs, access | DB topology, cross-domain deps + evidence map |
| 4 — Migration strategy | What infra / patterns feasible? | Pipeline, traffic routing, feature flags | Deployment arch, constraints, feasibility + evidence map |

### Orchestrator: Dispatch

> *The orchestrator detects that code-exploration sub-agents are available on the platform. It dispatches all 4 briefs concurrently.*
>
> "Dispatching investigation of 4 areas to sub-agents in parallel for faster completion."

### Sub-Agents Execute Concurrently

*Each sub-agent works independently and does not communicate with the others.*

### Sub-Agent A Returns — Service Decomposition

**Current State**: package-by-layer (`controller/`, `service/`, `repository/`, `domain/`); three domains — CreditCard (40%), BankTransfer (30%), Wallet (25%), Shared (5%); `PaymentOrchestrator` (1200 lines) coordinates all types; credit card service imports bank transfer domain objects.
**Constraints**: full redeploy for any payment-type change; wallet cannot scale independently; 3 teams step on each other's code.

### Sub-Agent B Returns — Inter-service Communication

**Current State**: all internal communication in-process; external REST (bank APIs), gRPC (wallet provider), SOAP (legacy acquirer); no message broker, no Kafka/RabbitMQ experience; no circuit breaker — external failures propagate to users.
**Constraints**: no async messaging experience; SOAP legacy must be maintained.

### Sub-Agent C Returns — Database Decomposition

**Current State**: single PostgreSQL, ~80 tables; `transactions`, `accounts`, `audit_log` shared across all payment types; 12 stored procedures for settlement (2000+ lines); no per-payment-type access control.
**Constraints**: stored procedures are a migration blocker; cross-payment-type queries in `transactions`.

### Sub-Agent D Returns — Migration Strategy

**Current State**: Kubernetes (EKS), 3 replicas; Kong API Gateway routes `/api/payments/*` to monolith; GitHub Actions CI/CD with canary support; no feature flags or traffic splitting.
**Constraints**: no traffic splitting at the gateway; canaries not tested for routing-based migration.

### Orchestrator: Synthesize

> *All 4 sub-agents returned. Cross-area consistency: Agent A + C both flagged tight coupling; Agent B + D both noted missing migration infrastructure; no contradictions. The orchestrator embeds each returned per-area evidence map into the consolidated findings doc below — `file:line` entry points annotated inline plus the Evidence & Verification section (see `reference/findings-document-guide.md`).*

---

## Phase 2b: Compile Findings Documents

*[Orchestrator applies compile-findings-doc — producing one consolidated findings document from the synthesized investigation results of all 4 sub-agents]*

### Findings Document: `findings-payment-migration.md`

*[write-solution-doc skill applied to current state; evidence maps embedded inline per `reference/findings-document-guide.md`]*

**C2 Container Diagram (Current State)**: Monolithic Spring Boot app on Kubernetes → single PostgreSQL, behind Kong API Gateway.

**Current Architecture (synthesized from 4 sub-agent investigations)**:

| Area | Current State | Key Constraint |
|---|---|---|
| Service decomposition | Single app, package-by-layer, 3 intermingled domains | `PaymentOrchestrator` (1200 lines) couples all types |
| Inter-service communication | In-process calls; external REST/gRPC/SOAP | No async messaging experience on team |
| Database decomposition | Single PostgreSQL ~80 tables, shared `transactions`/`accounts` | 12 stored procedures (2000+ lines) block migration |
| Migration strategy | K8s + Kong API Gateway + GitHub Actions CI/CD | No traffic splitting or feature flags |

**Cross-Area Observations**: Area 1 + 3 couple via the shared `transactions` table — both must be addressed together; Area 2 + 4 lack async/traffic-split infra — migration must start synchronous.

**Evidence & Verification** (per-area evidence maps embedded inline):

| Claim / Question | Verdict | Evidence (`file:line`) | Confidence |
|---|---|---|---|
| Circuit breaker around external calls? | No | `grep "CircuitBreaker\|Resilience4j\|fallback"` across `payment-service` — no matches | Verified (negative) |
| All internal calls in-process? | Yes | `service/PaymentOrchestrator.java:88` — no internal HTTP client found | Verified |
| Can Kong split traffic? | Unknown | `kong/kong.yml:34` — single upstream, no weighted upstreams | Inferred |

**Searched-Negatives**: `grep -ri "kafka\|rabbit\|mq"` in `payment-service` — no broker usage; `grep -ri "featureflag\|trafficsplit"` in `infra-configs` — none found.

> *Entry points (`file:line`) annotate the C2/sequence diagrams. Findings consolidated from 4 parallel sub-agents; cross-area consistency verified, no contradictions. This is the current-state baseline and evidence home.*

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
Decision drivers: 99.9% SLA; no data loss; align with existing teams
Options: A) Payment-type services — clear ownership, independent scaling; shared-lib coupling. B) Domain-driven services — cleaner dependencies; team restructuring. C) Strangler extraction — lowest risk; temporary hybrid complexity.
Assumed solution: Option A (Payment-type services)
Findings doc: findings-payment-migration.md — Evidence & Verification section (key locations, ledger, coupling); cite evidence without re-scanning
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

> *All 4 ADRs reviewed for consistency: ADR-001 (payment-type services) + ADR-003 (DB per service) are consistent; ADR-002 (Kafka) + ADR-004 (Strangler + gateway routing) are complementary; ADR-004 cross-references ADR-001 correctly. No conflicts — presenting for review.*

---

## Phase 5: Compile Solution Doc — SINGLE-TASK DISPATCH

*The solution doc is one unit synthesizing all ADRs, so it dispatches as a single task (context preservation, not parallelism). Brief: business context, findings doc, 4 assumed solutions; load `write-solution-doc`, produce the target-state doc.*

> "Dispatching solution-doc compilation to a sub-agent."

**Final Output Bundle**: `findings-payment-migration.md` (current-state + evidence maps) · `solution.md` (C4, API contracts, RAID, RACI — decision-only) · ADR-001 (Payment-type services) · ADR-002 (Hybrid sync/async) · ADR-003 (DB per service) · ADR-004 (Strangler Fig).

---

## Key Takeaways: Direct vs. Sub-Agent Dispatch

| Aspect | Direct (fallback only) | Sub-Agent (default) |
|---|---|---|
| Orchestrator context | High — all reasoning stays in its window | Low — work happens in isolated contexts |
| Time | Sum of all areas/ADRs | Max of any single one when concurrent |
| Coordination | None | Brief prep + synthesis |
| When used | Only when no suitable sub-agent exists | Always — even single-task spikes |
| Risk | Orchestrator context bloat | Incomplete briefs need re-prompting |
