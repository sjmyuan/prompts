# Workflow Procedures

Direct-execution procedures and validation checklists for spike workflow capabilities, loaded on demand when a phase runs without a sub-agent. Dispatch briefs live in **reference/dispatch-briefs.md**; dispatch-vs-direct rules live in **reference/multi-agent-orchestration.md**.

## Investigate per area (investigate-per-area)

### Direct investigation (fallback — no sub-agent available)

Announce: "Investigating area: [area name]". Load the `investigate-code` skill and apply its capabilities — its **spike-integration** scopes the investigation to the area and updates the evidence map per **findings-document-guide.md**. Compile the area summary: **current state**, **constraints & pain points**, **relevant diagrams** (C4/sequence).

## Evaluate problem solutions (evaluate-problem-solutions)

### Direct evaluation (fallback — no sub-agent available)

Per problem (batch a whole area's problems in one pass when they share its evidence): load the `draft-adr` skill and apply its evaluate chain — **define-decision-drivers** → **define-considered-options** → **evaluate-options** — seeded with the area's findings doc (its embedded evidence map); its **evaluate-options** applies **detail-options-tech** whenever findings are available. Record the **assumed solution** — provisional, may change after ADR review.

**Check for findings gaps**: if any option revealed a constraint, risk, or fact not captured in the findings document, update the affected sections and note the correction when presenting the evaluation summary.

Repeat per problem within each area. **Spike-specific validation** (generic checks — 2+ options, pros/cons tied to drivers — belong to `draft-adr`'s **compile-adr** checklist): tech details grounded in the evidence map (no invented code); assumed solution follows logically; findings-gap corrections captured. Present a summary table of areas → problems with assumed solutions and corrections.

## Continue prior spike (continue-prior-spike)

Follow **continue-prior-spike** in SKILL.md. Distinct dispatch detail: confirm the scope map (`scope.md`) and apply the confirmed deltas first; seed sub-agents with the area's existing findings doc / evidence map so covered code is not re-scanned; scope strictly to answering the open problems; revise existing ADRs in place.


