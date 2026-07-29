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

Findings documents are produced by the `write-solution-doc` skill, applied to the **current state** instead of the target state. Load that skill to access its full document structure, diagramming, and formatting capabilities. The key difference: label all diagrams as "current state," replace RAID/RACI sections with **constraints & pain points** and **raw data & metrics** from the investigation findings, and append a **Discovery Log** section at the end — see **reference/discovery-log-guide.md** for the full format and usage.

The Discovery Log records facts, corrections, and insights discovered during investigation or evaluation, along with their evidence. It creates an audit trail from initial assumptions to final conclusions. Every correction to the findings document (whether from investigation, evaluation, deep-dive, or user review) must be recorded in the Discovery Log.

## Relationship to other artifacts

- **ADRs** reference findings docs for evidence: "The current C2 topology (Findings Doc §2) shows all payment types sharing a single database..."
- **The solution document** is produced by loading the findings doc(s), then evolving each section from current-state → target-state using `write-solution-doc`. Diagrams are updated in-place; new API contracts are added; RAID replaces constraints & pain points.
- When findings change (e.g., after a deep-dive), update the affected findings doc and any ADRs that reference it.
