---
name: conduct-spike
description: Conduct spike investigations to explore technical problems and produce ADRs, findings documents, solution documents, and change summaries. Use when conducting, scoping, investigating, evaluating, formalizing findings, continuing, parallelizing, deep-diving, summarizing required changes, or modularizing solution documents for a spike.
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

A well-conducted spike produces four artifact types:
- **Findings Documents** — current-state architecture (C4, sequence, API/event contracts) per area or consolidated; the factual baseline that ADRs evaluate against
- **N ADRs** — one Architecture Decision Record per area, each evaluating options and recommending a solution, referencing findings docs for evidence
- **1 Solution Document** — target-state architecture evolved from findings docs, with C4 diagrams, API contracts, RAID analysis, and RACI matrix; split into modular sub-documents when large to keep individual documents AI-friendly
- **1 Change Summary** (optional) — concrete code-level changes required to implement the solution, grouped by area/service and traceable to ADRs; produced when the user wants to understand implementation scope
</spike-definition>

<inappropriate-scenarios>
This skill is NOT appropriate when:
- The user wants a quick answer or informal recommendation without formal documentation
- The problem has already been decided and only needs implementation
- The scope is trivial (single well-understood option, no architectural impact)
- The user wants to write code or build a prototype immediately — spikes produce decisions, not production code
</inappropriate-scenarios>

<deep-dive-mode>
When a user has previously conducted a spike and now wants to drill deeper into specific unresolved areas, the skill operates in **deep-dive mode** — distinct from a full spike (starts from scratch), from-existing-findings (skips investigation), or ADR revision (text-only update). Areas not selected for deep-dive are left as-is. See **reference/deep-dive-mode-guide.md** for the full comparison of modes and when each applies.
</deep-dive-mode>

<findings-document>
A findings document captures the **current-state architecture** using the `write-solution-doc` skill's format (C4 diagrams, sequence diagrams, API/event contracts) but describes the as-is rather than the to-be. This makes findings docs directly transformable into the solution document in Phase 5, and gives ADRs a precise baseline to compare options against. For the full guide on format, strategy, and artifact relationships, see **reference/findings-document-guide.md**.
</findings-document>

<change-summary>
A change summary translates the delta between findings documents (current state) and the solution document (target state) into concrete, actionable change items. It bridges architectural decisions and implementation planning. Changes are grouped by category — New, Modified, Retired, Configuration, Data, Dependency, Test — and traceable to ADRs. The quality of scope estimates depends on code access: with code access, estimates are concrete and code-path-verified; without it, estimates are architectural approximations. Always be transparent about which mode is in effect. For the full format, categories, and code-access guidance, see **reference/change-summary-guide.md**.
</change-summary>

<solution-doc-modularity>
Large solution documents become unwieldy for AI context windows. When a solution document exceeds manageable size (~3000 words or 5+ major sections), identify sections that are independently understandable and extract them into separate reference documents. The main solution document becomes a hub with concise summaries (2–4 sentences) and cross-reference links to the extracted docs. Each extracted doc must include enough context to stand alone and a back-reference to the hub. Split by service, by architectural layer, or by decision area — whichever produces the most independently-loadable pieces. For the full splitting heuristics, patterns, cross-reference format, and validation checklist, see **reference/solution-doc-modularity-guide.md**.
</solution-doc-modularity>

<discovery-tracking>
Spike investigations are iterative — new facts surface, assumptions get invalidated, and earlier conclusions may need revision. When this happens, record **what changed, why, and the evidence** directly in the affected document so the spike's reasoning trail is never lost. This practice serves three purposes:

1. **Audit trail**: Anyone reading the final artifacts can trace how the team arrived at the correct solution — which assumptions were tested, which were disproven, and what evidence drove each correction.
2. **Lesson capture**: The discovery log becomes a compact record of what the team learned during the spike, making post-spike retrospectives and knowledge transfer more efficient.
3. **Review confidence**: Reviewers can see that conclusions weren't simply asserted — they were tested against evidence, and when evidence contradicted earlier beliefs, the documents were corrected.

**When to record a discovery entry:**
- Investigation reveals a fact that contradicts or refines a previous assumption in the findings document.
- Evaluation of solution options uncovers a constraint or risk not captured in the findings.
- A deep-dive produces new information that changes the understanding of an area.
- An ADR's chosen option needs revision because new evidence surfaced during a later phase.

**Where to record:** Each findings document includes a **Discovery Log** section (see **reference/discovery-log-guide.md** for format). When a correction affects an ADR or the solution document, update those documents too and note the change in their respective revision sections.

**What a discovery entry captures:**
- **What was found or corrected** — the specific fact, constraint, or insight.
- **Evidence** — code traces, benchmarks, documentation, experiments, or reasoning that supports it.
- **Impact** — which sections of which documents were updated as a result.
- **Date** — when the discovery was made (so the timeline is traceable).

For the full log format, entry structure, and examples, see **reference/discovery-log-guide.md**.
</discovery-tracking>

<greenfield-scenarios>
When there is no existing implementation to investigate (greenfield), adapt the investigate phase:
- Research industry approaches, open-source solutions, and similar systems in the organization
- Study constraints from the operational environment (cloud provider, team expertise, compliance)
- Build proof-of-concept prototypes instead of tracing existing code
- The remaining phases (evaluate, draft ADRs, compile solution doc) proceed unchanged
</greenfield-scenarios>

<spike-workflow-phases>
The spike workflow proceeds through five sequential phases. Phases 2 and 4 can be parallelized across sub-agents when there are multiple investigation areas:

| Phase | What happens | Leverages |
|---|---|---|
| 1. Define scope | Clarify the spike goal and decompose into investigation areas | — |
| 2. Investigate | Understand the current implementation relevant to each area; dispatch to sub-agents in parallel for multi-area spikes | `investigate-code` skill, code-exploration sub-agents |
| 2b. Compile findings doc(s) | Produce findings documents in solution-doc format via `write-solution-doc` skill, adapted for current-state architecture | `write-solution-doc` skill (applied to as-is) |
| 3. Evaluate | Brainstorm and evaluate solution options per area, grounded in the findings documents | — |
| 4. Draft ADRs | Produce one formal ADR per investigation area; dispatch to sub-agents in parallel for multi-area spikes | `draft-adr` skill, sub-agents |
| 5. Compile solution doc | Consolidate all ADRs into a system-level solution document | `write-solution-doc` skill |
</spike-workflow-phases>

<multi-agent-orchestration>
For spikes with multiple investigation areas, dispatch independent work to sub-agents in parallel for Phases 2 (investigate) and 4 (draft ADRs). See the full dispatch pattern, parallelization rules, and platform-detection guidance in **reference/multi-agent-orchestration.md**.
</multi-agent-orchestration>

<problem-decomposition-guide>
When breaking down a spike problem into investigation areas, apply the heuristics and patterns in **reference/decomposition-rubric.md**. Key rules:
- Target 2–5 investigation areas. Fewer than 2 means the problem may not need a spike; more than 5 suggests the scope may be too broad and should be narrowed.
- Load the full rubric when the problem is complex or the initial breakdown needs validation.
</problem-decomposition-guide>

<solution-brainstorming-prompts>
When helping the user brainstorm solution options for an investigation area, prompt them to consider status quo, incremental improvement, industry-standard approaches, build-vs-buy-vs-adopt, greenfield rewrite, and hybrid/phased strategies. See the full prompt set in **reference/solution-brainstorming-prompts.md**.
</solution-brainstorming-prompts>

<skill-integration-points>
This skill orchestrates three sub-skills and optional sub-agents. It provides the when-to-invoke and what-context-to-seed; the sub-skills handle detailed execution.

| Phase | Invokes | Purpose |
|---|---|---|
| 2. Investigate | `investigate-code` (direct or via sub-agents) | Codebase understanding for each area |
| 2b. Findings docs | `write-solution-doc` (adapted to current-state) | Structured as-is documentation |
| 4. Draft ADRs | `draft-adr` (direct or via sub-agents) | One ADR per area, seeded with evaluation results |
| 5. Solution doc | `write-solution-doc` (target-state) | Consolidated to-be architecture |

When invoking a sub-skill, load its SKILL.md to access its full capabilities.
</skill-integration-points>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Conducting a full end-to-end spike from scope to solution doc | Complete walkthrough with all 5 phases for a real-world migration problem | [examples/end-to-end-spike.md](examples/end-to-end-spike.md) |
| Conducting a single-area spike with narrow scope | Condensed workflow for a single-area spike producing one ADR + solution doc | [examples/single-area-spike.md](examples/single-area-spike.md) |
| Working from pre-existing investigation findings without re-investigating | Workflow starting from pre-existing investigation results | [examples/from-existing-findings.md](examples/from-existing-findings.md) |
| Decomposing a complex problem into investigation areas | Decomposition rubric with examples and edge cases | [reference/decomposition-rubric.md](reference/decomposition-rubric.md) |
| Conducting a heavy multi-area spike that benefits from parallel sub-agent execution | Walkthrough of dispatching investigation and ADR drafting to sub-agents in parallel | [examples/multi-agent-investigation.md](examples/multi-agent-investigation.md) |
| Continuing a previous spike by digging deeper into specific unresolved areas | Walkthrough of deep-dive mode: loading existing context, focusing investigation, updating ADRs | [examples/deep-dive-continuation.md](examples/deep-dive-continuation.md) |
| Dispatching investigation or ADR drafting to sub-agents in parallel | Full dispatch pattern, parallelization rules, and platform-detection guidance | [reference/multi-agent-orchestration.md](reference/multi-agent-orchestration.md) |
| Brainstorming solution options during the evaluate phase | Full set of solution-brainstorming prompts | [reference/solution-brainstorming-prompts.md](reference/solution-brainstorming-prompts.md) |
| Producing or understanding findings documents (format, per-area vs consolidated strategy, artifact relationships) | Full findings document guide: format rationale, strategy selection, relationship to ADRs and solution doc | [reference/findings-document-guide.md](reference/findings-document-guide.md) |
| Determining whether the user's request is a deep-dive vs full spike vs from-existing-findings vs ADR revision | Full comparison of spike modes and when each applies | [reference/deep-dive-mode-guide.md](reference/deep-dive-mode-guide.md) |
| Executing a deep-dive on specific areas (continuing a previous spike) | Full detailed deep-dive procedure with prompts and validation checks per step | [reference/deep-dive-procedure.md](reference/deep-dive-procedure.md) |
| Generating a change summary (code-level changes required to implement the solution) | Full change summary guide: format, categories, code-access guidance, relationship to other artifacts | [reference/change-summary-guide.md](reference/change-summary-guide.md) |
| Assessing and splitting a large solution document into modular, AI-friendly pieces | Full modularity guide: splitting heuristics, patterns, cross-reference format, validation checklist | [reference/solution-doc-modularity-guide.md](reference/solution-doc-modularity-guide.md) |
| Producing a concrete change summary with code access, demonstrating all change categories | End-to-end change summary for a multi-service migration, with code-verified scope estimates | [examples/change-summary-example.md](examples/change-summary-example.md) |
| Recording new discoveries, corrections, or invalidated assumptions discovered during investigation or evaluation | Discovery log format, entry structure, when and how to record corrections in findings documents | [reference/discovery-log-guide.md](reference/discovery-log-guide.md) |

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
   - For each investigation area, prepare a focused brief containing:
     - The area name and one-line description from the scope definition.
     - The spike goal for shared context.
     - Whether this is brownfield (provide guidance on relevant code paths to explore) or greenfield (see **greenfield-scenarios**).
     - Expected output format: current state, constraints & pain points, relevant diagrams.
   - Detect what code-exploration agents are available on the current platform, then dispatch all briefs to them concurrently. Sub-agents operate independently.
   - When all sub-agents complete, collect their findings.
   - Synthesize findings: review each sub-agent's output for completeness, resolve any cross-area inconsistencies, and compile each area's findings into the structured summary format (current state, constraints & pain points, relevant diagrams).

4. After all areas are investigated (via either method), present a consolidated investigation summary. For each area where the investigation revealed something that contradicts or refines a prior assumption, flag it explicitly: "New discovery in [area]: [what was found and the evidence]." Record each such discovery in the findings document's Discovery Log when the findings doc is compiled.
5. Ask the user to confirm the investigation findings before proceeding.
6. After the user confirms, apply **compile-findings-doc** to formalize the investigation results into a structured findings document before moving to evaluation. Any discoveries flagged in step 4 must appear in the findings document's Discovery Log.
</investigate-per-area>

<evaluate-solutions-per-area>
1. For each investigation area, guide the user through solution evaluation:
   - Ask: "Based on the investigation findings, what solution options do you see for [area name]?"
   - If the user has only one option, use **solution-brainstorming-prompts** to generate alternatives.
   - For each option, capture:
     - **Description**: What is the approach? (2–3 sentences)
     - **Pros**: Advantages relative to the current state and other options.
     - **Cons**: Disadvantages, risks, trade-offs.
     - **Feasibility**: Is it achievable? What unknowns remain?
   - Help the user identify **decision drivers** for this area (hard constraints and soft preferences).
   - Relate pros/cons back to decision drivers.
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
   - For each investigation area, prepare a focused brief containing:
     - The area name and one-line description.
     - The complete evaluation results: decision drivers, considered options with pros/cons, and the assumed solution.
     - Instructions to load the `draft-adr` skill and produce a complete, self-contained ADR.
   - Detect what agents are available on the current platform, then dispatch all briefs to sub-agents concurrently. Each sub-agent loads `draft-adr` independently.
   - When all sub-agents complete, collect and review each ADR for completeness and consistency.

4. After all ADRs are drafted (via either method), present them as a set and ask: "Would you like to adjust any ADR before compiling the solution document?"
5. Validate each ADR: confirm the chosen option follows logically from the decision drivers, all evaluated options are fairly represented, consequences include both positive and negative impacts, and the ADR can be understood without reading other ADRs.
6. Note: The chosen option in each ADR is the **assumed solution**. The solution document will adopt these. If an ADR decision changes later, the solution document should be updated accordingly.
</draft-area-adrs>

<compile-solution-doc>
1. Load the `write-solution-doc` skill's SKILL.md and apply its capabilities to produce the full solution document. Seed it with spike context:
   - **Business context**: The spike goal and problem statement.
   - **Current-state baseline**: The findings documents — evolve their diagrams and contracts from as-is → to-be.
   - **Assumed solutions**: The chosen option from each ADR.
2. The C4 diagrams should show the **target architecture**, not just the current state.
3. **Assess solution doc size and modularity**: After producing the initial solution document, apply the heuristics in **solution-doc-modularity** to determine whether it should be split:
   - Does the document exceed ~3000 words or have 5+ major sections?
   - Are there sections that are independently understandable and would be useful as standalone references (e.g., detailed API contracts for a specific service, infrastructure topology, data schemas)?
   - Would different reviewers or implementers need different sections?
   - If the answer to any of these is yes, identify candidate sections for extraction.
4. **Extract independent sections**: For each identified section:
   - Create a standalone document with the extracted content, ensuring it includes enough context to be understood independently (service context, role in system, back-reference to the hub).
   - Replace the extracted section in the main solution document with a concise summary (2–4 sentences) and a cross-reference link.
   - Apply the cross-reference format from **solution-doc-modularity**: hub summarizes + links out; extracted doc has back-reference + standalone context.
   - If the solution is small and simple (single service, few sections), skip extraction and keep a single document.
5. Compile the final output bundle:
   - **Findings Documents** (the output from compile-findings-doc — current-state architecture, one per area or consolidated)
   - **N ADRs** (the output from draft-area-adrs, one per investigation area)
   - **1 Solution Document** (the hub — target-state architecture with cross-references to modular sub-documents if split)
   - **Modular sub-documents** (if extracted — API contracts, infrastructure details, data schemas, etc.)
6. Validate the bundle: verify every ADR's chosen solution is reflected in the solution document, cross-references between all artifact types are consistent (ADRs cite findings doc sections, solution doc evolves findings doc diagrams from as-is → to-be), all diagrams in the solution doc match the assumed solutions, and extracted sub-documents have correct back-references to the hub.
7. Present the complete bundle to the user. Remind them:
   - The findings documents are the current-state record — keep them even if decisions change; they're useful for onboarding and future reference.
   - ADRs are formal decision records — they should be reviewed and approved by the team.
   - The solution document is the target-state architecture. If an ADR decision changes, update the solution document accordingly.
   - If the solution document was split into modular pieces, the hub + the relevant sub-document can be loaded independently — AI and reviewers don't need to load everything at once.
   - Consider version-controlling all artifacts in the project repository.
</compile-solution-doc>

<compile-findings-doc>
1. Determine the document strategy based on the number of investigation areas and their coupling:
   - **Per-area findings docs** (recommended for 2+ loosely-coupled areas): One findings document per investigation area. Each is self-contained and independently updatable.
   - **One consolidated findings doc** (for tightly-coupled areas or single-area spikes): All areas in one document with cross-area observations.
   - Ask the user: "Should we produce one findings document per area (easier to update independently) or one consolidated document (better for cross-cutting concerns)?"

2. For each findings document to produce, load the `write-solution-doc` skill's SKILL.md and apply its capabilities to produce a **current-state document**. The key adaptation: label all diagrams as "current state," replace RAID/RACI sections with **constraints & pain points** and **raw data & metrics** from the investigation findings. Include a **Discovery Log** section at the end of each findings document, following the format in **reference/discovery-log-guide.md**. Populate it with any discoveries flagged during investigation (from **investigate-per-area** step 4). Seed with Phase 2 results rather than gathering context from scratch.

3. Cross-reference between findings docs (if per-area): Note where one area's current state creates constraints for another. For example: "Area 1 (service boundaries): the monolithic `PaymentOrchestrator` → constrains Area 2 (communication): all calls are in-process, no service mesh exists."

4. Present each findings document to the user and ask: "Does this accurately capture the current state? Anything to add, correct, or remove?"

5. After confirmation, ensure the Discovery Log is up to date — any corrections from user feedback in step 4 should be recorded as discovery entries.

6. Note that the findings documents are now the **current-state baseline**:
   - Evaluation will compare solution options against this baseline.
   - ADRs will cite specific sections of findings docs as evidence.
   - The solution document will evolve each findings doc's diagrams and contracts from as-is → to-be.
</compile-findings-doc>

<summarize-required-changes>
1. Confirm prerequisites: the findings documents and solution document must be finalized. Ask: "Would you like me to generate a summary of the concrete code changes required to implement this solution?" Do not produce this artifact unless the user wants it — it is optional.
2. Determine code access: Ask: "Can I access the current codebase to verify the scope of changes?" 
   - **With code access**: Explore the relevant code paths identified in the findings documents. Trace which files, classes, and packages correspond to each area. Estimate scope concretely (file counts, LOC ranges, specific classes to modify). Mark estimates as code-verified.
   - **Without code access**: Generate the summary at an architectural level based on the findings and solution documents alone. Mark all scope estimates as unverified architectural approximations. Note where code access would improve accuracy.
3. For each investigation area/ADR, map the delta from current state (findings doc) to target state (solution doc) using the change categories defined in **change-summary-guide**:
   - **New**: services, modules, packages, files to create from scratch.
   - **Modified**: existing code to change, with scope estimates.
   - **Retired**: code to deprecate or delete, with timing (which migration phase).
   - **Configuration**: environment variables, feature flags, CI/CD, infrastructure-as-code changes.
   - **Data**: schema migrations, data transforms, ETL jobs.
   - **Dependency**: new libraries, frameworks, or external services to adopt.
   - **Test**: new or updated test suites needed.
4. Group changes by area/service, labeling each cluster with its ADR reference for traceability. Identify cross-cutting concerns that span multiple areas (e.g., shared library changes, auth integration, logging standards).
5. Compile the change summary document following the format in **change-summary-guide**. Include a notes section for caveats, assumptions, and open questions.
6. Present the summary and ask: "Does this change scope look accurate? Anything missing, overestimated, or underestimated?"
7. Note to the user: the change summary is a planning aid, not a detailed task breakdown or implementation plan. Each change item traces back to an ADR decision and a solution doc section. For effort estimation or sprint planning, use this summary as input — not as the final word.
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

<rule>After scope is confirmed, apply **investigate-per-area**. For multi-area spikes, this dispatches investigation to sub-agents in parallel per **multi-agent-orchestration**. For single-area spikes, investigation runs directly.</rule>

<rule>After investigation findings are confirmed by the user, apply **compile-findings-doc** to produce the findings document(s) before moving to evaluation. The findings documents are the current-state baseline for all subsequent phases.</rule>

<rule>After the findings document(s) are compiled and confirmed, apply **evaluate-solutions-per-area** for each area to brainstorm, evaluate, and select assumed solutions. Ground all evaluation in the findings documents — each option's pros/cons should reference specific findings.</rule>

<rule>After assumed solutions are selected for all areas, apply **draft-area-adrs**. For multi-area spikes, this dispatches ADR drafting to sub-agents in parallel per **multi-agent-orchestration**. For single-area spikes, ADR drafting runs directly.</rule>

<rule>After all ADRs are drafted and confirmed, apply **compile-solution-doc** to produce the consolidated solution document. Load the `write-solution-doc` skill to access its capabilities.</rule>

<rule>If the user provides pre-existing investigation findings (e.g., from a previous exploration), skip **investigate-per-area** and proceed directly to **compile-findings-doc** (to formalize the provided findings), then continue to **evaluate-solutions-per-area**.</rule>

<rule>If the spike has only one investigation area, the workflow still applies in full: investigate → compile findings doc → evaluate → draft one ADR → compile solution doc. All four artifact types (findings doc, ADR, solution doc, and optional change summary) are available even for single-area spikes.</rule>

<rule>If the problem is greenfield (no existing implementation), adapt **investigate-per-area** per the **greenfield-scenarios** guidance — research industry approaches, study constraints, and prototype instead of tracing code.</rule>

<rule>If the user wants to revise a specific area's assumed solution after ADRs are drafted, re-apply **draft-area-adrs** for that area only, then re-apply **compile-solution-doc** to update the solution document. The findings documents do not need to change unless the underlying current-state facts have changed.</rule>

<rule>If the user wants to continue a previous spike and dig deeper into specific unresolved areas (not just revise an existing ADR), apply **deep-dive-specific-areas**. This is distinct from simple ADR revision — the area needs re-investigation, not just text editing.</rule>

<rule>If the user wants to add a new investigation area mid-spike, apply **define-spike-scope** (step 4 only) to confirm the addition, then apply the remaining capabilities for the new area.</rule>

<rule>If the user asks for a quick recommendation without formal documentation, decline to use this skill — direct them to a regular conversation instead. See **inappropriate-scenarios**.</rule>

<rule>After each phase, pause and ask the user to confirm before proceeding. Do not skip phases unless the user explicitly requests it.</rule>

<rule>If sub-agents are not available on the current platform, fall back to sequential execution within the orchestrating agent. The spike workflow proceeds normally, just without parallelism.</rule>

<rule>After the solution document is compiled and presented, if the user wants to understand the implementation scope, apply **summarize-required-changes** to produce a concrete change summary. Skip this if the user declines or if the spike is purely exploratory with no implementation planned.</rule>

<rule>When the solution document is large (multiple services, complex API surfaces, extensive infrastructure), apply the modularity steps in **compile-solution-doc** to split independent sections into separate reference documents before presenting the final bundle. This keeps individual documents small enough for efficient AI context loading.</rule>

</rules>
