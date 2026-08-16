# Findings-Doc Brief

Dispatch brief for `compile-findings-doc` → `solution-doc-writer` — loaded on demand when dispatching findings-doc compilation so the other briefs are never pulled in. Shared evidence-map input/output contract: **reference/dispatch-briefs.md**; evidence-map embedding rules: **reference/findings-document-guide.md**.

**Announce**: "Dispatching findings-doc compilation to a sub-agent."

Brief: document strategy (per-area vs. consolidated), investigation results (summaries **with each area's evidence map**). Instructions: load `write-solution-doc` and produce a **current-state document** in **current-state mode** (see `write-solution-doc`'s **reference/current-state-mode.md**), with evidence maps embedded per **reference/findings-document-guide.md**. After collection, review for evidence-map fidelity and cross-area consistency.
