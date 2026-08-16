# ADR-Drafting Brief

Per-phase dispatch brief for `draft-problem-adrs` → `adr-writer` — loaded on demand when dispatching ADR drafting so the other phases' briefs are never pulled in. Shared evidence-map input/output contract: **reference/dispatch-briefs.md**.

**Announce**: "Dispatching ADR drafting for [N] problem(s) to a sub-agent."

Brief per problem (batch a whole area's problems in one brief when they share its evidence): problem name ("How to …?"), its area + description, evaluation results (decision drivers, options with pros/cons, **tech details per option**, assumed solution), the area's findings doc (evidence sections). Instructions: load `draft-adr` and apply **compile-adr** seeded with the evaluation results; tag the ADR with its `Area:`. After collection, review each ADR.
