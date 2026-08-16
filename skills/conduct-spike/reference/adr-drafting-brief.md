# ADR-Drafting Brief

Dispatch brief for `draft-problem-adrs` → `adr-writer` — loaded on demand when dispatching ADR drafting so the other briefs are never pulled in. Shared evidence-map input/output contract: **reference/dispatch-briefs.md**.

**Announce**: "Dispatching ADR drafting for [N] problem(s) to a sub-agent."

Brief per problem (batch a whole area's problems in one brief when they share its evidence): problem name ("How to …?"), its area + description, spike goal, the area's findings doc (evidence sections). Instructions: load `draft-adr` and run the full flow — **define-decision-drivers** → **define-considered-options** → **evaluate-options** (applying **detail-options-tech** when tech details are needed) → **compile-adr** — with the user dialog inside the sub-agent session; tag the ADR with its `Area:`. When an option reveals a constraint, risk, or fact the findings doc lacks, report it back so the spike can sync it (per **artifact-maintenance-doctrine**). After collection, review each ADR.
