---
name: conduct-spike
description: Conduct spike investigations producing ADRs, findings, solution docs, and change summaries. Use when scoping, investigating, evaluating, discussing ADRs needing investigation, formalizing, continuing, deep-diving, modularizing, summarizing changes, syncing updates, suggesting direction.
---

<when-to-use-this-skill>
- User wants to conduct a spike investigation on a technical problem or feature — researching, evaluating, and comparing solution approaches before committing to one
- User wants to produce ADRs for each decision area alongside a consolidated solution document
- User is discussing an ADR (drafting, reviewing, or adjusting a decision) and the outcome depends on unverified assumptions, unknown feasibility, or missing evidence that needs investigation
- User needs to understand current implementation before proposing changes or solutions
- User wants to break down a large technical problem into independently decidable investigation areas, or split a large solution document into modular sub-documents
- User has pre-existing investigation findings and wants to formalize them into ADRs and a solution document
- User wants to continue a previous spike by digging deeper into one or more specific investigation areas that were not fully resolved
- User wants to summarize the concrete code changes required to implement the chosen solution (change summary) or get suggestions for the next steps in the spike (direction candidates)
- User found new evidence or changed a decision and wants every artifact — findings doc, ADR, solution doc, change summary — updated together and kept consistent
- Do NOT load for plain ADR drafting, solution-doc writing, or code investigation — `draft-adr`, `write-solution-doc`, and `investigate-code` handle those directly; load only when a decision needs investigation first
</when-to-use-this-skill>

<knowledge>

<spike-definition>
A spike reduces uncertainty around a technical problem through research and prototyping; its output is documented decisions, not production code. It produces: **Findings Documents** (current-state baseline, each embedding its area's evidence map — `file:line` entry points, call chains, evidence ledger, searched-negatives), **N ADRs** (one per area: evaluated options, recommendation, per-option code changes), **1 Solution Document** (target-state architecture with C4, API contracts, RAID, RACI — decision-only), and optionally **1 Change Summary** (code-level changes traceable to ADRs).
</spike-definition>

<spike-artifact-layout>
All spike artifacts are versioned together in **one folder per spike**:

```
spikes/<spike-name>/
├── adrs/                     # one file per ADR — ADR-001-<kebab-name>.md, …
├── solution.md               # the solution document (hub)
├── change-summary.md         # only when requested
└── docs/                     # findings documents — findings-<area>.md each
```

Modularized solution sub-docs (see **solution-doc-modularity**) live in `solution-doc/` next to the hub. Artifacts cross-reference each other with relative paths inside the spike folder.
</spike-artifact-layout>

<inappropriate-scenarios>
Do NOT use this skill for: quick answers without formal documentation, already-decided problems needing only implementation, trivial scope with no architectural impact, or immediate prototyping — spikes produce decisions, not production code.
</inappropriate-scenarios>

<findings-document>
A findings document captures the **current-state architecture** using the `write-solution-doc` skill's format (C4, sequence, API/event contracts) but as-is rather than to-be, making it directly transformable into the solution doc and giving ADRs a precise baseline. It is also the spike's **evidence home**: each findings doc embeds its area's evidence map — `file:line` entry points and key locations annotated inline, sequence diagrams for call chains, an evidence ledger (claim → verdict → confidence), and searched-negatives. ADRs, change summaries, and dispatched sub-agents cite findings docs for code evidence without re-scanning. See **reference/findings-document-guide.md**.
</findings-document>

<change-summary>
A change summary translates the delta between findings (current state) and solution doc (target state) into concrete change items grouped by category — New, Modified, Retired, Configuration, Data, Dependency, Test — traceable to ADRs. Estimate quality depends on code access; always be transparent about which mode applies. For full format and guidance, see **reference/change-summary-guide.md**. It is consumed by **orchestrate-feature-delivery** to split the spiked work into features/phases and orchestrate delivery.
</change-summary>

<option-tech-details>
Tech details (target-state diagrams + code change profiles) per ADR option are produced by the `draft-adr` skill's **detail-options-tech** capability, grounded in this spike's findings doc (its embedded evidence map). During evaluation and ADR drafting, delegate to `draft-adr` rather than producing them directly (see **professional-doc-authoring**).
</option-tech-details>

<solution-doc-modularity>
When a solution document exceeds ~3000 words or 5+ major sections, split independently understandable sections into standalone reference documents. The main doc becomes a hub with 2–4 sentence summaries and cross-references; each extracted doc must stand alone and back-reference the hub. See **reference/solution-doc-modularity-guide.md** for full heuristics and validation checklist.
</solution-doc-modularity>

<deep-dive-mode>
When drilling deeper into specific unresolved areas from a previous spike, the skill operates in **deep-dive mode**; areas not selected are left as-is. See **reference/deep-dive-mode-guide.md** for full mode comparison.
</deep-dive-mode>

<greenfield-scenarios>
When there is no existing implementation (greenfield): research industry approaches and similar systems, study operational constraints (cloud, team, compliance), build proof-of-concept prototypes instead of tracing code. Remaining phases proceed unchanged.
</greenfield-scenarios>

<multi-agent-orchestration>
Sub-agent dispatch for investigation (Phase 2), findings-doc compilation (Phase 2b), ADR drafting (Phase 4), and solution-doc compilation (Phase 5) — including single-task spikes — keeps the orchestrating agent's context small; parallel speed is a secondary benefit. Every artifact write dispatches when a sub-agent is available; direct execution is only the fallback. Dispatch pattern and fallback rules: **reference/multi-agent-orchestration.md**.
</multi-agent-orchestration>

<sub-agent-verification>
Sub-agent results — investigation findings (Phase 2), ADR decisions (Phase 4), and dispatched findings/solution-doc compilations (Phases 2b, 5) — are questioned and verified before acceptance into artifacts. The original sub-agent instance is never reused — every verifier and re-investigator is a NEW sub-agent of the same type. Compilations synthesize already-verified material, so verification focuses on fidelity to that material.
</sub-agent-verification>

<verification-principles>
Independence (verify with a NEW same-type sub-agent, never the original instance), primary sources (answer from code, docs, data, or logs, not by re-stating the result), and traceability (every verdict maps to one challenge; never verify wholesale). Full rules: **reference/verification-protocol.md**.
</verification-principles>

<loop-control>
The verification loop caps at 3 rounds. Comparison and escalation rules: **reference/verification-protocol.md**.
</loop-control>

<problem-decomposition-guide>
When breaking down a spike problem into investigation areas, target 2–5 areas. Fewer than 2 means the problem may not need a spike; more than 5 suggests the scope may be too broad. For the full rubric with heuristics and edge cases, see **reference/decomposition-rubric.md**.
</problem-decomposition-guide>

<solution-brainstorming-prompts>
When helping the user brainstorm solution options, prompt them to consider: status quo, incremental improvement, industry-standard approaches, build-vs-buy-vs-adopt, greenfield rewrite, and hybrid/phased strategies. See the full prompt set in **reference/solution-brainstorming-prompts.md**.
</solution-brainstorming-prompts>

<spike-direction-suggestions>
After each spike round, suggest 3 go-deeper and 3 go-broader candidate questions grounded in investigation evidence — never guesswork. For candidate-generation heuristics, go-deeper vs. go-broader patterns, and output format, see **reference/spike-direction-suggestions-guide.md**.
</spike-direction-suggestions>

<adr-uncertainty-signals>
During ADR discussion (drafting, reviewing, or adjusting a decision), suggest a spike when the decision hinges on something reasoning alone cannot settle:
- **Unverified assumption**: the chosen option assumes a fact no one has checked
- **Unknown feasibility**: whether the option can work in this codebase or organization is unknown
- **Missing measurement**: the decision depends on cost, latency, capacity, or effort data not yet collected
- **Undecidable comparison**: two options stay close and the tiebreaker requires evidence, not opinion
- **Uninvestigated dependency**: success depends on a system whose behavior is unknown
- **Reviewer disagreement**: reviewers can't converge and need data rather than debate

This is the "Untested assumption in ADR" go-deeper heuristic from **reference/spike-direction-suggestions-guide.md**, applied during ADR discussion rather than only after an investigation round.
</adr-uncertainty-signals>

<professional-doc-authoring>
ADRs and the solution document are always written by their owning skills — never hand-edited. Every ADR write (draft, revise, in-place rewrite, deep-dive update) goes through the `draft-adr` skill; every solution-doc write (compile, refresh, in-place rewrite, modular split) goes through the `write-solution-doc` skill. Findings docs also go through `write-solution-doc` (current-state adaptation). Load the owning skill's SKILL.md and apply its capabilities, seeding with the existing document plus the change — inside the spike workflow or in a standalone ADR/solution-doc session. Bypassing the owning skill degrades the artifact.
</professional-doc-authoring>

<latest-state-doctrine>
ADRs and the solution document are **single-source-of-truth documents maintained at the latest state**: rewrite changed sections **in place** so they read as if the current decision was always the decision; superseded content is **deleted**, not marked; git is the document's only history.

This permits **no** "Note:", "Updated", "Changed", "v2", "As of", "Previously" language and no in-document changelogs. Where notes are legitimately allowed (change summary, findings docs, conversation), see **reference/clean-artifact-principle.md** — which defines the rewrite-in-place procedure and the **no-note scan** gate.
</latest-state-doctrine>

<artifact-sync-doctrine>
Artifacts form a dependency chain — a change must propagate to every downstream artifact so the user always sees one consistent picture: **Findings Docs → ADRs → Solution Doc → Change Summary**.

| Change origin | Propagate to |
|---|---|
| Findings doc (new evidence or correction) | ADR → solution doc → change summary |
| ADR decision change | Solution doc → change summary |
| Solution doc change | Change summary |

Propagation stops at the first artifact a change does not affect. The change summary is **never final** — recompute it whenever its baseline or target changes. See **reference/artifact-sync-guide.md**.
</artifact-sync-doctrine>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Conducting a full end-to-end spike from scope to solution doc | 5-phase walkthrough for a real-world migration problem | [examples/end-to-end-spike.md](examples/end-to-end-spike.md) |
| Conducting a single-area spike with narrow scope | Single-area workflow with one ADR + solution doc | [examples/single-area-spike.md](examples/single-area-spike.md) |
| Working from pre-existing investigation findings without re-investigating | Workflow starting from existing investigation results | [examples/from-existing-findings.md](examples/from-existing-findings.md) |
| Decomposing a complex problem into investigation areas | Decomposition rubric with examples and edge cases | [reference/decomposition-rubric.md](reference/decomposition-rubric.md) |
| Conducting a heavy multi-area spike that benefits from parallel sub-agent execution | Multi-area parallel dispatch walkthrough with per-area evidence maps embedded in the findings doc | [examples/multi-agent-investigation.md](examples/multi-agent-investigation.md) |
| Continuing a previous spike by digging deeper into specific unresolved areas | Deep-dive walkthrough: load context, focus investigation, update ADRs | [examples/deep-dive-continuation.md](examples/deep-dive-continuation.md) |
| Dispatching investigation, findings-doc, ADR, or solution-doc work to sub-agents (single or multiple tasks) | Dispatch pattern, context-preservation rationale, and fallback rules | [reference/multi-agent-orchestration.md](reference/multi-agent-orchestration.md) |
| Executing a workflow phase (investigate, evaluate, draft ADRs, compile findings/solution doc, summarize changes, sync artifacts) | Full phase procedures — dispatch brief templates, direct-execution steps, validation checklists | [reference/workflow-procedure.md](reference/workflow-procedure.md) |
| Raising challenges on a sub-agent's returned result | Skeptic questioning dimensions and concrete questions per dimension | `question-everything`: [reference/questioning-dimensions.md](../question-everything/reference/questioning-dimensions.md) |
| Verifying challenges on a sub-agent's returned result before acceptance | Verification brief template, dispatch rules, comparison and loop-control rules | [reference/verification-protocol.md](reference/verification-protocol.md) |
| Seeing a worked verification loop — accept vs. contradict → new round | End-to-end examples of the question → verify → accept/re-investigate loop | [examples/confirming-result.md](examples/confirming-result.md), [examples/contradicting-result.md](examples/contradicting-result.md) |
| Brainstorming solution options during the evaluate phase | Solution-brainstorming prompt set | [reference/solution-brainstorming-prompts.md](reference/solution-brainstorming-prompts.md) |
| Producing or understanding findings documents (format, per-area vs consolidated strategy, embedded evidence map — `file:line` annotations, evidence ledger, searched-negatives) | Findings doc format, strategy selection, and evidence-map embedding rules | [reference/findings-document-guide.md](reference/findings-document-guide.md) |
| Drafting, revising, or compiling ADRs and the solution doc — keeping them at the latest state, free of logs and process language | Latest-state rewrite-in-place protocol, allowed vs banned notes map, and the no-note scan checklist | [reference/clean-artifact-principle.md](reference/clean-artifact-principle.md) |
| Entering or executing deep-dive mode (continuing a previous spike on unresolved areas) | Mode comparison guide and deep-dive procedure | [reference/deep-dive-mode-guide.md](reference/deep-dive-mode-guide.md), [reference/deep-dive-procedure.md](reference/deep-dive-procedure.md) |
| Generating a change summary (code-level changes required to implement the solution) | Format, categories, and code-access guidance | [reference/change-summary-guide.md](reference/change-summary-guide.md) |
| Assessing and splitting a large solution document into modular, AI-friendly pieces | Splitting heuristics, patterns, and validation checklist | [reference/solution-doc-modularity-guide.md](reference/solution-doc-modularity-guide.md) |
| Producing a concrete change summary with code access, demonstrating all change categories | End-to-end change summary with code-verified scope estimates | [examples/change-summary-example.md](examples/change-summary-example.md) |
| Suggesting candidate questions to narrow or broaden a spike after a round completes | Candidate-generation heuristics, go-deeper vs go-broader patterns, and the direction-menu template | [reference/spike-direction-suggestions-guide.md](reference/spike-direction-suggestions-guide.md) |
| Seeing a worked example of direction suggestions — 3 go-deeper and 3 go-broader candidates grounded in investigation evidence | Walkthrough of generating direction candidates after a spike round, with rationale for each | [examples/spike-direction-suggestions.md](examples/spike-direction-suggestions.md) |
| Revising an existing ADR or solution doc after a deep-dive or decision change — seeing how rewrite-in-place replaces the old decision cleanly | Before → after walkthrough of an ADR rewritten in place, with the banned-language absent list | [examples/update-artifact-in-place.md](examples/update-artifact-in-place.md) |
| Suggesting a spike when ADR discussion reveals a decision hinges on unverified assumptions or unknown facts | Worked example of detecting ADR uncertainty and offering a focused spike before finalizing the ADR | [examples/adr-uncertainty-spike-suggestion.md](examples/adr-uncertainty-spike-suggestion.md) |
| Synchronizing artifacts after a fact or decision change (new evidence, ADR revision, deep-dive) | Propagation matrix, sync procedure, and consistency checklist | [reference/artifact-sync-guide.md](reference/artifact-sync-guide.md) |
| Seeing a decision change propagated through ADR, solution doc, and change summary together | Walkthrough of syncing all artifacts after new evidence flips an ADR decision | [examples/sync-update-across-artifacts.md](examples/sync-update-across-artifacts.md) |
| Placing produced artifacts into the per-spike folder (`adrs/`, `solution.md`, `change-summary.md`, `docs/`) | Worked example of the spike folder layout with every artifact placed | [examples/spike-artifact-layout.md](examples/spike-artifact-layout.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<run-spike-workflow>
1. Apply **define-spike-scope** to establish the spike goal and decompose the problem into investigation areas. Do not proceed until the scope is confirmed.
2. Apply **investigate-per-area**, dispatching to a sub-agent whenever one is available (even single-area — see **multi-agent-orchestration**); always record **evidence maps**, never narrative only; verify results with **verify-sub-agent-results** before proceeding; then offer direction suggestions (3 go-deeper, 3 go-broader). A selected direction loops back to step 1 as the new goal; a confirmed-complete investigation proceeds to step 3.
3. Apply **compile-findings-doc** to formalize the results into a structured findings document embedding each area's evidence map inline — dispatching to a sub-agent whenever one is available.
4. After findings are confirmed, apply **evaluate-solutions-per-area** to brainstorm, compare, and select an assumed solution per area.
5. Apply **draft-area-adrs** to produce one formal ADR per area, verifying each with **verify-sub-agent-results** before it is saved.
6. Apply **compile-solution-doc** to consolidate the ADRs into a system-level solution document — dispatching to a sub-agent whenever one is available.
7. Pause for user confirmation after each phase; do not skip phases unless the user requests it or an override rule applies.
</run-spike-workflow>

<define-spike-scope>
1. Ask: "What technical problem or feature do you want to spike? Describe it in 2–4 sentences." Then clarify the goal: what question(s) should this spike answer, what uncertainty should it reduce?
2. Decompose into **investigation areas** using **problem-decomposition-guide**: propose an initial breakdown, write a one-sentence description per area, and ask whether any area should be split, merged, added, or removed.
3. Confirm the final ordered list and record the scope summary: spike goal (1 sentence) and investigation areas (ordered list with one-line descriptions).
4. Validate: each area is independently decidable, the count is 2–5 (or justified outside that range), and the goal is clear enough to know when the spike is complete. If greenfield, note it — the investigate phase adapts (see **greenfield-scenarios**).
</define-spike-scope>

<investigate-per-area>
1. Choose the execution strategy: dispatch to a code-exploration sub-agent whenever one is available — even for a single area (step 2); fall back to direct investigation only when none exists (step 3). See **multi-agent-orchestration**.
2. **Sub-agent dispatch (preferred)**: announce "Dispatching investigation of [N] area(s) to a sub-agent," prepare per-area briefs (area, spike goal, brownfield/greenfield, the area's existing findings doc / evidence map, expected output including a per-area evidence map), dispatch concurrently for multiple areas, then collect and synthesize — resolving cross-area inconsistencies. Full brief template: **reference/workflow-procedure.md**.
3. **Direct investigation (fallback)**: load the `investigate-code` skill and apply its capabilities; record the area's evidence map as you investigate (entry points, `file:line` key locations, call chains, evidence verdicts, searched-negatives); compile current state, constraints & pain points, and relevant diagrams. See **reference/findings-document-guide.md**.
4. Apply **verify-sub-agent-results** to question and re-verify the collected results, then present a consolidated investigation summary, flagging facts that contradict or refine prior assumptions.
5. Apply **suggest-spike-directions** (3 go-deeper, 3 go-broader candidates grounded in the evidence), then ask: "Would you like to pursue any of these directions, or is the investigation complete?" A selected direction loops back to scope definition; confirmation proceeds to step 6.
6. Hand off to **compile-findings-doc**, which embeds the recorded evidence maps inline.
</investigate-per-area>

<evaluate-solutions-per-area>
1. Per area, guide solution evaluation: ask what options the user sees, use **solution-brainstorming-prompts** if only one is offered, capture each option's description/pros/cons/feasibility, identify decision drivers, and relate pros/cons to them.
2. Per option, load the `draft-adr` skill and apply its **detail-options-tech** to produce the option's tech details (target-state diagrams + code change profile), seeding it with the area's findings doc. Present per option for feasibility comparison; skip only if the user declines or the option has no code impact.
3. Ask: "Which option do you recommend as the assumed solution for [area name]?" If unsure, compare top contenders against drivers and tech details. Record the **assumed solution** — provisional until ADR review.
4. **Check for findings gaps**: if any option revealed a constraint, risk, or fact not captured in the findings doc, update the affected sections and note the correction.
5. Repeat per area, then validate each evaluation — at least 2 options, pros/cons relate to drivers, tech details grounded in the evidence map (no invented code), assumed solution follows logically. Present a summary table of all areas with assumed solutions and any findings corrections.
</evaluate-solutions-per-area>

<draft-area-adrs>
1. Choose the execution strategy: dispatch to a sub-agent whenever one is available — even for a single ADR (step 2); fall back to direct drafting only when none exists (step 3). See **multi-agent-orchestration**.
2. **Sub-agent dispatch (preferred)**: announce "Dispatching ADR drafting for [N] area(s) to a sub-agent," prepare per-area briefs (area, evaluation results — drivers, options with pros/cons, tech details per option, assumed solution, the area's findings doc evidence sections — plus instructions to load `draft-adr`), dispatch concurrently, then collect and review each ADR. Full brief template: **reference/workflow-procedure.md**.
3. **Direct drafting or revising (fallback)**: load the `draft-adr` skill and apply its capabilities (define-problem → define-decision-drivers → define-considered-options → evaluate-options → compile-adr), seeding each with the evaluation results including each option's tech details. Revising is the same procedure seeded with the existing ADR plus the change; never hand-edit (see **professional-doc-authoring**).
4. Apply **verify-sub-agent-results** to verify each ADR, save each to `<spike-folder>/adrs/ADR-00X-<kebab-name>.md` (apply **save-artifacts**), present as a set, and ask: "Would you like to adjust any ADR before compiling the solution document?" On ADR uncertainty, apply **suggest-spike-on-adr-uncertainty** first.
5. Keep each ADR at the latest state per **latest-state-doctrine** (see **reference/clean-artifact-principle.md**): only the decision, no process notes; on revision route through `draft-adr` and rewrite affected sections in place — delete superseded text, never annotate; cite the findings doc for evidence.
6. Validate each ADR — decision follows from the drivers, options fairly represented with tech details carried in, consequences balanced, standalone-readable — then run the **no-note scan** (banned language: "Note:", "Updated", "Changed", "v2", "As of", "Previously") and rewrite until none remain.
7. Note: the chosen option is the **assumed solution**; if an ADR decision changes later, apply **sync-update-artifacts**.
</draft-area-adrs>

<verify-sub-agent-results>
1. Apply the `question-everything` skill's **question-the-result** to raise prioritized challenges on the returned result (investigation findings or ADR decisions).
2. Dispatch a NEW same-type sub-agent — never the original instance — to verify each challenge against primary sources (codebase for findings; findings docs + `draft-adr` for ADRs), treating the result as unverified; collect per-challenge verdicts (AGREE / DISAGREE / UNCERTAIN), each traceable to its challenge.
3. Compare verdicts with the returned result: accept only if every material verdict is AGREE (report agreed claims and residual uncertainty). If any is DISAGREE or UNCERTAIN, dispatch a NEW same-type sub-agent to redo the investigation with the corrected understanding, then loop back to step 1.
4. Loop until all challenges AGREE or the 3-round cap is reached; at the cap, present both versions to the user and let them decide — never silently pick one.
5. Only after verification, synthesize the result into the findings doc or save the ADR (see **compile-findings-doc** / **draft-area-adrs**). Load **reference/verification-protocol.md** for the full loop — independence rules, brief template, comparison and re-investigation rules, traps.
</verify-sub-agent-results>

<compile-solution-doc>
1. Choose the execution strategy: dispatch to a sub-agent whenever one is available (step 2); fall back to direct compilation only when none exists (step 3). See **multi-agent-orchestration**.
2. **Sub-agent dispatch (preferred)**: announce "Dispatching solution-doc compilation to a sub-agent," prepare a brief (business context — spike goal, current-state baseline — findings docs, assumed solutions — chosen option from each ADR, plus instructions to load `write-solution-doc` and produce a **target-state** document), dispatch, then collect and review. Full brief template: **reference/workflow-procedure.md**.
3. **Direct compilation (fallback)**: load the `write-solution-doc` skill and apply its capabilities — for compiling AND revising. Seed with: business context (spike goal), current-state baseline (findings docs — evolve diagrams as-is → to-be), and assumed solutions (chosen option from each ADR). C4 diagrams show the **target architecture**, not current state. Revising is the same procedure seeded with the existing doc plus the change (see **professional-doc-authoring**).
4. **Assess size and modularity** per **solution-doc-modularity**: if the doc exceeds ~3000 words or has 5+ major sections, identify independently useful sections for extraction.
5. **Extract independent sections**: for each candidate, create a standalone doc with standalone context and back-reference, replace it in the hub with a 2–4 sentence summary and cross-reference link. Skip extraction for small, single-service solutions.
6. Compile the output bundle — findings docs, N ADRs, 1 solution doc (hub), modular sub-docs (if extracted) — and save per **spike-artifact-layout** (apply **save-artifacts**): findings → `docs/`, ADRs → `adrs/`, solution doc → `solution.md`.
7. Keep the solution doc at the latest state per **latest-state-doctrine** (see **reference/clean-artifact-principle.md**): only the target-state architecture, no process notes; on refresh route through `write-solution-doc` and rewrite affected sections in place.
8. Validate the bundle — every ADR's chosen solution reflected, cross-references consistent, diagrams match assumed solutions, extracted sub-docs back-reference correctly — then run the **no-note scan** and rewrite until none remain.
9. Present the bundle and remind the user: findings docs are the current-state record; ADRs are formal decision records (review and approve); the solution doc is the target-state architecture; version-control all artifacts together in the spike folder.
</compile-solution-doc>

<compile-findings-doc>
1. Determine document strategy: **per-area** (recommended for 2+ loosely-coupled areas) or **one consolidated doc** (tightly-coupled or single-area). Ask the user which they prefer.
2. Choose the execution strategy: dispatch to a sub-agent whenever one is available (step 3); fall back to direct compilation only when none exists (step 4). See **multi-agent-orchestration**.
3. **Sub-agent dispatch (preferred)**: announce "Dispatching findings-doc compilation to a sub-agent," prepare a brief (document strategy, Phase 2 results **with each area's evidence map**, plus instructions to load `write-solution-doc` and produce a **current-state document** with the evidence maps embedded inline), dispatch, then collect and review. Full brief template: **reference/workflow-procedure.md**.
4. **Direct compilation (fallback)**: load the `write-solution-doc` skill and apply its capabilities to produce a **current-state document**: label all diagrams "current state," replace RAID/RACI with **constraints & pain points** and **raw data & metrics** from the findings. Seed with Phase 2 results (summaries **and their evidence maps**).
5. **Validate each area's evidence map is embedded inline** per **reference/findings-document-guide.md**: entry points and key locations annotated with `file:line`, call chains as sequence diagrams, an **Evidence & Verification** section per area (evidence ledger — claim → verdict → evidence `file:line` → confidence **verified**/**inferred**/**unverified** — and searched-negatives). Never vague references like "the service layer"; never present inference as evidence.
6. Cross-reference between findings docs (if per-area): note where one area's current state creates constraints for another.
7. Present each doc and ask: "Does this accurately capture the current state? Anything to add, correct, or remove?" Then save to `<spike-folder>/docs/findings-<area>.md` (apply **save-artifacts**).
8. Findings docs are the **current-state baseline and evidence home** — evaluation compares against them, ADRs cite them, sub-agent briefs carry their evidence sections, the solution doc evolves their diagrams as-is → to-be. Update the embedded evidence map the moment new evidence is found — no round/version tracking.
</compile-findings-doc>

<save-artifacts>
1. Determine the **spike folder path** (`spikes/<spike-name>/`) — ask the user or detect an existing spike folder; name it after the spike.
2. Create the structure per **spike-artifact-layout**: `<spike-folder>/adrs/` and `<spike-folder>/docs/`.
3. Save each artifact: findings → `docs/findings-<area>.md` (or one consolidated doc); each ADR → `adrs/ADR-00X-<kebab-name>.md`; solution doc → `solution.md` (modular sub-docs → `solution-doc/`); change summary → `change-summary.md` (only when requested).
4. Rewrite cross-references between artifacts as relative paths inside the spike folder, then confirm the layout with the user.
</save-artifacts>

<summarize-required-changes>
1. Confirm prerequisites (findings + solution doc finalized) and ask: "Would you like me to generate a summary of the concrete code changes required to implement this solution?" Optional — never produce unless requested.
2. Determine code access ("Can I access the current codebase to verify the scope of changes?"): **with access**, trace code paths from the findings doc's key locations and call chains, estimate scope concretely (file counts, LOC ranges, classes to modify), mark code-verified; **without access**, generate at architectural level and mark estimates as unverified approximations.
3. Per area/ADR, map the delta from current to target state using the categories in **change-summary-guide** (New, Modified, Retired, Configuration, Data, Dependency, Test); group by area/service labeled with ADR references; identify cross-cutting concerns.
4. Compile the change summary per **change-summary-guide** with a notes section for caveats and open questions; save to `<spike-folder>/change-summary.md` (apply **save-artifacts**).
5. Present and ask: "Does this change scope look accurate? Anything missing, overestimated, or underestimated?"
6. Note: the change summary is a planning aid, **never final** — if findings or the solution doc change, apply **sync-update-artifacts** to refresh it.
</summarize-required-changes>

<sync-update-artifacts>
1. Identify the change and its origin artifact: new evidence or corrected fact (findings doc), changed decision (ADR), or target-state change (solution doc).
2. Trace the propagation path with **artifact-sync-doctrine** to determine the affected downstream artifacts.
3. Apply the change to the origin artifact through its owning skill — `draft-adr` for ADRs, `write-solution-doc` for findings/solution docs (see **professional-doc-authoring**); propagate to each affected downstream artifact, re-running the owning capability seeded with the current artifact plus the delta; for the change summary recompute the affected clusters against the updated baseline and target.
4. Validate consistency — every artifact reflects the latest facts; ADRs cite only current findings; the solution doc mirrors every ADR; the change summary traces to current ADRs — and run the **no-note scan** on each touched ADR and solution doc.
5. Present the delta in conversation — what changed and how the artifacts now agree; never inside the artifacts (see **latest-state-doctrine**).
</sync-update-artifacts>

<deep-dive-specific-areas>
1. **Gather existing context** and **confirm the deep-dive scope** — which areas to revisit, what questions remain, which stay as-is.
2. **Deep-dive per selected area**: dispatch to a code-exploration sub-agent whenever one is available (even single-area — see **multi-agent-orchestration**), seeding it with the area's findings doc (evidence map) so covered code is not re-scanned; collect, verify with **verify-sub-agent-results**, and synthesize → update the findings doc's evidence map and any new facts/corrections → evaluate solutions → apply **draft-area-adrs** to update or produce ADRs.
3. **Sync downstream artifacts** — apply **sync-update-artifacts**: refresh the solution doc via **compile-solution-doc** if ADR changes affect the system-level view, and the change summary if one exists.
4. **Present results** — ADRs and the solution doc are **rewritten in place** to the latest state (delete superseded text, never annotate; see **latest-state-doctrine** and **reference/clean-artifact-principle.md**); run the **no-note scan** on each updated artifact; narrate the delta in conversation, never inside the document.
5. After presenting, apply **suggest-spike-directions** for the next round. Full step-by-step procedure with prompts and validation checks: **reference/deep-dive-procedure.md**.
</deep-dive-specific-areas>

<suggest-spike-directions>
1. **Review what was learned this round**: from the investigation summary (or findings doc / solution doc), extract key discoveries — systems identified, constraints measured, surprises, open questions.
2. **Generate 3 go-deeper candidates**: concrete, answerable questions narrowing the spike into a specific unresolved detail. Each must reference a specific finding ("We found X, but didn't explore Y"), be investigable (codebase or prototype can answer it), and include a 1-sentence rationale.
3. **Generate 3 go-broader candidates**: concrete questions expanding the spike to an adjacent concern the user may have missed. Each must reference something the scope excluded or touched, be a genuine decision, and include a 1-sentence rationale.
4. **Present as a direction menu** using the template in **reference/spike-direction-suggestions-guide.md** (Go Deeper + Go Broader tables: candidate question, evidence anchor, rationale).
5. Ask: "Would you like to pursue any of these directions? Pick one (or more) and I'll start a new spike round. Or if you're satisfied with the current results, we can stop here." A selected direction becomes a new spike scope — apply **define-spike-scope** with it as the goal.
</suggest-spike-directions>

<suggest-spike-on-adr-uncertainty>
1. Detect uncertainty signals in the ADR discussion using **adr-uncertainty-signals** — unverified assumption, unknown feasibility, missing measurement, undecidable comparison, uninvestigated dependency, or reviewer disagreement.
2. Name the uncertainty precisely: "This decision seems to hinge on [the unverified assumption / the unknown fact / the unresolved comparison]." Explain why it matters for the chosen option.
3. Offer a spike — "Would you like to spike this before finalizing the ADR?" — and do not start one without explicit confirmation. If agreed, define a focused scope (single goal, 1–3 areas) and apply **define-spike-scope**; treat the ADR as provisional until resolved.
4. If declined, continue the ADR flow (via `draft-adr` per **professional-doc-authoring**) and record the uncertainty as a **risk** in the ADR's Consequences section — never as a free-form note.
</suggest-spike-on-adr-uncertainty>

</capabilities>

<rules>
<rule>When the user initiates a spike investigation, apply **run-spike-workflow** to orchestrate all phases from scope definition through solution compilation.</rule>
<rule>If the user provides pre-existing investigation findings (e.g., from a previous exploration), skip **investigate-per-area** and proceed directly to **compile-findings-doc** (to formalize the provided findings), then continue to **evaluate-solutions-per-area**.</rule>
<rule>If the spike has only one area, the workflow still applies in full. If the problem is greenfield, adapt **investigate-per-area** per **greenfield-scenarios**.</rule>
<rule>Mid-spike modifications: to add a new area, apply **define-spike-scope** (step 4) then remaining capabilities; to revise an area's assumed solution, re-apply **draft-area-adrs** then **compile-solution-doc**; to deep-dive unresolved areas, apply **deep-dive-specific-areas**.</rule>
<rule>If the user asks for a quick recommendation without formal documentation, decline — direct them to a regular conversation instead (see **inappropriate-scenarios**). If sub-agents are not available, fall back to direct execution.</rule>
<rule>When dispatching any work to a sub-agent, include the relevant findings doc (or its evidence sections) in the brief and instruct it to skip already-covered code.</rule>
<rule>When compiling or updating an artifact — findings docs, ADRs, or the solution doc — dispatch to a sub-agent whenever one is available and fall back to direct execution only when none exists (see **multi-agent-orchestration**).</rule>
<rule>After the solution doc is compiled: if the user wants implementation scope, apply **summarize-required-changes**; if the doc is large, apply modularity steps in **compile-solution-doc** to split independent sections.</rule>
<rule>When the user discusses an ADR (drafting, reviewing, or adjusting it — inside the spike workflow or in a standalone ADR session) and the decision depends on an unverified assumption, unknown feasibility, missing evidence, or an unresolved option comparison, apply **suggest-spike-on-adr-uncertainty** to propose investigating it with a spike before the ADR is finalized.</rule>
<rule>When updating or revising an ADR — deep-dive continuation, decision change, in-place rewrite — always apply **draft-area-adrs** so the change goes through the `draft-adr` skill; never hand-edit the ADR (see **professional-doc-authoring**).</rule>
<rule>When updating or refreshing the solution document — deep-dive, ADR decision change, modular split — always apply **compile-solution-doc** so the change goes through the `write-solution-doc` skill; never hand-edit the solution doc (see **professional-doc-authoring**).</rule>
<rule>When a fact or decision changes — new evidence, findings correction, ADR revision, deep-dive, or solution-doc refresh — apply **sync-update-artifacts** to propagate the change through every affected downstream artifact so the bundle never goes stale.</rule>
<rule>When the user wants to evaluate options by their technical implementation — or asks for diagrams, code diffs, or change locations per option — delegate tech-detail production to `draft-adr`'s **detail-options-tech** during **evaluate-solutions-per-area** (see **option-tech-details**).</rule>
<rule>When compiling or updating any artifact — findings docs, ADRs, solution doc, change summary — apply **save-artifacts** to write each artifact into its spike folder location per **spike-artifact-layout**.</rule>
</rules>
