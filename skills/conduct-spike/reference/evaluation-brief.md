# Evaluation Brief

Per-phase dispatch brief for `evaluate-problem-solutions` → `adr-writer` — loaded on demand when dispatching a problem's evaluation so the other phases' briefs are never pulled in. Shared evidence-map input/output contract: **reference/dispatch-briefs.md**.

**Announce**: "Dispatching evaluation of [N] problem(s) to a sub-agent."

Brief per problem (batch a whole area's problems in one brief when they share its subject/evidence): problem name ("How to …?"), its area + description, spike goal, the area's findings doc (evidence sections). Instructions: load `draft-adr` and run the interactive evaluate chain — **define-decision-drivers** → **define-considered-options** → **evaluate-options** — with the user dialog inside the sub-agent session. Expected output: the problem's assumed solution. After collection, review each for fidelity to the findings doc and cross-area consistency; definitive verification lands on the Phase 4 ADR.
