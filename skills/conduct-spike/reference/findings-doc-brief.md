# Findings-Doc Brief

Ready-to-fill structured brief for `compile-findings-doc` → `solution-doc-writer` — loaded on demand when dispatching findings-doc compilation. Fills the **structured brief shape**; shared evidence-map contract: **reference/dispatch-briefs.md** (**Evidence map in every brief**); embedding rules: **reference/findings-document-guide.md**.

**Announce**: "Dispatching findings-doc compilation to a sub-agent."

## 1. Mission
You are the `solution-doc-writer`. Deliver: the spike's findings document — the current-state baseline with each area's evidence map embedded.

## 2. Context
- Spike goal: **[goal]**
- Document strategy: **per-area** | **consolidated**
- Investigation results: **[summaries, each with its area's evidence map]**

## 3. Inputs
- Investigation results (summaries + evidence maps) — already verified; embed faithfully, do not re-investigate.

## 4. Tasks
1. Load `write-solution-doc` and produce a **current-state document** in **current-state mode** (per `write-solution-doc`'s **reference/current-state-mode.md**).
2. Embed each area's evidence map per **reference/findings-document-guide.md**.

## 5. Output contract
- Findings doc: current-state architecture, per-area sections, evidence maps embedded inline (entry points, `file:line`, call chains, evidence ledger, searched-negatives).

## 6. Constraints
- Never add claims beyond the provided results.
- Never alter a **Verified** verdict or an evidence `file:line`.

## 7. Report back
- Flag evidence-map gaps and cross-area inconsistencies found in the source results.
