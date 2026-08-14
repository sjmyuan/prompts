# Workflow Procedures

Full step-by-step procedures for the spike workflow capabilities, loaded on demand while executing a phase. Each section corresponds to a capability in SKILL.md and supplies its full dispatch brief templates, direct-execution steps, and validation checklists.

## Investigate per area (investigate-per-area)

### Sub-agent dispatch — per-area brief template

Each brief carries: area name and description, spike goal, brownfield/greenfield designation, the area's existing findings doc / evidence map (if one exists), and the expected output including a per-area evidence map (entry points, key locations with `file:line`, call chains, evidence verdicts, searched-negatives). Dispatch concurrently for multiple areas, individually for a single area. Announce: "Dispatching investigation of [N] area(s) to a sub-agent." After collection, synthesize the results, resolving cross-area inconsistencies for the findings doc.

### Direct investigation (fallback — no sub-agent available)

Announce: "Investigating area: [area name]". Load the `investigate-code` skill's SKILL.md and apply its capabilities — its **spike-integration** scopes the investigation to the area and updates the evidence map per **findings-document-guide.md**. Compile findings into a structured summary: **current state** (what exists today), **constraints & pain points** (what's limiting or broken), and **relevant diagrams** (C4/sequence showing current architecture).

## Evaluate solutions per area (evaluate-solutions-per-area)

### Sub-agent dispatch — per-area brief template

Each brief carries: area name and description, spike goal, the area's findings doc (evidence sections), and instructions to load `draft-adr` and apply its evaluate chain — **define-decision-drivers** → **define-considered-options** → **evaluate-options** — running the interactive dialog with the user inside the sub-agent session and returning the area's assumed solution. Dispatch concurrently for multiple areas, individually for a single area. Announce: "Dispatching evaluation of [N] area(s) to a sub-agent." After collection, review each returned assumed solution for fidelity to the findings doc and cross-area consistency; definitive verification lands with the ADR drafted in Phase 4.

### Direct evaluation (fallback — no sub-agent available)

Per area: load the `draft-adr` skill and apply its evaluate chain — **define-decision-drivers** → **define-considered-options** → **evaluate-options** — seeded with the area's findings doc (its embedded evidence map); its **evaluate-options** applies **detail-options-tech** whenever findings are available. Record the **assumed solution** — provisional, may change after ADR review.

**Check for findings gaps**: if any option revealed a constraint, risk, or fact not captured in the findings document, update the affected sections and note the correction when presenting the evaluation summary.

Repeat for each investigation area. **Spike-specific validation** (generic checks — 2+ options, pros/cons tied to drivers — belong to `draft-adr`'s **compile-adr** checklist): each option's tech details are grounded in the findings doc's evidence map (no invented code); the assumed solution follows logically from the comparison; findings-gap corrections captured. Present a summary table of all areas with their assumed solutions and any findings corrections.

## Draft area ADRs (draft-area-adrs)

### Sub-agent dispatch — per-area brief template

Each brief carries: area name and description, evaluation results (decision drivers, options with pros/cons, **tech details per option**, assumed solution), the area's findings doc (evidence sections), and instructions to load `draft-adr` and apply **compile-adr** seeded with the evaluation results. Dispatch concurrently for multiple ADRs, individually for a single ADR. Announce: "Dispatching ADR drafting for [N] area(s) to a sub-agent." After collection, review each ADR.

### Direct drafting or revising (fallback — no sub-agent available)

Load the `draft-adr` skill's SKILL.md and apply **compile-adr**, seeding it with the evaluation results: problem from the area scope, drivers/options/assumed solution, and each option's tech details (already produced via `draft-adr` during evaluation). Run the full chain (define-problem → define-decision-drivers → define-considered-options → evaluate-options → compile-adr) only if evaluation was skipped or is incomplete.

Revising is the same procedure: re-load `draft-adr` and re-apply **compile-adr**, seeding with the existing ADR plus the changed decision. Never hand-edit an ADR — every write goes through `draft-adr` (see **professional-doc-authoring**).

### ADR validation checklist

Apply `draft-adr`'s **compile-adr** step 6 quality checklist. Spike-specific additions: each option's tech details are carried into its evaluation section; the ADR stands alone without reading other ADRs; it cites the findings doc for evidence. Then run the **no-note scan** from **clean-artifact-principle** — scan for banned process language ("Note:", "Updated", "Changed", "v2", "As of", "Previously", status parentheticals, in-document changelogs) and rewrite in place until none remain.

## Compile findings doc (compile-findings-doc)

1. Determine document strategy: **per-area** (recommended for 2+ loosely-coupled areas) or **one consolidated doc** (tightly-coupled or single-area). Ask the user which they prefer.
2. Choose the execution strategy: dispatch to a sub-agent whenever one is available; fall back to direct compilation only when none exists (see **multi-agent-orchestration.md**).

### Sub-agent dispatch — brief template

Each brief carries: document strategy, Phase 2 results (investigation summaries **and their evidence maps**), and instructions to load `write-solution-doc` and produce a **current-state document** in **current-state mode** (see `write-solution-doc`'s **reference/current-state-mode.md**), with evidence maps embedded per **findings-document-guide.md**. Announce: "Dispatching findings-doc compilation to a sub-agent." After collection, review for evidence-map fidelity and cross-area consistency.

### Direct compilation (fallback — no sub-agent available)

Load the `write-solution-doc` skill's SKILL.md and apply its capabilities in **current-state mode** (see `write-solution-doc`'s **reference/current-state-mode.md**). Seed with Phase 2 results (investigation summaries and their evidence maps) rather than gathering context from scratch.

### Evidence-map embedding and validation (both paths)

**Embed each area's evidence map inline** per **reference/findings-document-guide.md**: annotate entry points and key locations with `file:line` beside the sections that use them, express call chains as sequence diagrams, and add an **Evidence & Verification** section per area — evidence ledger (claim → verdict → evidence `file:line` → confidence per the `investigate-code` 5-tag model) and searched-negatives. Preserve `file:line` precision — never vague references like "the service layer"; never present inference as evidence. Cross-reference between findings docs (if per-area): note where one area's current state creates constraints for another. Present each findings document and ask: "Does this accurately capture the current state? Anything to add, correct, or remove?" Then save it to `<spike-folder>/docs/findings-<area>.md` (apply **save-artifacts**). Findings docs are the **current-state baseline and evidence home**: evaluation compares options against them, ADRs cite them as evidence, sub-agent briefs carry their evidence sections, and the solution doc evolves their diagrams as-is → to-be. Update the embedded evidence map the moment new evidence is found — no round/version tracking.

## Compile solution doc (compile-solution-doc)

1. Choose the execution strategy: dispatch to a sub-agent whenever one is available; fall back to direct compilation only when none exists (see **multi-agent-orchestration.md**).

### Sub-agent dispatch — brief template

Each brief carries: business context (spike goal), current-state baseline (findings docs), assumed solutions (chosen option from each ADR), and instructions to load `write-solution-doc` and produce a **target-state** document in **baseline-input mode** (see `write-solution-doc`'s **reference/current-state-mode.md**). Announce: "Dispatching solution-doc compilation to a sub-agent." After collection, review for completeness and consistency with the ADRs.

### Direct compilation (fallback — no sub-agent available)

Load the `write-solution-doc` skill's SKILL.md and apply its capabilities in **baseline-input mode** (see `write-solution-doc`'s **reference/current-state-mode.md**) — for compiling AND revising. Seed with: business context (spike goal), current-state baseline (findings docs), and assumed solutions (chosen option from each ADR). Revising is the same procedure seeded with the existing doc plus the changed decisions (see **professional-doc-authoring**).

### Modularity, validation, presentation (both paths)

2. **Assess size and modularity** per **solution-doc-modularity**: if the doc exceeds ~3000 words, has 5+ major sections, or has independently useful sections for different audiences, identify candidate sections for extraction.
3. **Extract independent sections**: for each candidate, create a standalone doc with standalone context and back-reference, replace it in the hub with a 2–4 sentence summary and cross-reference link. Skip extraction for small, single-service solutions.
4. Compile the output bundle — findings docs, N ADRs, 1 solution doc (hub), modular sub-docs (if extracted) — and save per **spike-artifact-layout** (apply **save-artifacts**): findings → `docs/`, ADRs → `adrs/`, solution doc → `solution.md`.
5. Keep the solution doc at the latest state per **latest-state-doctrine** (see **reference/clean-artifact-principle.md**): only the target-state architecture, no process notes. On refresh, route through `write-solution-doc` and rewrite affected sections in place — delete superseded text, never annotate; cross-reference the findings document.
6. Validate the bundle: every ADR's chosen solution is reflected, cross-references between all artifacts are consistent, diagrams match assumed solutions, extracted sub-docs have correct back-references. Run the **no-note scan** on the solution doc and rewrite until none remain.
7. Present the bundle and remind the user: findings docs are the current-state record (keep even if decisions change); ADRs are formal decision records (review and approve with the team); the solution doc is the target-state architecture; version-control all artifacts together in the spike folder.

## Summarize required changes (summarize-required-changes)

1. Confirm prerequisites: findings docs and solution doc finalized. Ask: "Would you like me to generate a summary of the concrete code changes required to implement this solution?" Optional — do not produce unless requested.
2. Determine code access: ask "Can I access the current codebase to verify the scope of changes?" **With code access**: trace the code paths from the findings doc's key locations and call chains, estimate scope concretely (file counts, LOC ranges, classes to modify), mark as code-verified. **Without code access**: generate at architectural level, mark estimates as unverified approximations, note where code access would improve accuracy.
3. For each area/ADR, map the delta from current state to target state using the categories in **change-summary-guide** (New, Modified, Retired, Configuration, Data, Dependency, Test).
4. Group changes by area/service, labeling each cluster with its ADR reference for traceability. Identify cross-cutting concerns that span multiple areas (shared library changes, auth integration, logging standards).
5. Compile the change summary following **change-summary-guide**; include a notes section for caveats, assumptions, and open questions. Save to `<spike-folder>/change-summary.md` (apply **save-artifacts**).
6. Present and ask: "Does this change scope look accurate? Anything missing, overestimated, or underestimated?"
7. The change summary is a planning aid tracing back to ADR decisions and solution doc sections — **never final**; if findings or the solution doc change, apply **sync-update-artifacts** to refresh it. For sprint planning, use it as input, not the final word.

## Sync update artifacts (sync-update-artifacts)

1. Identify the change and its origin artifact: new evidence or corrected fact (findings doc), changed decision (ADR), or target-state change (solution doc).
2. Trace the propagation path with **artifact-sync-doctrine** to determine which downstream artifacts the change affects.
3. Apply the change to the origin artifact through its owning skill — `draft-adr` for ADRs, `write-solution-doc` for findings/solution docs (the findings doc carries the evidence map — see **professional-doc-authoring**).
4. Propagate to each affected downstream artifact in order, re-running the owning capability seeded with the current artifact plus the delta. For the change summary, recompute the affected clusters against the updated baseline and target, and refresh cross-cutting concerns.
5. Validate consistency: every artifact reflects the latest facts and decisions; ADRs cite only current findings; the solution doc mirrors every ADR; the change summary traces to current ADRs. Run the **no-note scan** on each touched ADR and solution doc.
6. Present the delta in conversation — what changed in each artifact and how they now agree; never inside the artifacts (see **latest-state-doctrine**).
