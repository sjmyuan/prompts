# Example: Syncing All Artifacts After New Evidence Flips an ADR Decision

**Scenario**: A spike produced findings, ADR-002 (REST), a solution doc, and a change summary. A follow-up prototype measures a 3K orders/sec REST throttle — below the 10K peak. The user asks to update the ADR. The assistant propagates the change through every downstream artifact so the whole bundle stays consistent.

**Applies**: `sync-update-artifacts`

**What makes this distinct**: Unlike `examples/update-artifact-in-place.md` (one ADR rewritten in place), this example shows the full propagation — one change rippling through ADR → solution doc → change summary, with the consistency checks in between.

---

## Context

Artifacts after the original spike:

- Findings doc: current state; peak load unmeasured (listed as an assumption)
- ADR-002: "Synchronous REST" (chosen because it is the simplest option)
- Solution doc: target architecture with REST request/response contracts
- Change summary: REST client/server clusters cited under ADR-002

## The change (user request)

> "We measured the load in a prototype — REST throttles at 3K orders/sec, below the 10K peak. Update the ADR."

## Propagation trace (what the assistant determines)

| Origin | Affected downstream |
|---|---|
| Code reference (new evidence: 3K/sec measured limit) | Findings doc → ADR-002 → solution doc → change summary |

## What the assistant does, artifact by artifact

1. **Code reference** (via `compile-code-reference`): records the measured 3K/sec throttle with `file:line` and a **verified** confidence tag.
2. **Findings doc** (via `write-solution-doc`): replaces the "peak load unmeasured" assumption with the measured 3K/sec limit; adds the REST throttle to constraints & pain points.
3. **ADR-002** (via `draft-adr`): decision changes to "Event-driven Kafka" — chosen option, justification, and consequences rewritten in place (see `update-artifact-in-place.md` for the before/after shape).
4. **Solution doc** (via `write-solution-doc`): inter-service communication section evolves from REST contracts to Kafka topics; C4/sequence diagrams updated; no "changed from REST" language.
5. **Change summary**: ADR-002 cluster updated — "Add Kafka client library" (Dependency), "Provision Kafka topics" (Configuration), "Refactor `PaymentOrchestrator` to publish events" (Modified); REST server/client items retired; cross-cutting "team Kafka training" added.

## Consistency check

- [x] ADR-002 cites the measured 3K/sec fact from the findings doc
- [x] Solution doc mirrors Kafka as the chosen option
- [x] Change summary clusters trace to current ADR-002 and solution-doc sections
- [x] No-note scan passes: no "changed from REST", "v2", or "Updated" in the ADR or solution doc

## What the assistant says (in conversation)

> "The prototype measured 3K/sec — below the 10K peak. I updated the findings doc with the measurement, flipped ADR-002 to Kafka in place, refreshed the solution doc's communication section and diagrams, and reworked the change summary: REST items retired, Kafka dependency/configuration items added. All four artifacts now agree."

## What is deliberately absent from the artifacts

- No "Updated"/"v2"/"Previously" markers in the ADR or solution doc
- No change history inside the documents — git keeps it
- The delta exists only in conversation
