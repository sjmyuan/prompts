# Findings-Doc Brief

Ready-to-fill structured brief for `compile-findings-doc` → `solution-doc-writer` — loaded on demand when dispatching findings-doc compilation. Fills the **structured brief shape**; shared evidence-map contract: **reference/dispatch-briefs.md** (**Evidence map in every brief**); embedding rules: **reference/findings-document-guide.md**.

**Announce**: "Dispatching findings-doc compilation to a sub-agent."

## 1. Mission
You are the `solution-doc-writer`. Deliver: the findings document for **one investigation area** — that area's current-state baseline with its evidence map embedded. One findings doc per area, always (`docs/findings-<area>.md`).

## 2. Context
- Spike goal: **[goal]**
- Area: **[area name]** — this brief compiles only this area's findings doc
- Investigation results: **[the area's summary + its evidence map]**

## 3. Inputs
- Investigation results (summaries + evidence maps) — already verified; embed faithfully, do not re-investigate.

## 4. Tasks
1. Load `write-solution-doc` and produce a **current-state document** for this area in **current-state mode** (per `write-solution-doc`'s **reference/current-state-mode.md**).
2. Embed the area's evidence map per **reference/findings-document-guide.md**.

## 5. Output contract
- Findings doc: the area's current-state architecture, its evidence map embedded inline (entry points, `file:line`, call chains, evidence ledger, searched-negatives); cross-area constraints noted as cross-references to the other area's findings doc.

## 6. Constraints
- Never add claims beyond the provided results.
- Never alter a **Verified** verdict or an evidence `file:line`.

## 7. Report back
- Flag evidence-map gaps and cross-area inconsistencies found in the source results.
