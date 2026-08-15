---
name: conduct-spike
description: Conduct spike investigations producing ADRs, findings, solution docs, and change summaries. Use when scoping, investigating, evaluating, discussing ADRs needing investigation, formalizing, continuing, deep-diving, modularizing, summarizing changes, syncing updates.
---

<when-to-use-this-skill>
- User wants to conduct a spike investigation on a technical problem or feature — researching, evaluating, and comparing solution approaches before committing to one
- User wants to produce ADRs for each decision area alongside a consolidated solution document
- User is discussing an ADR (drafting, reviewing, or adjusting a decision) and the outcome depends on unverified assumptions, unknown feasibility, or missing evidence that needs investigation
- User needs to understand current implementation before proposing changes or solutions
- User wants to break down a large technical problem into independently decidable investigation areas, or split a large solution document into modular sub-documents
- User has pre-existing investigation findings and wants to formalize them into ADRs and a solution document
- User wants to continue a previous spike by digging deeper into one or more specific investigation areas that were not fully resolved
- User wants to summarize the concrete code changes required to implement the chosen solution (change summary)
- User found new evidence or changed a decision and wants every artifact — findings doc, ADR, solution doc, change summary — updated together and kept consistent
- Do NOT load for plain ADR drafting, solution-doc writing, or code investigation — `draft-adr`, `write-solution-doc`, and `investigate-code` handle those directly; load only when a decision needs investigation first
</when-to-use-this-skill>

<knowledge>

<spike-definition>
A spike reduces uncertainty via research and prototyping; its output is documented decisions, not production code. It produces: **Findings Documents** (current-state baseline, each embedding its area's evidence map — `file:line` entry points, call chains, evidence ledger, searched-negatives), **N ADRs** (one per area), **1 Solution Document** (target-state architecture with C4, API contracts, RAID, RACI — decision-only), and optionally **1 Change Summary** (code-level changes traceable to ADRs).
</spike-definition>

<spike-artifact-layout>
All spike artifacts version together in **one folder per spike**:

```
spikes/<spike-name>/
├── adrs/                   # one file per ADR — ADR-001-<kebab-name>.md, …
├── solution.md             # the solution document (hub)
├── change-summary.md       # only when requested
└── docs/                   # findings documents — findings-<area>.md each
```

Modularized solution sub-docs (see **solution-doc-modularity**) live in `solution-doc/` next to the hub. Artifacts cross-reference each other with relative paths inside the spike folder.
</spike-artifact-layout>

<inappropriate-scenarios>
Do NOT use for: quick answers without formal documentation, already-decided problems needing only implementation, trivial scope with no architectural impact, or immediate prototyping — spikes produce decisions, not production code.
</inappropriate-scenarios>

<findings-document>
A findings doc captures the **current-state architecture** (via `write-solution-doc`'s **current-state mode**, so it is directly transformable into the solution doc) and is the spike's **evidence home**: each embeds its area's evidence map — `file:line` annotations, sequence diagrams for call chains, an evidence ledger (claim → verdict → confidence, 5-tag model), and searched-negatives. ADRs, change summaries, and sub-agents cite findings docs without re-scanning. See **reference/findings-document-guide.md**.
</findings-document>

<change-summary>
A change summary translates the delta between findings (current state) and solution doc (target state) into change items grouped by category — New, Modified, Retired, Configuration, Data, Dependency, Test — traceable to ADRs. Estimate quality depends on code access; always state which mode applies. Consumed by **orchestrate-feature-delivery**. See **reference/change-summary-guide.md**.
</change-summary>

<option-tech-details>
Tech details (target-state diagrams + code change profiles) per ADR option are produced by `draft-adr`'s **detail-options-tech**, grounded in the findings doc's evidence map. During evaluation and ADR drafting, delegate to `draft-adr` rather than producing them directly (see **professional-doc-authoring**).
</option-tech-details>

<solution-doc-modularity>
When a solution doc exceeds ~3000 words or 5+ major sections, split independently understandable sections into standalone docs: the main doc becomes a hub with 2–4 sentence summaries and cross-references; each extracted doc must stand alone and back-reference the hub. See **reference/solution-doc-modularity-guide.md**.
</solution-doc-modularity>

<continuation-mode>
Continuing a previous spike is **another round of the same workflow**, seeded with the prior spike's artifacts: confirm which areas to revisit (unselected areas stay as-is), then run the standard capabilities in **revise-in-place** mode — investigate-per-area already seeds sub-agents with existing evidence maps; compile-findings-doc, draft-area-adrs, and compile-solution-doc already support revising; sync-update-artifacts propagates downstream. See **examples/continue-prior-spike.md**.
</continuation-mode>

<greenfield-scenarios>
Greenfield (no existing implementation): research industry approaches and similar systems, study operational constraints (cloud, team, compliance), build proof-of-concept prototypes instead of tracing code. Remaining phases proceed unchanged.
</greenfield-scenarios>

<multi-agent-orchestration>
Dispatch investigation (Phase 2), findings-doc compilation (Phase 2b), evaluation (Phase 3), ADR drafting (Phase 4), and solution-doc compilation (Phase 5) — including single-task spikes — to sub-agents whenever one is available; direct execution is only the fallback. Primary goal: keep the orchestrating agent's context small; parallel speed is secondary. Dispatch pattern and fallback rules: **reference/multi-agent-orchestration.md**.
</multi-agent-orchestration>

<sub-agent-verification>
Sub-agent results (Phases 2, 2b, 4, 5) are questioned and verified before acceptance. The original sub-agent instance is never reused — every verifier/re-investigator is a NEW same-type sub-agent. Principles: independence, primary sources (code/docs/data/logs), traceability (every verdict maps to one challenge). Compilations verify fidelity to already-verified material; Phase 3 returns **provisional assumed solutions** verified at the Phase 4 ADR. The loop caps at 3 rounds — at the cap, present both versions and let the user decide. Full rules: **reference/verification-protocol.md**.
</sub-agent-verification>

<problem-decomposition-guide>
Target 2–5 investigation areas: fewer than 2 means the problem may not need a spike; more than 5 suggests scope is too broad. Full rubric with heuristics and edge cases: **reference/decomposition-rubric.md**.
</problem-decomposition-guide>

<adr-uncertainty-signals>
During ADR discussion (drafting, reviewing, or adjusting a decision), suggest a spike when the decision hinges on something reasoning alone cannot settle: **unverified assumption**, **unknown feasibility**, **missing measurement**, **undecidable comparison**, **uninvestigated dependency**, or **reviewer disagreement**.
</adr-uncertainty-signals>

<professional-doc-authoring>
ADRs and the solution document are always written by their owning skills — never hand-edited: every ADR write goes through `draft-adr`; every findings/solution-doc write through `write-solution-doc` (findings in current-state mode). Load the owning skill's SKILL.md and apply its capabilities, seeding with the existing document plus the change — inside the spike workflow or standalone. Bypassing the owning skill degrades the artifact.
</professional-doc-authoring>

<artifact-maintenance-doctrine>
Artifacts form a dependency chain — **Findings Docs → ADRs → Solution Doc → Change Summary** — and are kept **at the latest state**: rewrite changed sections **in place**, **delete** superseded content (git is the only history) — no "Note:", "Updated", "Changed", "v2", "As of", "Previously", no changelogs. Notes allowed only in change summary, findings docs, conversation.

| Change origin | Propagate to |
|---|---|
| Findings doc (new evidence or correction) | ADR → solution doc → change summary |
| ADR decision change | Solution doc → change summary |
| Solution doc change | Change summary |

Propagation stops at the first artifact a change does not affect. The change summary is **never final** — recompute it whenever its baseline or target changes. Full protocol: **reference/artifact-maintenance-guide.md** (rewrite-in-place procedure, notes allowed/banned map, no-note scan, propagation matrix).
</artifact-maintenance-doctrine>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Full end-to-end spike (scope → solution doc) | 5-phase walkthrough for a real migration problem | [examples/end-to-end-spike.md](examples/end-to-end-spike.md) |
| Single-area spike with narrow scope | Single-area workflow with one ADR + solution doc | [examples/single-area-spike.md](examples/single-area-spike.md) |
| Working from pre-existing findings without re-investigating | Workflow starting from existing investigation results | [examples/from-existing-findings.md](examples/from-existing-findings.md) |
| Decomposing a complex problem into areas | Decomposition rubric with examples and edge cases | [reference/decomposition-rubric.md](reference/decomposition-rubric.md) |
| Heavy multi-area spike benefiting from parallel sub-agents | Multi-area parallel dispatch walkthrough with evidence maps embedded | [examples/multi-agent-investigation.md](examples/multi-agent-investigation.md) |
| Continuing a previous spike by digging deeper into unresolved areas | Continuation walkthrough: load prior artifacts, confirm subset, run the workflow in revise-in-place mode | [examples/continue-prior-spike.md](examples/continue-prior-spike.md) |
| Dispatching investigation, findings-doc, evaluation, ADR, or solution-doc work to sub-agents | Dispatch pattern, context-preservation rationale, fallback rules | [reference/multi-agent-orchestration.md](reference/multi-agent-orchestration.md) |
| Executing a workflow phase (investigate, evaluate, draft ADRs, compile, summarize, sync) | Full phase procedures — dispatch briefs, direct-execution steps, validation checklists | [reference/workflow-procedure.md](reference/workflow-procedure.md) |
| Raising challenges on a sub-agent's returned result | Skeptic questioning dimensions and questions per dimension | `question-everything`: [reference/questioning-dimensions.md](../question-everything/reference/questioning-dimensions.md) |
| Verifying challenges before acceptance | Verification brief, dispatch rules, comparison and loop-control rules | [reference/verification-protocol.md](reference/verification-protocol.md) |
| Seeing a worked verification loop — accept vs. contradict → new round | Examples of the question → verify → accept/re-investigate loop | [examples/confirming-result.md](examples/confirming-result.md), [examples/contradicting-result.md](examples/contradicting-result.md) |
| Producing or understanding findings docs (format, strategy, evidence map) | Findings doc format, strategy selection, evidence-map embedding rules | [reference/findings-document-guide.md](reference/findings-document-guide.md) |
| Rewriting or syncing artifacts after a fact/decision change — keeping them at the latest state | Rewrite-in-place protocol, notes allowed/banned map, no-note scan, propagation matrix, consistency checklist | [reference/artifact-maintenance-guide.md](reference/artifact-maintenance-guide.md) |
| Generating a change summary | Format, categories, and code-access guidance | [reference/change-summary-guide.md](reference/change-summary-guide.md) |
| Splitting a large solution doc into modular pieces | Splitting heuristics, patterns, and validation checklist | [reference/solution-doc-modularity-guide.md](reference/solution-doc-modularity-guide.md) |
| Producing a change summary with code access, all categories | End-to-end change summary with code-verified scope estimates | [examples/change-summary-example.md](examples/change-summary-example.md) |
| Suggesting a spike when ADR discussion hinges on unverified assumptions | Worked example of detecting ADR uncertainty and offering a focused spike | [examples/adr-uncertainty-spike-suggestion.md](examples/adr-uncertainty-spike-suggestion.md) |
| Seeing a fact/decision change propagated through findings, ADR, solution doc, and change summary | Walkthrough of syncing all artifacts after new evidence flips an ADR decision, with the rewrite-in-place before/after | [examples/sync-update-across-artifacts.md](examples/sync-update-across-artifacts.md) |
| Placing produced artifacts into the per-spike folder | Worked example of the spike folder layout with every artifact placed | [examples/spike-artifact-layout.md](examples/spike-artifact-layout.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<run-spike-workflow>
1. Apply **define-spike-scope**; do not proceed until scope is confirmed.
2. Apply **investigate-per-area** (dispatch when available; record **evidence maps**; verify with **verify-sub-agent-results**); a new direction loops to step 1.
3. Apply **compile-findings-doc**, embedding each area's evidence map inline.
4. Apply **evaluate-solutions-per-area** to select an assumed solution per area.
5. Apply **draft-area-adrs**, verifying each before saving.
6. Apply **compile-solution-doc** to consolidate ADRs into the solution document.
7. Pause for user confirmation after each phase; skip only if the user requests it.
</run-spike-workflow>

<define-spike-scope>
1. Ask: "What technical problem or feature do you want to spike? Describe it in 2–4 sentences." Then clarify the goal — what question(s) to answer, what uncertainty to reduce?
2. Decompose into **investigation areas** per **problem-decomposition-guide** (target 2–5): propose a breakdown with one-line descriptions; confirm split/merge/add/remove.
3. Confirm the ordered list and record the scope summary: goal (1 sentence) + areas.
4. Validate: each area independently decidable, count 2–5 (or justified), goal clear enough to know completion; note greenfield (see **greenfield-scenarios**).
</define-spike-scope>

<investigate-per-area>
1. Dispatch each area to a code-exploration sub-agent when one is available — even single-area; fall back to direct investigation only when none exists (see **multi-agent-orchestration**).
2. **Dispatch**: announce "Dispatching investigation of [N] area(s) to a sub-agent"; brief per area (spike goal, brownfield/greenfield, existing evidence map; expected output = per-area evidence map); dispatch concurrently; collect and synthesize, resolving cross-area inconsistencies. Full brief: **reference/workflow-procedure.md**.
3. **Direct (fallback)**: load `investigate-code` — its **spike-integration** scopes to the area and updates the evidence map; compile current state, constraints & pain points, diagrams.
4. Apply **verify-sub-agent-results**; present a consolidated summary; ask: "Is the investigation complete, or continue in a new direction?" — a new direction loops to scope definition.
5. Hand off to **compile-findings-doc** with the recorded evidence maps.
</investigate-per-area>

<evaluate-solutions-per-area>
1. Dispatch each area to a sub-agent when one is available — even single-area; fall back to direct evaluation only when none exists (see **multi-agent-orchestration**).
2. **Dispatch**: announce "Dispatching evaluation of [N] area(s) to a sub-agent"; brief per area (spike goal, findings-doc evidence sections; load `draft-adr`, run its evaluate chain — **define-decision-drivers** → **define-considered-options** → **evaluate-options** — with the user dialog inside the sub-agent session; return the assumed solution); collect and review. Full brief: **reference/workflow-procedure.md**.
3. **Direct (fallback)**: load `draft-adr` and apply its evaluate chain, seeded with the findings doc (its **evaluate-options** auto-applies **detail-options-tech** when findings exist). Record the **assumed solution** — provisional until ADR review.
4. **Check for findings gaps**: if any option revealed a constraint, risk, or fact not in the findings doc, update the affected sections.
5. Validate spike-specific checks (tech details grounded in the evidence map — no invented code; assumed solution follows logically; corrections captured); present the summary table — the handoff to **draft-area-adrs**.
</evaluate-solutions-per-area>

<draft-area-adrs>
1. Dispatch each ADR to a sub-agent when one is available — even single-ADR; fall back to direct drafting only when none exists (see **multi-agent-orchestration**).
2. **Dispatch**: announce "Dispatching ADR drafting for [N] area(s) to a sub-agent"; brief per area (evaluation results — drivers, options with pros/cons, tech details per option, assumed solution, findings-doc evidence sections; load `draft-adr`, apply **compile-adr**); collect and review. Full brief: **reference/workflow-procedure.md**.
3. **Direct drafting or revising (fallback)**: load `draft-adr` and apply **compile-adr** seeded with the evaluation results; run the full chain only if evaluation was skipped. Revising = same procedure seeded with the existing ADR plus the change; never hand-edit (see **professional-doc-authoring**).
4. Apply **verify-sub-agent-results**; save each ADR to `<spike-folder>/adrs/ADR-00X-<kebab-name>.md` (see **save-artifacts**); ask: "Would you like to adjust any ADR before compiling the solution document?" On uncertainty, apply **suggest-spike-on-adr-uncertainty** first.
5. Keep each ADR at the latest state (see **artifact-maintenance-doctrine**); validate via `draft-adr`'s **compile-adr** checklist + spike checks (tech details in each option's evaluation, standalone-readable, cites the findings doc); run the **no-note scan** until clean.
</draft-area-adrs>

<verify-sub-agent-results>
1. Apply `question-everything`'s **question-the-result** to raise prioritized challenges.
2. Dispatch a NEW same-type sub-agent — never the original — to verify each challenge against primary sources; collect per-challenge verdicts (AGREE / DISAGREE / UNCERTAIN), each traceable to its challenge.
3. Accept only if every material verdict is AGREE; if any is DISAGREE or UNCERTAIN, dispatch a NEW same-type sub-agent to redo the investigation with the corrected understanding, then loop to step 1.
4. Loop until all AGREE or the 3-round cap; at the cap, present both versions to the user — never silently pick one.
5. Synthesize into the findings doc or save the ADR only after verification. Full loop: **reference/verification-protocol.md**.
</verify-sub-agent-results>

<compile-solution-doc>
1. Dispatch to a sub-agent when one is available; fall back to direct compilation only when none exists (see **multi-agent-orchestration**).
2. **Dispatch**: announce "Dispatching solution-doc compilation to a sub-agent"; brief (spike goal, findings docs, assumed solutions — chosen option from each ADR; load `write-solution-doc`, produce a **target-state** doc in **baseline-input mode**); collect and review. Full brief: **reference/workflow-procedure.md**.
3. **Direct (fallback)**: load `write-solution-doc` in **baseline-input mode** (evolve findings-doc sections as-is → to-be; C4 shows the **target architecture**) — for compiling AND revising. Seed with spike goal, findings docs, assumed solutions.
4. **Assess modularity** per **solution-doc-modularity**: if >~3000 words or 5+ major sections, extract sections into standalone docs with back-references; replace each in the hub with a 2–4 sentence summary + link.
5. Save per **spike-artifact-layout** (see **save-artifacts**): findings → `docs/`, ADRs → `adrs/`, solution doc → `solution.md`.
6. Keep the solution doc at the latest state (see **artifact-maintenance-doctrine**).
7. Validate: every ADR's chosen solution reflected, cross-references consistent, diagrams match, sub-docs back-reference; run the **no-note scan** until clean.
8. Present the bundle: findings = current-state record; ADRs = decision records (review/approve); solution doc = target-state architecture; version-control together.
</compile-solution-doc>

<compile-findings-doc>
1. Determine the document strategy: **per-area** (2+ loosely-coupled areas) or **one consolidated doc** (tightly-coupled or single-area). Ask the user.
2. Dispatch to a sub-agent when one is available; fall back to direct compilation only when none exists (see **multi-agent-orchestration**).
3. **Dispatch**: announce "Dispatching findings-doc compilation to a sub-agent"; brief (document strategy, Phase 2 results **with each area's evidence map**; load `write-solution-doc`, produce a **current-state document** in **current-state mode** with evidence maps embedded); collect and review. Full brief: **reference/workflow-procedure.md**.
4. **Direct (fallback)**: load `write-solution-doc` in **current-state mode** (see `write-solution-doc`'s **reference/current-state-mode.md**), seeded with Phase 2 results and their evidence maps.
5. Validate each area's evidence map is embedded inline per **reference/findings-document-guide.md**: `file:line` entry points, call chains as sequence diagrams, an **Evidence & Verification** section per area (evidence ledger — claim → verdict → evidence `file:line` → confidence, `investigate-code` 5-tag model — and searched-negatives). Never vague references; never present inference as evidence.
6. Cross-reference between findings docs (if per-area): note cross-area constraints.
7. Present each doc and ask: "Does this accurately capture the current state? Anything to add, correct, or remove?" Save to `<spike-folder>/docs/findings-<area>.md` (see **save-artifacts**).
8. Findings docs are the **current-state baseline and evidence home**; update the evidence map the moment new evidence is found — no round/version tracking.
</compile-findings-doc>

<save-artifacts>
1. Determine the spike folder path (`spikes/<spike-name>/`) — ask the user or detect an existing spike folder.
2. Create `<spike-folder>/adrs/` and `<spike-folder>/docs/` per **spike-artifact-layout**.
3. Save: findings → `docs/findings-<area>.md`; each ADR → `adrs/ADR-00X-<kebab-name>.md`; solution doc → `solution.md` (sub-docs → `solution-doc/`); change summary → `change-summary.md` (only when requested).
4. Rewrite cross-references as relative paths inside the spike folder; confirm the layout.
</save-artifacts>

<summarize-required-changes>
1. Confirm findings + solution doc finalized; ask: "Would you like me to generate a summary of the concrete code changes required to implement this solution?" Optional — never produce unless requested.
2. Determine code access: **with access**, trace code paths and estimate scope (file counts, LOC ranges, classes to modify), mark code-verified; **without access**, generate at architectural level, mark estimates as unverified.
3. Per area/ADR, map the delta using **change-summary-guide** categories (New, Modified, Retired, Configuration, Data, Dependency, Test); group by area/service with ADR references; identify cross-cutting concerns.
4. Compile per **change-summary-guide** with a notes section; save to `<spike-folder>/change-summary.md` (see **save-artifacts**).
5. Present and ask: "Does this change scope look accurate? Anything missing, overestimated, or underestimated?"
6. The change summary is **never final** — if findings or the solution doc change, apply **sync-update-artifacts**.
</summarize-required-changes>

<sync-update-artifacts>
1. Identify the change and its origin artifact: new evidence/correction (findings doc), changed decision (ADR), or target-state change (solution doc).
2. Trace the propagation path with **artifact-maintenance-doctrine**.
3. Apply the change at the origin through its owning skill — `draft-adr` for ADRs, `write-solution-doc` for findings/solution docs (see **professional-doc-authoring**) — rewriting affected sections **in place** per the latest-state protocol.
4. Run the **no-note scan** on each touched ADR and solution doc (see **reference/artifact-maintenance-guide.md**); rewrite until clean.
5. Propagate downstream in order, re-running the owning capability seeded with the current artifact plus the delta; recompute the change summary's affected clusters.
6. Validate consistency — every artifact reflects the latest facts; ADRs cite only current findings; the solution doc mirrors every ADR; the change summary traces to current ADRs.
7. Present the delta in conversation, never inside the artifacts (see **artifact-maintenance-doctrine**).
</sync-update-artifacts>

<continue-prior-spike>
1. Load the prior spike's artifacts — scope summary, findings docs, ADRs, solution doc, change summary (if any). If unavailable, ask the user to share or summarize them.
2. Confirm the continuation scope: which areas to revisit, the open question for each, and which areas stand as-is.
3. Validate: selected areas independently decidable; unselected areas' decisions preserved.
4. Run the standard workflow in revise-in-place mode per **continuation-mode**: **investigate-per-area** (seed sub-agents with existing evidence maps so covered code is not re-scanned; target only what answers the open questions), then **compile-findings-doc** → **evaluate-solutions-per-area** → **draft-area-adrs**.
5. Apply **sync-update-artifacts** to propagate changes downstream.
6. Ask whether to continue with another round or conclude; a continuation becomes the new scope via **define-spike-scope**.
</continue-prior-spike>

<suggest-spike-on-adr-uncertainty>
1. Detect uncertainty signals via **adr-uncertainty-signals** — unverified assumption, unknown feasibility, missing measurement, undecidable comparison, uninvestigated dependency, reviewer disagreement.
2. Name the uncertainty precisely: "This decision seems to hinge on [the unverified assumption / the unknown fact / the unresolved comparison]." Explain why it matters.
3. Offer: "Would you like to spike this before finalizing the ADR?" — never start without explicit confirmation. If agreed, define a focused scope (single goal, 1–3 areas) via **define-spike-scope**; treat the ADR as provisional.
4. If declined, continue the ADR flow (via `draft-adr` per **professional-doc-authoring**) and record the uncertainty as a **risk** in the ADR's Consequences section — never a free-form note.
</suggest-spike-on-adr-uncertainty>

</capabilities>

<rules>
<rule>When the user initiates a spike investigation, apply **run-spike-workflow** to orchestrate all phases from scope definition through solution compilation.</rule>
<rule>If the user provides pre-existing investigation findings, skip **investigate-per-area** and proceed directly to **compile-findings-doc**, then continue to **evaluate-solutions-per-area**.</rule>
<rule>If the spike has only one area, the workflow still applies in full. If the problem is greenfield, adapt **investigate-per-area** per **greenfield-scenarios**.</rule>
<rule>Mid-spike modifications: add an area → apply **define-spike-scope** then the remaining capabilities; revise an assumed solution → re-apply **draft-area-adrs** then **compile-solution-doc**; continue unresolved areas from a previous spike → apply **continue-prior-spike**, then the standard workflow.</rule>
<rule>If the user asks for a quick recommendation without formal documentation, decline (see **inappropriate-scenarios**).</rule>
<rule>When dispatching to a sub-agent, include the area's findings doc (or its evidence sections) in the brief and instruct it to skip covered code.</rule>
<rule>After the solution doc is compiled: if the user wants implementation scope, apply **summarize-required-changes**; if the doc is large, apply the modularity steps in **compile-solution-doc**.</rule>
<rule>When the user discusses an ADR (drafting, reviewing, or adjusting it) and the decision depends on an unverified assumption, unknown feasibility, missing evidence, or an unresolved option comparison, apply **suggest-spike-on-adr-uncertainty** before the ADR is finalized.</rule>
<rule>When updating or revising an ADR, always apply **draft-area-adrs** (through `draft-adr`); when updating or refreshing the solution doc, always apply **compile-solution-doc** (through `write-solution-doc`); never hand-edit either (see **professional-doc-authoring**).</rule>
<rule>When a fact or decision changes — new evidence, findings correction, ADR revision, continuation round, or solution-doc refresh — apply **sync-update-artifacts** to propagate the change through every affected downstream artifact.</rule>
<rule>When the user wants tech implementation detail per option (diagrams, code diffs, change locations), delegate to `draft-adr`'s **detail-options-tech** during **evaluate-solutions-per-area** (see **option-tech-details**).</rule>
<rule>When compiling or updating any artifact, apply **save-artifacts** to write it into its spike folder location per **spike-artifact-layout**.</rule>
</rules>
