---
name: conduct-spike
description: Conduct spike investigations producing ADRs, findings, and solution docs. Use when scoping, investigating decisions, evaluating options, discussing undecided ADRs, formalizing findings, continuing spikes, syncing updates.
---

<when-to-use-this-skill>
- Conduct a spike investigation on a technical problem — researching, evaluating, and comparing solution approaches before committing to one
- Produce ADRs — one per decision problem, grouped by area — alongside a consolidated solution document
- Discuss an ADR (drafting, reviewing, or adjusting) whose outcome depends on unverified assumptions, unknown feasibility, or missing evidence
- Understand current implementation as an investigation area within a spike before a decision is made
- Break a large technical problem into areas, each holding its decision problems ("How to …")
- Formalize pre-existing investigation findings into ADRs and a solution document
- Continue a previous spike, digging deeper into specific areas not fully resolved
- Sync every artifact — findings doc, ADR, solution doc — after new evidence or a changed decision
- Do NOT load for plain ADR drafting, solution-doc writing, or code investigation — `draft-adr`, `write-solution-doc`, `investigate-code` handle those; load only when a decision needs investigation first
</when-to-use-this-skill>

<knowledge>

<spike-definition>
A spike reduces uncertainty via research and prototyping; its output is documented decisions, not production code. It produces: **Findings Documents** (current-state baseline, each embedding its area's evidence map — `file:line` entry points, call chains, evidence ledger, searched-negatives), **ADRs** (one per problem — a "How to …" decision — tagged with its area), and **1 Solution Document** (target-state architecture with C4, API contracts, RAID, RACI — decision-only, ADR decisions mirrored grouped by area).
</spike-definition>

<spike-artifact-layout>
All spike artifacts version together in **one folder per spike**:

```
spikes/<spike-name>/
├── scope.md                # canonical area → problem map + status dashboard (see scope-map)
├── adrs/                   # one file per ADR — adr-<area>-<NN>-<problem>.md, …
├── solution.md             # the solution document (hub, decisions grouped by area)
└── docs/                   # findings documents — findings-<area>.md each
```

Artifacts cross-reference each other with relative paths inside the spike folder.

Every producing capability saves its output per this layout: determine the spike folder path (ask the user or detect an existing `spikes/<spike-name>/`), create `adrs/` and `docs/` as needed, then confirm the layout after saving.
</spike-artifact-layout>

<scope-map>
`scope.md` is the spike's **canonical area → problem map** — the single source of truth for grouping and a live **status dashboard** (see **scope-map-status**). Record it at **define-spike-scope** (goal + areas, each with its findings-doc link, status, and problems); confirm and edit it at **continue-prior-spike** (add/adjust areas; add/adjust problems under an area). Each problem maps to one ADR; each ADR carries its `Area:` tag; `solution.md` renders the map grouped by area.
</scope-map>

<scope-map-status>
`scope.md` also tracks live status so the spike's state is readable at a glance. **Problem status** (stored — ground truth): `investigating` (no ADR yet) → `deciding` (ADR drafted, option awaiting user confirmation) → `done` (ADR + user-confirmed option). **Area status** (derived from its problems + findings link, never stored separately): `preparing` (findings doc not compiled) · `spiking` (findings compiled, ≥1 problem not `done`) · `done` (all problems `done`). Transitions: findings doc saved → area `preparing`→`spiking`; ADR saved → problem `investigating`→`deciding`; user confirms option → problem `deciding`→`done`; all problems `done` → area `spiking`→`done`; new evidence or changed decision reopens (`done`→`deciding`). Validate on save: a `done` problem has its ADR present; an area is never `done` with an open problem.
</scope-map-status>

<inappropriate-scenarios>
Do NOT use for: quick answers without formal documentation, already-decided problems needing only implementation, trivial scope with no architectural impact, or immediate prototyping — spikes produce decisions, not production code.
</inappropriate-scenarios>

<findings-document>
Captures **current-state architecture** (via `write-solution-doc` **current-state mode**, directly transformable to the solution doc) and is the spike's **evidence home**: embeds each area's evidence map — `file:line` annotations, sequence diagrams for call chains, evidence ledger (claim → verdict → confidence, 5-tag model), searched-negatives. ADRs and sub-agents cite it without re-scanning. Details: **reference/findings-document-guide.md**.
</findings-document>

<option-tech-details>
ADR option tech details (target-state diagrams + code change profiles) come from `draft-adr` **detail-options-tech**, grounded in the findings doc's evidence map — delegate to `draft-adr` during evaluation and ADR drafting (see **professional-doc-authoring**).
</option-tech-details>

<continuation-mode>
Continuing a spike = **another round of the same workflow**, seeded with prior artifacts: read `scope.md`'s statuses (see **scope-map-status**) to pick open work — `investigating` problems need investigation, `deciding` need confirmation; confirm add/adjust areas and problems; each delta maps to its affected ADR(s) and the solution doc's area section. Unchanged items stay as-is; run capabilities in **revise-in-place** mode, updating statuses as phases complete; **sync-update-artifacts** propagates downstream. See **examples/continue-prior-spike.md**.
</continuation-mode>

<greenfield-scenarios>
No existing implementation: research industry approaches and similar systems, study operational constraints (cloud, team, compliance), build proof-of-concept prototypes instead of tracing code; remaining phases unchanged.
</greenfield-scenarios>

<multi-agent-orchestration>
Dispatch investigation, findings-doc compilation, evaluation, ADR drafting, and solution-doc compilation — including single-task spikes — to sub-agents whenever available; direct execution is only the fallback. Goal: keep the orchestrating agent's context small; parallel speed secondary. Details: **reference/multi-agent-orchestration.md**.
</multi-agent-orchestration>

<sub-agent-verification>
Sub-agent results (Phases 2, 2b, 4, 5) are verified before acceptance via `question-everything`'s **verify-sub-agent-results** — question, verify with a NEW same-type sub-agent (never the original instance), accept or re-investigate, capped at 3 rounds. Phase 3 returns **provisional assumed solutions** — definitive verification lands on the Phase 4 ADR. Full rules: `question-everything`'s **reference/verification-protocol.md**.
</sub-agent-verification>

<problem-decomposition-guide>
Decompose into **areas** (shared-subject groupings, target 2–5), each holding **problems** ("How to …?" decisions, target 1–3 per area; one ADR each). <2 areas may not need a spike; >5 areas or >~8 total problems → narrow or split. Full rubric: **reference/decomposition-rubric.md**.
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
| Scope-map delta (add/adjust area or problem) | Affected ADR(s) → solution doc area section |

Propagation stops at the first artifact a change does not affect. Full protocol: **reference/artifact-maintenance-guide.md**.
</artifact-maintenance-doctrine>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Full end-to-end spike (scope → solution doc) | 5-phase walkthrough | [examples/end-to-end-spike.md](examples/end-to-end-spike.md) |
| Single-area spike, narrow scope | Single-area workflow | [examples/single-area-spike.md](examples/single-area-spike.md) |
| Starting from pre-existing findings | Workflow without re-investigation | [examples/from-existing-findings.md](examples/from-existing-findings.md) |
| Decomposing a complex problem into areas and problems | Decomposition rubric + edge cases | [reference/decomposition-rubric.md](reference/decomposition-rubric.md) |
| Heavy multi-area spike with parallel sub-agents | Parallel dispatch walkthrough | [examples/multi-agent-investigation.md](examples/multi-agent-investigation.md) |
| Continuing a spike into unresolved areas | Continuation walkthrough (revise-in-place) | [examples/continue-prior-spike.md](examples/continue-prior-spike.md) |
| Dispatching phase work to sub-agents | Dispatch pattern, fallback rules | [reference/multi-agent-orchestration.md](reference/multi-agent-orchestration.md) |
| Preparing a phase dispatch brief | Per-phase brief templates | [reference/dispatch-briefs.md](reference/dispatch-briefs.md) |
| Executing a workflow phase directly | Direct-execution procedures, validation checklists | [reference/workflow-procedure.md](reference/workflow-procedure.md) |
| Raising challenges on sub-agent results | Questioning dimensions | `question-everything`: [questioning-dimensions.md](../question-everything/reference/questioning-dimensions.md) |
| Verifying challenges before acceptance | Verification brief, loop control | `question-everything`: [verification-protocol.md](../question-everything/reference/verification-protocol.md) |
| Worked verification loop (accept/contradict) | Verification examples | `question-everything`: [confirming-result.md](../question-everything/examples/confirming-result.md), [contradicting-result.md](../question-everything/examples/contradicting-result.md) |
| Producing/understanding findings docs | Format, evidence-map rules | [reference/findings-document-guide.md](reference/findings-document-guide.md) |
| Syncing artifacts after a fact/decision change | Rewrite-in-place protocol, propagation | [reference/artifact-maintenance-guide.md](reference/artifact-maintenance-guide.md) |
| ADR discussion hinging on unverified assumptions | Uncertainty-spike suggestion example | [examples/adr-uncertainty-spike-suggestion.md](examples/adr-uncertainty-spike-suggestion.md) |
| Fact/decision change propagated through artifacts | Sync walkthrough | [examples/sync-update-across-artifacts.md](examples/sync-update-across-artifacts.md) |
| Placing artifacts into the spike folder | Layout example | [examples/spike-artifact-layout.md](examples/spike-artifact-layout.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<run-spike-workflow>
1. Apply **define-spike-scope**; do not proceed until scope is confirmed.
2. Apply **investigate-per-area** (dispatch when available; record **evidence maps**; verify via `question-everything`'s **verify-sub-agent-results**); a new direction loops to step 1.
3. Apply **compile-findings-doc**, embedding each area's evidence map inline.
4. Apply **evaluate-problem-solutions** to select an assumed solution per problem.
5. Apply **draft-problem-adrs**, verifying each before saving.
6. Apply **compile-solution-doc** to consolidate ADRs into the solution document.
7. Pause for user confirmation after each phase; skip only if the user requests it.
</run-spike-workflow>

<continue-prior-spike>
1. Load the prior spike's artifacts — scope summary, findings docs, ADRs, solution doc. If unavailable, ask the user to share or summarize them.
2. Confirm the continuation scope against the **scope map** (`scope.md`): read statuses to surface open problems (`investigating`/`deciding` per **scope-map-status**), then decide which areas to add/adjust/remove and which problems to add/adjust/remove under each — each delta maps to its affected ADR(s) and solution section.
3. Validate: changed problems independently decidable; unchanged items' decisions preserved; the scope map reflects the confirmed deltas.
4. Run the standard workflow in revise-in-place mode per **continuation-mode**, updating `scope.md` statuses as each phase completes: **investigate-per-area** (seed sub-agents with existing evidence maps; target only what answers the open problems), then **compile-findings-doc** → **evaluate-problem-solutions** → **draft-problem-adrs**.
5. Apply **sync-update-artifacts** to propagate changes downstream (new area → findings doc + ADRs + solution section; new problem → ADR + solution subsection).
6. Ask whether to continue with another round or conclude; a continuation becomes the new scope via **define-spike-scope**.
</continue-prior-spike>

<define-spike-scope>
1. Ask: "What technical problem or feature do you want to spike? Describe it in 2–4 sentences." Then clarify the goal — what question(s) to answer, what uncertainty to reduce?
2. Decompose into **investigation areas** per **problem-decomposition-guide** (target 2–5): propose a breakdown with one-line descriptions; confirm split/merge/add/remove.
3. For each area, enumerate its **problems** ("How to …?" — one per ADR, target 1–3): propose them; confirm split/merge/add/remove.
4. Record the **scope map** in `scope.md` per **scope-map** and **scope-map-status**: goal (1 sentence) + areas (`preparing`, empty findings link), each with its problems (`investigating`).
5. Validate: each problem independently decidable (areas are shared-subject groupings), 2–5 areas and ~1–3 problems per area (or justified), goal clear enough to know completion; note greenfield (see **greenfield-scenarios**).
</define-spike-scope>

<investigate-per-area>
1. Dispatch each area's investigation to `code-investigator` per **multi-agent-orchestration**; brief per **reference/dispatch-briefs.md**.
2. Direct fallback: apply the direct investigation procedure per **reference/workflow-procedure.md** (load `investigate-code` **spike-integration**).
3. Verify each area's result via `question-everything`'s **verify-sub-agent-results**.
4. Ask: "Is the investigation complete, or continue in a new direction?" — a new direction loops to scope.
5. Hand off to **compile-findings-doc** with the evidence maps.
</investigate-per-area>

<evaluate-problem-solutions>
1. Dispatch each **problem's** evaluation to `adr-writer` per **multi-agent-orchestration**; batch a whole area's problems in one brief when they share its subject/evidence (brief per **reference/dispatch-briefs.md**; the interactive `draft-adr` evaluate chain runs inside the `adr-writer` session).
2. Direct fallback: apply the direct evaluation procedure per **reference/workflow-procedure.md** (load `draft-adr` evaluate chain seeded with the findings doc). Record the **assumed solution** per problem — provisional until ADR review.
3. **Check for findings gaps**: update the findings doc if an option revealed a constraint, risk, or fact it lacks.
4. Validate spike-specifically: tech details grounded in the evidence map (no invented code); assumed solution follows logically; corrections captured. Present the summary table per area → problem — handoff to **draft-problem-adrs**.
</evaluate-problem-solutions>

<draft-problem-adrs>
1. Dispatch ADR drafting for each **problem** to `adr-writer` per **multi-agent-orchestration**; batch a whole area's problems in one brief when they share its evidence (brief per **reference/dispatch-briefs.md**).
2. Direct fallback: apply the direct drafting/revising procedure per **reference/workflow-procedure.md** (load `draft-adr` **compile-adr** seeded with the evaluation results; run the full chain only if evaluation was skipped; never hand-edit — see **professional-doc-authoring**).
3. Verify each drafted ADR via `question-everything`'s **verify-sub-agent-results**.
4. Save each ADR to `<spike-folder>/adrs/adr-<area>-<NN>-<problem>.md` per **spike-artifact-layout**, carrying its `Area:` tag from the scope map; mark the problem `deciding` in `scope.md` per **scope-map-status**.
5. Ask: "Would you like to adjust any ADR before compiling the solution document?" On uncertainty, apply **suggest-spike-on-adr-uncertainty** first. On user confirmation, mark each confirmed problem `done` in `scope.md` per **scope-map-status**.
6. Validate via `draft-adr`'s **compile-adr** checklist + spike checks (tech details in each option, standalone-readable, cites findings doc); run the **no-note scan** until clean.
</draft-problem-adrs>

<compile-solution-doc>
1. Dispatch solution-doc compilation to `solution-doc-writer` per **multi-agent-orchestration**; brief per **reference/dispatch-briefs.md**.
2. Direct fallback: apply the direct compilation procedure per **reference/workflow-procedure.md** (load `write-solution-doc` in **baseline-input mode** — for compiling AND revising; never hand-edit — see **professional-doc-authoring**).
3. Verify the compiled doc via `question-everything`'s **verify-sub-agent-results**.
4. Save per **spike-artifact-layout** (scope map → `scope.md`, findings → `docs/`, ADRs → `adrs/`, solution doc → `solution.md`); keep at the latest state (see **artifact-maintenance-doctrine**); recompute each area's derived status per **scope-map-status**.
5. Validate: the solution doc mirrors every ADR's chosen solution **grouped by area** (per **scope-map**), cross-references consistent, diagrams match; run the **no-note scan** until clean.
6. Present the bundle: findings = current-state record; ADRs = decision records (review/approve); solution doc = target-state architecture; version-control together.
</compile-solution-doc>

<compile-findings-doc>
1. Determine the document strategy: **per-area** (2+ loosely-coupled areas) or **one consolidated doc** (tightly-coupled or single-area). Ask the user.
2. Dispatch findings-doc compilation to `solution-doc-writer` per **multi-agent-orchestration**; brief per **reference/dispatch-briefs.md**.
3. Direct fallback: apply the direct compilation procedure per **reference/workflow-procedure.md** (load `write-solution-doc` in **current-state mode**, see `write-solution-doc`'s **reference/current-state-mode.md**; never hand-edit — see **professional-doc-authoring**).
4. Verify the compiled doc via `question-everything`'s **verify-sub-agent-results**.
5. Validate per **reference/findings-document-guide.md**: each area's evidence map embedded inline — `file:line` entry points, call-chain sequence diagrams, an **Evidence & Verification** section per area (ledger: claim → verdict → `file:line` → confidence, 5-tag model; searched-negatives). Never vague references; never present inference as evidence.
6. Cross-reference between findings docs (if per-area): note cross-area constraints.
7. Ask: "Does this accurately capture the current state? Anything to add, correct, or remove?"
8. Save to `<spike-folder>/docs/findings-<area>.md` per **spike-artifact-layout**, then set the area's findings link and mark it `spiking` in `scope.md` per **scope-map-status**; findings docs are the **current-state baseline and evidence home** — update the evidence map on new evidence, no round/version tracking.
</compile-findings-doc>

<sync-update-artifacts>
1. Identify the change and its origin artifact: new evidence/correction (findings doc), changed decision (ADR — reopen the problem to `deciding` in `scope.md` per **scope-map-status**), changed problem or area (scope map), or target-state change (solution doc).
2. Trace the propagation path with **artifact-maintenance-doctrine** — per area: findings → that area's ADRs → the solution doc's area section; a scope-map delta (add/adjust area or problem) propagates to the affected ADR(s) and solution sections.
3. Apply the change at the origin through its owning skill — `draft-adr` for ADRs, `write-solution-doc` for findings/solution docs (see **professional-doc-authoring**) — rewriting affected sections **in place** per the latest-state protocol.
4. Run the **no-note scan** on each touched ADR and solution doc (see **reference/artifact-maintenance-guide.md**); rewrite until clean.
5. Propagate downstream in order, re-running the owning capability seeded with the current artifact plus the delta.
6. Validate consistency — every artifact reflects the latest facts; ADRs cite only current findings; the solution doc mirrors every ADR grouped by area.
7. Present the delta in conversation, never inside the artifacts (see **artifact-maintenance-doctrine**).
</sync-update-artifacts>

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
</rules>
