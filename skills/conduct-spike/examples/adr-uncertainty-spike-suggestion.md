# Example: ADR Uncertainty Triggers a Focused Spike Suggestion

**Scenario**: The spike workflow has reached the ADR drafting phase. The user is reviewing `adr-communication-01-service-communication.md` (problem: how to handle service-to-service communication) and hesitates: "I'm not sure about EventBridge — can it actually handle our peak volume?" The decision hinges on an unverified assumption, so instead of finalizing the ADR on guesswork, the skill names the uncertainty and offers a focused spike before the ADR is recorded.

**Applies**: `suggest-spike-on-adr-uncertainty` — invoked when ADR discussion reveals the decision depends on facts that haven't been established

**What makes this distinct**: This fires *during* ADR discussion, detects a single uncertainty signal, and offers one focused spike to resolve it before the ADR is finalized — rather than broad next-step candidates after an investigation round.

---

## Context: Mid-Spike, ADR Review

**Spike in progress**: "Migrate order processing to an event-driven architecture."

**Areas → problems**: (1) service boundaries → split the monolith, (2) communication mechanism → service-to-service communication, (3) data consistency → keep data consistent.

**Phase**: `draft-problem-adrs` — `adr-communication-01-service-communication.md` is being reviewed. The assumed solution is AWS EventBridge with an `OrderReceived` event, chosen because it is already present in the codebase.

**User's hesitation**: "I'm not sure about committing to EventBridge as the assumed solution. It's already in the codebase, but I don't actually know if it can handle our peak of 10K orders/sec — or whether we'd be better off with a Kafka-style bus for replay."

---

## Assistant Output: Uncertainty Detection + Spike Offer

> "Good catch — this decision seems to hinge on an assumption we haven't verified: **that EventBridge can handle your 10K orders/sec peak and provide the replay behavior the team may need.** Right now that's the deciding factor between EventBridge and a Kafka-style bus, and nobody has measured it.
>
> Before we finalize the communication ADR, would you like to spike this? We'd investigate:
>
> 1. **EventBridge throughput and throttling behavior at 10K orders/sec** — what the docs guarantee, what the current account limits are, and whether the existing deployment is anywhere near them
> 2. **Replay and redelivery semantics** — whether EventBridge's retention and lack of replay cover the team's audit and recovery needs, or whether that requires a different bus
>
> The ADR would stay provisional until the spike resolves these two questions — then we update it with evidence and continue to the solution document. Or, if you'd rather record the assumption as a risk in the ADR's consequences and move on, we can do that instead."

---

### User Response

> "Yes, let's spike it. Start with the throughput question — if EventBridge throttles at our peak, the decision changes completely."

### Assistant

> "Understood. New spike scope — **Goal**: determine whether EventBridge can handle the 10K orders/sec peak and what replay/redelivery semantics it offers. **Area**: communication mechanism. **Problems**: (1) EventBridge throughput limits and current usage, (2) replay/redelivery semantics vs. team needs. The communication ADR stays provisional. Let me define the scope details..."

---

## Key Takeaways

1. **One uncertainty signal, one focused spike**: The capability doesn't generate 6 candidates — it names the single unresolved fact and offers a spike scoped to resolve exactly that.
2. **The ADR stays provisional**: The spike is a gate before finalizing the ADR, not a parallel side quest. The example shows the ADR is updated with evidence afterward.
3. **Decline is respected**: The user is offered the alternative of recording the assumption as a risk in the ADR's consequences and moving on — no spike is forced.
4. **Focused, not broad**: This capability fires during ADR discussion and proposes a single focused investigation before the decision is recorded — not a broad set of next-step candidates.
