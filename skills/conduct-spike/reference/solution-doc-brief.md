# Solution-Doc Brief

Ready-to-fill structured brief for `compile-solution-doc` → `solution-doc-writer` — loaded on demand when dispatching solution-doc compilation. Fills the **structured brief shape**; shared evidence-map contract: **reference/dispatch-briefs.md** (**Evidence map in every brief**).

**Announce**: "Dispatching solution-doc compilation to a sub-agent."

## 1. Mission
You are the `solution-doc-writer`. Deliver: the spike's target-state solution document — decision-only, mirroring each ADR's chosen option.

## 2. Context
- Spike goal: **[goal]**
- Current-state baseline: **[findings docs]**
- Assumed solutions: **[chosen option from each ADR]**

## 3. Inputs
- **[findings doc path(s)]** — current-state baseline to evolve.
- **[ADR path(s)]** — decisions to mirror.

## 4. Tasks
1. Load `write-solution-doc` and produce a **target-state** document in **baseline-input mode**.
2. Mirror each ADR's chosen option, grouped by area.

## 5. Output contract
- Solution doc: target-state architecture, decision-only, ADR decisions grouped by area (per `write-solution-doc` structure).

## 6. Constraints
- Never include code references — decision-only.
- Never alter an ADR decision.

## 7. Report back
- Flag decisions with no ADR backing, or any ADR ↔ findings inconsistency.
