# Example: Multi-Agent Parallel Investigation — Payment Service Migration

**Scenario**: The user wants to conduct a heavy spike with 4 investigation areas on migrating a legacy payment service. The orchestrating agent dispatches investigation and ADR drafting to sub-agents in parallel to reduce wall-clock time.

**Applies**: `define-spike-scope` → `investigate-per-area` (parallel dispatch) → `compile-findings-doc` → `draft-problem-adrs` (parallel dispatch, option evaluation via `draft-adr`) → `compile-solution-doc`

**What makes this distinct**: Demonstrates parallel sub-agent orchestration — the orchestrator delegates independent work units concurrently, then synthesizes. Dispatch is the default for **all** spikes (even single-area) to preserve the orchestrating agent's context; parallel speed is secondary (see `reference/multi-agent-orchestration.md`).

---

## Define Spike Scope

*(Scope definition proceeds as in `examples/end-to-end-spike.md` — the same payment service migration problem with 4 investigation areas. See that example for the full scope-definition dialog.)*

**Areas and problems** (4 areas — qualifies for parallel dispatch; each problem → one ADR):

| # | Area | Problem ("How to …?") |
|---|---|---|
| 1 | Service decomposition boundaries | How to split the monolith? What are the bounded contexts and service boundaries? |
| 2 | Inter-service communication | How to handle service-to-service communication (sync vs. async, protocol, message format)? |
| 3 | Database decomposition strategy | How to break up the monolithic database? One DB per service, shared DB with views, or event-driven? |
| 4 | Migration strategy | How to transition from monolith to microservices with zero downtime? |

> *User confirms the breakdown. The orchestrator notes: 4 areas → parallel dispatch for investigation (per area) and ADR drafting (per problem).*

---

## Investigate Per Area — PARALLEL DISPATCH

### Orchestrator: Prepare Briefs

The orchestrator prepares 4 self-contained briefs, one per area — area description, spike goal, expected output — each **requiring a per-area evidence map** (entry points, `file:line` key locations, call chains, verdicts, searched-negatives). No findings doc exists yet, so this round seeds the evidence map (see `reference/findings-document-guide.md`).

| Brief | Investigate | Scope | Expected output |
|---|---|---|---|
| 1 — Service decomposition | How to split the monolith? | Bounded contexts, package deps, ownership | Findings + evidence map |
| 2 — Inter-service communication | What patterns exist / needed? | Integration points, async familiarity | Findings + evidence map |
| 3 — Database decomposition | How is the DB structured / decomposable? | Table ownership, stored procs, access | Findings + evidence map |
| 4 — Migration strategy | What infra / patterns feasible? | Pipeline, traffic routing, feature flags | Findings + evidence map |

### Orchestrator: Dispatch

> The orchestrator detects that code-exploration sub-agents are available on the platform and dispatches all 4 briefs concurrently.
>
> "Dispatching investigation of 4 areas to sub-agents in parallel for faster completion."

### Sub-Agents Execute Concurrently

*Each sub-agent works independently and does not communicate with the others.*

### Sub-Agents Return

| Agent | Current State | Constraints |
|---|---|---|
| A — Service decomposition | Package-by-layer; CreditCard 40% / BankTransfer 30% / Wallet 25%; `PaymentOrchestrator` (1200 lines) couples all types | Redeploy on any change; wallet can't scale; 3 teams contend |
| B — Inter-service communication | All in-process; external REST/gRPC/SOAP; no broker, no circuit breaker | No async experience; SOAP must stay |
| C — Database decomposition | Single PostgreSQL ~80 tables; `transactions`/`accounts`/`audit_log` shared; 12 settlement procs (2000+ lines) | Procs block migration; cross-type queries |
| D — Migration strategy | K8s (EKS) 3 replicas; Kong routes `/api/payments/*`; GH Actions canary CI/CD | No traffic splitting; canaries untested for routing |

### Orchestrator: Synthesize

> All 4 sub-agents returned. Cross-area consistency: A + C both flagged tight coupling; B + D both noted missing migration infrastructure; no contradictions. The orchestrator embeds each returned per-area evidence map into the consolidated findings doc below (see `reference/findings-document-guide.md`).

---

## Compile Findings Documents

*(compile-findings-doc — one consolidated findings document synthesized from all 4 sub-agent investigations)*

### Findings Document: `findings-payment-migration.md`

*(write-solution-doc applied to current state; evidence maps embedded inline per `reference/findings-document-guide.md`)*

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

## Draft ADRs — PARALLEL DISPATCH

*(Each problem's ADR — evaluation included — is drafted by an `adr-writer` sub-agent running the full `draft-adr` flow; a whole area's problems share one brief. The assumed solutions below are the evaluate stage of each drafting session.)*

**Assumed Solutions Summary** (per area → problem, from each session's evaluation):

| Area → Problem | Assumed Solution |
|---|---|
| Service decomposition → split the monolith | Payment-type services (Wallet, Bank Transfer, Credit Card) |
| Inter-service communication → service communication | Hybrid: REST for queries, Kafka events for commands |
| Database decomposition → break up the database | Database per service, phased by payment type |
| Migration strategy → zero-downtime migration | Strangler Fig, starting with Wallet payments |

### Orchestrator: Prepare Briefs

The orchestrator prepares 4 briefs — one per problem (the database area batches both problems into one brief since they share evidence):

**Brief 1 — ADR for Service Decomposition (problem: split the monolith)**:
```
Produce ADR for problem: How to split the monolith? (Area: Service Decomposition)
Decision drivers: 99.9% SLA; no data loss; align with existing teams
Options: A) Payment-type services — clear ownership, independent scaling; shared-lib coupling. B) Domain-driven services — cleaner dependencies; team restructuring. C) Strangler extraction — lowest risk; temporary hybrid complexity.
Assumed solution: Option A (Payment-type services)
Findings doc: findings-payment-migration.md — Evidence & Verification section (key locations, ledger, coupling); cite evidence without re-scanning
Load draft-adr skill and produce a complete ADR tagged Area: Service Decomposition.
```

*(Similar briefs prepared for the other problems — each includes its area's findings doc (evidence sections).)*

### Orchestrator: Dispatch

> The orchestrator detects suitable sub-agents and dispatches all 4 ADR drafting briefs concurrently.
>
> "Dispatching ADR drafting for 4 areas to sub-agents in parallel."

### Sub-Agents Execute Concurrently

*Each sub-agent loads the `draft-adr` skill and produces one ADR independently.*

### Sub-Agent Results

**`adr-service-decomposition-01-split-monolith.md`**: Payment-type services
**`adr-communication-01-service-communication.md`**: Hybrid sync/async
**`adr-database-01-break-up-database.md`**: Database per service
**`adr-migration-01-zero-downtime-migration.md`**: Strangler Fig

### Orchestrator: Synthesize

> *All 4 ADRs reviewed for consistency: service-decomposition (payment-type services) + database-decomposition (DB per service) are consistent; communication (Kafka) + migration (Strangler + gateway routing) are complementary; the migration ADR cross-references the decomposition ADR correctly. No conflicts — presenting for review.*

---

## Compile Solution Doc — SINGLE-TASK DISPATCH

*(The solution doc is one unit synthesizing all ADRs, so it dispatches as a single task — context preservation, not parallelism. Brief: business context, findings doc, 4 assumed solutions; load `write-solution-doc`, produce the target-state doc.)*

> "Dispatching solution-doc compilation to a sub-agent."

**Final Output Bundle**: `scope.md` (area → problem map) · `findings-payment-migration.md` (current-state + evidence maps) · `solution.md` (C4, API contracts, RAID, RACI — decision-only, ADR decisions grouped by area) · the 4 area-prefixed ADRs in `adrs/`.

---

## Key Takeaways: Sub-Agent Dispatch

| Aspect | Value |
|---|---|
| Orchestrator context | Low — work happens in isolated contexts |
| Time | Max of any single unit when concurrent |
| Coordination | Brief prep + synthesis |
| When used | Always — a sub-agent is available for every step; even single-task spikes |
| Risk | Incomplete briefs need re-prompting |
