# Example: Proving an ADR Option with Compare-POCs

**Scenario**: ADR-002 (`adr-002-cache.md`) weighs two cache options — **Redis** vs **in-process**. The team can't decide on drivers alone; the user says: "Run a POC for each option to prove which is better — then pick."

**Applies**: **define-poc-scope** → **orchestrate-delivery** → **update-delivery-index**

## 1. Flag + sequence POC cells

Decomposition marks two POC cells (Wave 0, parallel) and one **poc-gated** implementation cell:

| Cell | Type | ADR / Option | Success criteria | Status |
|---|---|---|---|---|
| order-service/F5a | poc | ADR-002 · Redis | p99 < 50ms @ 2k rps; ≤ 3 new ops deps | unplanned |
| order-service/F5b | poc | ADR-002 · in-process | p99 < 50ms @ 2k rps; zero new deps | unplanned |
| order-service/F5 | feature | — (poc-gated on F5a/F5b decision) | — | unplanned |

## 2. Dispatch (POC mode, parallel)

- **Agent A** (coding-assistant) → plan + execute `F5a` (**plan-development-task** `plan-poc` / **execute-plan** POC mode) — brief carries `type: poc`, ADR-002, option Redis, success criteria.
- **Agent B** (coding-assistant) → plan + execute `F5b` (in-process) in parallel — same repo ⇒ serialize execution waves or split to different repos when possible.

## 3. Decision gate (user-recorded)

Both cells reach **poc-ready**. The orchestrator waits — the user reads the evaluation reports vs success criteria and records the decision directly in the index:

| Criterion | F5a (Redis) | F5b (in-process) |
|---|---|---|
| p99 < 50ms @ 2k rps | 34ms ✅ | 41ms ✅ |
| New ops deps | 1 (redis client) | 0 ✅ |

User records: F5a **adopted** (Redis), F5b **rejected**.

## 4. Adopt + reject

- Dispatch **adr-writer** (draft-adr): ADR-002 records the Redis decision + POC evidence.
- **F5a (POC-as-implementation)**: promote the branch — ask user, merge → **done**. No `replaces` target, so nothing is **superseded**.
- **F5b**: close **rejected**, archive branch; update index.
- **F5 (poc-gated)**: now dispatchable with the decided option — if the POC slice already ships the full feature, F5 may be dropped or reduced to the remaining scope.

## 5. Next actions

Index shows F5a **done**, F5b **rejected**, F5 unblocked. All statuses landed in the index before the next dispatch.
