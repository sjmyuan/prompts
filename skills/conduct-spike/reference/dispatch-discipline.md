# Dispatch Discipline

Cross-cutting rules for every spike sub-agent dispatch. Briefs: **reference/dispatch-briefs.md**; dispatch pattern: **reference/multi-agent-orchestration.md**.

## Model routing

Choose the least powerful model that can do the unit; **state it explicitly** — an omitted model inherits the orchestrator's session model, often the most expensive.

| Work unit | Tier |
|---|---|
| Investigation (multi-file tracing, call chains) | Capable |
| Findings-doc / solution-doc compilation (synthesis of verified material) | Standard |
| ADR drafting (evaluation + option detail) | Standard–capable |
| Verification (per `question-everything`) | Scaled to claim risk — cheap for mechanical claims, mid for subtle ones |
| Re-investigation after a DISAGREE / UNCERTAIN | One tier above the original investigator |

- Specify the model in every dispatch brief.
- A unit that stays stuck is escalated to a more capable model — never retried unchanged on the same model.

## Waiting on sub-agents

- Never poll with short timeouts; never sit in one silent, open-ended wait.
- While local work remains (scope-map updates, preparing the next brief), keep working — results arrive on their own.
- When genuinely idle, wait in bounded stretches (five to ten minutes where the platform allows).
- Between stretches, reconcile live children: list them and chase any that finished without reporting.

## No sub-agents from workers

A dispatched worker never spawns sub-agents — not helpers, and never a verifier. The orchestrator owns every verification seat; a worker-spawned verifier duplicates it at full cost and its verdict counts for nothing. A unit too large for one pass reports back so the orchestrator splits or re-briefs it.

## Availability and fallback

Before dispatching, detect the platform's agent mechanism and map each unit to the closest equivalent agent type (see **multi-agent-orchestration**).

- No suitable agent → ask the user how to proceed, or run the unit in-session with the same brief and verification — never skip the unit.
- Verification with no same-type agent → verify directly against primary sources in-session (per `question-everything`'s protocol).

## Common rationalizations

| Excuse | Reality |
|---|---|
| "Single area / single ADR — dispatching is overhead" | Context preservation is the goal, not parallelism; the unit is still dispatched. |
| "The investigator was thorough — verification is redundant" | Verification is the gate; the original instance is never reused. |
| "The evidence map looks complete" | Completeness is verified per challenge, not by inspection. |
| "I'll verify it myself in this session" | Dispatch a NEW same-type agent; verify in-session only when no agent exists. |
| "Re-investigate with the same agent — it has context" | It anchors on its own output; dispatch a new instance. |
| "One more round will converge" | Past the cap the failure is structural — present both versions to the user. |
| "The worker spawned its own reviewer — extra assurance" | A duplicate seat; the orchestrator's verification is the gate. |
| "It's only a scope note — I'll edit the ADR directly" | Artifacts are written by their owning skill; bypassing it degrades them. |
