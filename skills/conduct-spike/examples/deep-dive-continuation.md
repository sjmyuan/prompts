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

*[investigate-code skill applied with narrow, targeted focus]*

### Assistant Output

> "Deep-diving into: **Database Decomposition Strategy** — can we split the monolithic DB without breaking settlement logic?"

**Targeted Investigation** (narrower than the original Phase 2 investigation):

**What's NEW in this investigation** (things not covered in the original spike):

- **Stored procedure dependency graph**: Traced all 12 stored procedures to identify which ones span multiple payment types.
  - 8 of 12 procedures are payment-type-specific (can be isolated).
  - 4 procedures span types: `settle_cross_type()`, `reconcile_daily()`, `calculate_fees()`, `audit_trail()` — these join `transactions` across all payment types.
- **Table-level access analysis**: Mapped which payment types read/write to which tables:
  - `credit_card_auths` table: only CreditCardPayment service touches it → safe to isolate.
  - `bank_transfer_refs` table: only BankTransferPayment service → safe to isolate.
  - `transactions` table: ALL payment types read and write → the core conflict point.
  - `accounts` table: ALL payment types read; only settlement batch writes.
- **Settlement batch profiling**: Profiled the nightly settlement batch process:
  - Currently runs as a single stored procedure call with 4 dependent sub-procedures.
  - Processes ~500K transactions/night, takes 45 minutes.
  - The cross-type procedures are the bottleneck — they do full-table scans on `transactions`.
- **Prototype assessment**: Evaluated feasibility of extracting settlement into its own service:
  - Cross-type stored procedures could be rewritten as a standalone settlement service.
  - The settlement service would own the `transactions` and `accounts` tables.
  - Payment-type services would write to the settlement service via async events (aligns with ADR-002's Kafka decision).

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
| **A: One DB per service (full split)** | Each payment-type service gets its own database. `transactions` table duplicated or split. | Maximum independence; each service can choose its own DB; aligns with microservices ideal | Settlement logic must be completely rewritten; cross-type queries become distributed; data consistency challenges |
| **B: Shared DB with materialized views** | Keep single PostgreSQL. Each service accesses only its own tables + materialized views for cross-type data. | Lowest migration effort; stored procedures mostly untouched; team stays in comfort zone | Still a monolithic DB underneath; materialized view refresh lag; scaling bottleneck remains; doesn't enforce domain boundaries |
| **C: Shared DB + settlement extraction** (NEW) | Payment-type services own their type-specific tables. Settlement extracted as its own service that owns `transactions` and `accounts`. Payment services publish events; settlement service consumes and processes. | Gradual decomposition; settlement bottleneck gets its own scaling; aligns with ADR-002 (Kafka already decided); stored procedures rewritten incrementally | Settlement service becomes a critical dependency; eventual consistency between payment write and settlement processing; more complex than Option B initially |
| **D: Event sourcing + CQRS** | All payment events stored as immutable event stream. Each service projects its own read model. | Full audit trail built-in; services truly independent; replay capability for debugging | Massive paradigm shift; team has zero event sourcing experience; 2000+ lines of stored procedure logic must be rethought; overengineered for the problem |

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

### Updated ADR-003: Database Decomposition Strategy for Payment Microservices

**Title**: ADR-003: Gradual Database Decomposition with Settlement Extraction

**Status**: Draft (updated from unresolved)

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

---

## Step 6: Optionally Update Solution Document

### Assistant Output

> "ADR-003 now recommends settlement extraction with shared DB. This changes the system-level view — the C2 diagram needs a new Settlement Service container, and the sequence diagram for the nightly batch needs updating. Should I refresh the solution document?"

### User Response

> "Yes, please update it. The settlement service is a new architectural element that wasn't in the original diagram."

*[compile-solution-doc applied to refresh the solution document]*

**Changes to Solution Document**:
- **C2 Container Diagram**: Added Settlement Service container, connected to Kafka (inbound events) and PostgreSQL (owns `transactions` + `accounts` tables).
- **Sequence Diagram (Nightly Settlement)**: Updated to show: Payment Services → Kafka → Settlement Service → PostgreSQL (settlement batch), replacing the old monolith-internal stored procedure call.
- **RAID Analysis**: Added risk about Settlement Service being a critical dependency; added assumption that Kafka topic partitioning aligns with payment types for ordered processing.
- **Dependencies**: Added Settlement Service to the service inventory; noted it depends on Kafka cluster availability.

---

## Step 7: Present Deep-Dive Results

### Final Output Bundle

**Updated ADR**:
- ADR-003: Database Decomposition Strategy (now resolved — Option C: shared DB + settlement extraction)

**Updated Solution Document**: `solution-doc-payment-migration.md` (v2)
- Added Settlement Service to C2 and sequence diagrams
- Updated RAID and dependencies

**Unchanged ADRs** (not revisited):
- ADR-001: Service Decomposition Boundaries (payment-type services) — unchanged
- ADR-002: Inter-service Communication (hybrid REST + Kafka) — unchanged, leveraged by new ADR-003
- ADR-004: Migration Strategy (strangler fig) — unchanged

### Closing Notes

> **Deep-dive complete.** ADR-003 is now resolved with a concrete recommendation: shared DB + settlement extraction, phased incrementally. The settlement service reuses the Kafka infrastructure already decided in ADR-002. The other three ADRs were not revisited — their decisions remain valid.
>
> If new questions arise during implementation (e.g., the exact Kafka topic design for settlement events), we can deep-dive into those as follow-up investigations.
>
> As always: ADRs are formal decision records — review and approve with the team. The solution document should be version-controlled alongside the ADRs.
