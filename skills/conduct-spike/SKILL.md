---
name: conduct-spike
description: Conduct spike investigations to explore technical problems and produce ADRs with a solution document. Use when conducting, investigating, evaluating, breaking down, or producing formal ADRs for a spike.
---

<when-to-use-this-skill>
- User wants to conduct a spike investigation on a technical problem or feature
- User needs to research, evaluate, and compare solution approaches for a complex problem before committing to one
- User wants to produce ADRs for each decision area alongside a consolidated solution document
- User needs to understand current implementation before proposing changes or solutions
- User wants to break down a large technical problem into independently decidable investigation areas
- User has pre-existing investigation findings and wants to formalize them into ADRs and a solution document
- User has a heavy spike with multiple investigation areas and wants to parallelize work across sub-agents for faster completion
</when-to-use-this-skill>

<knowledge>

<spike-definition>
A spike is an investigation activity aimed at reducing uncertainty around a technical problem. Unlike a full implementation, a spike focuses on research, prototyping, and decision-making. The output is knowledge and documented decisions — not production code.

A well-conducted spike produces:
- **N ADRs** — one Architecture Decision Record per independently decidable investigation area, each evaluating options and recommending a solution
- **1 Solution Document** — a consolidated document that weaves together the assumed/recommended solutions from all ADRs into a coherent system-level view, with C4 diagrams, API contracts, RAID analysis, and RACI matrix
</spike-definition>

<inappropriate-scenarios>
This skill is NOT appropriate when:
- The user wants a quick answer or informal recommendation without formal documentation — use a direct conversation instead
- The problem has already been decided and only needs implementation — skip the spike and proceed to planning
- The scope is trivial (single well-understood option, no architectural impact) — a spike would be overkill
- The user wants to write code or build a prototype immediately — spikes produce decisions, not production code
</inappropriate-scenarios>

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
| 3. Evaluate | Brainstorm and evaluate solution options per area | — |
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
This skill orchestrates skills and sub-agents. Key integration points:

| Skill / Agent | When invoked | What it contributes |
|---|---|---|
| `investigate-code` | During Phase 2 (investigate) — loaded by orchestrator or sub-agents | Codebase understanding, C4/sequence diagrams, pattern discovery |
| Code-exploration sub-agents | During Phase 2 (parallel investigation) | Concurrent codebase exploration per investigation area |
| `draft-adr` | During Phase 4 (draft ADRs) — loaded by orchestrator or sub-agents | Structured ADR per area: problem → drivers → options → evaluation → decision |
| Sub-agents with `draft-adr` | During Phase 4 (parallel ADR drafting) | Concurrent ADR drafting per investigation area |
| `write-solution-doc` | During Phase 5 (compile) | Consolidated solution document with topology, contracts, RAID, RACI |

When invoking a sub-skill, load its SKILL.md to access its full capabilities. The spike skill provides the high-level orchestration; the sub-skills and sub-agents handle the detailed execution.
</skill-integration-points>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Conducting a full end-to-end spike from scope to solution doc | Complete walkthrough with all 5 phases for a real-world migration problem | [examples/end-to-end-spike.md](examples/end-to-end-spike.md) |
| Conducting a single-area spike with narrow scope | Condensed workflow for a single-area spike producing one ADR + solution doc | [examples/single-area-spike.md](examples/single-area-spike.md) |
| Working from pre-existing investigation findings without re-investigating | Workflow starting from pre-existing investigation results | [examples/from-existing-findings.md](examples/from-existing-findings.md) |
| Decomposing a complex problem into investigation areas | Decomposition rubric with examples and edge cases | [reference/decomposition-rubric.md](reference/decomposition-rubric.md) |
| Conducting a heavy multi-area spike that benefits from parallel sub-agent execution | Walkthrough of dispatching investigation and ADR drafting to sub-agents in parallel | [examples/multi-agent-investigation.md](examples/multi-agent-investigation.md) |
| Dispatching investigation or ADR drafting to sub-agents in parallel | Full dispatch pattern, parallelization rules, and platform-detection guidance | [reference/multi-agent-orchestration.md](reference/multi-agent-orchestration.md) |
| Brainstorming solution options during the evaluate phase | Full set of solution-brainstorming prompts | [reference/solution-brainstorming-prompts.md](reference/solution-brainstorming-prompts.md) |

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
   - Load the `investigate-code` skill's SKILL.md to access its full capabilities.
   - Apply `investigate-code` to understand the current implementation relevant to this area:
     - Discover relevant code, configuration, and dependencies.
     - Trace control and data flows through the relevant paths.
     - Draw C4 or sequence diagrams if they help clarify the current state.
     - Discover implementation patterns and note any inconsistencies.
   - Compile findings into a structured summary:
     - **Current state**: What exists today, key components, data flows.
     - **Constraints & pain points**: What's limiting, broken, or hard to change.
     - **Relevant diagrams**: C4/sequence diagrams showing current architecture.

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

4. After all areas are investigated (via either method), present a consolidated investigation summary and ask the user to confirm before proceeding to evaluation.
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
3. Repeat for each investigation area.
4. Validate each area's evaluation: confirm at least 2 options were considered, pros/cons relate to decision drivers, and the assumed solution follows logically from the comparison.
5. Present a summary table of all areas with their assumed solutions.
</evaluate-solutions-per-area>

<draft-area-adrs>
1. Determine the execution strategy based on the number of investigation areas:
   - **Single ADR (1 area)**: Draft directly using the sequential steps below (step 2).
   - **Multiple ADRs (2+ areas)**: Dispatch all areas' evaluation results to sub-agents in parallel (step 3). See **multi-agent-orchestration** for the dispatch pattern.

2. **For single ADR drafting (direct execution)**:
   - Load the `draft-adr` skill's SKILL.md to access its full capabilities.
   - Apply `draft-adr` to produce a complete ADR for the area:
     - **Problem statement**: The investigation area's scope, refined from the spike definition.
     - **Decision drivers**: Hard constraints and soft preferences identified during evaluation.
     - **Considered options**: All options brainstormed and evaluated, with pros/cons.
     - **Chosen option**: The assumed solution with synthesized justification.
     - **Consequences**: Positive impacts, risks, and mitigation strategies.
   - Each ADR should be self-contained and independently readable.
   - Use the standard ADR template and metadata format.

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
1. Load the `write-solution-doc` skill's SKILL.md to access its full capabilities.
2. Seed the solution document with context from the spike:
   - **Business context**: The spike goal and problem statement.
   - **Assumed solutions**: The chosen option from each ADR forms the basis of the solution architecture.
   - **Current-state diagrams**: C4/sequence diagrams from the investigation phase, updated to reflect the assumed solutions.
3. Apply `write-solution-doc` to produce the full solution document:
   - Walk through its capabilities in the order defined by that skill (typically: clarify business context, draw C4 topology and sequence diagrams, design API/event schemas, list dependencies/maintainers/RAID/RACI, then structure the final document).
   - For each step, use the pre-seeded spike context as the starting point rather than re-gathering from scratch.
   - The C4 diagrams should show the **target architecture** (post-solution), not just the current state.
4. Compile the final output bundle:
   - **1 Solution Document** (the consolidated output from write-solution-doc)
   - **N ADRs** (the output from draft-area-adrs, one per investigation area)
5. Validate the bundle: verify every ADR's chosen solution is reflected in the solution document, cross-references between ADRs and the solution doc are consistent, and all diagrams in the solution doc match the assumed solutions.
6. Present the complete bundle to the user. Remind them:
   - ADRs are formal decision records — they should be reviewed and approved by the team.
   - The solution document adopts the assumed solution from each ADR. If an ADR decision changes, update the solution document accordingly.
   - Consider version-controlling both ADRs and the solution document in the project repository.
</compile-solution-doc>

</capabilities>

<rules>

<rule>When the user initiates a spike investigation, apply **define-spike-scope** to establish the goal and investigation areas. Do not skip to investigation until the scope is confirmed.</rule>

<rule>After scope is confirmed, apply **investigate-per-area**. For multi-area spikes, this dispatches investigation to sub-agents in parallel per **multi-agent-orchestration**. For single-area spikes, investigation runs directly.</rule>

<rule>After all areas are investigated and findings confirmed, apply **evaluate-solutions-per-area** for each area to brainstorm, evaluate, and select assumed solutions.</rule>

<rule>After assumed solutions are selected for all areas, apply **draft-area-adrs**. For multi-area spikes, this dispatches ADR drafting to sub-agents in parallel per **multi-agent-orchestration**. For single-area spikes, ADR drafting runs directly.</rule>

<rule>After all ADRs are drafted and confirmed, apply **compile-solution-doc** to produce the consolidated solution document. Load the `write-solution-doc` skill to access its capabilities.</rule>

<rule>If the user provides pre-existing investigation findings (e.g., from a previous exploration), skip **investigate-per-area** and proceed directly to **evaluate-solutions-per-area** using the provided findings as context.</rule>

<rule>If the spike has only one investigation area, the workflow still applies in full: investigate → evaluate → draft one ADR → compile solution doc. The solution doc will be simpler but still structured.</rule>

<rule>If the problem is greenfield (no existing implementation), adapt **investigate-per-area** per the **greenfield-scenarios** guidance — research industry approaches, study constraints, and prototype instead of tracing code.</rule>

<rule>If the user wants to revise a specific area's assumed solution after ADRs are drafted, re-apply **draft-area-adrs** for that area only, then re-apply **compile-solution-doc** to update the solution document.</rule>

<rule>If the user wants to add a new investigation area mid-spike, apply **define-spike-scope** (step 4 only) to confirm the addition, then apply the remaining capabilities for the new area.</rule>

<rule>If the user asks for a quick recommendation without formal documentation, decline to use this skill — direct them to a regular conversation instead. See **inappropriate-scenarios**.</rule>

<rule>After each phase, pause and ask the user to confirm before proceeding. Do not skip phases unless the user explicitly requests it.</rule>

<rule>When dispatching work to sub-agents, prepare focused briefs that are self-contained — each sub-agent must have all the context it needs without depending on other sub-agents' results.</rule>

<rule>If sub-agents are not available on the current platform, fall back to sequential execution within the orchestrating agent. The spike workflow proceeds normally, just without parallelism.</rule>

<rule>After collecting results from parallel sub-agents, always synthesize and review for cross-area consistency before presenting to the user. Sub-agents work independently and may produce overlapping or contradictory findings.</rule>

</rules>
