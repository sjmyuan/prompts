# Artifact Maintenance Guide

Spike artifacts form a dependency chain: **Findings Docs → ADRs → Solution Doc → Change Summary**. Each artifact cites the one before it: ADRs cite findings (which embed the evidence map), the solution doc mirrors ADR decisions, and the change summary diffs findings (baseline) against the solution doc (target).

This guide backs the **artifact-maintenance-doctrine** knowledge entry and the **sync-update-artifacts** capability.

## Latest-state rewrite-in-place protocol

ADRs and the solution document are **single-source-of-truth, kept at the latest state**: they are decision documents, not investigation reports, and have no memory of their own past — version control (git) is the only history.

When a decision or fact changes (ADR revision, continuation round, mid-spike correction):

1. **Locate** the affected sections of the ADR / solution doc.
2. **Delete** the superseded text in full — do not keep it around with a marker.
3. **Rewrite** the sections so they state the current decision as the decision — no reference to the previous version, no "now we", no "changed from".
4. **Verify** no version markers or process language remain (run the no-note scan below).
5. Present the updated document; describe the delta **in conversation**, never inside the document.

### Where notes ARE allowed vs. banned

| Artifact | Notes allowed? | Notes go where |
|---|---|---|
| ADR | ❌ No notes, changelogs, or process history | In the findings document, or spoken in conversation |
| Solution document | ❌ No notes, version markers, or change lists | In the findings document, or spoken in conversation |
| Findings documents | ✅ Yes — current-state record may note raw data, metrics, searched-negatives | In the findings document itself |
| Change summary | ✅ Yes — has a Notes section for caveats, assumptions, open questions | In the change summary |
| Conversation | ✅ Yes — the assistant narrates what changed and why | In chat, not in the artifacts |

### No-note scan (validation gate)

Before presenting any ADR or solution document, scan it for banned process language and rewrite in place until none remain:

- "Note:" / "Notes:" (outside a legitimately note-bearing artifact)
- "Updated", "Changed", "Revised" used as in-document markers
- Version markers: "v2", "(v2)", "version 2"
- History references: "As of", "Previously", "we used to", "changed from", "was X, now Y"
- Status parentheticals: "Draft (updated from unresolved)"
- Process narration: "The corrections were applied…", "This section was added after review"
- In-document changelog / closing-notes sections

## Propagation matrix

| Change origin | Propagate to | Stopping condition |
|---|---|---|
| Findings doc (new evidence or correction) | ADR → solution doc → change summary | Evidence only confirms existing facts and decisions |
| ADR decision change | Solution doc → change summary | Decision has no target-state or code impact |
| Solution doc change | Change summary | Change has no code impact |

Propagation always stops at the first artifact the change does not affect. The change summary is **never final** — recompute it whenever its baseline (findings) or target (solution doc) changes.

## Sync procedure

1. Capture the change: what changed, which artifact is the origin, and what triggered it.
2. Trace the propagation path; identify every affected downstream artifact.
3. Apply the change at the origin through its owning skill — `draft-adr` for ADRs, `write-solution-doc` for findings/solution docs (the findings doc carries the evidence map). Never hand-edit.
4. Run the **no-note scan** on each touched ADR and solution doc; rewrite until clean.
5. Propagate downstream one artifact at a time, seeding each with the current artifact plus the delta.
6. For the change summary, recompute the affected clusters against the updated baseline (findings) and target (solution doc); refresh ADR citations and cross-cutting concerns. If no change summary exists, ask whether one is needed.
7. Validate consistency and present the delta in conversation.

## Consistency checklist (validation gate)

- [ ] Every artifact reflects the latest facts and decisions — nothing references superseded content
- [ ] Findings doc is the only home for evidence; ADRs cite it rather than copying it
- [ ] Solution doc mirrors every ADR's chosen option
- [ ] Change summary traces each cluster to a current ADR and solution-doc section
- [ ] No-note scan passes on every touched ADR and solution doc

## Common sync traps

- Updating an ADR but leaving the solution doc on the old decision
- Refreshing the solution doc but not the change summary (its target changed)
- Correcting a findings fact that a decision relied on, without revisiting the ADR
- Describing the delta inside the artifacts instead of in conversation
