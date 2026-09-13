# Example: Multi-Agent Parallel Investigation — Payment Service Migration

**Scenario**: A heavy spike with 4 investigation areas on migrating a legacy payment service. The orchestrator dispatches investigation and ADR drafting to sub-agents in parallel to reduce wall-clock time.

**Applies**: `define-spike-scope` → `investigate-per-area` (parallel dispatch) → `compile-findings-doc` → `draft-problem-adrs` (parallel dispatch, evaluation via `draft-adr`) → `compile-solution-doc`

**What makes this distinct**: Parallel sub-agent orchestration — independent work units dispatched concurrently, then synthesized. Dispatch is the default for all spikes (even single-area) to preserve context; parallel speed is secondary (see `reference/multi-agent-orchestration.md`).

---

## Define Spike Scope

*(As in `examples/end-to-end-spike.md` — the same payment migration problem with 4 areas.)*

| # | Area | Problem ("How to …?") |
|---|---|---|
| 1 | Service decomposition boundaries | How to split the monolith? |
| 2 | Inter-service communication | How to handle service-to-service communication? |
| 3 | Database decomposition strategy | How to break up the monolithic database? |
| 4 | Migration strategy | How to transition with zero downtime? |

> *User confirms. 4 areas → parallel dispatch for investigation (per area) and ADR drafting (per problem).*

---

## Investigate Per Area — PARALLEL DISPATCH

### Orchestrator: Prepare Briefs

4 self-contained briefs, one per area — area description, spike goal, expected output — each **requiring a per-area evidence map**. No findings doc exists yet, so this round seeds the map (see `reference/findings-document-guide.md`).

| Brief | Investigate | Scope | Expected output |
|---|---|---|---|
| 1 — Service decomposition | How to split the monolith? | Bounded contexts, package deps, ownership | Findings + evidence map |
| 2 — Inter-service communication | What patterns exist / needed? | Integration points, async familiarity | Findings + evidence map |
| 3 — Database decomposition | How is the DB structured / decomposable? | Table ownership, stored procs, access | Findings + evidence map |
| 4 — Migration strategy | What infra / patterns feasible? | Pipeline, traffic routing, feature flags | Findings + evidence map |

### Orchestrator: Dispatch

> The orchestrator detects that code-exploration sub-agents are available and dispatches all 4 briefs concurrently.
> "Dispatching investigation of 4 areas to sub-agents in parallel for faster completion."

### Sub-Agents Return

| Agent | Current State | Constraints |
|---|---|---|
| A — Service decomposition | Package-by-layer; CreditCard 40% / BankTransfer 30% / Wallet 25%; `PaymentOrchestrator` (1200 lines) | Redeploy on any change; wallet can't scale; 3 teams contend |
| B — Inter-service communication | All in-process; external REST/gRPC/SOAP; no broker, no circuit breaker | No async experience; SOAP must stay |
| C — Database decomposition | Single PostgreSQL ~80 tables; `transactions`/`accounts`/`audit_log` shared; 12 settlement procs | Procs block migration; cross-type queries |
| D — Migration strategy | K8s (EKS) 3 replicas; Kong routes `/api/payments/*`; GH Actions canary CI/CD | No traffic splitting; canaries untested for routing |

### Orchestrator: Synthesize

> All 4 returned. Cross-area consistency: A + C both flagged tight coupling; B + D both noted missing migration infrastructure; no contradictions. Each area's verified evidence map is handed to `compile-findings-doc`.

---

## Compile Findings Documents

*(one findings doc per area, always; four docs dispatched concurrently, each embedding its area's evidence map inline.)*

### `docs/findings-communication.md` (evidence map detail)

**Current State**: all calls in-process; external REST/gRPC/SOAP; no message broker; no circuit breaker.
**Constraints**: no async experience on team; SOAP contract must stay.

**Evidence & Verification**:

| Claim / Question | Verdict | Evidence (`file:line`) | Confidence |
|---|---|---|---|
| Circuit breaker around external calls? | No | `grep "CircuitBreaker\|Resilience4j\|fallback"` across `payment-service` — no matches | Verified (negative) |
| All internal calls in-process? | Yes | `service/PaymentOrchestrator.java:88` — no internal HTTP client found | Verified |

**Searched-Negatives**: `grep -ri "kafka\|rabbit\|mq"` in `payment-service` — no broker usage.

*(The other three findings docs follow the same shape — current state, constraints, evidence map.)*

**Cross-area constraints**: `findings-service-decomposition.md` ↔ `findings-database.md` (shared `transactions`/`accounts`/`audit_log`); `findings-communication.md` ↔ `findings-migration.md` (no async/traffic-split infra → migration starts synchronous).

---

## Draft ADRs — PARALLEL DISPATCH

*(Each problem's ADR is drafted headlessly by an `adr-writer` sub-agent from the drivers and findings carried in the brief; a whole area's problems share one brief. The orchestrator confirms each proposed chosen option afterward.)*

**Chosen Options Summary**:

| Area → Problem | Chosen Option |
|---|---|
| Service decomposition → split the monolith | Payment-type services (Wallet, Bank Transfer, Credit Card) |
| Inter-service communication → service communication | Hybrid: REST for queries, Kafka events for commands |
| Database decomposition → break up the database | Database per service, phased by payment type |
| Migration strategy → zero-downtime migration | Strangler Fig, starting with Wallet payments |

### Orchestrator: Prepare Briefs

4 briefs — one per problem (the database area batches both problems into one brief since they share evidence):

**Brief 1 — ADR for Service Decomposition (problem: split the monolith)**:
```
Produce ADR for problem: How to split the monolith? (Area: Service Decomposition)
Decision drivers: 99.9% SLA; no data loss; align with existing teams
Options: A) Payment-type services — clear ownership, independent scaling; shared-lib coupling. B) Domain-driven services — cleaner dependencies; team restructuring. C) Strangler extraction — lowest risk; temporary hybrid complexity.
Findings doc: docs/findings-service-decomposition.md — Evidence & Verification section (key locations, ledger, coupling); cite evidence without re-scanning
Load draft-adr skill and produce a complete ADR tagged Area: Service Decomposition.
```

### Orchestrator: Dispatch

> Dispatches all 4 ADR drafting briefs concurrently. "Dispatching ADR drafting for 4 areas to sub-agents in parallel."

### Sub-Agent Results

**`adr-service-decomposition-01-split-monolith.md`**: Payment-type services
**`adr-communication-01-service-communication.md`**: Hybrid sync/async
**`adr-database-01-break-up-database.md`**: Database per service
**`adr-migration-01-zero-downtime-migration.md`**: Strangler Fig

### Orchestrator: Synthesize

> All 4 ADRs reviewed: decomposition + database are consistent; communication + migration are complementary; migration cross-references decomposition correctly. No conflicts — presenting for review.

---

## Compile Solution Doc — SINGLE-TASK DISPATCH

*(One unit synthesizing all ADRs, so it dispatches as a single task — context preservation, not parallelism. Brief: business context, the 4 findings docs, 4 chosen options; load `write-solution-doc`, produce the target-state doc.)*

> "Dispatching solution-doc compilation to a sub-agent."

**Final bundle**: `scope.md` · `docs/findings-<area>.md` (one per area) · `solution.md` (decision-only, ADR decisions grouped by area) · the 4 area-prefixed ADRs in `adrs/`.

---

## Key Takeaways: Sub-Agent Dispatch

| Aspect | Value |
|---|---|
| Orchestrator context | Low — work happens in isolated contexts |
| Time | Max of any single unit when concurrent |
| Coordination | Brief prep + synthesis |
| When used | Always — a sub-agent is available for every step; even single-task spikes |
| Risk | Incomplete briefs need re-prompting |
