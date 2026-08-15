# Workflow Procedures

Direct-execution procedures and validation checklists for spike workflow capabilities, loaded on demand when a phase runs without a sub-agent. Dispatch briefs live in **reference/dispatch-briefs.md**; dispatch-vs-direct rules live in **reference/multi-agent-orchestration.md**.

## Investigate per area (investigate-per-area)

### Direct investigation (fallback — no sub-agent available)

Announce: "Investigating area: [area name]". Load the `investigate-code` skill and apply its capabilities — its **spike-integration** scopes the investigation to the area and updates the evidence map per **findings-document-guide.md**. Compile the area summary: **current state**, **constraints & pain points**, **relevant diagrams** (C4/sequence).

## Evaluate solutions per area (evaluate-solutions-per-area)

### Direct evaluation (fallback — no sub-agent available)

Per area: load the `draft-adr` skill and apply its evaluate chain — **define-decision-drivers** → **define-considered-options** → **evaluate-options** — seeded with the area's findings doc (its embedded evidence map); its **evaluate-options** applies **detail-options-tech** whenever findings are available. Record the **assumed solution** — provisional, may change after ADR review.

**Check for findings gaps**: if any option revealed a constraint, risk, or fact not captured in the findings document, update the affected sections and note the correction when presenting the evaluation summary.

Repeat per area. **Spike-specific validation** (generic checks — 2+ options, pros/cons tied to drivers — belong to `draft-adr`'s **compile-adr** checklist): tech details grounded in the evidence map (no invented code); assumed solution follows logically; findings-gap corrections captured. Present a summary table of areas with assumed solutions and corrections.

## Draft area ADRs (draft-area-adrs)

### Direct drafting or revising (fallback — no sub-agent available)

Load `draft-adr` and apply **compile-adr**, seeding with the evaluation results: problem from the area scope, drivers/options/assumed solution, and each option's tech details (already produced via `draft-adr` during evaluation). Run the full chain only if evaluation was skipped or is incomplete.

Revising = same procedure seeded with the existing ADR plus the changed decision; never hand-edit (see **professional-doc-authoring**).

### ADR validation checklist

Apply `draft-adr`'s **compile-adr** checklist. Spike-specific additions: each option's tech details are carried into its evaluation section; the ADR stands alone without reading other ADRs; it cites the findings doc for evidence. Then run the **no-note scan** per **artifact-maintenance-doctrine** (see **reference/artifact-maintenance-guide.md**) and rewrite until none remain.

## Compile findings doc (compile-findings-doc)

### Direct compilation (fallback — no sub-agent available)

Load the `write-solution-doc` skill's SKILL.md and apply its capabilities in **current-state mode** (see `write-solution-doc`'s **reference/current-state-mode.md**). Seed with Phase 2 results (investigation summaries and their evidence maps) rather than gathering context from scratch.

### Evidence-map embedding and validation (both paths)

**Embed each area's evidence map inline** per **reference/findings-document-guide.md**: `file:line` entry points, call chains as sequence diagrams, an **Evidence & Verification** section per area — evidence ledger (claim → verdict → evidence `file:line` → confidence, `investigate-code` 5-tag model) and searched-negatives. Never vague references like "the service layer"; never present inference as evidence. Cross-reference between findings docs (if per-area). Present each doc and ask: "Does this accurately capture the current state? Anything to add, correct, or remove?" Save to `<spike-folder>/docs/findings-<area>.md` per **spike-artifact-layout**. Findings docs are the **current-state baseline and evidence home**; update the evidence map the moment new evidence is found — no round/version tracking.

## Compile solution doc (compile-solution-doc)

### Direct compilation (fallback — no sub-agent available)

Load the `write-solution-doc` skill's SKILL.md and apply its capabilities in **baseline-input mode** (see `write-solution-doc`'s **reference/current-state-mode.md**) — for compiling AND revising. Seed with: business context (spike goal), current-state baseline (findings docs), and assumed solutions (chosen option from each ADR). Revising is the same procedure seeded with the existing doc plus the changed decisions (see **professional-doc-authoring**).

### Validation, presentation (both paths)

Compile the output bundle — findings docs, N ADRs, 1 solution doc — and save per **spike-artifact-layout**: findings → `docs/`, ADRs → `adrs/`, solution doc → `solution.md`. Keep the solution doc at the latest state per **artifact-maintenance-doctrine** (see **reference/artifact-maintenance-guide.md**): only target-state architecture, no process notes; on refresh route through `write-solution-doc` and rewrite affected sections in place — delete superseded text, never annotate. Validate the bundle: every ADR's chosen solution is reflected, cross-references between all artifacts are consistent, diagrams match assumed solutions. Run the **no-note scan** on the solution doc and rewrite until none remain. Present the bundle and remind the user: findings docs are the current-state record (keep even if decisions change); ADRs are formal decision records (review and approve with the team); the solution doc is the target-state architecture; version-control all artifacts together in the spike folder.

## Continue prior spike (continue-prior-spike)

Follow **continue-prior-spike** in SKILL.md. Distinct dispatch detail: seed sub-agents with the area's existing findings doc / evidence map so covered code is not re-scanned; scope strictly to answering the open questions; revise existing ADRs in place.

## Sync update artifacts (sync-update-artifacts)

Follow **sync-update-artifacts** in SKILL.md. Distinct detail: the findings doc carries the evidence map, so its owning-skill update flows through `write-solution-doc` (see **professional-doc-authoring**).
