# Workflow Procedures

Full step-by-step procedures for spike workflow capabilities, loaded on demand per phase: dispatch briefs, direct-execution steps, validation checklists.

## Investigate per area (investigate-per-area)

### Sub-agent dispatch — per-area brief template

Each brief carries: area name and description, spike goal, brownfield/greenfield, the area's existing findings doc / evidence map (if one exists), and expected output including a per-area evidence map (entry points, key locations with `file:line`, call chains, evidence verdicts, searched-negatives). Dispatch concurrently for multiple areas, individually for a single area. Announce: "Dispatching investigation of [N] area(s) to a sub-agent." After collection, synthesize the results, resolving cross-area inconsistencies for the findings doc.

### Direct investigation (fallback — no sub-agent available)

Announce: "Investigating area: [area name]". Load the `investigate-code` skill and apply its capabilities — its **spike-integration** scopes the investigation to the area and updates the evidence map per **findings-document-guide.md**. Compile the area summary: **current state**, **constraints & pain points**, **relevant diagrams** (C4/sequence).

## Evaluate solutions per area (evaluate-solutions-per-area)

### Sub-agent dispatch — per-area brief template

Each brief carries: area name and description, spike goal, the area's findings doc (evidence sections), and instructions to load `draft-adr` and apply its evaluate chain — **define-decision-drivers** → **define-considered-options** → **evaluate-options** — running the interactive dialog with the user inside the sub-agent session and returning the area's assumed solution. Dispatch concurrently for multiple areas, individually for a single area. Announce: "Dispatching evaluation of [N] area(s) to a sub-agent." After collection, review each assumed solution for fidelity to the findings doc and cross-area consistency; definitive verification lands at the Phase 4 ADR.

### Direct evaluation (fallback — no sub-agent available)

Per area: load the `draft-adr` skill and apply its evaluate chain — **define-decision-drivers** → **define-considered-options** → **evaluate-options** — seeded with the area's findings doc (its embedded evidence map); its **evaluate-options** applies **detail-options-tech** whenever findings are available. Record the **assumed solution** — provisional, may change after ADR review.

**Check for findings gaps**: if any option revealed a constraint, risk, or fact not captured in the findings document, update the affected sections and note the correction when presenting the evaluation summary.

Repeat per area. **Spike-specific validation** (generic checks — 2+ options, pros/cons tied to drivers — belong to `draft-adr`'s **compile-adr** checklist): tech details grounded in the evidence map (no invented code); assumed solution follows logically; findings-gap corrections captured. Present a summary table of areas with assumed solutions and corrections.

## Draft area ADRs (draft-area-adrs)

### Sub-agent dispatch — per-area brief template

Each brief carries: area name and description, evaluation results (decision drivers, options with pros/cons, **tech details per option**, assumed solution), the area's findings doc (evidence sections), and instructions to load `draft-adr` and apply **compile-adr** seeded with the evaluation results. Dispatch concurrently for multiple ADRs, individually for a single ADR. Announce: "Dispatching ADR drafting for [N] area(s) to a sub-agent." After collection, review each ADR.

### Direct drafting or revising (fallback — no sub-agent available)

Load `draft-adr` and apply **compile-adr**, seeding with the evaluation results: problem from the area scope, drivers/options/assumed solution, and each option's tech details (already produced via `draft-adr` during evaluation). Run the full chain only if evaluation was skipped or is incomplete.

Revising = same procedure seeded with the existing ADR plus the changed decision; never hand-edit (see **professional-doc-authoring**).

### ADR validation checklist

Apply `draft-adr`'s **compile-adr** checklist. Spike-specific additions: each option's tech details are carried into its evaluation section; the ADR stands alone without reading other ADRs; it cites the findings doc for evidence. Then run the **no-note scan** per **artifact-maintenance-doctrine** (see **reference/artifact-maintenance-guide.md**) and rewrite until none remain.

## Compile findings doc (compile-findings-doc)

1. Determine document strategy: **per-area** (2+ loosely-coupled areas) or **one consolidated doc** (tightly-coupled or single-area). Ask the user.
2. Dispatch to a sub-agent whenever one is available; fall back to direct compilation only when none exists (see **multi-agent-orchestration.md**).

### Sub-agent dispatch — brief template

Each brief carries: document strategy, Phase 2 results (investigation summaries **and their evidence maps**), and instructions to load `write-solution-doc` and produce a **current-state document** in **current-state mode** (see `write-solution-doc`'s **reference/current-state-mode.md**), with evidence maps embedded per **findings-document-guide.md**. Announce: "Dispatching findings-doc compilation to a sub-agent." After collection, review for evidence-map fidelity and cross-area consistency.

### Direct compilation (fallback — no sub-agent available)

Load the `write-solution-doc` skill's SKILL.md and apply its capabilities in **current-state mode** (see `write-solution-doc`'s **reference/current-state-mode.md**). Seed with Phase 2 results (investigation summaries and their evidence maps) rather than gathering context from scratch.

### Evidence-map embedding and validation (both paths)

**Embed each area's evidence map inline** per **reference/findings-document-guide.md**: `file:line` entry points, call chains as sequence diagrams, an **Evidence & Verification** section per area — evidence ledger (claim → verdict → evidence `file:line` → confidence, `investigate-code` 5-tag model) and searched-negatives. Never vague references like "the service layer"; never present inference as evidence. Cross-reference between findings docs (if per-area). Present each doc and ask: "Does this accurately capture the current state? Anything to add, correct, or remove?" Save to `<spike-folder>/docs/findings-<area>.md` per **spike-artifact-layout**. Findings docs are the **current-state baseline and evidence home**; update the evidence map the moment new evidence is found — no round/version tracking.

## Compile solution doc (compile-solution-doc)

1. Dispatch to a sub-agent whenever one is available; fall back to direct compilation only when none exists (see **multi-agent-orchestration.md**).

### Sub-agent dispatch — brief template

Each brief carries: business context (spike goal), current-state baseline (findings docs), assumed solutions (chosen option from each ADR), and instructions to load `write-solution-doc` and produce a **target-state** document in **baseline-input mode**. Announce: "Dispatching solution-doc compilation to a sub-agent." After collection, review for completeness and consistency with the ADRs.

### Direct compilation (fallback — no sub-agent available)

Load the `write-solution-doc` skill's SKILL.md and apply its capabilities in **baseline-input mode** (see `write-solution-doc`'s **reference/current-state-mode.md**) — for compiling AND revising. Seed with: business context (spike goal), current-state baseline (findings docs), and assumed solutions (chosen option from each ADR). Revising is the same procedure seeded with the existing doc plus the changed decisions (see **professional-doc-authoring**).

### Modularity, validation, presentation (both paths)

2. **Assess size and modularity** per **solution-doc-modularity**: if the doc exceeds ~3000 words, has 5+ major sections, or has independently useful sections, identify candidates for extraction.
3. **Extract independent sections**: for each candidate, create a standalone doc with standalone context and back-reference, replace it in the hub with a 2–4 sentence summary and cross-reference link. Skip extraction for small, single-service solutions.
4. Compile the output bundle — findings docs, N ADRs, 1 solution doc (hub), modular sub-docs (if extracted) — and save per **spike-artifact-layout**: findings → `docs/`, ADRs → `adrs/`, solution doc → `solution.md`.
5. Keep the solution doc at the latest state per **artifact-maintenance-doctrine** (see **reference/artifact-maintenance-guide.md**): only target-state architecture, no process notes; on refresh route through `write-solution-doc` and rewrite affected sections in place — delete superseded text, never annotate.
6. Validate the bundle: every ADR's chosen solution is reflected, cross-references between all artifacts are consistent, diagrams match assumed solutions, extracted sub-docs have correct back-references. Run the **no-note scan** on the solution doc and rewrite until none remain.
7. Present the bundle and remind the user: findings docs are the current-state record (keep even if decisions change); ADRs are formal decision records (review and approve with the team); the solution doc is the target-state architecture; version-control all artifacts together in the spike folder.

## Continue prior spike (continue-prior-spike)

Follow **continue-prior-spike** in SKILL.md. Distinct dispatch detail: seed sub-agents with the area's existing findings doc / evidence map so covered code is not re-scanned; scope strictly to answering the open questions; revise existing ADRs in place.

## Summarize required changes (summarize-required-changes)

Follow **summarize-required-changes** in SKILL.md. Distinct detail: determine code access first — with access, trace code paths and mark estimates code-verified; without access, generate at architectural level and mark estimates unverified.

## Sync update artifacts (sync-update-artifacts)

Follow **sync-update-artifacts** in SKILL.md. Distinct detail: the findings doc carries the evidence map, so its owning-skill update flows through `write-solution-doc` (see **professional-doc-authoring**).
