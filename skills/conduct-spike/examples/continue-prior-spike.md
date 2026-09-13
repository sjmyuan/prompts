# Example: Continue a Prior Spike — Database Decomposition Round 2

**Scenario**: A completed payment-migration spike left database decomposition unresolved. The user asks to dig into that area and add a schema-migration problem.

**Applies**: `continue-prior-spike` → `investigate-per-area` → `compile-findings-doc` → `draft-problem-adrs` (evaluation via `draft-adr`) → `sync-update-artifacts`

**What makes this distinct**: A continuation round — one area revisited **plus a new problem added** under it. The scope-map delta drives which ADRs change and how `solution.md`'s area section grows.

---

## Step 1: Load Prior Spike Artifacts

### User Input

> "Remember the payment monolith migration spike? We got ADRs for service decomposition, communication, and migration strategy, but got stuck on database decomposition. Can we dig into that? And we should also figure out how to migrate the schema safely — that wasn't covered."

### Assistant Output

**Loaded existing artifacts** (incl. `scope.md`): service-decomposition, communication, and migration ADRs `done`; `adr-database-01-break-up-database.md` unresolved (options surfaced, no decision); solution doc draft — "database strategy TBD"; `scope.md` Database area `spiking` (db-01 `deciding`, schema-migration `investigating`).

**`adr-database-01` prior context**: single PostgreSQL, ~80 tables; `transactions`/`accounts`/`audit_log` shared across payment types; 2000+ lines of settlement procedures.

**Scope-map delta requested**: add a new problem under `Database decomposition` — "How to migrate the schema safely?" → `adr-database-02-schema-migration.md`.

---

## Step 2: Confirm Continuation Scope (against the scope map)

> "You want to revisit `adr-database-01-break-up-database.md` and add a new problem — schema migration — under the same area. The other ADRs stand as-is. Open questions: (1) one DB per service, shared DB with views, or a third option? (2) how to migrate the schema safely given the stored procedures?"

### User

> "Yes. I'm worried the 2000+ lines of settlement procedures will break if we split the DB. Which approach actually works?"

### Assistant validates

- **Independently decidable**: yes — the other ADRs are decided, providing constraints only.
- **Narrow enough**: yes — answer the DB-split and schema-migration questions, not re-open the spike.
- **Scope map updated**: `scope.md` gains the new problem → `adr-database-02-schema-migration.md` (`investigating`).

---

## Step 3: Investigate Deeper (Seeded, Targeted)

*(Dispatched to a code-exploration sub-agent seeded with the area's existing evidence map so covered code is not re-scanned — see `reference/multi-agent-orchestration.md`.)*

> "Deep-diving into: Database Decomposition Strategy — can we split the monolithic DB without breaking settlement logic? And which schema-migration approach fits the stored procedures?"

**NEW findings** (not covered in the original spike):

- **Stored-procedure dependency graph**: 12 procedures — 8 payment-type-specific (isolable); 4 span types (`settle_cross_type()`, `reconcile_daily()`) joining `transactions` across all types.
- **Table-level access**: `credit_card_auths`/`bank_transfer_refs` single-type → safe to isolate; `transactions` read/written by ALL types (core conflict); `accounts` read by all, written only by the settlement batch.
- **Settlement profiling**: nightly call, ~500K transactions in 45 min; cross-type procedures are the bottleneck.
- **Extraction assessment**: cross-type procedures could become a standalone settlement service owning `transactions` + `accounts`, with payment services writing via async events (reuses Kafka).

**Already known** (not re-investigated): single PostgreSQL, ~80 tables, 2000+ lines of procedures, no DB-level access control.

**Findings doc updated in place**: new facts recorded in the Evidence & Verification section with `file:line` + confidence tags.

---

## Step 4: Draft/Revise Problem ADRs — Evaluate + Draft (Rewrite In Place)

*(draft-problem-adrs applied per problem, seeded with the updated findings doc; each ADR's evaluation runs via `draft-adr`'s **evaluate-options** inside the drafting session.)*

**Problem 1 — break up the database — evaluation**:

> "The dependency graph shows settlement procedures are the critical coupling point. That opens a third option: extracting settlement as its own service."

| Option | Description | Verdict |
|---|---|---|
| A: One DB per service | Each service owns its DB; `transactions` split or duplicated | Rejected — full rewrite of settlement logic; too risky in one step |
| B: Shared DB + views | Single PostgreSQL; services access tables + views | Rejected — scaling bottleneck remains; defers the hard problem |
| C: Shared DB + settlement extraction (NEW) | Payment services own type-specific tables; settlement service owns `transactions` + `accounts`; events via Kafka | **Chosen** — incremental; settlement scales independently; reuses the Kafka decision |
| D: Event sourcing + CQRS | Immutable event stream; per-service read models | Rejected — paradigm shift; zero team experience; overengineered |

> "Option C wasn't obvious before we traced the procedures — and it reuses the Kafka decision. What do you think?"

### User

> "Option C makes sense — a clear path without a big-bang split. Let's go with that."

**Problem 2 — migrate the schema safely** (new problem under the same area):

| Option | Verdict |
|---|---|
| A: Expand-contract (additive → backfill → drop) | **Chosen** — reversible per service; aligns with phased Option C |
| B: Copy-and-switch per table | Rejected — downtime; risky with cross-type procedures |
| C: Big-bang migration | Rejected — contradicts the incremental strategy |

### ADRs written (rewritten in place — old drafts deleted, no version markers; see `reference/artifact-maintenance-guide.md`)

**`adr-database-01-break-up-database.md` — Gradual Database Decomposition with Settlement Extraction** (revised)
- **Problem**: Single PostgreSQL DB (~80 tables) shared across all payment types; the nightly settlement batch (45 min, 500K transactions) is the critical coupling point.
- **Chosen Option**: Phase 1 — payment-type services own type-specific tables; settlement service owns `transactions` + `accounts`; events via Kafka. Phase 2 — further decompose.
- **Consequences**: (+) incremental; (+) settlement scales independently; (+) reuses Kafka; (−) settlement is a critical runtime dependency; (−) eventual consistency needs monitoring.

**`adr-database-02-schema-migration.md` — Schema Migration via Expand-Contract** (new)
- **Problem**: Splitting the DB needs a schema-migration approach that keeps the 2000+ line stored procedures working during the phased transition.
- **Chosen Option**: Expand-contract — additive columns, backfill, then drop; each migration ships with its owning service.
- **Consequences**: (+) reversible; (+) no downtime; (+) matches the phased split; (−) temporary dual-schema window; (−) backfill volume needs batching.

---

## Step 5: Sync Downstream

*(sync-update-artifacts — the database area now has two decided ADRs)*

> "The database area now has two decisions. The C2 diagram needs a Settlement Service container, and the solution doc's `Database decomposition` section gains a schema-migration subsection. I'll refresh the solution document."

**Solution doc** (via `write-solution-doc`, rewritten in place):
- `Database decomposition` section: settlement-extraction + schema-migration decisions (grouped by area per `scope.md`).
- C2: Settlement Service container (inbound Kafka events; owns `transactions` + `accounts`).
- Sequence (nightly settlement): Payment Services → Kafka → Settlement Service → PostgreSQL.
- RAID: Risk — Settlement Service is a critical dependency; Assumption — Kafka topic partitioning aligns with payment types.

**Consistency check**: [x] ADRs cite updated findings [x] solution doc mirrors both decisions grouped by area [x] no-note scan passes.

---

## Step 6: Present Results + Next Round

**Revised**: `adr-database-01-break-up-database.md` (resolved — Option C). **Added**: `adr-database-02-schema-migration.md` (expand-contract). **Updated**: `scope.md` (new problem), solution doc's database area section. **Unchanged**: the other three ADRs.

> "Database decomposition is resolved: shared DB + settlement extraction, phased; and schema migration via expand-contract. Would you like to continue with another round, or is this sufficient?"

### User

> "I'm satisfied with both database ADRs. I'll decide on follow-ups separately."

> "Understood. ADRs are formal decision records — review and approve with the team. All artifacts version together in the spike folder."
