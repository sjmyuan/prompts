# Investigation Brief

Per-phase dispatch brief for `investigate-per-area` → `code-investigator` — loaded on demand when dispatching an area's investigation so the other phases' briefs are never pulled in. Shared evidence-map input/output contract: **reference/dispatch-briefs.md** (see **Evidence map in every brief**).

**Announce**: "Dispatching investigation of [N] area(s) to a sub-agent."

Brief per area: area name + description, spike goal, brownfield/greenfield. Carry the area's existing findings doc / evidence map when one exists; require a per-area evidence map back (see **Evidence map in every brief**). After collection, synthesize, resolving cross-area inconsistencies for the findings doc.
