# Example: Continue a Prior Spike — Database Decomposition Round 2

**Scenario**: The user completed a spike on migrating a payment monolith to microservices. Four ADRs were drafted, but database decomposition was left unresolved. Now they ask to dig into that one area to reach a conclusion.

**Applies**: `continue-prior-spike` → `investigate-per-area` → `compile-findings-doc` → `evaluate-solutions-per-area` → `draft-area-adrs` → `sync-update-artifacts`

**What makes this distinct**: Not a full spike (scope already defined, other ADRs exist), not "from existing findings" (the area needs new investigation, not just formalization), and not a plain ADR revision (the area was never resolved). It shows a continuation round: one area revisited, the rest preserved.

---

## Step 1: Load Prior Spike Artifacts

### User Input

> "Remember the payment monolith migration spike? We got ADRs for service decomposition, communication, and migration strategy, but got stuck on database decomposition. Can we dig into that one?"

### Assistant Output

**Loaded existing artifacts**:

| Item | Status |
|---|---|
| Spike goal | Target architecture for decomposing the payment monolith into microservices |
| ADR-001 Service decomposition | ✅ Drafted |
| ADR-002 Communication (REST + Kafka) | ✅ Drafted |
| ADR-003 Database decomposition | ❌ Unresolved — options identified, no decision |
| ADR-004 Migration (strangler fig) | ✅ Drafted |
| Solution doc | Draft — "database strategy TBD" |

**ADR-003 prior context**: single PostgreSQL, ~80 tables; `transactions`/`accounts`/`audit_log` shared across payment types; 2000+ lines of settlement procedures; two options surfaced, not evaluated.

---

## Step 2: Confirm Continuation Scope

> "You want to revisit **ADR-003: Database Decomposition**. ADR-001/002/004 stand as-is. The open question: one DB per service, shared DB with views, or a third option?"

### User

> "Yes. I'm worried the 2000+ lines of settlement procedures will break if we split the DB. Which approach actually works?"

### Assistant validates

- **Independently decidable**: yes — ADR-001/002 are decided, providing constraints only.
- **Narrow enough**: yes — answer "can we split the DB without breaking settlement?", not re-open the spike.

---

## Step 3: Investigate Deeper (Seeded, Targeted)

*[Dispatched to a code-exploration sub-agent seeded with the area's existing findings doc (evidence map) so covered code is not re-scanned — see `reference/multi-agent-orchestration.md`. The sub-agent applies `investigate-code` with narrow focus.]*

> "Deep-diving into: Database Decomposition Strategy — can we split the monolithic DB without breaking settlement logic?"

**NEW findings** (not covered in the original spike):

- **Stored-procedure dependency graph**: 12 procedures traced — 8 payment-type-specific (isolable); 4 span types (`settle_cross_type()`, `reconcile_daily()`, …) joining `transactions` across all types.
- **Table-level access**: `credit_card_auths`/`bank_transfer_refs` single-type → safe to isolate; `transactions` read/written by ALL types (core conflict); `accounts` read by all, written only by the settlement batch.
- **Settlement batch profiling**: single nightly stored-procedure call, ~500K transactions in 45 min; the cross-type procedures are the bottleneck (full-table scans).
- **Prototype assessment**: cross-type procedures could become a standalone settlement service owning `transactions` + `accounts`, with payment-type services writing via async events (aligns with ADR-002's Kafka).

**Already known** (not re-investigated): single PostgreSQL, ~80 tables, 2000+ lines of procedures, no DB-level access control, strong PostgreSQL expertise.

**Findings doc updated in place**: new facts recorded in the Evidence & Verification section with `file:line` + confidence tags (per `reference/findings-document-guide.md`).

---

## Step 4: Evaluate With New Depth

*[evaluate-solutions-per-area applied, seeded with the updated findings doc]*

> "The dependency graph shows settlement procedures are the critical coupling point. That opens a third option: extracting settlement as its own service."

| Option | Description | Verdict |
|---|---|---|
| A: One DB per service | Each service owns its DB; `transactions` split or duplicated | Rejected — immediate full rewrite of settlement logic; too risky in one step |
| B: Shared DB + views | Single PostgreSQL; services access tables + views | Rejected — scaling bottleneck remains; no domain boundaries; defers the hard problem |
| C: Shared DB + settlement extraction (NEW) | Payment services own type-specific tables; settlement service owns `transactions` + `accounts`; events via Kafka | **Chosen** — incremental; settlement scales independently; reuses ADR-002's Kafka |
| D: Event sourcing + CQRS | Immutable event stream; per-service read models | Rejected — paradigm shift; zero team experience; overengineered |

> "Option C wasn't obvious before we traced the procedures — and it reuses ADR-002's Kafka. What do you think?"

### User

> "Option C makes sense — a clear path without a big-bang split. Let's go with that."

**Assumed solution**: Option C — keep shared PostgreSQL initially; extract settlement into its own service owning `transactions` + `accounts`; payment services publish events to Kafka.

---

## Step 5: Update ADR-003 (Rewrite In Place)

*[draft-area-adrs revising the existing ADR through `draft-adr`]*

**ADR-003: Gradual Database Decomposition with Settlement Extraction**

**Problem**: The payment monolith uses a single PostgreSQL database (~80 tables) shared across all payment types. Decomposing into microservices requires a database strategy that keeps data consistent while services evolve independently. The nightly settlement batch (45 min, 500K transactions) is the critical coupling point — its procedures span all payment types.

**Decision Drivers**: Hard — must not break the nightly settlement batch (45-min SLA); must maintain transactional consistency for payment capture. Soft — prefer incremental migration over big-bang; prefer solutions that leverage ADR-002's Kafka investment; minimize procedure rewrites initially.

**Considered Options**: A (one DB per service) — rejected: full rewrite of settlement logic in one step; B (shared DB + views) — rejected: keeps the bottleneck, defers the hard problem; C (shared DB + settlement extraction) — **chosen**: incremental, settlement scales independently, reuses Kafka; D (event sourcing + CQRS) — rejected: paradigm shift beyond team expertise.

**Chosen Option**: Phase 1 — payment-type services own type-specific tables; settlement service owns `transactions` + `accounts`; payment services publish events to Kafka for settlement consumption. Phase 2 — further decompose or move to per-service databases.

**Consequences**: (+) incremental migration; (+) settlement independently deployable/scalable; (+) reuses ADR-002's Kafka; (+) incremental procedure rewrites; (−) settlement becomes a critical runtime dependency; (−) eventual consistency between capture and settlement — needs monitoring.

*[The ADR was **rewritten in place**: the old unresolved draft's content was deleted and replaced by this single coherent decision. Corrections live in the findings doc; the ADR carries no "updated" markers — see `reference/artifact-maintenance-guide.md`.]*

---

## Step 6: Sync Downstream

*[sync-update-artifacts — ADR-003's decision changes the system-level view]*

> "ADR-003 now recommends settlement extraction. The C2 diagram needs a Settlement Service container and the nightly-batch sequence diagram needs updating. I'll refresh the solution document and change summary."

**Solution doc** (via `write-solution-doc`, rewritten in place):
- C2: Settlement Service container — inbound events from Kafka, owns `transactions` + `accounts`.
- Sequence (nightly settlement): Payment Services → Kafka → Settlement Service → PostgreSQL.
- RAID: Risk — Settlement Service is a critical dependency; Assumption — Kafka topic partitioning aligns with payment types.

**Change summary**: ADR-003 cluster recomputed — New: settlement service, Kafka topics; Modified: payment services publish events; retired items removed. Cross-cutting: settlement monitoring added.

**Consistency check**: [x] ADR cites updated findings [x] solution doc mirrors Option C [x] change summary traces to ADR-003 [x] no-note scan passes.

---

## Step 7: Present Results + Next Round

**Revised**: ADR-003 (resolved — Option C); solution doc + change summary refreshed in place. **Unchanged**: ADR-001, ADR-002, ADR-004 — decisions stand.

> "ADR-003 is resolved: shared DB + settlement extraction, phased. Would you like to continue with another round, or is this sufficient?"

### User

> "I'm satisfied with ADR-003. I'll decide on follow-ups separately."

> "Understood. ADRs are formal decision records — review and approve with the team. All artifacts version together in the spike folder."
