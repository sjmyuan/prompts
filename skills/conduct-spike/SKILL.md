---
name: conduct-spike
description: Conduct spike investigations producing ADRs, findings, and solution docs. Use when scoping, investigating decisions, evaluating options, discussing undecided ADRs, formalizing findings, continuing spikes, modularizing, syncing updates.
---

<when-to-use-this-skill>
- Conduct a spike investigation on a technical problem — researching, evaluating, and comparing solution approaches before committing to one
- Produce ADRs for each decision area alongside a consolidated solution document
- Discuss an ADR (drafting, reviewing, or adjusting) whose outcome depends on unverified assumptions, unknown feasibility, or missing evidence
- Understand current implementation as an investigation area within a spike before a decision is made
- Break a large technical problem into independently decidable areas, or split a large solution document into modular sub-documents
- Formalize pre-existing investigation findings into ADRs and a solution document
- Continue a previous spike, digging deeper into specific areas not fully resolved
- Sync every artifact — findings doc, ADR, solution doc — after new evidence or a changed decision
- Do NOT load for plain ADR drafting, solution-doc writing, or code investigation — `draft-adr`, `write-solution-doc`, `investigate-code` handle those; load only when a decision needs investigation first
</when-to-use-this-skill>

<knowledge>

<spike-definition>
A spike reduces uncertainty via research and prototyping; its output is documented decisions, not production code. It produces: **Findings Documents** (current-state baseline, each embedding its area's evidence map — `file:line` entry points, call chains, evidence ledger, searched-negatives), **N ADRs** (one per area), and **1 Solution Document** (target-state architecture with C4, API contracts, RAID, RACI — decision-only).
</spike-definition>

<spike-artifact-layout>
All spike artifacts version together in **one folder per spike**:

```
spikes/<spike-name>/
├── adrs/                   # one file per ADR — ADR-001-<kebab-name>.md, …
├── solution.md             # the solution document (hub)
└── docs/                   # findings documents — findings-<area>.md each
```

Modularized solution sub-docs (see **solution-doc-modularity**) live in `solution-doc/` next to the hub. Artifacts cross-reference each other with relative paths inside the spike folder.

Every producing capability saves its output per this layout: determine the spike folder path (ask the user or detect an existing `spikes/<spike-name>/`), create `adrs/` and `docs/` as needed, then confirm the layout after saving.
</spike-artifact-layout>

<inappropriate-scenarios>
Do NOT use for: quick answers without formal documentation, already-decided problems needing only implementation, trivial scope with no architectural impact, or immediate prototyping — spikes produce decisions, not production code.
</inappropriate-scenarios>

<findings-document>
Captures **current-state architecture** (via `write-solution-doc` **current-state mode**, directly transformable to the solution doc) and is the spike's **evidence home**: embeds each area's evidence map — `file:line` annotations, sequence diagrams for call chains, evidence ledger (claim → verdict → confidence, 5-tag model), searched-negatives. ADRs and sub-agents cite it without re-scanning. Details: **reference/findings-document-guide.md**.
</findings-document>

<option-tech-details>
ADR option tech details (target-state diagrams + code change profiles) come from `draft-adr` **detail-options-tech**, grounded in the findings doc's evidence map — delegate to `draft-adr` during evaluation and ADR drafting (see **professional-doc-authoring**).
</option-tech-details>

<solution-doc-modularity>
When a solution doc exceeds ~3000 words or 5+ major sections, split standalone sections into docs: hub keeps 2–4 sentence summaries + cross-refs; each extracted doc stands alone and back-references the hub. Details: **reference/solution-doc-modularity-guide.md**.
</solution-doc-modularity>

<continuation-mode>
Continuing a spike = **another round of the same workflow**, seeded with prior artifacts: confirm which areas to revisit (unselected stay as-is), run capabilities in **revise-in-place** mode; **sync-update-artifacts** propagates downstream. See **examples/continue-prior-spike.md**.
</continuation-mode>

<greenfield-scenarios>
No existing implementation: research industry approaches and similar systems, study operational constraints (cloud, team, compliance), build proof-of-concept prototypes instead of tracing code; remaining phases unchanged.
</greenfield-scenarios>

<multi-agent-orchestration>
Dispatch investigation, findings-doc compilation, evaluation, ADR drafting, and solution-doc compilation — including single-task spikes — to sub-agents whenever available; direct execution is only the fallback. Goal: keep the orchestrating agent's context small; parallel speed secondary. Details: **reference/multi-agent-orchestration.md**.
</multi-agent-orchestration>

<sub-agent-verification>
Sub-agent results (Phases 2, 2b, 4, 5) are questioned and verified before acceptance. The original instance is never reused — every verifier/re-investigator is a NEW same-type sub-agent. Principles: independence, primary sources, traceability (verdict → one challenge). Phase 3 returns **provisional assumed solutions** verified at Phase 4. Loop caps at 3 rounds — at the cap, present both versions. Full rules: **reference/verification-protocol.md**.
</sub-agent-verification>

<problem-decomposition-guide>
Target 2–5 investigation areas: <2 may not need a spike; >5 too broad. Full rubric: **reference/decomposition-rubric.md**.
</problem-decomposition-guide>

<adr-uncertainty-signals>
During ADR discussion, suggest a spike when the decision hinges on something reasoning alone cannot settle: **unverified assumption**, **unknown feasibility**, **missing measurement**, **undecidable comparison**, **uninvestigated dependency**, **reviewer disagreement**.
</adr-uncertainty-signals>

<professional-doc-authoring>
ADRs and the solution document are always written by their owning skills — never hand-edited: ADR writes via `draft-adr`; findings/solution-doc writes via `write-solution-doc` (findings in current-state mode). Load the owning skill's SKILL.md and apply its capabilities, seeded with the existing document plus the change — inside the spike workflow or standalone. Bypassing the owning skill degrades the artifact.
</professional-doc-authoring>

<artifact-maintenance-doctrine>
Artifacts form a dependency chain — **Findings Docs → ADRs → Solution Doc** — kept **at the latest state**: rewrite changed sections **in place**, **delete** superseded content (git is history) — no "Note:", "Updated", "Changed", "v2", "As of", "Previously", no changelogs. Notes allowed only in findings docs, conversation.

| Change origin | Propagate to |
|---|---|
| Findings doc (new evidence/correction) | ADR → solution doc |
| ADR decision change | Solution doc |

Propagation stops at the first artifact a change does not affect. Full protocol: **reference/artifact-maintenance-guide.md**.
</artifact-maintenance-doctrine>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Full end-to-end spike (scope → solution doc) | 5-phase walkthrough | [examples/end-to-end-spike.md](examples/end-to-end-spike.md) |
| Single-area spike, narrow scope | Single-area workflow | [examples/single-area-spike.md](examples/single-area-spike.md) |
| Starting from pre-existing findings | Workflow without re-investigation | [examples/from-existing-findings.md](examples/from-existing-findings.md) |
| Decomposing a complex problem into areas | Decomposition rubric + edge cases | [reference/decomposition-rubric.md](reference/decomposition-rubric.md) |
| Heavy multi-area spike with parallel sub-agents | Parallel dispatch walkthrough | [examples/multi-agent-investigation.md](examples/multi-agent-investigation.md) |
| Continuing a spike into unresolved areas | Continuation walkthrough (revise-in-place) | [examples/continue-prior-spike.md](examples/continue-prior-spike.md) |
| Dispatching phase work to sub-agents | Dispatch pattern, fallback rules | [reference/multi-agent-orchestration.md](reference/multi-agent-orchestration.md) |
| Executing a workflow phase | Phase procedures, briefs, checklists | [reference/workflow-procedure.md](reference/workflow-procedure.md) |
| Raising challenges on sub-agent results | Questioning dimensions | `question-everything`: [questioning-dimensions.md](../question-everything/reference/questioning-dimensions.md) |
| Verifying challenges before acceptance | Verification brief, loop control | [reference/verification-protocol.md](reference/verification-protocol.md) |
| Worked verification loop (accept/contradict) | Verification examples | [examples/confirming-result.md](examples/confirming-result.md), [examples/contradicting-result.md](examples/contradicting-result.md) |
| Producing/understanding findings docs | Format, evidence-map rules | [reference/findings-document-guide.md](reference/findings-document-guide.md) |
| Syncing artifacts after a fact/decision change | Rewrite-in-place protocol, propagation | [reference/artifact-maintenance-guide.md](reference/artifact-maintenance-guide.md) |
| Splitting a large solution doc | Splitting heuristics, checklist | [reference/solution-doc-modularity-guide.md](reference/solution-doc-modularity-guide.md) |
| ADR discussion hinging on unverified assumptions | Uncertainty-spike suggestion example | [examples/adr-uncertainty-spike-suggestion.md](examples/adr-uncertainty-spike-suggestion.md) |
| Fact/decision change propagated through artifacts | Sync walkthrough | [examples/sync-update-across-artifacts.md](examples/sync-update-across-artifacts.md) |
| Placing artifacts into the spike folder | Layout example | [examples/spike-artifact-layout.md](examples/spike-artifact-layout.md) |

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
1. Dispatch each area to a code-exploration sub-agent when available; direct is the fallback (see **multi-agent-orchestration**).
2. **Dispatch**: announce "Dispatching investigation of [N] area(s)"; brief per area (spike goal, brownfield/greenfield, existing evidence map; output = per-area evidence map); dispatch concurrently; synthesize, resolving cross-area inconsistencies. Full brief: **reference/workflow-procedure.md**.
3. **Direct (fallback)**: load `investigate-code` **spike-integration**; compile current state, constraints, diagrams.
4. Apply **verify-sub-agent-results**; ask: "Is the investigation complete, or continue in a new direction?" — a new direction loops to scope.
5. Hand off to **compile-findings-doc** with the evidence maps.
</investigate-per-area>

<evaluate-solutions-per-area>
1. Dispatch each area to a sub-agent when available; direct is the fallback (see **multi-agent-orchestration**).
2. **Dispatch**: announce "Dispatching evaluation of [N] area(s)"; brief per area (spike goal, findings-doc evidence; load `draft-adr`, run its evaluate chain — **define-decision-drivers** → **define-considered-options** → **evaluate-options** — with the user dialog inside the sub-agent session; return the assumed solution); collect and review. Full brief: **reference/workflow-procedure.md**.
3. **Direct (fallback)**: load `draft-adr` evaluate chain seeded with the findings doc (its **evaluate-options** auto-applies **detail-options-tech** when findings exist). Record the **assumed solution** — provisional until ADR review.
4. **Check for findings gaps**: update the findings doc if an option revealed a constraint, risk, or fact it lacks.
5. Validate: tech details grounded in the evidence map (no invented code); assumed solution follows logically; corrections captured. Present the summary table — handoff to **draft-area-adrs**.
</evaluate-solutions-per-area>

<draft-area-adrs>
1. Dispatch each ADR to a sub-agent when available; direct is the fallback (see **multi-agent-orchestration**).
2. **Dispatch**: announce "Dispatching ADR drafting for [N] area(s)"; brief per area (evaluation results — drivers, options with pros/cons, tech details, assumed solution, findings-doc evidence; load `draft-adr`, apply **compile-adr**); collect and review. Full brief: **reference/workflow-procedure.md**.
3. **Direct drafting or revising (fallback)**: load `draft-adr` **compile-adr** seeded with the evaluation results; run the full chain only if evaluation was skipped. Revising = same procedure seeded with the existing ADR plus the change; never hand-edit (see **professional-doc-authoring**).
4. Apply **verify-sub-agent-results**; save each ADR to `<spike-folder>/adrs/ADR-00X-<kebab-name>.md` per **spike-artifact-layout**; ask: "Would you like to adjust any ADR before compiling the solution document?" On uncertainty, apply **suggest-spike-on-adr-uncertainty** first.
5. Keep each ADR at the latest state (see **artifact-maintenance-doctrine**); validate via `draft-adr`'s **compile-adr** checklist + spike checks (tech details in each option, standalone-readable, cites findings doc); run the **no-note scan** until clean.
</draft-area-adrs>

<verify-sub-agent-results>
1. Apply `question-everything`'s **question-the-result** to raise prioritized challenges.
2. Dispatch a NEW same-type sub-agent — never the original — to verify each challenge against primary sources; collect per-challenge verdicts (AGREE / DISAGREE / UNCERTAIN), each traceable to its challenge.
3. Accept only if every material verdict is AGREE; if any is DISAGREE or UNCERTAIN, dispatch a NEW same-type sub-agent to redo the investigation with the corrected understanding, then loop to step 1.
4. Loop until all AGREE or the 3-round cap; at the cap, present both versions to the user — never silently pick one.
5. Synthesize into the findings doc or save the ADR only after verification. Full loop: **reference/verification-protocol.md**.
</verify-sub-agent-results>

<compile-solution-doc>
1. Dispatch to a sub-agent when available; direct is the fallback (see **multi-agent-orchestration**).
2. **Dispatch**: announce "Dispatching solution-doc compilation"; brief (spike goal, findings docs, assumed solutions; load `write-solution-doc`, produce a **target-state** doc in **baseline-input mode**); collect and review. Full brief: **reference/workflow-procedure.md**.
3. **Direct (fallback)**: load `write-solution-doc` in **baseline-input mode** (evolve findings-doc sections as-is → to-be; C4 shows the **target architecture**) — for compiling AND revising. Seed with spike goal, findings docs, assumed solutions.
4. **Assess modularity** per **solution-doc-modularity**: if >~3000 words or 5+ major sections, extract sections into standalone docs with back-references; replace each in the hub with a 2–4 sentence summary + link.
5. Save per **spike-artifact-layout** (findings → `docs/`, ADRs → `adrs/`, solution doc → `solution.md`); keep at the latest state (see **artifact-maintenance-doctrine**).
6. Validate: every ADR's chosen solution reflected, cross-references consistent, diagrams match, sub-docs back-reference; run the **no-note scan** until clean.
7. Present the bundle: findings = current-state record; ADRs = decision records (review/approve); solution doc = target-state architecture; version-control together.
</compile-solution-doc>

<compile-findings-doc>
1. Determine the document strategy: **per-area** (2+ loosely-coupled areas) or **one consolidated doc** (tightly-coupled or single-area). Ask the user.
2. Dispatch to a sub-agent when available; direct is the fallback (see **multi-agent-orchestration**).
3. **Dispatch**: announce "Dispatching findings-doc compilation"; brief (document strategy, Phase 2 results **with each area's evidence map**; load `write-solution-doc`, produce a **current-state document** in **current-state mode** with evidence maps embedded); collect and review. Full brief: **reference/workflow-procedure.md**.
4. **Direct (fallback)**: load `write-solution-doc` in **current-state mode** (see `write-solution-doc`'s **reference/current-state-mode.md**), seeded with Phase 2 results and their evidence maps.
5. Validate per **reference/findings-document-guide.md**: each area's evidence map embedded inline — `file:line` entry points, call-chain sequence diagrams, an **Evidence & Verification** section per area (ledger: claim → verdict → `file:line` → confidence, 5-tag model; searched-negatives). Never vague references; never present inference as evidence.
6. Cross-reference between findings docs (if per-area): note cross-area constraints.
7. Ask: "Does this accurately capture the current state? Anything to add, correct, or remove?" Save to `<spike-folder>/docs/findings-<area>.md` per **spike-artifact-layout**.
8. Findings docs are the **current-state baseline and evidence home**; update the evidence map on new evidence — no round/version tracking.
</compile-findings-doc>

<sync-update-artifacts>
1. Identify the change and its origin artifact: new evidence/correction (findings doc), changed decision (ADR), or target-state change (solution doc).
2. Trace the propagation path with **artifact-maintenance-doctrine**.
3. Apply the change at the origin through its owning skill — `draft-adr` for ADRs, `write-solution-doc` for findings/solution docs (see **professional-doc-authoring**) — rewriting affected sections **in place** per the latest-state protocol.
4. Run the **no-note scan** on each touched ADR and solution doc (see **reference/artifact-maintenance-guide.md**); rewrite until clean.
5. Propagate downstream in order, re-running the owning capability seeded with the current artifact plus the delta.
6. Validate consistency — every artifact reflects the latest facts; ADRs cite only current findings; the solution doc mirrors every ADR.
7. Present the delta in conversation, never inside the artifacts (see **artifact-maintenance-doctrine**).
</sync-update-artifacts>

<continue-prior-spike>
1. Load the prior spike's artifacts — scope summary, findings docs, ADRs, solution doc. If unavailable, ask the user to share or summarize them.
2. Confirm the continuation scope: which areas to revisit, the open question for each, and which areas stand as-is.
3. Validate: selected areas independently decidable; unselected areas' decisions preserved.
4. Run the standard workflow in revise-in-place mode per **continuation-mode**: **investigate-per-area** (seed sub-agents with existing evidence maps; target only what answers the open questions), then **compile-findings-doc** → **evaluate-solutions-per-area** → **draft-area-adrs**.
5. Apply **sync-update-artifacts** to propagate changes downstream.
6. Ask whether to continue with another round or conclude; a continuation becomes the new scope via **define-spike-scope**.
</continue-prior-spike>

<suggest-spike-on-adr-uncertainty>
1. Detect uncertainty signals via **adr-uncertainty-signals**.
2. Name the uncertainty precisely: "This decision seems to hinge on [the unverified assumption / the unknown fact / the unresolved comparison]." Explain why it matters.
3. Offer: "Would you like to spike this before finalizing the ADR?" — never start without explicit confirmation. If agreed, define a focused scope (single goal, 1–3 areas) via **define-spike-scope**; treat the ADR as provisional.
4. If declined, continue the ADR flow (via `draft-adr` per **professional-doc-authoring**) and record the uncertainty as a **risk** in the ADR's Consequences section — never a free-form note.
</suggest-spike-on-adr-uncertainty>

</capabilities>

<rules>
<rule>When the user initiates a spike investigation from scratch, apply **run-spike-workflow** to orchestrate all phases from scope definition through solution compilation.</rule>
<rule>When the user starts from existing material instead of a blank slate, apply **continue-prior-spike** to continue the previous spike.</rule>
<rule>After the solution doc is compiled, if the doc is large, apply the modularity steps in **compile-solution-doc**.</rule>
</rules>
