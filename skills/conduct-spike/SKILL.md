---
name: conduct-spike
description: Conduct spike investigations to produce ADRs, findings, solution docs, and change summaries. Use when conducting, scoping, investigating, evaluating, formalizing, continuing, parallelizing, deep-diving, summarizing changes, or modularizing documents for a spike.
---

<when-to-use-this-skill>
- User wants to conduct a spike investigation on a technical problem or feature
- User needs to research, evaluate, and compare solution approaches for a complex problem before committing to one
- User wants to produce ADRs for each decision area alongside a consolidated solution document
- User needs to understand current implementation before proposing changes or solutions
- User wants to break down a large technical problem into independently decidable investigation areas
- User has pre-existing investigation findings and wants to formalize them into ADRs and a solution document
- User has a heavy spike with multiple investigation areas and wants to parallelize work across sub-agents for faster completion
- User wants to continue a previous spike by digging deeper into one or more specific investigation areas that were not fully resolved
- User wants to summarize the concrete code changes required to implement the chosen solution (change summary)
- User wants to keep the solution document modular and efficiently loadable by AI (split large solution docs into independent sub-documents)
</when-to-use-this-skill>

<knowledge>

<spike-definition>
A spike is an investigation activity aimed at reducing uncertainty around a technical problem. Unlike a full implementation, a spike focuses on research, prototyping, and decision-making. The output is knowledge and documented decisions — not production code.

A well-conducted spike produces: **Findings Documents** (current-state architecture baseline per area or consolidated), **N ADRs** (one per area with evaluated options and recommendations), **1 Solution Document** (target-state architecture with C4, API contracts, RAID, RACI), and optionally **1 Change Summary** (code-level changes traceable to ADRs).
</spike-definition>

<inappropriate-scenarios>
Do NOT use this skill for: quick answers without formal documentation, already-decided problems needing only implementation, trivial scope with no architectural impact, or immediate prototyping — spikes produce decisions, not production code.
</inappropriate-scenarios>

<deep-dive-mode>
When a user wants to drill deeper into specific unresolved areas from a previous spike, the skill operates in **deep-dive mode**. Areas not selected are left as-is. See **reference/deep-dive-mode-guide.md** for full mode comparison.
</deep-dive-mode>

<findings-document>
A findings document captures the **current-state architecture** using the `write-solution-doc` skill's format (C4, sequence, API/event contracts) but describes the as-is rather than to-be. This makes them directly transformable into the solution doc and gives ADRs a precise baseline. For full format and strategy guidance, see **reference/findings-document-guide.md**.
</findings-document>

<change-summary>
A change summary translates the delta between findings (current state) and solution doc (target state) into concrete change items grouped by category — New, Modified, Retired, Configuration, Data, Dependency, Test — traceable to ADRs. Estimate quality depends on code access; always be transparent about which mode applies. For full format and guidance, see **reference/change-summary-guide.md**.
</change-summary>

<solution-doc-modularity>
When a solution document exceeds ~3000 words or 5+ major sections, split independently understandable sections into standalone reference documents. The main doc becomes a hub with 2–4 sentence summaries and cross-references; each extracted doc must stand alone and back-reference the hub. Split by service, architectural layer, or decision area. For full heuristics and validation checklist, see **reference/solution-doc-modularity-guide.md**.
</solution-doc-modularity>

<discovery-tracking>
Spike investigations are iterative — new facts may contradict earlier assumptions. When this happens, record **what changed, why, and the evidence** in the affected findings document's **Discovery Log** section. Update ADRs and the solution document if they are also affected. A discovery entry captures: the fact/correction, evidence, impact on documents, and date. For the full log format, entry structure, and when-to-record triggers, see **reference/discovery-log-guide.md**.
</discovery-tracking>

<greenfield-scenarios>
When there is no existing implementation to investigate (greenfield): research industry approaches and similar systems in the organization, study operational constraints (cloud, team, compliance), build proof-of-concept prototypes instead of tracing code. Remaining phases (evaluate, draft ADRs, compile solution doc) proceed unchanged.
</greenfield-scenarios>

<spike-workflow-phases>
The spike workflow proceeds through five sequential phases. Phases 2 and 4 can be parallelized across sub-agents when there are multiple investigation areas. This skill orchestrates three sub-skills (`investigate-code`, `write-solution-doc`, `draft-adr`); when invoking a sub-skill, load its SKILL.md to access its full capabilities.

| Phase | What happens | Invokes |
|---|---|---|
| 1. Define scope | Clarify the spike goal and decompose into investigation areas | — |
| 2. Investigate | Understand current implementation per area; dispatch to sub-agents in parallel for multi-area spikes | `investigate-code` |
| 2b. Compile findings doc(s) | Produce findings docs in solution-doc format, adapted for current-state architecture | `write-solution-doc` (as-is) |
| 3. Evaluate | Brainstorm and evaluate solution options per area, grounded in findings docs | — |
| 4. Draft ADRs | Produce one formal ADR per area; dispatch to sub-agents in parallel for multi-area spikes | `draft-adr` |
| 5. Compile solution doc | Consolidate all ADRs into a system-level solution document | `write-solution-doc` (to-be) |
</spike-workflow-phases>

<multi-agent-orchestration>
For spikes with multiple investigation areas, dispatch independent work to sub-agents in parallel for Phases 2 (investigate) and 4 (draft ADRs). See the full dispatch pattern and parallelization rules in **reference/multi-agent-orchestration.md**.
</multi-agent-orchestration>

<problem-decomposition-guide>
When breaking down a spike problem into investigation areas, target 2–5 areas. Fewer than 2 means the problem may not need a spike; more than 5 suggests the scope may be too broad. For the full rubric with heuristics and edge cases, see **reference/decomposition-rubric.md**.
</problem-decomposition-guide>

<solution-brainstorming-prompts>
When helping the user brainstorm solution options, prompt them to consider: status quo, incremental improvement, industry-standard approaches, build-vs-buy-vs-adopt, greenfield rewrite, and hybrid/phased strategies. See the full prompt set in **reference/solution-brainstorming-prompts.md**.
</solution-brainstorming-prompts>

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
| Entering or executing deep-dive mode (continuing a previous spike on unresolved areas) | Mode comparison guide and deep-dive procedure | [reference/deep-dive-mode-guide.md](reference/deep-dive-mode-guide.md), [reference/deep-dive-procedure.md](reference/deep-dive-procedure.md) |
| Generating a change summary (code-level changes required to implement the solution) | Format, categories, and code-access guidance | [reference/change-summary-guide.md](reference/change-summary-guide.md) |
| Assessing and splitting a large solution document into modular, AI-friendly pieces | Splitting heuristics, patterns, and validation checklist | [reference/solution-doc-modularity-guide.md](reference/solution-doc-modularity-guide.md) |
| Producing a concrete change summary with code access, demonstrating all change categories | End-to-end change summary with code-verified scope estimates | [examples/change-summary-example.md](examples/change-summary-example.md) |
| Recording new discoveries, corrections, or invalidated assumptions during investigation or evaluation | Discovery log format and when-to-record guidance | [reference/discovery-log-guide.md](reference/discovery-log-guide.md) |

</context-loading-guide>

</knowledge>

<capabilities>

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
   - Compile findings into a structured summary: **current state** (what exists today), **constraints & pain points** (what's limiting or broken), and **relevant diagrams** (C4/sequence showing current architecture).

3. **For multi-area investigation (parallel dispatch)**:
   - Announce: "Dispatching investigation of [N] areas to sub-agents in parallel for faster completion."
   - For each investigation area, prepare a brief with: area name and description, spike goal, brownfield/greenfield designation (see **greenfield-scenarios**), and expected output format (current state, constraints & pain points, relevant diagrams).
   - Detect what code-exploration agents are available on the current platform, then dispatch all briefs to them concurrently. Sub-agents operate independently.
   - When all sub-agents complete, collect their findings.
   - Synthesize findings: review each sub-agent's output for completeness, resolve any cross-area inconsistencies, and compile each area's findings into the structured summary format (current state, constraints & pain points, relevant diagrams).

4. Present a consolidated investigation summary. For each area where the investigation revealed a discovery that contradicts or refines a prior assumption, flag it: "New discovery in [area]: [what was found, evidence]." Record each discovery in the findings doc's Discovery Log.
5. Ask the user to confirm the investigation findings before proceeding.
6. After the user confirms, apply **compile-findings-doc** to formalize the investigation results into a structured findings document before moving to evaluation. Any discoveries flagged in step 4 must appear in the findings document's Discovery Log.
</investigate-per-area>

<evaluate-solutions-per-area>
1. For each area, guide the user through solution evaluation: ask what options they see, use **solution-brainstorming-prompts** if only one option is offered, capture each option's description/pros/cons/feasibility, identify decision drivers (hard constraints, soft preferences), and relate pros/cons to decision drivers.
2. After all options are evaluated, ask: "Which option do you recommend as the assumed solution for [area name]?"
   - If the user is unsure, help them compare the top contenders against decision drivers.
   - Record the **assumed solution** — this is provisional and may change after formal ADR review.
3. **Check for findings gaps**: During evaluation, did any option reveal a constraint, risk, or fact that was not captured in the findings document? If so:
   - Record the new discovery in the findings document's Discovery Log (what was found, evidence, impact).
   - Update the affected sections of the findings document.
   - Note the correction when presenting the evaluation summary.
4. Repeat for each investigation area.
5. Validate each area's evaluation: confirm at least 2 options were considered, pros/cons relate to decision drivers, and the assumed solution follows logically from the comparison. Also confirm any findings corrections from step 3 were recorded in the Discovery Log.
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
   - For each area, prepare a brief with: area name/description, complete evaluation results (decision drivers, options with pros/cons, assumed solution), and instructions to load `draft-adr` to produce a self-contained ADR.
   - Detect what agents are available on the current platform, then dispatch all briefs to sub-agents concurrently. Each sub-agent loads `draft-adr` independently.
   - When all sub-agents complete, collect and review each ADR for completeness and consistency.

4. After all ADRs are drafted (via either method), present them as a set and ask: "Would you like to adjust any ADR before compiling the solution document?"
5. Validate each ADR: confirm the chosen option follows logically from the decision drivers, all evaluated options are fairly represented, consequences include both positive and negative impacts, and the ADR can be understood without reading other ADRs.
6. Note: The chosen option in each ADR is the **assumed solution**. The solution document will adopt these. If an ADR decision changes later, the solution document should be updated accordingly.
</draft-area-adrs>

<compile-solution-doc>
1. Load the `write-solution-doc` skill's SKILL.md and apply its capabilities. Seed with: business context (spike goal, problem statement), current-state baseline (findings docs — evolve diagrams from as-is → to-be), and assumed solutions (chosen option from each ADR). C4 diagrams must show the **target architecture**, not just current state.
3. **Assess solution doc size and modularity**: Apply the heuristics in **solution-doc-modularity**. If the doc exceeds ~3000 words, has 5+ major sections, or has independently useful sections for different audiences, identify candidate sections for extraction.
4. **Extract independent sections**: For each candidate, create a standalone doc with standalone context and back-reference, replace it in the hub with a 2–4 sentence summary and cross-reference link per **solution-doc-modularity**. Skip extraction for small, single-service solutions.
5. Compile the final output bundle: Findings Documents, N ADRs, 1 Solution Document (hub), and modular sub-documents (if extracted).
6. Validate the bundle: every ADR's chosen solution is reflected in the solution doc, cross-references between all artifacts are consistent, diagrams match assumed solutions, and extracted sub-docs have correct back-references.
7. Present the complete bundle. Remind the user:
   - Findings docs are the current-state record — keep them even if decisions change.
   - ADRs are formal decision records — review and approve with the team.
   - The solution doc is the target-state architecture; update it if an ADR decision changes.
   - Version-control all artifacts in the project repository.
</compile-solution-doc>

<compile-findings-doc>
1. Determine document strategy: **per-area** (recommended for 2+ loosely-coupled areas) or **one consolidated doc** (tightly-coupled or single-area). Ask the user which they prefer.

2. For each findings document to produce, load the `write-solution-doc` skill's SKILL.md and apply its capabilities to produce a **current-state document**. The key adaptation: label all diagrams as "current state," replace RAID/RACI sections with **constraints & pain points** and **raw data & metrics** from the investigation findings. Include a **Discovery Log** section at the end of each findings document, following the format in **reference/discovery-log-guide.md**. Populate it with any discoveries flagged during investigation (from **investigate-per-area** step 4). Seed with Phase 2 results rather than gathering context from scratch.

3. Cross-reference between findings docs (if per-area): Note where one area's current state creates constraints for another. For example: "Area 1 (service boundaries): the monolithic `PaymentOrchestrator` → constrains Area 2 (communication): all calls are in-process, no service mesh exists."

4. Present each findings document to the user and ask: "Does this accurately capture the current state? Anything to add, correct, or remove?"

5. After confirmation, ensure the Discovery Log is up to date — any corrections from user feedback in step 4 should be recorded as discovery entries.

6. The findings docs are now the **current-state baseline**: evaluation compares options against them, ADRs cite them as evidence, and the solution doc evolves their diagrams from as-is → to-be.
</compile-findings-doc>

<summarize-required-changes>
1. Confirm prerequisites: the findings documents and solution document must be finalized. Ask: "Would you like me to generate a summary of the concrete code changes required to implement this solution?" Do not produce this artifact unless the user wants it — it is optional.
2. Determine code access: Ask: "Can I access the current codebase to verify the scope of changes?" 
   - **With code access**: Explore the relevant code paths identified in the findings documents. Trace which files, classes, and packages correspond to each area. Estimate scope concretely (file counts, LOC ranges, specific classes to modify). Mark estimates as code-verified.
   - **Without code access**: Generate the summary at an architectural level based on the findings and solution documents alone. Mark all scope estimates as unverified architectural approximations. Note where code access would improve accuracy.
3. For each area/ADR, map the delta from current state to target state using the categories in **change-summary-guide**: New, Modified, Retired, Configuration, Data, Dependency, Test.
4. Group changes by area/service, labeling each cluster with its ADR reference for traceability. Identify cross-cutting concerns that span multiple areas (e.g., shared library changes, auth integration, logging standards).
5. Compile the change summary document following the format in **change-summary-guide**. Include a notes section for caveats, assumptions, and open questions.
6. Present the summary and ask: "Does this change scope look accurate? Anything missing, overestimated, or underestimated?"
7. Note: the change summary is a planning aid tracing back to ADR decisions and solution doc sections. For sprint planning, use it as input — not the final word.
</summarize-required-changes>

<deep-dive-specific-areas>
1. **Gather existing context** and **confirm the deep-dive scope** — which areas to revisit, what questions remain, which areas stay as-is.
2. **Deep-dive per selected area**: investigate deeper with targeted focus → update findings doc (including Discovery Log entries for any new facts or corrections) → evaluate solutions with new findings → update or produce ADRs.
3. **Optionally update the solution document** if ADR changes affect the system-level view.
4. **Present the deep-dive results** — updated findings with Discovery Log entries, new/updated ADRs, refreshed solution doc (if applicable).

For the full step-by-step procedure with prompts and validation checks per step, load **reference/deep-dive-procedure.md**.
</deep-dive-specific-areas>

</capabilities>

<rules>

<rule>When the user initiates a spike investigation, apply **define-spike-scope** to establish the goal and investigation areas. Do not skip to investigation until the scope is confirmed.</rule>

<rule>The spike workflow runs sequentially through all phases per **spike-workflow-phases**: **define-spike-scope** → **investigate-per-area** → **compile-findings-doc** → **evaluate-solutions-per-area** → **draft-area-adrs** → **compile-solution-doc**. After each phase, pause for user confirmation before proceeding. Do not skip phases unless the user explicitly requests it. For multi-area spikes, Phases 2 and 4 dispatch work to sub-agents in parallel per **multi-agent-orchestration**.</rule>

<rule>If the user provides pre-existing investigation findings (e.g., from a previous exploration), skip **investigate-per-area** and proceed directly to **compile-findings-doc** (to formalize the provided findings), then continue to **evaluate-solutions-per-area**.</rule>

<rule>If the spike has only one area, the workflow still applies in full. If the problem is greenfield, adapt **investigate-per-area** per **greenfield-scenarios**: research, study constraints, prototype instead of tracing code.</rule>

<rule>Mid-spike modifications: to add a new area, apply **define-spike-scope** (step 4) then remaining capabilities; to revise an area's assumed solution, re-apply **draft-area-adrs** then **compile-solution-doc**; to deep-dive unresolved areas, apply **deep-dive-specific-areas**.</rule>

<rule>If the user asks for a quick recommendation without formal documentation, decline — direct them to a regular conversation instead (see **inappropriate-scenarios**). If sub-agents are not available, fall back to sequential execution.</rule>

<rule>After the solution doc is compiled: if the user wants implementation scope, apply **summarize-required-changes**; if the doc is large, apply modularity steps in **compile-solution-doc** to split independent sections.</rule>

</rules>
