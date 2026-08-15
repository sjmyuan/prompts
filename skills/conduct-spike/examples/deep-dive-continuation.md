# Example: Deep-Dive Continuation — Database Decomposition After Spike

**Scenario**: The user previously conducted a spike on migrating a payment monolith to microservices. Four ADRs were drafted, but the database decomposition area was left unresolved — the team couldn't decide between "one DB per service" and "shared DB with views". Now the user wants to dig deeper into just this area to reach a conclusion.

**Applies**: `deep-dive-specific-areas` — loads existing spike context, targets one unresolved area with deeper investigation, evaluates with new depth, and updates the ADR.

**What makes this distinct**: This is not a full spike (scope is already defined, other ADRs exist), not a "from existing findings" case (the area needs new investigation, not just formalization), and not a simple ADR revision (the area was never resolved). It demonstrates the focused deep-dive workflow where only one area is revisited.

---

## Step 1: Gather Existing Context

### User Input
> "Remember the payment monolith migration spike we did last week? We got ADRs for service decomposition, inter-service communication, and migration strategy. But we got stuck on database decomposition. Can we dig into that one?"

### Assistant Output

*[Assistant loads context from the previous spike session or asks the user to summarize]*

**Loaded Existing Context**:

| Item | Status |
|---|---|
| Spike goal | Determine target architecture for decomposing payment monolith into microservices |
| ADR-001: Service decomposition (payment-type services) | ✅ Drafted |
| ADR-002: Inter-service communication (hybrid REST + Kafka) | ✅ Drafted |
| ADR-003: Database decomposition strategy | ❌ Unresolved — options identified but no decision |
| ADR-004: Migration strategy (strangler fig) | ✅ Drafted |
| Solution document | Draft exists, notes "database strategy TBD" |

**Existing ADR-003 Context** (what was already known):

- Single PostgreSQL database, ~80 tables
- `transactions`, `accounts`, and `audit_log` tables shared across all payment types
- 2000+ lines of stored procedures for settlement logic
- Two options were surfaced but not evaluated in depth:
  - **Option A**: One DB per service (full decomposition)
  - **Option B**: Shared DB with materialized views per service

---

## Step 2: Confirm Deep-Dive Scope

### Assistant Output

> "You want to deep-dive into **ADR-003: Database Decomposition Strategy**. The other three ADRs stand as-is. The unresolved question is: should we go with one DB per service, shared DB with views, or is there a third option we haven't fully explored?"

### User Confirms

> "Yes, exactly. I'm worried about the stored procedures — they're 2000+ lines and tangled across payment types. And I don't know if splitting the DB will break the settlement logic. We need to figure out which approach actually works."

### Assistant Validates

- **Area is independently decidable**: Yes — database decomposition is a standalone architectural decision. It interacts with ADR-001 (service boundaries) and ADR-002 (communication patterns), but those are already decided and provide constraints, not dependencies.
- **Deep-dive scope is narrow enough**: Yes — focus is on answering "can we split the DB without breaking settlement?", not re-opening the entire spike.

---

## Step 3: Investigate Deeper

*[Single deep-dive task — dispatched to a code-exploration sub-agent seeded with the area's existing findings doc (evidence map) to keep the orchestrating agent's context small (see `reference/multi-agent-orchestration.md`). The sub-agent applies `investigate-code` with narrow, targeted focus.]*

### Assistant Output

> "Deep-diving into: **Database Decomposition Strategy** — can we split the monolithic DB without breaking settlement logic?"

**Targeted Investigation** (narrower than the original Phase 2 investigation):

**What's NEW in this investigation** (things not covered in the original spike):

- **Stored procedure dependency graph**: 12 procedures traced — 8 are payment-type-specific (isolable); 4 span types (`settle_cross_type()`, `reconcile_daily()`, `calculate_fees()`, `audit_trail()`) joining `transactions` across all types.
- **Table-level access analysis**: `credit_card_auths` and `bank_transfer_refs` are single-type → safe to isolate; `transactions` is read/written by ALL types (core conflict point); `accounts` read by all, written only by settlement batch.
- **Settlement batch profiling**: nightly batch runs as a single stored procedure call with 4 dependent sub-procedures, ~500K transactions in 45 minutes; the cross-type procedures are the bottleneck (full-table scans on `transactions`).
- **Prototype assessment**: cross-type procedures could be rewritten as a standalone settlement service owning `transactions` and `accounts`, with payment-type services writing via async events (aligns with ADR-002's Kafka decision).

**What was ALREADY KNOWN** (from previous spike, not re-investigated):
- Single PostgreSQL, ~80 tables, 2000+ lines of stored procedures.
- No database-level access control per payment type.
- Team has strong PostgreSQL expertise but no experience with distributed transactions.

---

## Step 4: Evaluate Solutions

*[evaluate-solutions-per-area applied with deepened context]*

### Assistant Output

> "Based on the deeper investigation, we now know the settlement stored procedures are the critical coupling point. This opens up a third option we didn't fully explore before: extracting settlement as its own service. Here are the updated options:"

### Area: Database Decomposition Strategy (Revisited)

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A: One DB per service** | Each service gets its own DB; `transactions` duplicated or split. | Maximum independence; per-service DB choice; microservices ideal | Settlement logic rewritten; distributed cross-type queries; consistency challenges |
| **B: Shared DB + materialized views** | Keep single PostgreSQL; each service accesses its tables + views for cross-type data. | Lowest migration effort; stored procedures mostly untouched; team comfort zone | Still a monolithic DB; view refresh lag; scaling bottleneck remains; no domain boundaries |
| **C: Shared DB + settlement extraction** (NEW) | Payment-type services own type-specific tables; settlement extracted as its own service owning `transactions` + `accounts`; payment services publish events, settlement consumes. | Gradual decomposition; settlement scales independently; aligns with ADR-002 (Kafka already decided); incremental stored-procedure rewrite | Settlement becomes a critical dependency; eventual consistency between write and settlement; initially more complex than B |
| **D: Event sourcing + CQRS** | All payment events stored as an immutable stream; each service projects its own read model. | Built-in audit trail; fully independent services; replay capability | Massive paradigm shift; zero team experience; 2000+ lines of procedure logic rethought; overengineered |

**Decision Drivers** (unchanged from original spike):
- Hard: Must not break nightly settlement batch (45-min SLAs); Must maintain transactional consistency for payment capture
- Soft: Prefer incremental migration over big-bang; Prefer solutions that leverage ADR-002's Kafka investment

### Assistant Output

> "Option C wasn't obvious before because we didn't know the stored procedures were the core coupling point. Now that we've traced them, extracting settlement as a service is a natural fit — especially since we already decided on Kafka for inter-service communication in ADR-002. Option D (event sourcing) is probably overkill. What do you think?"

### User Response

> "Option C makes a lot of sense. The settlement extraction gives us a clear path forward without a big-bang DB split. And it reuses the Kafka investment from ADR-002. Let's go with that."

**Assumed Solution**: Option C — Keep a shared PostgreSQL initially, extract settlement logic into its own service that owns `transactions` and `accounts` tables, with payment-type services owning their type-specific tables and publishing events to Kafka for settlement processing.

---

## Step 5: Update ADR-003

*[draft-area-adrs skill applied to update the existing ADR]*

### ADR-003: Database Decomposition Strategy for Payment Microservices

**Title**: ADR-003: Gradual Database Decomposition with Settlement Extraction

**Status**: Draft

**Problem**: The payment monolith uses a single PostgreSQL database (~80 tables) shared across all payment types. Decomposing into microservices requires a database strategy that maintains data consistency while allowing services to evolve independently. The nightly settlement batch (45 min, 500K transactions) is the critical coupling point — its stored procedures span all payment types.

**Decision Drivers**:
- Hard: Must not break nightly settlement batch (45-min SLA); Must maintain transactional consistency for payment capture
- Soft: Prefer incremental migration over big-bang; Prefer solutions that leverage ADR-002's Kafka investment; Prefer to minimize stored procedure rewrites in initial phase

**Considered Options**:
- **Option A**: One DB per service (full split) — Rejected: requires immediate rewrite of all settlement logic; too risky for a single migration step.
- **Option B**: Shared DB with materialized views — Rejected: doesn't solve the scaling bottleneck; doesn't enforce domain boundaries; postpones the hard problem.
- **Option C**: Shared DB + settlement extraction — **Chosen**: Incremental approach; settlement becomes independently deployable and scalable; reuses Kafka from ADR-002.
- **Option D**: Event sourcing + CQRS — Rejected: paradigm shift too large for current team expertise; overengineered for the immediate needs.

**Chosen Option**: Option C — Shared DB with gradual settlement extraction. Phase 1: payment-type services own their type-specific tables; settlement service owns `transactions` and `accounts`; payment services publish events to Kafka for settlement consumption. Phase 2 (future): further decompose settlement or migrate to per-service databases as needed.

**Consequences**:
- (+) Incremental migration — each payment type can be extracted independently.
- (+) Settlement becomes independently deployable and scalable, addressing the 45-min bottleneck.
- (+) Reuses Kafka investment from ADR-002; consistent communication patterns across all services.
- (+) Stored procedures rewritten incrementally as logic moves into the settlement service.
- (-) Settlement service becomes a critical runtime dependency — if it's down, cross-type reconciliation pauses.
- (-) Eventual consistency between payment capture and settlement processing — requires monitoring and alerting.
- (-) Shared DB remains in the short term — full per-service databases deferred to Phase 2.

*[The ADR above was **rewritten in place**: the old unresolved draft's content was deleted and replaced by this single coherent decision. The deep-dive corrections (stored procedure dependency graph, settlement batch profiling) live in the findings document. The ADR carries no logs, no "updated" markers, and no version history — the delta is narrated here in conversation, not inside the document (see **reference/clean-artifact-principle.md**).]*

---

## Step 6: Optionally Update Solution Document

### Assistant Output

> "ADR-003 now recommends settlement extraction with shared DB. This changes the system-level view — the C2 diagram needs a new Settlement Service container, and the sequence diagram for the nightly batch needs updating. Should I refresh the solution document?"

### User Response

> "Yes, please update it. The settlement service is a new architectural element that wasn't in the original diagram."

*[compile-solution-doc applied to refresh the solution document]*

*[The affected sections of the solution document are **rewritten in place** — the doc now reads as if the Settlement Service was always part of the target state. No version markers or change notes appear in the document; the delta is described here in conversation.]*

**Solution document (affected sections, rewritten in place)**:
- **C2 Container Diagram**: Settlement Service container, connected to Kafka (inbound events) and PostgreSQL (owns `transactions` + `accounts` tables).
- **Sequence Diagram (Nightly Settlement)**: Payment Services → Kafka → Settlement Service → PostgreSQL (settlement batch).
- **RAID Analysis**: Risk — Settlement Service is a critical dependency; Assumption — Kafka topic partitioning aligns with payment types for ordered processing.
- **Dependencies**: Settlement Service depends on Kafka cluster availability.

---

## Step 7: Present Deep-Dive Results

### Final Output Bundle

**Revised ADR**:
- ADR-003: Database Decomposition Strategy (resolved — Option C: shared DB + settlement extraction)

**Solution Document**: `solution.md` — C2 and sequence diagrams now include the Settlement Service; RAID and dependencies refreshed (rewritten in place, no version markers)

**Unchanged ADRs** (not revisited):
- ADR-001: Service Decomposition Boundaries (payment-type services)
- ADR-002: Inter-service Communication (hybrid REST + Kafka) — leveraged by ADR-003
- ADR-004: Migration Strategy (strangler fig)

### Wrap-Up (conversation level — not written into any artifact)

> **Deep-dive complete.** ADR-003 is now resolved with a concrete recommendation: shared DB + settlement extraction, phased incrementally. The settlement service reuses the Kafka infrastructure already decided in ADR-002. The other three ADRs were not revisited — their decisions remain valid.

---

## Step 8: Wrap-Up and Next Round

*[Deep-dive complete — the assistant confirms whether to continue or conclude]*

### Assistant

> "ADR-003 is now resolved. Would you like to continue with another deep-dive round, or is this sufficient?"

### User Response

> "I'm satisfied with ADR-003 as-is. I'll decide on any follow-ups separately."

### Assistant

> "Understood. ADR-003 is finalized.
>
> As always: ADRs are formal decision records — review and approve with the team. The solution document and ADRs are version-controlled together in the spike folder — ADRs in `adrs/`, solution doc at the root (see `examples/spike-artifact-layout.md`)."
