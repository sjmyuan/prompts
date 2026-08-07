# Artifact Sync Guide

Spike artifacts form a dependency chain. Any change — new evidence, corrected fact, changed decision — must propagate to every downstream artifact so the user always sees one consistent picture. This guide backs the **artifact-sync-doctrine** knowledge entry and the **sync-update-artifacts** capability.

## Dependency chain

```
Findings Docs → ADRs → Solution Doc → Change Summary
```

Each artifact cites the one before it: ADRs cite findings (which embed the evidence map), the solution doc mirrors ADR decisions, and the change summary diffs findings (baseline) against the solution doc (target).

## Propagation matrix

| Change origin | Propagate to | Stopping condition |
|---|---|---|
| Findings doc (new evidence or correction) | ADR → solution doc → change summary | Evidence only confirms existing facts and decisions |
| ADR decision change | Solution doc → change summary | Decision has no target-state or code impact |
| Solution doc change | Change summary | Change has no code impact |

Propagation always stops at the first artifact the change does not affect.

## Sync procedure

1. Capture the change: what changed, which artifact is the origin, and what triggered it.
2. Trace the propagation path; identify every affected downstream artifact.
3. Apply the change at the origin through its owning skill — `draft-adr` for ADRs, `write-solution-doc` for findings/solution docs (the findings doc carries the evidence map). Never hand-edit.
4. Propagate downstream one artifact at a time, seeding each with the current artifact plus the delta.
5. For the change summary, recompute the affected clusters against the updated baseline (findings) and target (solution doc); refresh ADR citations and cross-cutting concerns. If no change summary exists, ask whether one is needed.
6. Validate consistency and present the delta in conversation.

## Consistency checklist (validation gate)

- [ ] Every artifact reflects the latest facts and decisions — nothing references superseded content
- [ ] Findings doc is the only home for evidence; ADRs cite it rather than copying it
- [ ] Solution doc mirrors every ADR's chosen option
- [ ] Change summary traces each cluster to a current ADR and solution-doc section
- [ ] No-note scan passes on every touched ADR and solution doc (see `clean-artifact-principle.md`)

## Common sync traps

- Updating an ADR but leaving the solution doc on the old decision
- Refreshing the solution doc but not the change summary (its target changed)
- Correcting a findings fact that a decision relied on, without revisiting the ADR
- Describing the delta inside the artifacts instead of in conversation
