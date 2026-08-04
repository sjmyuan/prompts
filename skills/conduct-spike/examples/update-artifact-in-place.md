# Example: Updating an ADR In Place After a Decision Change

**Scenario**: An ADR already exists for a decision area. A focused spike changes the decision. The assistant rewrites the ADR **in place** — the document reads as if the new decision was always the decision, with no "Updated", "v2", or "Previously" markers, and no changelog.

**Applies**: `deep-dive-specific-areas` (update ADR step) — demonstrates the **latest-state rewrite-in-place protocol** and the **no-note scan** from `reference/clean-artifact-principle.md`

**What makes this distinct**: Unlike `examples/deep-dive-continuation.md` (which shows the whole deep-dive workflow), this example zooms into the single act of revising an artifact — showing the before and after of the same ADR side by side so the rewrite behavior is unambiguous.

---

## Context

ADR-002 (inter-service communication) was drafted as "Synchronous REST". A follow-up spike on peak-load handling measures that REST cannot meet the 10K orders/sec peak; Kafka becomes the choice. The ADR must now reflect Kafka as the decision.

## Before: the ADR as it was drafted

```markdown
# ADR-002: Inter-Service Communication

* Status: Draft
* Owners: Payments Team
* Date: 2026-08-02

## Context and Problem Statement

Order processing services must exchange order lifecycle events. The team has no async messaging experience.

## Decision Outcome

Chosen option: "Synchronous REST", because the team is familiar with it and it is the simplest option.

## Consequences

- (+) Simplest option; no new infrastructure
- (-) Tight coupling; cascading failures on peak load
```

## The rewrite (what the assistant says, in conversation)

> "ADR-002's decision changed after the load spike — REST can't handle the 10K orders/sec peak. I'll rewrite the affected sections in place: the chosen option, justification, and consequences now state Kafka as the decision. The old REST content is deleted, not annotated — git keeps the history."

## After: the same ADR, rewritten in place

```markdown
# ADR-002: Inter-Service Communication

* Status: Draft
* Owners: Payments Team
* Date: 2026-08-02

## Context and Problem Statement

Order processing services must exchange order lifecycle events. Peak load is 10K orders/sec; the audit path requires replay and redelivery semantics.

## Decision Outcome

Chosen option: "Event-driven Kafka", because the measured 10K orders/sec peak exceeds REST's throttling limits, and Kafka provides the replay and redelivery semantics the audit path requires.

## Consequences

- (+) Decoupled services; survives peak load
- (+) Built-in replay and redelivery for the audit path
- (-) New infrastructure and team learning curve; eventual consistency
```

## What is deliberately absent from the after-version

- No "Updated", "Changed", "v2", or "As of" markers
- No "we used to use REST" or "previously the choice was REST" history
- No Note section, changelog, or process narration
- The old REST content is gone — the document has no memory of its own past

The delta is described in conversation only. The pre-rewrite state remains recoverable via version control.
