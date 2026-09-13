---
name: conduct-spike
description: Conduct spike investigations producing ADRs, findings, and solution docs. Use when scoping, investigating, evaluating, producing ADRs, discussing undecided ADRs, understanding current state, formalizing findings, continuing or reworking spikes, syncing updates.
---

<when-to-use-this-skill>
- Conduct a spike investigation — research, evaluate, and compare approaches before committing
- Produce ADRs (one per problem, grouped by area) and a consolidated solution document
- Discuss an ADR whose outcome depends on unverified assumptions, unknown feasibility, or missing evidence
- Understand the current implementation as an investigation area before deciding
- Break a large technical problem into areas, each holding its decision problems ("How to …")
- Formalize pre-existing investigation findings into ADRs and a solution document
- Continue a previous spike into areas not fully resolved
- Re-investigate a decided ADR after implementation revealed a problem (focused rework spike)
- Sync findings doc, ADR, and solution doc after new evidence or a changed decision
</when-to-use-this-skill>

<knowledge>

<spike-definition>
A spike reduces uncertainty via research and analysis; its output is **documented decisions, not production code**:

| Artifact | Role |
|---|---|
| **Findings Documents** | Current-state baseline; each embeds its area's evidence map (`file:line` entry points, call chains, evidence ledger, searched-negatives) |
| **ADRs** | One per problem — a "How to …" decision — tagged with its area |
| **1 Solution Document** | Target-state architecture (C4, API contracts, RAID, RACI) — decision-only, ADR decisions mirrored grouped by area |
</spike-definition>

<spike-artifact-layout>
One folder per spike — `spikes/<spike-name>/` with `scope.md`, `adrs/adr-<area>-<NN>-<problem>.md`, `solution.md`, `docs/findings-<area>.md`, cross-referenced by relative path. The `spikes/` segment anchors the write boundary. Unnamed root → `resolve-artifact-location`; record `Artifact root:` atop `scope.md`.
</spike-artifact-layout>

<write-boundary>
Writes are confined to the spike folder (`**/spikes/**`) — never code, config, tests, or any file outside it; never build prototypes or POCs (`orchestrate-feature-delivery` delivers them). Run the boundary check after every write capability: **reference/write-boundary-guide.md**.
</write-boundary>

<scope-map>
The spike's canonical **area → problem map** and live status dashboard. Each problem maps to one ADR; each ADR carries its `Area:` tag; `solution.md` renders the map grouped by area. Record at **define-spike-scope**; edit at **continue-prior-spike**.
</scope-map>

<scope-map-status>
Problem (stored): `investigating` → `deciding` → `done`; area (derived): `preparing` → `spiking` → `done`. A `done` problem has its ADR; an area is never `done` with an open problem; new evidence reopens `done` → `deciding`. Full model: **reference/scope-map-guide.md**.
</scope-map-status>

<inappropriate-scenarios>
Do NOT use for quick answers, already-decided problems needing only implementation, trivial scope, immediate POC implementation, or plain ADR drafting / solution-doc writing / code investigation — `draft-adr`, `write-solution-doc`, and `investigate-code` handle those.
</inappropriate-scenarios>

<pre-existing-findings>
When the user supplies investigation material, skip **investigate-per-area** and seed **compile-findings-doc** directly; treat it as the area's evidence map. See **examples/from-existing-findings.md**.
</pre-existing-findings>

<findings-document>
The spike's **evidence home** — current-state architecture (via `write-solution-doc` **current-state mode**) embedding each area's evidence map (`file:line` annotations, call chains, evidence ledger). Cross-area constraints travel as cross-references. Details: **reference/findings-document-guide.md**.
</findings-document>

<continuation-mode>
Another round seeded with prior artifacts: read `scope.md` statuses for open work, confirm add/adjust areas and problems, run capabilities **revise-in-place**, then **sync-update-artifacts**.
</continuation-mode>

<greenfield-scenarios>
No existing implementation: research industry approaches and comparable systems and study operational constraints instead of tracing code. Never build POCs — `orchestrate-feature-delivery` delivers any POC.
</greenfield-scenarios>

<multi-agent-orchestration>
Dispatch investigation, findings-doc compilation, ADR drafting (evaluation included via `draft-adr`), and solution-doc compilation to sub-agents — including single-task spikes; dispatch is the default. Details: **reference/multi-agent-orchestration.md**; model routing, waiting, fallback: **reference/dispatch-discipline.md**.
</multi-agent-orchestration>

<sub-agent-verification>
Every dispatched result is verified before acceptance via `question-everything`'s **verify-sub-agent-results** — verify with a NEW same-type sub-agent, accept or re-investigate, capped at 3 rounds. Full rules: `question-everything`'s **reference/verification-protocol.md**.
</sub-agent-verification>

<problem-decomposition-guide>
Decompose into **areas** (shared-subject groupings, target 2–5 — one is valid), each holding **problems** ("How to …?" decisions, target 1–3; one ADR each). >5 areas or >~8 problems → narrow or split. Rubric: **reference/decomposition-rubric.md**.
</problem-decomposition-guide>

<adr-uncertainty-signals>
During ADR discussion, suggest a spike when the decision hinges on something reasoning alone cannot settle: **unverified assumption**, **unknown feasibility**, **missing measurement**, **undecidable comparison**, **uninvestigated dependency**, **reviewer disagreement**.
</adr-uncertainty-signals>

<professional-doc-authoring>
ADRs and the solution document are always written by their owning skills — never hand-edited: ADRs via `draft-adr`; findings/solution docs via `write-solution-doc` (findings in current-state mode). Option tech details come from `draft-adr`'s **detail-options-tech**, grounded in the findings doc's evidence map.
</professional-doc-authoring>

<artifact-maintenance-doctrine>
Dependency chain — **Findings Docs → ADRs → Solution Doc** — kept at the latest state: rewrite changed sections in place, delete superseded content (git is history), no version markers or changelogs. Notes allowed only in findings docs and conversation.

| Change origin | Propagate to |
|---|---|
| Findings doc (new evidence) | ADR → solution doc |
| ADR decision change | Solution doc |
| Scope-map delta | Affected ADR(s) → solution doc area section |

Propagation stops at the first unaffected artifact. Full protocol: **reference/artifact-maintenance-guide.md**.
</artifact-maintenance-doctrine>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Full end-to-end spike (scope → solution doc) | End-to-end walkthrough | [examples/end-to-end-spike.md](examples/end-to-end-spike.md) |
| Starting from pre-existing findings | Workflow without re-investigation | [examples/from-existing-findings.md](examples/from-existing-findings.md) |
| Decomposing a complex problem into areas and problems | Decomposition rubric + edge cases | [reference/decomposition-rubric.md](reference/decomposition-rubric.md) |
| Reading/updating `scope.md` statuses | Status model, transitions, validation | [reference/scope-map-guide.md](reference/scope-map-guide.md) |
| Watching statuses move through a spike | Status lifecycle walkthrough | [examples/scope-status-lifecycle.md](examples/scope-status-lifecycle.md) |
| Continuing a spike (walkthrough) | Continuation walkthrough (revise-in-place) | [examples/continue-prior-spike.md](examples/continue-prior-spike.md) |
| Heavy multi-area spike with parallel sub-agents | Parallel dispatch walkthrough | [examples/multi-agent-investigation.md](examples/multi-agent-investigation.md) |
| Verifying sub-agent results | Questioning dimensions + verification protocol | [questioning-dimensions.md](../question-everything/reference/questioning-dimensions.md), [verification-protocol.md](../question-everything/reference/verification-protocol.md) |
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
1. Apply the continuation procedure per **reference/continue-prior-spike-procedure.md** — load prior artifacts, confirm the scope delta, run revise-in-place, sync downstream.
</continue-prior-spike>

<define-spike-scope>
1. Ask: "What technical problem or feature do you want to spike? Describe it in 2–4 sentences."
2. Apply the scope-definition procedure per **reference/define-spike-scope-procedure.md** — clarify goal, decompose, record `scope.md`, validate, note greenfield.
</define-spike-scope>

<investigate-per-area>
1. Apply the investigation procedure per **reference/investigate-per-area-procedure.md** — dispatch, brief, verify, hand off evidence maps.
</investigate-per-area>

<draft-problem-adrs>
1. Apply the ADR-drafting procedure per **reference/draft-problem-adrs-procedure.md**: dispatch → evaluate + draft via `draft-adr` → verify → sync findings gaps → save → ask → validate.
</draft-problem-adrs>

<compile-solution-doc>
1. Apply the solution-doc compilation procedure per **reference/solution-doc-compilation.md**: dispatch → verify → save → validate → present.
</compile-solution-doc>

<compile-findings-doc>
1. Apply the findings-doc compilation procedure per **reference/findings-doc-compilation.md** — one per area: dispatch → verify → validate → save (mark each area `spiking` per **scope-map-status**).
</compile-findings-doc>

<sync-update-artifacts>
1. Apply the sync procedure per **reference/artifact-maintenance-guide.md**: capture the change and origin, trace propagation, apply at the origin via the owning skill, run the no-note scan, propagate downstream, validate.
</sync-update-artifacts>

<suggest-spike-on-adr-uncertainty>
1. Detect uncertainty signals via **adr-uncertainty-signals**.
2. Offer: "Would you like to spike this before finalizing the ADR?" — never start without explicit confirmation.
3. Apply the procedure per **reference/suggest-spike-on-adr-uncertainty-procedure.md**.
</suggest-spike-on-adr-uncertainty>

</capabilities>

<rules>
<rule>When the user initiates a spike investigation from scratch, apply **run-spike-workflow**.</rule>
<rule>When the user supplies pre-existing investigation material, apply **compile-findings-doc** directly, skipping **investigate-per-area** per **pre-existing-findings**.</rule>
<rule>When the user resumes a prior spike or re-investigates a decided ADR, apply **continue-prior-spike**.</rule>
<rule>When a fact or decision changes after spike artifacts exist, apply **sync-update-artifacts**.</rule>
<rule>When ADR discussion hinges on unverified assumptions or missing evidence, apply **suggest-spike-on-adr-uncertainty** before finalizing the ADR.</rule>
<rule>When the artifact base root is unresolved, apply `resolve-artifact-location` before the scope map is saved.</rule>
<rule>When any write capability completes, run the write-boundary check per **reference/write-boundary-guide.md**; stop and report on any out-of-folder change.</rule>
</rules>
