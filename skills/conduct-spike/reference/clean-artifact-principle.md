# Clean Artifact Principle

ADRs and the solution document are decision documents, not investigation reports. Keep them as clean as possible.

## What belongs in each document

| Document | Contains only |
|---|---|
| ADR | The decision — problem, decision drivers, considered options, chosen option, consequences |
| Solution document | The target-state architecture — business context, C4/sequence diagrams, API contracts, RAID, RACI |

## What never belongs

Investigation logs, raw data dumps, evidence trails, process history, or change notes.

## Where supporting detail goes

All such detail belongs in the separate findings document. Cite it with a cross-reference instead of copying it in. If content does not help a reader understand or act on the decision, it does not belong in the ADR or solution document.
