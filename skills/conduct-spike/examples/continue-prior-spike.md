# Example: Continue a Prior Spike — Database Decomposition Round 2

**Scenario**: The user completed a spike on migrating a payment monolith to microservices. Four ADRs were drafted, but database decomposition was left unresolved. Now they ask to dig into that one area to reach a conclusion.

**Applies**: `continue-prior-spike` → `investigate-per-area` → `compile-findings-doc` → `evaluate-problem-solutions` → `draft-problem-adrs` → `sync-update-artifacts`

**What makes this distinct**: Not a full spike (scope already defined, other ADRs exist), not "from existing findings" (the area needs new investigation), and not a plain ADR revision (the problem was never resolved). It shows a continuation round: one area revisited **plus a new problem added under it** — the scope-map delta drives which ADRs change and how `solution.md`'s area section grows.

---

## Step 1: Load Prior Spike Artifacts

### User Input

> "Remember the payment monolith migration spike? We got ADRs for service decomposition, communication, and migration strategy, but got stuck on database decomposition. Can we dig into that? And we should also figure out how to migrate the schema safely — that wasn't covered."

### Assistant Output

**Loaded existing artifacts** (incl. the scope map `scope.md`):

| Item | Status |
|---|---|
| Spike goal | Target architecture for decomposing the payment monolith into microservices |
| `adr-service-decomposition-01-split-monolith.md` | ✅ Drafted |
| `adr-communication-01-service-communication.md` | ✅ Drafted |
| `adr-database-01-break-up-database.md` | ❌ Unresolved — options identified, no decision |
| `adr-migration-01-zero-downtime-migration.md` | ✅ Drafted |
| Solution doc | Draft — "database strategy TBD" |
| `scope.md` (status dashboard) | Service/Communication/Migration areas `done`; Database `spiking` (db-01 `deciding`, schema-migration `investigating`) |

**`adr-database-01` prior context**: single PostgreSQL, ~80 tables; `transactions`/`accounts`/`audit_log` shared across payment types; 2000+ lines of settlement procedures; two options surfaced, not evaluated.

**Scope-map delta requested**: add a new problem under `Database decomposition` — "How to migrate the schema safely?" → would become `adr-database-02-schema-migration.md`.

---

## Step 2: Confirm Continuation Scope (against the scope map)

> "You want to revisit **`adr-database-01-break-up-database.md`** and **add a new problem** — schema migration — under the same area. The decomposition/communication/migration ADRs stand as-is. Open questions: (1) one DB per service, shared DB with views, or a third option? (2) how to migrate the schema safely given the stored procedures?"

### User

> "Yes. I'm worried the 2000+ lines of settlement procedures will break if we split the DB. Which approach actually works?"

### Assistant validates

- **Independently decidable**: yes — the other ADRs are decided, providing constraints only.
- **Narrow enough**: yes — answer "can we split the DB without breaking settlement?" and "how to migrate the schema safely?", not re-open the spike.
- **Scope map updated**: `scope.md` gains the new problem under `Database decomposition` → `adr-database-02-schema-migration.md` (`investigating`).

---

## Step 3: Investigate Deeper (Seeded, Targeted)

*[Dispatched to a code-exploration sub-agent seeded with the area's existing findings doc (evidence map) so covered code is not re-scanned — see `reference/multi-agent-orchestration.md`. The sub-agent applies `investigate-code` with narrow focus.]*

> "Deep-diving into: Database Decomposition Strategy — can we split the monolithic DB without breaking settlement logic? And which schema-migration approach fits the stored procedures?"

**NEW findings** (not covered in the original spike):

- **Stored-procedure dependency graph**: 12 procedures traced — 8 payment-type-specific (isolable); 4 span types (`settle_cross_type()`, `reconcile_daily()`, …) joining `transactions` across all types.
- **Table-level access**: `credit_card_auths`/`bank_transfer_refs` single-type → safe to isolate; `transactions` read/written by ALL types (core conflict); `accounts` read by all, written only by the settlement batch.
- **Settlement batch profiling**: single nightly stored-procedure call, ~500K transactions in 45 min; the cross-type procedures are the bottleneck (full-table scans).
- **Prototype assessment**: cross-type procedures could become a standalone settlement service owning `transactions` + `accounts`, with payment-type services writing via async events (aligns with the Kafka decision).

**Already known** (not re-investigated): single PostgreSQL, ~80 tables, 2000+ lines of procedures, no DB-level access control, strong PostgreSQL expertise.

**Findings doc updated in place**: new facts recorded in the Evidence & Verification section with `file:line` + confidence tags (per `reference/findings-document-guide.md`).

---

## Step 4: Evaluate With New Depth

*[evaluate-problem-solutions applied per problem, seeded with the updated findings doc]*

**Problem 1 — break up the database**:

> "The dependency graph shows settlement procedures are the critical coupling point. That opens a third option: extracting settlement as its own service."

| Option | Description | Verdict |
|---|---|---|
| A: One DB per service | Each service owns its DB; `transactions` split or duplicated | Rejected — immediate full rewrite of settlement logic; too risky in one step |
| B: Shared DB + views | Single PostgreSQL; services access tables + views | Rejected — scaling bottleneck remains; no domain boundaries; defers the hard problem |
| C: Shared DB + settlement extraction (NEW) | Payment services own type-specific tables; settlement service owns `transactions` + `accounts`; events via Kafka | **Chosen** — incremental; settlement scales independently; reuses the Kafka decision |
| D: Event sourcing + CQRS | Immutable event stream; per-service read models | Rejected — paradigm shift; zero team experience; overengineered |

> "Option C wasn't obvious before we traced the procedures — and it reuses the Kafka decision. What do you think?"

### User

> "Option C makes sense — a clear path without a big-bang split. Let's go with that."

**Assumed solution**: Option C — keep shared PostgreSQL initially; extract settlement into its own service owning `transactions` + `accounts`; payment services publish events to Kafka.

**Problem 2 — migrate the schema safely** (new problem under the same area):

| Option | Verdict |
|---|---|
| A: Expand-contract (additive columns → backfill → drop) | **Chosen** — reversible per service; aligns with phased Option C |
| B: Copy-and-switch per table | Rejected — downtime during switch; risky with cross-type procedures |
| C: Big-bang migration | Rejected — contradicts the incremental DB strategy |

**Assumed solution**: Option A — expand-contract migrations shipped with each service.

---

## Step 5: Draft/Revise Problem ADRs (Rewrite In Place)

*[draft-problem-adrs revising `adr-database-01-break-up-database.md` and drafting new `adr-database-02-schema-migration.md` through `draft-adr`]*

**`adr-database-01-break-up-database.md`: Gradual Database Decomposition with Settlement Extraction**

**Problem**: The payment monolith uses a single PostgreSQL database (~80 tables) shared across all payment types. Decomposing into microservices requires a database strategy that keeps data consistent while services evolve independently. The nightly settlement batch (45 min, 500K transactions) is the critical coupling point — its procedures span all payment types.

**Decision Drivers**: Hard — must not break the nightly settlement batch (45-min SLA); must maintain transactional consistency for payment capture. Soft — prefer incremental migration over big-bang; prefer solutions that leverage the Kafka decision; minimize procedure rewrites initially.

**Considered Options**: A (one DB per service) — rejected: full rewrite of settlement logic in one step; B (shared DB + views) — rejected: keeps the bottleneck, defers the hard problem; C (shared DB + settlement extraction) — **chosen**: incremental, settlement scales independently, reuses Kafka; D (event sourcing + CQRS) — rejected: paradigm shift beyond team expertise.

**Chosen Option**: Phase 1 — payment-type services own type-specific tables; settlement service owns `transactions` + `accounts`; payment services publish events to Kafka for settlement consumption. Phase 2 — further decompose or move to per-service databases.

**Consequences**: (+) incremental migration; (+) settlement independently deployable/scalable; (+) reuses the Kafka decision; (+) incremental procedure rewrites; (−) settlement becomes a critical runtime dependency; (−) eventual consistency between capture and settlement — needs monitoring.

*[The ADR was **rewritten in place**: the old unresolved draft's content was deleted and replaced by this single coherent decision. Corrections live in the findings doc; the ADR carries no "updated" markers — see `reference/artifact-maintenance-guide.md`.]*

**`adr-database-02-schema-migration.md`: Schema Migration via Expand-Contract** (new — added problem under the same area)

**Problem**: Splitting the monolithic database needs a schema-migration approach that keeps the 2000+ line stored procedures working during the phased transition.

**Decision Drivers**: Hard — no downtime; must not break the nightly settlement batch. Soft — prefer migrations shipped with each service; prefer reversible steps.

**Considered Options**: A (expand-contract) — **chosen**: additive, reversible per service, aligns with Option C's phasing; B (copy-and-switch) — rejected: downtime during switch, risky with cross-type procedures; C (big-bang) — rejected: contradicts the incremental strategy.

**Chosen Option**: Expand-contract — additive columns first, backfill, then drop; each migration ships with its owning service.

**Consequences**: (+) reversible; (+) no downtime; (+) matches phased DB split; (−) temporary dual-schema window; (−) backfill volume on large tables needs batching.

---

## Step 6: Sync Downstream

*[sync-update-artifacts — the database area now has two decided ADRs]*

> "The database area now has two decisions. The C2 diagram needs a Settlement Service container, and the solution doc's `Database decomposition` section gains a schema-migration subsection. I'll refresh the solution document."

**Solution doc** (via `write-solution-doc`, rewritten in place):
- `Database decomposition` area section: settlement-extraction decision + new schema-migration decision (grouped under the same area per `scope.md`).
- C2: Settlement Service container — inbound events from Kafka, owns `transactions` + `accounts`.
- Sequence (nightly settlement): Payment Services → Kafka → Settlement Service → PostgreSQL.
- RAID: Risk — Settlement Service is a critical dependency; Assumption — Kafka topic partitioning aligns with payment types.

**Consistency check**: [x] ADRs cite updated findings [x] solution doc mirrors both decisions grouped by area [x] no-note scan passes.

---

## Step 7: Present Results + Next Round

**Revised**: `adr-database-01-break-up-database.md` (resolved — Option C). **Added**: `adr-database-02-schema-migration.md` (expand-contract). **Updated**: `scope.md` (new problem), solution doc's database area section. **Unchanged**: the other three ADRs.

> "Database decomposition is resolved: shared DB + settlement extraction, phased; and schema migration via expand-contract. Would you like to continue with another round, or is this sufficient?"

### User

> "I'm satisfied with both database ADRs. I'll decide on follow-ups separately."

> "Understood. ADRs are formal decision records — review and approve with the team. All artifacts version together in the spike folder."
