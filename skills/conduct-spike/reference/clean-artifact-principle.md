# Clean Artifact Principle

ADRs and the solution document are decision documents, not investigation reports. They are also **single-source-of-truth documents maintained at the latest state**: when a decision changes, the document is rewritten in place so it reads as if the current decision was always the decision.

## What belongs in each document

| Document | Contains only |
|---|---|
| ADR | The decision — problem, decision drivers, considered options, chosen option, consequences |
| Solution document | The target-state architecture — business context, C4/sequence diagrams, API contracts, RAID, RACI |

## What never belongs

Investigation logs, raw data dumps, evidence trails, process history, or change notes. The document has **no memory of its own past** — version control (git) is the only history.

## Where supporting detail goes

All such detail belongs in the separate findings document. Cite it with a cross-reference instead of copying it in. If content does not help a reader understand or act on the decision, it does not belong in the ADR or solution document.

## Latest-state rewrite-in-place protocol

When a decision or fact changes (deep-dive, ADR revision, mid-spike correction):

1. **Locate** the affected sections of the ADR / solution doc.
2. **Delete** the superseded text in full — do not keep it around with a marker.
3. **Rewrite** the sections so they state the current decision as the decision — no reference to the previous version, no "now we", no "changed from".
4. **Verify** no version markers or process language remain (run the no-note scan below).
5. Present the updated document; describe the delta **in conversation**, never inside the document.

## Where notes ARE allowed vs. banned

| Artifact | Notes allowed? | Notes go where |
|---|---|---|
| ADR | ❌ No notes, changelogs, or process history | In the findings document, or spoken in conversation |
| Solution document | ❌ No notes, version markers, or change lists | In the findings document, or spoken in conversation |
| Findings documents | ✅ Yes — current-state record may note raw data, metrics, searched-negatives | In the findings document itself |
| Change summary | ✅ Yes — has a Notes section for caveats, assumptions, open questions | In the change summary |
| Conversation | ✅ Yes — the assistant narrates what changed and why | In chat, not in the artifacts |

## No-note scan (validation gate)

Before presenting any ADR or solution document, scan it for banned process language and rewrite in place until none remain:

- "Note:" / "Notes:" (outside a legitimately note-bearing artifact)
- "Updated", "Changed", "Revised" used as in-document markers
- Version markers: "v2", "(v2)", "version 2"
- History references: "As of", "Previously", "we used to", "changed from", "was X, now Y"
- Status parentheticals: "Draft (updated from unresolved)"
- Process narration: "The deep-dive corrections were applied…", "This section was added after review"
- In-document changelog / closing-notes sections
