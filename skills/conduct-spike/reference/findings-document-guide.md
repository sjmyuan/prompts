# Findings Document Guide

A findings document documents the **current-state architecture** — what exists in the code today. It uses the same format as a solution document (C4 diagrams, sequence diagrams, API/event contracts, dependency maps) but describes the as-is rather than the to-be. This makes findings documents directly transformable into the solution document during Phase 5.

## Why the solution-doc format?

Most of the time, the current implementation *is* a solution — just the existing one. Documenting it in solution-doc format means:

- The solution document (Phase 5) can start from the findings doc and evolve diagrams from as-is → to-be, rather than drawing from scratch.
- ADRs have a precise, structured baseline to compare options against: "The current architecture (see Findings Doc §3, C2 diagram) couples payment types via shared tables..."
- Reviewers can diff the findings doc against the solution doc to see exactly what changes are proposed.

## One per area or one consolidated?

Either approach is valid:

- **Per-area findings docs** (recommended for multi-area spikes): Each investigation area gets its own findings document. This keeps each doc focused and independently updatable. Best when areas are loosely coupled.
- **One consolidated findings doc**: All areas in a single document with per-area sections and cross-area observations. Best when areas are tightly coupled and cross-cutting concerns are significant.

## Document format

Findings documents are produced by the `write-solution-doc` skill in **current-state mode** — same structure, diagramming, and formatting as a solution doc, applied to the **current state** instead of the target state. Load `write-solution-doc`'s **reference/current-state-mode.md** for the full adaptation rules.

## Embedded evidence map (the spike's code evidence)

The findings doc is the spike's **evidence home** — the single place where code evidence lives. Each area's evidence map is embedded inline, close to the code it describes:

- **Entry points & key locations**: annotate the current-state sections and diagrams with `file:line` beside the component or flow they describe. Preserve `file:line` precision — never vague references like "the service layer".
- **Call chains**: the findings doc's sequence diagrams express call chains; annotate each step with `file:line`.
- **Evidence & Verification section** (per area): an evidence ledger table and a searched-negatives table.

**Evidence ledger**

| Claim / Question | Verdict | Evidence (file:line) | Confidence |

Claims are the spike's questions ("Is there a circuit breaker?"); the verdict is the answer; evidence is the exact location. Confidence uses the `investigate-code` 5-tag model: **Verified** (directly read, `file:line` confirmed), **Inferred** (reasoned from evidence), **Assumption** (taken for granted), **Inconsistency** (contradiction — code vs code, docs, or config, both sides located), **Gap** (searched but not found, or not investigated). Never present inference as evidence — Inferred/Assumption claims are not Verified; Gap claims also go in searched-negatives.

**Searched-negatives**

| Area | Search performed (pattern/query) | Result | Next step |

Dead-end searches recorded so later sub-agents don't repeat them; open questions still to investigate.

**Maintenance**: update the embedded evidence map the moment new evidence is found during any later work (deep-dive, follow-ups) — no round/version tracking, never rebuilt from scratch. Pass the findings doc (or its evidence sections) to sub-agents so covered code is not re-scanned.

## Relationship to other artifacts

- **ADRs** reference findings docs for evidence: "The current C2 topology (Findings Doc §2) shows all payment types sharing a single database..."
- **The solution document** is produced by loading the findings doc(s) and applying `write-solution-doc` in **baseline-input mode** — evolving each section as-is → to-be (see `write-solution-doc`'s **reference/current-state-mode.md**).
- When findings change (e.g., after a deep-dive), update the affected findings doc and any ADRs that reference it.
- **ADRs and the solution document stay clean**: investigation detail and raw data live only in this findings document. ADRs and the solution doc carry the decision and the target-state architecture, citing the findings doc for evidence rather than embedding it.
