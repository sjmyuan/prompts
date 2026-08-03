---
name: conduct-spike
description: Conduct spike investigations to produce ADRs, findings, solution docs, and change summaries. Use when scoping, investigating, evaluating, discussing ADR decisions needing investigation, formalizing, continuing, deep-diving, modularizing, summarizing changes, or suggesting direction.
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
</when-to-use-this-skill>

<knowledge>

<spike-definition>
A spike is an investigation activity aimed at reducing uncertainty around a technical problem. Unlike a full implementation, a spike focuses on research, prototyping, and decision-making. The output is knowledge and documented decisions — not production code.

A well-conducted spike produces: **Findings Documents** (current-state architecture baseline per area or consolidated), **1 Code Reference** (evidence map — entry points, key code locations, call chains, evidence ledger, searched-negatives), **N ADRs** (one per area with evaluated options and recommendations), **1 Solution Document** (target-state architecture with C4, API contracts, RAID, RACI), and optionally **1 Change Summary** (code-level changes traceable to ADRs).
</spike-definition>

<inappropriate-scenarios>
Do NOT use this skill for: quick answers without formal documentation, already-decided problems needing only implementation, trivial scope with no architectural impact, or immediate prototyping — spikes produce decisions, not production code.
</inappropriate-scenarios>

<findings-document>
A findings document captures the **current-state architecture** using the `write-solution-doc` skill's format (C4, sequence, API/event contracts) but describes the as-is rather than to-be. This makes them directly transformable into the solution doc and gives ADRs a precise baseline. For full format and strategy guidance, see **reference/findings-document-guide.md**.
</findings-document>

<code-reference>
A code reference is the spike's living evidence map: where investigation evidence lives in the code — entry points, key code locations (file:line), call chains, claim→evidence verdicts, cross-area coupling, and searched-negatives. It exists so findings docs, ADRs, change summaries, and dispatched sub-agents can cite or reuse code evidence without re-scanning the codebase. Kept continuously up to date as investigation progresses — no round/version tracking — and **always included in sub-agent briefs**. For the full structure and maintenance rules, see **reference/code-reference-guide.md**.
</code-reference>

<change-summary>
A change summary translates the delta between findings (current state) and solution doc (target state) into concrete change items grouped by category — New, Modified, Retired, Configuration, Data, Dependency, Test — traceable to ADRs. Estimate quality depends on code access; always be transparent about which mode applies. For full format and guidance, see **reference/change-summary-guide.md**.
</change-summary>

<solution-doc-modularity>
When a solution document exceeds ~3000 words or 5+ major sections, split independently understandable sections into standalone reference documents. The main doc becomes a hub with 2–4 sentence summaries and cross-references; each extracted doc must stand alone and back-reference the hub. See **reference/solution-doc-modularity-guide.md** for full heuristics and validation checklist.
</solution-doc-modularity>

<deep-dive-mode>
When drilling deeper into specific unresolved areas from a previous spike, the skill operates in **deep-dive mode**; areas not selected are left as-is. See **reference/deep-dive-mode-guide.md** for full mode comparison.
</deep-dive-mode>

<greenfield-scenarios>
When there is no existing implementation to investigate (greenfield): research industry approaches and similar systems in the organization, study operational constraints (cloud, team, compliance), build proof-of-concept prototypes instead of tracing code. Remaining phases (evaluate, draft ADRs, compile solution doc) proceed unchanged.
</greenfield-scenarios>

<multi-agent-orchestration>
For spikes with multiple investigation areas, dispatch independent work to sub-agents in parallel for Phases 2 (investigate) and 4 (draft ADRs). See the full dispatch pattern and parallelization rules in **reference/multi-agent-orchestration.md**.
</multi-agent-orchestration>

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
During ADR discussion (drafting, reviewing, or adjusting a decision — inside the spike workflow or in a standalone ADR session), suggest a spike when the decision hinges on something reasoning alone cannot settle:
- **Unverified assumption**: the chosen option assumes a fact no one has checked (e.g., "the message bus can handle peak volume")
- **Unknown feasibility**: whether the option can actually work in this codebase or organization is unknown
- **Missing measurement**: the decision depends on cost, latency, capacity, or effort data that hasn't been collected
- **Undecidable comparison**: two options remain close and the tiebreaker requires evidence, not opinion
- **Uninvestigated dependency**: the chosen option's success depends on a system whose behavior is unknown
- **Reviewer disagreement**: reviewers can't converge and need data rather than debate

This is the "Untested assumption in ADR" go-deeper heuristic from **reference/spike-direction-suggestions-guide.md**, applied while the ADR is still being discussed rather than only after an investigation round.
</adr-uncertainty-signals>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Conducting a full end-to-end spike from scope to solution doc | 5-phase walkthrough for a real-world migration problem | [examples/end-to-end-spike.md](examples/end-to-end-spike.md) |
| Conducting a single-area spike with narrow scope | Single-area workflow with one ADR + solution doc | [examples/single-area-spike.md](examples/single-area-spike.md) |
| Working from pre-existing investigation findings without re-investigating | Workflow starting from existing investigation results | [examples/from-existing-findings.md](examples/from-existing-findings.md) |
| Decomposing a complex problem into investigation areas | Decomposition rubric with examples and edge cases | [reference/decomposition-rubric.md](reference/decomposition-rubric.md) |
| Conducting a heavy multi-area spike that benefits from parallel sub-agent execution | Multi-area parallel dispatch walkthrough | [examples/multi-agent-investigation.md](examples/multi-agent-investigation.md) |
| Continuing a previous spike by digging deeper into specific unresolved areas | Deep-dive walkthrough: load context, focus investigation, update ADRs | [examples/deep-dive-continuation.md](examples/deep-dive-continuation.md) |
| Dispatching investigation or ADR drafting to sub-agents in parallel | Dispatch pattern and parallelization rules | [reference/multi-agent-orchestration.md](reference/multi-agent-orchestration.md) |
| Brainstorming solution options during the evaluate phase | Solution-brainstorming prompt set | [reference/solution-brainstorming-prompts.md](reference/solution-brainstorming-prompts.md) |
| Producing or understanding findings documents (format, per-area vs consolidated strategy, artifact relationships) | Findings doc format and strategy selection | [reference/findings-document-guide.md](reference/findings-document-guide.md) |
| Compiling or maintaining the code reference (7-section structure, confidence tags, searched-negatives rules) | Full code reference structure and maintenance rules | [reference/code-reference-guide.md](reference/code-reference-guide.md) |
| Seeing a worked code reference with entry points, call chains, evidence ledger, and searched-negatives | Worked example of a structured code reference for a 4-area spike | [examples/code-reference-example.md](examples/code-reference-example.md) |
| Drafting ADRs or compiling the solution document — keeping decision docs free of logs and investigation detail | Clean-document rules for ADRs and the solution doc | [reference/clean-artifact-principle.md](reference/clean-artifact-principle.md) |
| Entering or executing deep-dive mode (continuing a previous spike on unresolved areas) | Mode comparison guide and deep-dive procedure | [reference/deep-dive-mode-guide.md](reference/deep-dive-mode-guide.md), [reference/deep-dive-procedure.md](reference/deep-dive-procedure.md) |
| Generating a change summary (code-level changes required to implement the solution) | Format, categories, and code-access guidance | [reference/change-summary-guide.md](reference/change-summary-guide.md) |
| Assessing and splitting a large solution document into modular, AI-friendly pieces | Splitting heuristics, patterns, and validation checklist | [reference/solution-doc-modularity-guide.md](reference/solution-doc-modularity-guide.md) |
| Producing a concrete change summary with code access, demonstrating all change categories | End-to-end change summary with code-verified scope estimates | [examples/change-summary-example.md](examples/change-summary-example.md) |
| Suggesting candidate questions to narrow or broaden a spike after a round completes | Candidate-generation heuristics, go-deeper vs go-broader patterns, and output format | [reference/spike-direction-suggestions-guide.md](reference/spike-direction-suggestions-guide.md) |
| Seeing a worked example of direction suggestions — 3 go-deeper and 3 go-broader candidates grounded in investigation evidence | Walkthrough of generating direction candidates after a spike round, with rationale for each | [examples/spike-direction-suggestions.md](examples/spike-direction-suggestions.md) |
| Suggesting a spike when ADR discussion reveals a decision hinges on unverified assumptions or unknown facts | Worked example of detecting ADR uncertainty and offering a focused spike before finalizing the ADR | [examples/adr-uncertainty-spike-suggestion.md](examples/adr-uncertainty-spike-suggestion.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<run-spike-workflow>
1. Apply **define-spike-scope** to establish the spike goal and decompose the problem into investigation areas. Do not proceed until the scope is confirmed by the user.
2. Apply **investigate-per-area** to understand the current implementation per area. For multi-area spikes, dispatch investigation to sub-agents in parallel per **multi-agent-orchestration**. Investigation always records **code references** (entry points, key code locations, call chains, evidence, searched-negatives) — never narrative only. After the investigation summary, direction suggestions are presented (3 go-deeper, 3 go-broader).
   - **If the user selects a direction candidate**: treat it as a new spike scope — loop back to step 1 with the selected question as the goal.
   - **If the user confirms the investigation is complete**: proceed to step 3.
3. Apply **compile-code-reference** to consolidate the recorded code references into one structured document before formalizing findings.
4. Apply **compile-findings-doc** to formalize the investigation results into a structured findings document, citing the code reference as its evidence source.
5. After findings are confirmed, apply **evaluate-solutions-per-area** to brainstorm, compare, and select an assumed solution for each area.
6. After evaluation, apply **draft-area-adrs** to produce one formal ADR per area documenting the decision.
7. After all ADRs are finalized, apply **compile-solution-doc** to consolidate all ADRs into a system-level solution document.
8. Pause for user confirmation after each phase. Do not skip phases unless the user explicitly requests it or a specific override rule applies (e.g., pre-existing findings, deep-dive continuation).
</run-spike-workflow>

<define-spike-scope>
1. Ask the user: "What technical problem or feature do you want to spike? Describe it in 2–4 sentences."
2. Clarify the spike's **goal**: What question(s) should this spike answer? What uncertainty should it reduce?
3. Decompose the problem into **investigation areas** using the heuristics in **problem-decomposition-guide**:
   - Propose an initial breakdown based on the problem description.
   - For each area, write a one-sentence description of what needs to be investigated and decided.
   - Ask the user: "Does this breakdown cover all the key decisions? Should any area be split, merged, added, or removed?"
4. Confirm the final list of investigation areas and their order. Record the scope summary:
   - Spike goal (1 sentence)
   - Investigation areas (ordered list with one-line descriptions)
5. Validate the scope: check that each area is independently decidable, the count is 2–5 (or justified if outside that range), and the goal is clear enough to know when the spike is complete. If this is a greenfield problem, note it — the investigate phase will adapt accordingly (see **greenfield-scenarios**).
</define-spike-scope>

<investigate-per-area>
1. Determine the execution strategy based on the number of investigation areas:
   - **Single area (1 area)**: Investigate directly using the sequential steps below (step 2).
   - **Multiple areas (2+ areas)**: Dispatch all areas to code-exploration sub-agents in parallel (step 3). See **multi-agent-orchestration** for the dispatch pattern.

2. **For single-area investigation (direct execution)**:
   - Announce: "Investigating area: [area name]"
   - Load the `investigate-code` skill's SKILL.md and apply its capabilities to understand the current implementation relevant to this area.
   - **Record the area's code reference as you investigate**: entry points (file:line), key code locations (symbol, role, why it matters), call chains for key flows, and searched-negatives (what you searched and didn't find). See **reference/code-reference-guide.md**.
   - Compile findings into a structured summary: **current state** (what exists today), **constraints & pain points** (what's limiting or broken), and **relevant diagrams** (C4/sequence showing current architecture).

3. **For multi-area investigation (parallel dispatch)**:
   - Announce: "Dispatching investigation of [N] areas to sub-agents in parallel for faster completion."
   - Prepare per-area briefs (area name/description, spike goal, brownfield/greenfield designation, **the existing code reference if one exists**, expected output format **including a per-area code reference**), detect available code-exploration agents, dispatch all briefs concurrently, then collect and synthesize results — resolving any cross-area inconsistencies and **merging the returned per-area code references**. See **multi-agent-orchestration** for the dispatch pattern.

4. Present a consolidated investigation summary, noting any facts that contradict or refine prior assumptions so they can be corrected in the findings document.
5. After presenting the investigation summary, apply **suggest-spike-directions** to present 3 go-deeper and 3 go-broader candidate questions grounded in the investigation evidence.
6. Ask the user: "Would you like to pursue any of these directions, or is the investigation complete?"
   - If the user selects a direction: the workflow loops back to scope definition with the selected question as the new spike goal.
   - If the user confirms the investigation is complete: proceed to step 7.
7. Hand off to the workflow orchestrator for **compile-code-reference** (consolidate the recorded evidence map), then **compile-findings-doc**.
</investigate-per-area>

<evaluate-solutions-per-area>
1. For each area, guide the user through solution evaluation: ask what options they see, use **solution-brainstorming-prompts** if only one option is offered, capture each option's description/pros/cons/feasibility, identify decision drivers (hard constraints, soft preferences), and relate pros/cons to decision drivers.
2. After all options are evaluated, ask: "Which option do you recommend as the assumed solution for [area name]?"
   - If the user is unsure, help them compare the top contenders against decision drivers.
   - Record the **assumed solution** — this is provisional and may change after formal ADR review.
3. **Check for findings gaps**: During evaluation, did any option reveal a constraint, risk, or fact that was not captured in the findings document? If so, update the affected sections of the findings document and note the correction when presenting the evaluation summary.
4. Repeat for each investigation area.
5. Validate each area's evaluation: confirm at least 2 options were considered, pros/cons relate to decision drivers, and the assumed solution follows logically from the comparison.
6. Present a summary table of all areas with their assumed solutions and any findings corrections made.
</evaluate-solutions-per-area>

<draft-area-adrs>
1. Determine the execution strategy based on the number of investigation areas:
   - **Single ADR (1 area)**: Draft directly using the sequential steps below (step 2).
   - **Multiple ADRs (2+ areas)**: Dispatch all areas' evaluation results to sub-agents in parallel (step 3). See **multi-agent-orchestration** for the dispatch pattern.

2. **For single ADR drafting (direct execution)**:
   - Load the `draft-adr` skill's SKILL.md and apply its capabilities (define-problem → define-decision-drivers → define-considered-options → evaluate-options → compile-adr) to produce a complete, self-contained ADR for the area.
   - Seed each capability with the evaluation results from Phase 3: problem statement from the investigation area scope, decision drivers from the evaluation, considered options from the brainstorming, and the assumed solution as the chosen option.

3. **For multi-ADR drafting (parallel dispatch)**:
   - Announce: "Dispatching ADR drafting for [N] areas to sub-agents in parallel."
   - Prepare per-area briefs (area name/description, complete evaluation results — decision drivers, options with pros/cons, assumed solution — **the area's code reference slice**, and instructions to load `draft-adr` to produce a self-contained ADR), detect available agents, dispatch all briefs concurrently, then collect and review each ADR for completeness and consistency. See **multi-agent-orchestration** for the dispatch pattern.

4. After all ADRs are drafted (via either method), present them as a set and ask: "Would you like to adjust any ADR before compiling the solution document?" If the user raises uncertainty about any ADR's decision — an unverified assumption, unknown feasibility, or unresolved comparison — apply **suggest-spike-on-adr-uncertainty** before finalizing.
5. Keep each ADR clean per **clean-artifact-principle** (see **reference/clean-artifact-principle.md**): it contains only the decision — problem, decision drivers, considered options, chosen option, and consequences. No logs, raw data, evidence dumps, or process history. Cite the findings document for evidence rather than embedding it.
6. Validate each ADR: confirm the chosen option follows logically from the decision drivers, all evaluated options are fairly represented, consequences include both positive and negative impacts, and the ADR can be understood without reading other ADRs.
7. Note: The chosen option in each ADR is the **assumed solution**. The solution document will adopt these. If an ADR decision changes later, the solution document should be updated accordingly.
</draft-area-adrs>

<compile-solution-doc>
1. Load the `write-solution-doc` skill's SKILL.md and apply its capabilities. Seed with: business context (spike goal, problem statement), current-state baseline (findings docs — evolve diagrams from as-is → to-be), and assumed solutions (chosen option from each ADR). C4 diagrams must show the **target architecture**, not just current state.
2. **Assess solution doc size and modularity**: Apply the heuristics in **solution-doc-modularity**. If the doc exceeds ~3000 words, has 5+ major sections, or has independently useful sections for different audiences, identify candidate sections for extraction.
3. **Extract independent sections**: For each candidate, create a standalone doc with standalone context and back-reference, replace it in the hub with a 2–4 sentence summary and cross-reference link per **solution-doc-modularity**. Skip extraction for small, single-service solutions.
4. Compile the final output bundle: Findings Documents, N ADRs, 1 Solution Document (hub), and modular sub-documents (if extracted).
5. Keep the solution document clean per **clean-artifact-principle** (see **reference/clean-artifact-principle.md**): it contains only the target-state architecture — business context, C4/sequence diagrams, API contracts, RAID, RACI. No logs, raw investigation data, process history, or change notes. Where supporting detail exists, it lives in the findings document — cross-reference it rather than copying it in.
6. Validate the bundle: every ADR's chosen solution is reflected in the solution doc, cross-references between all artifacts are consistent, diagrams match assumed solutions, and extracted sub-docs have correct back-references.
7. Present the complete bundle. Remind the user:
   - Findings docs are the current-state record — keep them even if decisions change.
   - ADRs are formal decision records — review and approve with the team.
   - The solution doc is the target-state architecture; update it if an ADR decision changes.
   - Version-control all artifacts in the project repository.
</compile-solution-doc>

<compile-code-reference>
1. Gather the per-area code references recorded during investigation (or the existing code reference when continuing a deep-dive).
2. Consolidate them into one structured document following **reference/code-reference-guide.md**:
   - Scope (repos, areas, last updated)
   - Entry points per area (file:line)
   - Key code locations (file:line, symbol, role, why it matters)
   - Call chains for key flows
   - Evidence ledger (claim → verdict → evidence file:line → confidence)
   - Cross-area dependencies
   - Searched-negatives & gaps
3. Preserve file:line precision — every code-derived claim must carry a verifiable location, never vague references like "the service layer".
4. Tag confidence on every evidence verdict: **verified** (directly read), **inferred** (derived from surrounding code), or **unverified** (assumption). Never present inference as evidence.
5. Record searched-negatives — searches that returned nothing — so later sub-agents do not repeat dead-end scans.
6. Keep it always current: update it the moment new evidence is found during any subsequent work (deep-dive, follow-ups) — no round/version tracking, never rebuilt from scratch.
7. Present it alongside the findings doc; it is the evidence source that findings, ADRs, and the change summary cite.
</compile-code-reference>

<compile-findings-doc>
1. Determine document strategy: **per-area** (recommended for 2+ loosely-coupled areas) or **one consolidated doc** (tightly-coupled or single-area). Ask the user which they prefer.

2. For each findings document to produce, load the `write-solution-doc` skill's SKILL.md and apply its capabilities to produce a **current-state document**. The key adaptation: label all diagrams as "current state," replace RAID/RACI sections with **constraints & pain points** and **raw data & metrics** from the investigation findings. Seed with Phase 2 results (investigation summaries **and their code references**) rather than gathering context from scratch; cite the code reference for evidence locations instead of re-reading code.

3. Cross-reference between findings docs (if per-area): Note where one area's current state creates constraints for another. For example: "Area 1 (service boundaries): the monolithic `PaymentOrchestrator` → constrains Area 2 (communication): all calls are in-process, no service mesh exists."

4. Present each findings document to the user and ask: "Does this accurately capture the current state? Anything to add, correct, or remove?"

5. The findings docs are now the **current-state baseline**: evaluation compares options against them, ADRs cite them as evidence, and the solution doc evolves their diagrams from as-is → to-be.
</compile-findings-doc>

<summarize-required-changes>
1. Confirm prerequisites: the findings documents and solution document must be finalized. Ask: "Would you like me to generate a summary of the concrete code changes required to implement this solution?" Do not produce this artifact unless the user wants it — it is optional.
2. Determine code access: Ask: "Can I access the current codebase to verify the scope of changes?" 
   - **With code access**: Explore the relevant code paths identified in the findings documents, **starting from the code reference's key locations and call chains**. Trace which files, classes, and packages correspond to each area. Estimate scope concretely (file counts, LOC ranges, specific classes to modify). Mark estimates as code-verified.
   - **Without code access**: Generate the summary at an architectural level based on the findings and solution documents alone. Mark all scope estimates as unverified architectural approximations. Note where code access would improve accuracy.
3. For each area/ADR, map the delta from current state to target state using the categories in **change-summary-guide**: New, Modified, Retired, Configuration, Data, Dependency, Test.
4. Group changes by area/service, labeling each cluster with its ADR reference for traceability. Identify cross-cutting concerns that span multiple areas (e.g., shared library changes, auth integration, logging standards).
5. Compile the change summary document following the format in **change-summary-guide**. Include a notes section for caveats, assumptions, and open questions.
6. Present the summary and ask: "Does this change scope look accurate? Anything missing, overestimated, or underestimated?"
7. Note: the change summary is a planning aid tracing back to ADR decisions and solution doc sections. For sprint planning, use it as input — not the final word.
</summarize-required-changes>

<deep-dive-specific-areas>
1. **Gather existing context** and **confirm the deep-dive scope** — which areas to revisit, what questions remain, which areas stay as-is.
2. **Deep-dive per selected area**: investigate deeper with targeted focus, **starting from the existing code reference** (entry points, call chains, searched-negatives) so covered code is not re-scanned → update the code reference with new locations and verdicts → update findings doc with any new facts or corrections → evaluate solutions with new findings → update or produce ADRs.
3. **Optionally update the solution document** if ADR changes affect the system-level view.
4. **Present the deep-dive results** — updated findings, new/updated ADRs, refreshed solution doc (if applicable). ADRs and the solution doc are updated cleanly with the corrected decisions and facts, without logs or change notes (see **reference/clean-artifact-principle.md**).
5. After presenting the results, apply **suggest-spike-directions** to present direction candidates for the next spike round.

For the full step-by-step procedure with prompts and validation checks per step, load **reference/deep-dive-procedure.md**.
</deep-dive-specific-areas>

<suggest-spike-directions>
1. **Review what was learned this round**: From the investigation summary (or findings document if already compiled, or solution doc if after a full spike), extract the key discoveries — systems identified, constraints measured, surprises found, open questions that remain.
2. **Generate 3 go-deeper candidates**: For each, write a concrete, answerable question that narrows the spike into a specific unresolved detail. Each candidate must:
   - Reference a specific finding from this round ("We found X, but didn't explore Y")
   - Be investigable — the codebase or a prototype can answer it
   - Include a 1-sentence rationale: why going deeper here matters
3. **Generate 3 go-broader candidates**: For each, write a concrete question that expands the spike to an adjacent concern the user may have missed. Each candidate must:
   - Reference something the current spike scope excluded or touched but didn't investigate
   - Be a genuine decision the user will need to make, not a tangent
   - Include a 1-sentence rationale: why broadening here matters
4. **Present as a direction menu**:
   ```
   ## Where to take this spike next?

   ### Go Deeper (narrow the focus)
   | # | Candidate question | Based on (evidence from this round) | Why it matters |
   |---|---|---|---|
   | D1 | [concrete question] | [specific finding] | [1-sentence rationale] |
   | D2 | [concrete question] | [specific finding] | [1-sentence rationale] |
   | D3 | [concrete question] | [specific finding] | [1-sentence rationale] |

   ### Go Broader (expand the scope)
   | # | Candidate question | Based on (evidence from this round) | Why it matters |
   |---|---|---|---|
   | B1 | [concrete question] | [specific finding or gap] | [1-sentence rationale] |
   | B2 | [concrete question] | [specific finding or gap] | [1-sentence rationale] |
   | B3 | [concrete question] | [specific finding or gap] | [1-sentence rationale] |
   ```
5. Ask the user: "Would you like to pursue any of these directions? Pick one (or more) and I'll start a new spike round. Or if you're satisfied with the current results, we can stop here."
6. If the user selects a direction, treat it as a new spike scope — apply **define-spike-scope** with the selected question as the goal, then proceed through the workflow phases.
</suggest-spike-directions>

<suggest-spike-on-adr-uncertainty>
1. Detect uncertainty signals in the ADR discussion using **adr-uncertainty-signals** in the knowledge section — an unverified assumption, unknown feasibility, missing measurement, undecidable comparison, uninvestigated dependency, or reviewer disagreement.
2. Name the uncertainty precisely: "This decision seems to hinge on [the unverified assumption / the unknown fact / the unresolved comparison]." Explain why it matters for the chosen option.
3. Offer a spike: "Would you like to spike this before finalizing the ADR?" Do not start one without explicit confirmation.
4. If the user agrees, define a focused spike scope: a single goal (the uncertainty to resolve) and 1–3 investigation areas, then apply **define-spike-scope** to confirm before proceeding. Treat the ADR as provisional until the spike resolves the uncertainty.
5. If the user declines, continue the current ADR flow and record the uncertainty as an open question in the ADR's consequences so it isn't lost.
</suggest-spike-on-adr-uncertainty>

</capabilities>

<rules>

<rule>When the user initiates a spike investigation, apply **run-spike-workflow** to orchestrate all phases from scope definition through solution compilation.</rule>

<rule>If the user provides pre-existing investigation findings (e.g., from a previous exploration), skip **investigate-per-area** and proceed directly to **compile-findings-doc** (to formalize the provided findings), then continue to **evaluate-solutions-per-area**.</rule>

<rule>If the spike has only one area, the workflow still applies in full. If the problem is greenfield, adapt **investigate-per-area** per **greenfield-scenarios**: research, study constraints, prototype instead of tracing code.</rule>

<rule>Mid-spike modifications: to add a new area, apply **define-spike-scope** (step 4) then remaining capabilities; to revise an area's assumed solution, re-apply **draft-area-adrs** then **compile-solution-doc**; to deep-dive unresolved areas, apply **deep-dive-specific-areas**.</rule>

<rule>If the user asks for a quick recommendation without formal documentation, decline — direct them to a regular conversation instead (see **inappropriate-scenarios**). If sub-agents are not available, fall back to sequential execution.</rule>

<rule>When dispatching any work to a sub-agent (investigation, ADR drafting, deep-dive), always include the relevant code reference in the brief and instruct it to skip already-covered code — only dig into marked gaps and searched-negatives.</rule>

<rule>After the solution doc is compiled: if the user wants implementation scope, apply **summarize-required-changes**; if the doc is large, apply modularity steps in **compile-solution-doc** to split independent sections.</rule>

<rule>When the user discusses an ADR (drafting, reviewing, or adjusting it — inside the spike workflow or in a standalone ADR session) and the decision depends on an unverified assumption, unknown feasibility, missing evidence, or an unresolved option comparison, apply **suggest-spike-on-adr-uncertainty** to propose investigating it with a spike before the ADR is finalized.</rule>

</rules>
