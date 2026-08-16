# Dispatch Briefs

Per-phase brief index + the shared evidence-map input/output contract for dispatching spike work to sub-agents. The phase→agent mapping and dispatch rules live in **reference/multi-agent-orchestration.md**. Each phase's brief template lives in its own file, loaded on demand:

| Phase | Capability → agent | Brief file |
|---|---|---|
| 2. Investigate | investigate-per-area → `code-investigator` | [investigation-brief.md](investigation-brief.md) |
| 2b. Compile findings docs | compile-findings-doc → `solution-doc-writer` | [findings-doc-brief.md](findings-doc-brief.md) |
| 3. Draft problem ADRs (evaluate + draft) | draft-problem-adrs → `adr-writer` | [adr-drafting-brief.md](adr-drafting-brief.md) |
| 4. Compile solution doc | compile-solution-doc → `solution-doc-writer` | [solution-doc-brief.md](solution-doc-brief.md) |

Dispatch multiple work units concurrently, a single unit on its own. Each brief is dispatched to the mapped agent (per the table above). After collection, review each returned result against the phase's spike-specific checks (in its brief file). All briefs carry the shared evidence-map input/output contract below.

## Evidence map in every brief

The evidence map (embedded in findings docs) is the input/output contract every brief carries:

- **Input — include the findings doc**: pass the area's findings doc (or its evidence sections) so the sub-agent starts from verified `file:line` locations instead of scanning from scratch. Instruct it to treat the evidence ledger's **Verified** claims as settled and only dig into marked **Gap**s/**Inconsistencies** or **Inferred**/**Assumption** claims.
- **Output — require an evidence map back**: every investigation brief asks the sub-agent to return a per-area evidence map (entry points, key code locations with `file:line`, call chains, evidence verdicts, searched-negatives) alongside its narrative findings — the orchestrator embeds it in the area's findings doc (see **compile-findings-doc**).
- **Searched-negatives travel with the findings doc**: a documented "not found" tells the next sub-agent not to repeat the scan.
- **ADR-drafting briefs** include the area's findings doc (evidence sections) so ADRs can cite evidence locations without re-reading code.
- **First pass is the seed**: when no findings doc exists yet, briefs omit the input but still require the evidence-map output — the first investigation builds the map the findings doc embeds.
