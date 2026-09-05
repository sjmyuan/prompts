---
name: conduct-spike
description: Conduct spike investigations producing ADRs, findings, and solution docs. Use when scoping, investigating, evaluating, producing ADRs, discussing undecided ADRs, understanding current state, formalizing findings, continuing spikes, syncing updates.
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
A spike reduces uncertainty via research and prototyping; its output is **documented decisions, not production code**:

| Artifact | Role |
|---|---|
| **Findings Documents** | Current-state baseline; each embeds its area's evidence map (`file:line` entry points, call chains, evidence ledger, searched-negatives) |
| **ADRs** | One per problem — a "How to …" decision — tagged with its area |
| **1 Solution Document** | Target-state architecture (C4, API contracts, RAID, RACI) — decision-only, ADR decisions mirrored grouped by area |
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

Artifacts cross-reference each other with relative paths inside the spike folder. All producing capabilities save into this layout; the folder path is asked or detected from an existing `spikes/<spike-name>/`, with `adrs/` and `docs/` created as needed.
</spike-artifact-layout>

<scope-map>
`scope.md` is the spike's **canonical area → problem map** — single source of truth for grouping and a live **status dashboard** (see **scope-map-status**). Each problem maps to one ADR; each ADR carries its `Area:` tag; `solution.md` renders the map grouped by area. Record it at **define-spike-scope**; confirm and edit it at **continue-prior-spike**.
</scope-map>

<scope-map-status>
`scope.md` tracks live status — **problem status** (stored): `investigating` → `deciding` → `done`; **area status** (derived, never stored): `preparing` → `spiking` → `done`. Events: findings doc saved → area `spiking`; ADR saved → problem `deciding`; option confirmed → problem `done`; all problems `done` → area `done`; new evidence / changed decision reopens `done` → `deciding`. Validate on save: a `done` problem has its ADR; an area is never `done` with an open problem. Full status model, transitions, and validation: **reference/scope-map-guide.md**.
</scope-map-status>

<inappropriate-scenarios>
Do NOT use for: quick answers without formal documentation, already-decided problems needing only implementation, trivial scope with no architectural impact, or immediate prototyping — spikes produce decisions, not production code.
</inappropriate-scenarios>

<findings-document>
The spike's **evidence home** — captures **current-state architecture** (via `write-solution-doc` **current-state mode**, directly transformable to the solution doc) and embeds each area's evidence map:
- `file:line` annotations and call-chain sequence diagrams
- Evidence ledger — claim → verdict → confidence (5-tag model)
- Searched-negatives

Cross-area constraints (tightly-coupled areas) travel as cross-references between the affected findings docs. ADRs and sub-agents cite their area's doc without re-scanning. Details: **reference/findings-document-guide.md**.
</findings-document>

<continuation-mode>
Continuing a spike = **another round of the same workflow**, seeded with prior artifacts:
- Read `scope.md` statuses to pick open work — `investigating` problems need investigation, `deciding` need confirmation
- Confirm add/adjust areas and problems; each delta maps to its affected ADR(s) and the solution doc's area section
- Run capabilities in **revise-in-place** mode, updating statuses as each step completes; unchanged items stay as-is
- **sync-update-artifacts** propagates downstream

See **examples/continue-prior-spike.md**.
</continuation-mode>

<greenfield-scenarios>
No existing implementation: research industry approaches and similar systems, study operational constraints (cloud, team, compliance), build proof-of-concept prototypes instead of tracing code; remaining workflow unchanged.
</greenfield-scenarios>

<multi-agent-orchestration>
Dispatch investigation, findings-doc compilation, ADR drafting (including option evaluation via `draft-adr`), and solution-doc compilation to sub-agents — **including single-task spikes**; a sub-agent is always available. Goal: keep the orchestrating agent's context small; parallel speed secondary. Details: **reference/multi-agent-orchestration.md**.
</multi-agent-orchestration>

<sub-agent-verification>
Every dispatched result (investigation, findings, ADRs, solution doc) is verified before acceptance via `question-everything`'s **verify-sub-agent-results** — verify with a NEW same-type sub-agent (never the original instance), accept or re-investigate, capped at 3 rounds. Full rules: `question-everything`'s **reference/verification-protocol.md**.
</sub-agent-verification>

<problem-decomposition-guide>
Decompose into **areas** (shared-subject groupings, target 2–5 — a single area is valid and runs the identical flow), each holding **problems** ("How to …?" decisions, target 1–3 per area; one ADR each). >5 areas or >~8 total problems → narrow or split. Full rubric: **reference/decomposition-rubric.md**.
</problem-decomposition-guide>

<adr-uncertainty-signals>
During ADR discussion, suggest a spike when the decision hinges on something reasoning alone cannot settle: **unverified assumption**, **unknown feasibility**, **missing measurement**, **undecidable comparison**, **uninvestigated dependency**, **reviewer disagreement**.
</adr-uncertainty-signals>

<professional-doc-authoring>
ADRs and the solution document are always written by their owning skills — never hand-edited: ADR writes via `draft-adr`; findings/solution-doc writes via `write-solution-doc` (findings in current-state mode). Option tech details (target-state diagrams + code change profiles) come from `draft-adr`'s **detail-options-tech**, grounded in the findings doc's evidence map. Load the owning skill and apply its capabilities, seeded with the existing document plus the change — inside the spike workflow or standalone. Bypassing the owning skill degrades the artifact.
</professional-doc-authoring>

<artifact-maintenance-doctrine>
Artifacts form a dependency chain — **Findings Docs → ADRs → Solution Doc** — kept **at the latest state**: rewrite changed sections **in place**, **delete** superseded content (git is history) — no version markers ("Note:", "Updated", "v2", "As of"), no changelogs. Notes allowed only in findings docs and conversation.

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
| Starting from pre-existing findings | Workflow without re-investigation | [examples/from-existing-findings.md](examples/from-existing-findings.md) |
| Decomposing a complex problem into areas and problems | Decomposition rubric + edge cases | [reference/decomposition-rubric.md](reference/decomposition-rubric.md) |
| Defining the spike scope | Scope-definition procedure | [reference/define-spike-scope-procedure.md](reference/define-spike-scope-procedure.md) |
| Reading/updating `scope.md` statuses | Status model, transitions, validation | [reference/scope-map-guide.md](reference/scope-map-guide.md) |
| Heavy multi-area spike with parallel sub-agents | Parallel dispatch walkthrough | [examples/multi-agent-investigation.md](examples/multi-agent-investigation.md) |
| Running the full workflow from scratch | Master workflow sequence | [reference/run-spike-workflow-procedure.md](reference/run-spike-workflow-procedure.md) |
| Investigating each area | Dispatch/brief/verify procedure | [reference/investigate-per-area-procedure.md](reference/investigate-per-area-procedure.md) |
| Suggesting a spike on ADR uncertainty | Uncertainty-spike procedure | [reference/suggest-spike-on-adr-uncertainty-procedure.md](reference/suggest-spike-on-adr-uncertainty-procedure.md) |
| Continuing a spike into unresolved areas | Continuation walkthrough (revise-in-place) | [examples/continue-prior-spike.md](examples/continue-prior-spike.md) |
| Dispatching workflow steps to sub-agents | Dispatch pattern | [reference/multi-agent-orchestration.md](reference/multi-agent-orchestration.md) |
| Preparing a dispatch brief | Brief index + structured brief shape + evidence-map contract | [reference/dispatch-briefs.md](reference/dispatch-briefs.md) |
| Compiling the findings doc | Full compile-findings-doc procedure | [reference/findings-doc-compilation.md](reference/findings-doc-compilation.md) |
| Compiling the solution doc | Full compile-solution-doc procedure | [reference/solution-doc-compilation.md](reference/solution-doc-compilation.md) |
| Drafting ADRs for the area's problems | Full draft-problem-adrs procedure | [reference/draft-problem-adrs-procedure.md](reference/draft-problem-adrs-procedure.md) |
| Verifying sub-agent results (challenge/accept/contradict) | Questioning dimensions + verification loop + worked examples | [questioning-dimensions.md](../question-everything/reference/questioning-dimensions.md), [verification-protocol.md](../question-everything/reference/verification-protocol.md), [confirming-result.md](../question-everything/examples/confirming-result.md), [contradicting-result.md](../question-everything/examples/contradicting-result.md) |
| Producing/understanding findings docs | Format, evidence-map rules | [reference/findings-document-guide.md](reference/findings-document-guide.md) |
| Syncing artifacts after a fact/decision change | Rewrite-in-place protocol, propagation | [reference/artifact-maintenance-guide.md](reference/artifact-maintenance-guide.md) |
| ADR discussion hinging on unverified assumptions | Uncertainty-spike suggestion example | [examples/adr-uncertainty-spike-suggestion.md](examples/adr-uncertainty-spike-suggestion.md) |
| Fact/decision change propagated through artifacts | Sync walkthrough | [examples/sync-update-across-artifacts.md](examples/sync-update-across-artifacts.md) |
| Placing artifacts into the spike folder | Layout example | [examples/spike-artifact-layout.md](examples/spike-artifact-layout.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<run-spike-workflow>
1. Apply the spike workflow per **reference/run-spike-workflow-procedure.md** — define-spike-scope → investigate-per-area → compile-findings-doc → draft-problem-adrs → compile-solution-doc, pausing for user confirmation after each capability (skip a pause only if the user requests it).
</run-spike-workflow>

<continue-prior-spike>
1. Load the prior spike's artifacts — scope summary, findings docs, ADRs, solution doc; ask the user to share or summarize them when any are unavailable.
2. Confirm the continuation scope against `scope.md`; read statuses to surface open problems (`investigating`/`deciding` per **scope-map-status**).
3. Confirm which areas and problems to add, adjust, or remove; map each delta to its affected ADR(s) and solution section.
4. Validate changed problems are independently decidable and unchanged decisions are preserved; update the scope map.
5. Run the standard workflow in revise-in-place mode per **continuation-mode**: apply **investigate-per-area** (seeded with existing evidence maps), **compile-findings-doc**, **draft-problem-adrs**, then **sync-update-artifacts**.
6. Update `scope.md` statuses as each step completes.
7. Ask whether to continue with another round or conclude.
8. Apply **define-spike-scope** when continuing, adopting the continuation as the new scope.
</continue-prior-spike>

<define-spike-scope>
1. Ask: "What technical problem or feature do you want to spike? Describe it in 2–4 sentences."
2. Apply the scope-definition procedure per **reference/define-spike-scope-procedure.md** — clarify goal, decompose into areas and problems, record the scope map in `scope.md`, validate, note greenfield.
</define-spike-scope>

<investigate-per-area>
1. Apply the investigation procedure per **reference/investigate-per-area-procedure.md** — dispatch each area to `code-investigator`, brief, verify, ask to continue, hand off evidence maps.
</investigate-per-area>

<draft-problem-adrs>
1. Apply the ADR-drafting procedure per **reference/draft-problem-adrs-procedure.md**: dispatch → evaluate + draft via `draft-adr` → verify → sync findings gaps → save → ask → validate.
</draft-problem-adrs>

<compile-solution-doc>
1. Apply the solution-doc compilation procedure per **reference/solution-doc-compilation.md**: dispatch → verify → save → validate → present.
</compile-solution-doc>

<compile-findings-doc>
1. Apply the findings-doc compilation procedure per **reference/findings-doc-compilation.md** — one findings doc per area, always: dispatch → verify → validate → save (mark each area `spiking` in `scope.md` per **scope-map-status**).
</compile-findings-doc>

<sync-update-artifacts>
1. Apply the sync procedure per **reference/artifact-maintenance-guide.md**: capture the change and its origin, trace the propagation path, apply at the origin via the owning skill, run the no-note scan, propagate downstream, validate and present the delta.
</sync-update-artifacts>

<suggest-spike-on-adr-uncertainty>
1. Detect uncertainty signals via **adr-uncertainty-signals**.
2. Offer: "Would you like to spike this before finalizing the ADR?" — never start without explicit confirmation.
3. Apply the rest of the procedure per **reference/suggest-spike-on-adr-uncertainty-procedure.md** — name the uncertainty, define a focused scope via **define-spike-scope** when the user agrees, treat the ADR as provisional, or continue the ADR flow via `draft-adr` when the user declines; record the uncertainty as a **risk** in the ADR's Consequences section.
</suggest-spike-on-adr-uncertainty>

</capabilities>

<rules>
<rule>When the user initiates a spike investigation from scratch, apply **run-spike-workflow**.</rule>
<rule>When the user starts from existing material instead of a blank slate, apply **continue-prior-spike**.</rule>
<rule>When a fact or decision changes after spike artifacts exist, apply **sync-update-artifacts**.</rule>
<rule>When ADR discussion hinges on an unverified assumption, unknown feasibility, or missing evidence, apply **suggest-spike-on-adr-uncertainty** before finalizing the ADR.</rule>
</rules>
