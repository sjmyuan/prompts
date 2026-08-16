# Artifact Maintenance Guide

Spike artifacts form a dependency chain: **Findings Docs → ADRs → Solution Doc**. Each artifact cites the one before it: ADRs cite findings (which embed the evidence map), and the solution doc mirrors ADR decisions.

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
| Findings doc (new evidence or correction) | ADR → solution doc | Evidence only confirms existing facts and decisions |
| ADR decision change | Solution doc | Decision has no target-state impact |

Propagation always stops at the first artifact the change does not affect.

## Sync procedure

1. Capture the change: what changed, which artifact is the origin (findings doc / ADR / scope map / solution doc), and what triggered it. A changed decision reopens its problem to `deciding` in `scope.md` per the scope-map status.
2. Trace the propagation path per the **Propagation matrix** — per area: findings → that area's ADRs → the solution doc's area section; a scope-map delta (add/adjust area or problem) propagates to the affected ADR(s) and solution sections.
3. Apply the change at the origin through its owning skill — `draft-adr` for ADRs, `write-solution-doc` for findings/solution docs (the findings doc carries the evidence map). Never hand-edit.
4. Run the **no-note scan** on each touched ADR and solution doc; rewrite until clean.
5. Propagate downstream one artifact at a time, seeding each with the current artifact plus the delta.
6. Validate consistency — every artifact reflects the latest facts; ADRs cite only current findings; the solution doc mirrors every ADR grouped by area — and present the delta in conversation, never inside the artifacts.

## Consistency checklist (validation gate)

- [ ] Every artifact reflects the latest facts and decisions — nothing references superseded content
- [ ] Findings doc is the only home for evidence; ADRs cite it rather than copying it
- [ ] Solution doc mirrors every ADR's chosen option
- [ ] No-note scan passes on every touched ADR and solution doc

## Common sync traps

- Updating an ADR but leaving the solution doc on the old decision
- Correcting a findings fact that a decision relied on, without revisiting the ADR
- Describing the delta inside the artifacts instead of in conversation
