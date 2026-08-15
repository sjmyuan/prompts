# Dispatch Briefs

Per-phase brief templates for dispatching spike work to sub-agents. Dispatch-vs-direct rules and the phase→agent mapping live in **reference/multi-agent-orchestration.md**; direct-execution procedures live in **reference/workflow-procedure.md**.

Dispatch multiple work units concurrently, a single unit on its own. Each brief is dispatched to the mapped agent (below). After collection, review each returned result against the phase's spike-specific checks. All briefs carry the shared evidence-map input/output contract (see **Evidence map in every brief** below).

## Investigation — investigate-per-area → `code-investigator`

**Announce**: "Dispatching investigation of [N] area(s) to a sub-agent."

Brief per area: area name + description, spike goal, brownfield/greenfield. Carry the area's existing findings doc / evidence map when one exists; require a per-area evidence map back (see **Evidence map in every brief**). After collection, synthesize, resolving cross-area inconsistencies for the findings doc.

## Evaluation — evaluate-solutions-per-area → `adr-writer`

**Announce**: "Dispatching evaluation of [N] area(s) to a sub-agent."

Brief per area: area name + description, spike goal, the area's findings doc (evidence sections). Instructions: load `draft-adr` and run the interactive evaluate chain — **define-decision-drivers** → **define-considered-options** → **evaluate-options** — with the user dialog inside the sub-agent session. Expected output: the area's assumed solution. After collection, review each for fidelity to the findings doc and cross-area consistency; definitive verification lands on the Phase 4 ADR.

## ADR drafting — draft-area-adrs → `adr-writer`

**Announce**: "Dispatching ADR drafting for [N] area(s) to a sub-agent."

Brief per area: area name + description, evaluation results (decision drivers, options with pros/cons, **tech details per option**, assumed solution), the area's findings doc (evidence sections). Instructions: load `draft-adr` and apply **compile-adr** seeded with the evaluation results. After collection, review each ADR.

## Findings-doc compilation — compile-findings-doc → `solution-doc-writer`

**Announce**: "Dispatching findings-doc compilation to a sub-agent."

Brief: document strategy (per-area vs. consolidated), Phase 2 results (investigation summaries **with each area's evidence map**). Instructions: load `write-solution-doc` and produce a **current-state document** in **current-state mode** (see `write-solution-doc`'s **reference/current-state-mode.md**), with evidence maps embedded per **reference/findings-document-guide.md**. After collection, review for evidence-map fidelity and cross-area consistency.

## Solution-doc compilation — compile-solution-doc → `solution-doc-writer`

**Announce**: "Dispatching solution-doc compilation to a sub-agent."

Brief: business context (spike goal), current-state baseline (findings docs), assumed solutions (chosen option from each ADR). Instructions: load `write-solution-doc` and produce a **target-state** document in **baseline-input mode**. After collection, review for completeness and consistency with the ADRs.

## Evidence map in every brief

The evidence map (embedded in findings docs) is the input/output contract every brief carries:

- **Input — include the findings doc**: pass the area's findings doc (or its evidence sections) so the sub-agent starts from verified `file:line` locations instead of scanning from scratch. Instruct it to treat the evidence ledger's **Verified** claims as settled and only dig into marked **Gap**s/**Inconsistencies** or **Inferred**/**Assumption** claims.
- **Output — require an evidence map back**: every investigation brief asks the sub-agent to return a per-area evidence map (entry points, key code locations with `file:line`, call chains, evidence verdicts, searched-negatives) alongside its narrative findings — the orchestrator embeds it in the area's findings doc (see **compile-findings-doc**).
- **Searched-negatives travel with the findings doc**: a documented "not found" tells the next sub-agent not to repeat the scan.
- **ADR-drafting briefs** include the area's findings doc (evidence sections) so ADRs can cite evidence locations without re-reading code.
- **First pass is the seed**: when no findings doc exists yet, briefs omit the input but still require the evidence-map output — the first investigation builds the map the findings doc embeds.
