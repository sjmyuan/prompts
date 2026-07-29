# Discovery Log Guide

A Discovery Log is a section appended to each findings document that records facts, corrections, and insights discovered during the spike — along with the evidence that supports them. It creates an audit trail from initial assumptions to final conclusions.

## Why a Discovery Log?

Spike investigations are iterative. You form hypotheses, investigate, and sometimes find that reality contradicts your assumptions. Without a log:

- Readers of the final artifacts can't tell which conclusions were hard-won vs. obvious from the start.
- Post-spike retrospectives lack a record of what was learned and when.
- If an assumption gets invalidated in Phase 3 (evaluation), there's no trace of why the findings document was updated.

A Discovery Log makes the reasoning trail transparent and the lessons from the spike reusable.

## When to record an entry

Record a discovery entry whenever:

| Trigger | Example |
|---|---|
| Investigation reveals a fact that contradicts a prior assumption | "Assumed service A calls service B synchronously, but code trace shows it's actually fire-and-forget via a queue." |
| Investigation reveals a fact that was simply unknown before | "Discovered that the payment gateway has a 500ms SLA on the `/authorize` endpoint — this constrains our retry strategy." |
| Evaluation of options uncovers a constraint not in the findings | "While evaluating Option C (message bus), realized the org has a policy against Kafka — must use RabbitMQ." |
| A deep-dive produces new information that changes the understanding of an area | "Deeper profiling shows the bottleneck is not the DB query (as initially thought) but the ORM hydration step." |
| User feedback during review corrects or refines a finding | "User corrected: the auth service is not a monolith — it was split into auth-core and auth-gateway in Q2." |

## Where to record

Each findings document includes a **Discovery Log** section at the end, after the constraints & pain points and raw data & metrics sections. When a discovery affects an ADR or the solution document, update those documents too and note the change.

## Entry format

Each entry follows this structure:

```markdown
## Discovery Log

### [YYYY-MM-DD] [One-line summary of the discovery]

**What was found or corrected**: [2–4 sentences describing the specific fact, constraint, or insight. Be precise — name the code paths, services, or data involved.]

**Evidence**: [How was this discovered? Code trace, benchmark, documentation, experiment, user confirmation, etc. Include file paths, commit hashes, or test results when available.]

**Impact**: [Which sections of which documents were updated as a result? E.g., "Updated Findings Doc §3.2 (Communication Patterns) and §4.1 (Sequence Diagram). ADR-002's Option A pros/cons re-evaluated."]

---
```

## Example entries

```markdown
## Discovery Log

### [2026-07-15] Payment gateway has 500ms SLA — not 2s as assumed

**What was found or corrected**: The payment gateway provider's SLA doc (ref: `docs/integration/payment-gateway-sla.pdf` §2.3) specifies a 500ms p95 latency target for the `/authorize` endpoint, not the 2s we initially assumed based on anecdotal experience. This means our sync-call pattern may violate the SLA under peak load.

**Evidence**: SLA document from provider dashboard, confirmed by ops team. Load test results from `perf/2026-07/payment-auth-latency.json` show p95 at 480ms in staging, leaving only 20ms headroom.

**Impact**: Updated Findings Doc §3.1 (External Dependencies) to correct the SLA value. Re-evaluated ADR-001 Option A (keep sync calls) — the 500ms SLA makes this option riskier than initially assessed. Added new Option D (async with circuit breaker) to ADR-001.

---

### [2026-07-15] Auth service already split — not monolithic

**What was found or corrected**: User review of findings doc corrected the assumption that the auth service is a monolith. It was split into `auth-core` (token management) and `auth-gateway` (rate limiting, routing) in Q2 2026. The C2 diagram and communication patterns section were inaccurate.

**Evidence**: User confirmation during findings doc review. Verified against `auth-core/README.md` and `auth-gateway/README.md` in the repository.

**Impact**: Updated Findings Doc §2 (C2 Container Diagram) to show two containers. Updated §3.2 (Communication Patterns) — calls between auth-core and auth-gateway are gRPC, not in-process. ADR-003 evaluation not affected (both options work with either topology).

---

### [2026-07-16] ORM hydration is the bottleneck, not the DB query

**What was found or corrected**: Deep-dive profiling revealed that the 800ms response time in the order listing endpoint is caused by ORM object hydration (650ms), not the SQL query itself (150ms). Initial investigation had incorrectly attributed the latency to a missing DB index.

**Evidence**: Profiler trace from `py-spy` run on 2026-07-16 (`profiles/order-list-20260716.svg`). Flame graph shows `sqlalchemy.orm.loading.instances()` consuming 81% of request time. DB query plan (`EXPLAIN ANALYZE`) confirms index is used correctly, query returns in 150ms.

**Impact**: Updated Findings Doc §3.3 (Performance Characteristics) — root cause changed from "missing index" to "ORM hydration overhead." ADR-004 re-evaluated: Option B (raw SQL + dataclasses) is now the recommended approach instead of Option A (add index).
```

## Anti-patterns to avoid

- **Vague entries**: "Found some issues with the DB." → Instead: "Found that the `orders` table has no index on `customer_id`, causing full table scans on the listing query."
- **No evidence**: "The service is slow." → Instead: "p95 latency is 2.3s according to Datadog dashboard (link). Profiler trace at `profiles/slow-endpoint.svg` shows 1.8s spent in `calculateTax()`."
- **No impact**: An entry that says something changed but doesn't say which documents were updated. Every entry must state which sections were corrected.
- **Rewriting history**: Don't delete old entries when findings change. The log is a timeline — old entries show what was believed and why, new entries show the correction. This is what makes the audit trail valuable.
