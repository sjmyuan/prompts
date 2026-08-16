# Dispatch Briefs

Brief index + the shared **structured brief shape** and evidence-map input/output contract for dispatching spike work to sub-agents. The capability→agent mapping and dispatch rules live in **reference/multi-agent-orchestration.md**. Each ready-to-fill brief lives in its own file, loaded on demand:

| Capability → agent | Brief file |
|---|---|
| investigate-per-area → `code-investigator` | [investigation-brief.md](investigation-brief.md) |
| compile-findings-doc → `solution-doc-writer` | [findings-doc-brief.md](findings-doc-brief.md) |
| draft-problem-adrs → `adr-writer` | [adr-drafting-brief.md](adr-drafting-brief.md) |
| compile-solution-doc → `solution-doc-writer` | [solution-doc-brief.md](solution-doc-brief.md) |

Dispatch multiple work units concurrently, a single unit on its own. Fill each brief from its file per the **structured brief shape**, dispatch it to the mapped agent, then review each returned result against the capability's spike-specific checks (in its brief file). All briefs carry the shared evidence-map input/output contract below.

## Structured brief shape

Every dispatch brief follows the same 7-section skeleton so a filled brief is self-contained — the sub-agent follows the sections in order and never guesses. Each brief file (table above) is the ready-to-fill form: the orchestrator substitutes the `[bracketed]` fields and dispatches verbatim to the mapped agent.

| # | Section | Filled as |
|---|---|---|
| 1 | Mission | Who I am + the one-sentence deliverable |
| 2 | Context | Spike goal, scope, brownfield/greenfield |
| 3 | Inputs | Paths to load + how to use each |
| 4 | Tasks | Ordered actions to perform |
| 5 | Output contract | Exactly what to return and its format |
| 6 | Constraints | Guardrails — what never to do |
| 7 | Report back | What to flag to the orchestrator |

## Evidence map in every brief

The evidence map (embedded in findings docs) is the input/output contract every brief carries:

- **Input — include the findings doc**: pass the area's findings doc (or its evidence sections) so the sub-agent starts from verified `file:line` locations instead of scanning from scratch. Instruct it to treat the evidence ledger's **Verified** claims as settled and only dig into marked **Gap**s/**Inconsistencies** or **Inferred**/**Assumption** claims.
- **Output — require an evidence map back**: every investigation brief asks the sub-agent to return a per-area evidence map (entry points, key code locations with `file:line`, call chains, evidence verdicts, searched-negatives) alongside its narrative findings — the orchestrator embeds it in the area's findings doc (see **compile-findings-doc**).
- **Searched-negatives travel with the findings doc**: a documented "not found" tells the next sub-agent not to repeat the scan.
- **ADR-drafting briefs** include the area's findings doc (evidence sections) so ADRs can cite evidence locations without re-reading code.
- **First pass is the seed**: when no findings doc exists yet, briefs omit the input but still require the evidence-map output — the first investigation builds the map the findings doc embeds.
