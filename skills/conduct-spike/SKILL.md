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
ADR option tech details (target-state diagrams + code change profiles) come from `draft-adr` **detail-options-tech**, grounded in the findings doc's evidence map — delegate to `draft-adr` during ADR drafting (see **professional-doc-authoring**).
</option-tech-details>

<continuation-mode>
Continuing a spike = **another round of the same workflow**, seeded with prior artifacts: read `scope.md`'s statuses (see **scope-map-status**) to pick open work — `investigating` problems need investigation, `deciding` need confirmation; confirm add/adjust areas and problems; each delta maps to its affected ADR(s) and the solution doc's area section. Unchanged items stay as-is; run capabilities in **revise-in-place** mode, updating statuses as each step completes; **sync-update-artifacts** propagates downstream. See **examples/continue-prior-spike.md**.
</continuation-mode>

<greenfield-scenarios>
No existing implementation: research industry approaches and similar systems, study operational constraints (cloud, team, compliance), build proof-of-concept prototypes instead of tracing code; remaining workflow unchanged.
</greenfield-scenarios>

<multi-agent-orchestration>
Dispatch investigation, findings-doc compilation, ADR drafting (including option evaluation via `draft-adr`), and solution-doc compilation — including single-task spikes — to sub-agents; a sub-agent is always available. Goal: keep the orchestrating agent's context small; parallel speed secondary. Details: **reference/multi-agent-orchestration.md**.
</multi-agent-orchestration>

<sub-agent-verification>
All dispatched sub-agent results (investigation, findings, ADRs, solution doc) are verified before acceptance via `question-everything`'s **verify-sub-agent-results** — question, verify with a NEW same-type sub-agent (never the original instance), accept or re-investigate, capped at 3 rounds. Full rules: `question-everything`'s **reference/verification-protocol.md**.
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
| Full end-to-end spike (scope → solution doc) | End-to-end walkthrough | [examples/end-to-end-spike.md](examples/end-to-end-spike.md) |
| Single-area spike, narrow scope | Single-area workflow | [examples/single-area-spike.md](examples/single-area-spike.md) |
| Starting from pre-existing findings | Workflow without re-investigation | [examples/from-existing-findings.md](examples/from-existing-findings.md) |
| Decomposing a complex problem into areas and problems | Decomposition rubric + edge cases | [reference/decomposition-rubric.md](reference/decomposition-rubric.md) |
| Heavy multi-area spike with parallel sub-agents | Parallel dispatch walkthrough | [examples/multi-agent-investigation.md](examples/multi-agent-investigation.md) |
| Continuing a spike into unresolved areas | Continuation walkthrough (revise-in-place) | [examples/continue-prior-spike.md](examples/continue-prior-spike.md) |
| Dispatching workflow steps to sub-agents | Dispatch pattern | [reference/multi-agent-orchestration.md](reference/multi-agent-orchestration.md) |
| Preparing a dispatch brief | Brief index + shared evidence-map contract | [reference/dispatch-briefs.md](reference/dispatch-briefs.md) |
| Compiling the findings doc | Full compile-findings-doc procedure | [reference/findings-doc-compilation.md](reference/findings-doc-compilation.md) |
| Compiling the solution doc | Full compile-solution-doc procedure | [reference/solution-doc-compilation.md](reference/solution-doc-compilation.md) |
| Drafting ADRs for the area's problems | Full draft-problem-adrs procedure | [reference/draft-problem-adrs-procedure.md](reference/draft-problem-adrs-procedure.md) |
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
1. Apply **define-spike-scope**.
2. Do not proceed until the scope is confirmed.
3. Apply **investigate-per-area**, recording each area's **evidence map**.
4. Verify each result via `question-everything`'s **verify-sub-agent-results**.
5. Loop to step 1 when a new investigation direction emerges.
6. Apply **compile-findings-doc**, embedding each area's evidence map inline.
7. Apply **draft-problem-adrs** — evaluating options and drafting each ADR via `draft-adr`, verifying each before saving.
8. Apply **compile-solution-doc** to consolidate ADRs into the solution document.
9. Pause for user confirmation after each capability.
10. Skip a pause only if the user requests it.
</run-spike-workflow>

<continue-prior-spike>
1. Load the prior spike's artifacts — scope summary, findings docs, ADRs, solution doc.
2. Ask the user to share or summarize them when any are unavailable.
3. Confirm the continuation scope against the **scope map** (`scope.md`).
4. Read statuses to surface open problems (`investigating`/`deciding` per **scope-map-status**).
5. Decide which areas to add, adjust, or remove and which problems to add, adjust, or remove under each.
6. Map each delta to its affected ADR(s) and solution section.
7. Validate changed problems are independently decidable.
8. Validate unchanged items' decisions are preserved.
9. Validate the scope map reflects the confirmed deltas.
10. Run the standard workflow in revise-in-place mode per **continuation-mode**.
11. Update `scope.md` statuses as each step completes.
12. Apply **investigate-per-area**, seeding sub-agents with existing evidence maps and targeting only what answers the open problems.
13. Apply **compile-findings-doc**.
14. Apply **draft-problem-adrs**, evaluating options and drafting each ADR via `draft-adr`.
15. Apply **sync-update-artifacts** to propagate changes downstream.
16. Propagate a new area's delta to its findings doc, ADRs, and solution section.
17. Propagate a new problem's delta to its ADR and solution subsection.
18. Ask whether to continue with another round or conclude.
19. Apply **define-spike-scope** when continuing, adopting the continuation as the new scope.
</continue-prior-spike>

<define-spike-scope>
1. Ask: "What technical problem or feature do you want to spike? Describe it in 2–4 sentences."
2. Clarify the goal — what question(s) to answer, what uncertainty to reduce.
3. Decompose into **investigation areas** per **problem-decomposition-guide** (target 2–5).
4. Propose a breakdown with one-line descriptions for each area.
5. Confirm split, merge, add, or remove of areas.
6. Enumerate each area's **problems** ("How to …?" — one per ADR, target 1–3).
7. Propose the problems for each area.
8. Confirm split, merge, add, or remove of problems.
9. Record the **scope map** in `scope.md` per **scope-map** and **scope-map-status**.
10. Record the goal (1 sentence) and each area (`preparing`, empty findings link) with its problems (`investigating`).
11. Validate each problem is independently decidable (areas are shared-subject groupings).
12. Validate 2–5 areas and ~1–3 problems per area (or justified).
13. Validate the goal is clear enough to know completion.
14. Note greenfield per **greenfield-scenarios**.
</define-spike-scope>

<investigate-per-area>
1. Dispatch each area's investigation to `code-investigator` per **multi-agent-orchestration**.
2. Brief each investigation per **reference/investigation-brief.md**.
3. Verify each area's result via `question-everything`'s **verify-sub-agent-results**.
4. Ask: "Is the investigation complete, or continue in a new direction?"
5. Loop to scope when a new direction is chosen.
6. Hand off to **compile-findings-doc** with the evidence maps.
</investigate-per-area>

<draft-problem-adrs>
1. Apply the ADR-drafting procedure per **reference/draft-problem-adrs-procedure.md**: dispatch → evaluate + draft via `draft-adr` → verify → sync findings gaps → save → ask → validate.
</draft-problem-adrs>

<compile-solution-doc>
1. Apply the solution-doc compilation procedure per **reference/solution-doc-compilation.md**: dispatch → verify → save → validate → present.
</compile-solution-doc>

<compile-findings-doc>
1. Apply the findings-doc compilation procedure per **reference/findings-doc-compilation.md**: confirm strategy → dispatch → verify → validate → save (mark the area `spiking` in `scope.md` per **scope-map-status**).
</compile-findings-doc>

<sync-update-artifacts>
1. Apply the sync procedure per **reference/artifact-maintenance-guide.md**: capture the change and its origin, trace the propagation path, apply at the origin via the owning skill, run the no-note scan, propagate downstream, validate and present the delta.
</sync-update-artifacts>

<suggest-spike-on-adr-uncertainty>
1. Detect uncertainty signals via **adr-uncertainty-signals**.
2. Name the uncertainty precisely: "This decision seems to hinge on [the unverified assumption / the unknown fact / the unresolved comparison]."
3. Explain why the uncertainty matters.
4. Offer: "Would you like to spike this before finalizing the ADR?"
5. Never start without explicit confirmation.
6. Define a focused scope (single goal, 1–3 areas) via **define-spike-scope** when the user agrees.
7. Treat the ADR as provisional.
8. Continue the ADR flow via `draft-adr` per **professional-doc-authoring** when the user declines.
9. Record the uncertainty as a **risk** in the ADR's Consequences section — never a free-form note.
</suggest-spike-on-adr-uncertainty>

</capabilities>

<rules>
<rule>When the user initiates a spike investigation from scratch, apply **run-spike-workflow** to orchestrate the full workflow from scope definition through solution compilation.</rule>
<rule>When the user starts from existing material instead of a blank slate, apply **continue-prior-spike** to continue the previous spike.</rule>
</rules>
