# Solution-Doc Brief

Dispatch brief for `compile-solution-doc` → `solution-doc-writer` — loaded on demand when dispatching solution-doc compilation so the other briefs are never pulled in. Shared evidence-map input/output contract: **reference/dispatch-briefs.md**.

**Announce**: "Dispatching solution-doc compilation to a sub-agent."

Brief: business context (spike goal), current-state baseline (findings docs), assumed solutions (chosen option from each ADR). Instructions: load `write-solution-doc` and produce a **target-state** document in **baseline-input mode**. After collection, review for completeness and consistency with the ADRs.
