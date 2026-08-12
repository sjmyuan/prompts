---
name: draft-adr
description: Guide users through drafting well-structured ADRs, proactively visualizing context and solutions with diagrams, and detailing each option's technical implementation. Use when creating, writing, drafting, or authoring an ADR, documenting decisions, evaluating options or their technical implementation, or compiling a record from raw notes.
---

<when-to-use-this-skill>
- User wants to create, write, draft, or author an Architecture Decision Record (ADR)
- User needs to document an architectural or technical decision
- User wants to evaluate and compare architecture options for a decision
- User wants to evaluate each option by its technical implementation — target-state diagrams and concrete code changes with locations
- User needs help structuring unstructured thoughts or notes into an ADR format
- User wants to compile a polished ADR document from raw discussion points
- User is conducting a spike investigation (via the `conduct-spike` skill) and needs an ADR drafted per decision area
</when-to-use-this-skill>

<knowledge>

<about-adr>
An Architecture Decision Record (ADR) captures a significant architectural decision along with its context, options considered, and consequences. It serves as a historical record for the team and future contributors, making the rationale behind decisions transparent and traceable.
</about-adr>

<decision-driver-categories>
When prompting the user for decision drivers, suggest these common categories:
- **Performance**: latency, throughput, resource usage
- **Cost**: licensing, infrastructure, operational, migration
- **Timeline**: delivery deadlines, team availability
- **Team expertise**: existing skills, learning curve, hiring needs
- **Maintainability**: code complexity, debugging, onboarding
- **Security**: compliance, data protection, attack surface
- **Scalability**: horizontal/vertical scaling, future growth
- **Compatibility**: existing systems, ecosystem fit, vendor lock-in

Help the user distinguish between **hard constraints** (must-haves / knock-out criteria) and **soft preferences** (nice-to-haves).
</decision-driver-categories>

<option-brainstorming-prompts>
When the user has only one option, prompt them to consider alternatives from these categories:
- **Do nothing / status quo**: What happens if we don't change anything?
- **Industry-standard approaches**: What do similar teams or companies do?
- **Open-source alternatives**: Are there OSS tools that address this?
- **Build vs. buy**: Should we build it ourselves or purchase a solution?
- **Incremental vs. big-bang**: Can we phase the change, or does it need to be all at once?
</option-brainstorming-prompts>

<diagram-selection>
Use diagrams proactively whenever explaining context or a solution — never wait to be asked. Choose the diagram type by the context you want to explain, not by which ADR step you are in. Draw all diagrams with Mermaid.

| Diagram | Draw when explaining | Shows |
|---|---|---|
| C4 context diagram | The overall system landscape — who or what interacts with the system(s) in scope | Systems in scope, actors, external dependencies |
| C4 container diagram | Zooming into a system — the high-level applications and data stores that compose it | Containers, technology choices, container relationships |
| C4 component diagram | Zooming into a single container — the components inside it and how they interact | Components, their responsibilities, component relationships |
| Flowchart | A step-by-step process or flow | Flow steps, decision branches |
| Sequence diagram | The order and timing of interactions between components | Lifelines, message sequence, sync/async calls |
| Decision driver map | The trade-off space that drives the decision | Hard constraints vs soft preferences |
| Option comparison matrix + elimination tree | How options compare against the drivers, or why options were dropped | Driver satisfaction per option, elimination reasoning |

Zoom in level by level: C4 context → container → component for structure, then a flowchart or sequence diagram for a specific flow or interaction. The solution architecture is simply a C4/flowchart view of the target state — no separate diagram type is required. Draw C4 diagrams with Mermaid's native C4 types — `C4Context` (context), `C4Container` (container), `C4Component` (component) — with C4-PlantUML-compatible syntax (`Person`, `System`, `System_Ext`, `Container`, `ContainerDb`, `Component`, `Rel`, `System_Boundary`, `Container_Boundary`). Keep each diagram to a single message. Load **reference/diagram-guide.md** for the notation and snippets.
</diagram-selection>

<option-tech-details>
Tech details make each option's implementation concrete in the ADR: **target-state diagrams** (C4 + sequence, option-specific) and a **code change profile** (per change: `file:line` location, current code, git-style diff block, how-to, confidence). Produced per option by **detail-options-tech** and rendered as a `#### Tech Details` subsection in each option's evaluation section (omit when absent). **Grounding contract**: tech details must trace to code investigation evidence — findings from the `conduct-spike` pipeline (their embedded evidence map), or an on-demand evidence map built via `investigate-code`. Without evidence they stay architectural-level and unverified, and a spike is recommended before relying on them. See **reference/option-tech-details-guide.md**.
</option-tech-details>

<concise-writing>
All ADR prose follows BLUF (conclusion first), hard caps, atomic bullets, and tables-over-prose. Every heading's first line is a bolded one-line takeaway; no banned phrases; every sentence passes the "so what?" test. Load **reference/writing-style.md** for the full rules (caps table, banned-phrase list, sentence surgery).
</concise-writing>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Compiling the final ADR document (compile-adr capability step 3) | Complete ADR markdown template with all sections and placeholder annotations | [reference/adr-template.md](reference/adr-template.md) |
| Drawing any diagram (any capability) | Mermaid notation for C4 (context / container / component), flowchart, sequence, driver map, and comparison diagrams, with snippets | [reference/diagram-guide.md](reference/diagram-guide.md) |
| User provides a complete, well-formed problem statement and wants to see a full end-to-end walkthrough | Full walkthrough of all 5 capabilities for a database selection decision | [examples/database-selection.md](examples/database-selection.md) |
| User has partial notes or rough ideas and needs help structuring them into an ADR | Full walkthrough of all 5 capabilities starting from unstructured input | [examples/from-rough-notes.md](examples/from-rough-notes.md) |
| User corrects content or new findings emerge mid-session and diagrams need to stay current | Walkthrough of **sync-diagrams** updating affected diagrams and adding new ones | [examples/diagram-sync.md](examples/diagram-sync.md) |
| Detailing each option's technical implementation (diagrams + code changes) during evaluation, or rendering tech details in the ADR | Per-option tech details format, grounding contract, and code-access handling | [reference/option-tech-details-guide.md](reference/option-tech-details-guide.md) |
| Seeing per-option tech details with C4/sequence diagrams and code diffs grounded in a code reference | Worked example of detailing two options for one area, and how they render in the ADR | [examples/option-tech-details-example.md](examples/option-tech-details-example.md) |
| Writing or reviewing any ADR prose | BLUF rules, sentence/paragraph caps, banned-phrase list, atomic bullets | [reference/writing-style.md](reference/writing-style.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<define-problem>
1. Ask the user to describe the architectural decision they need to make in 2–3 sentences.
2. If the description is vague, ask follow-up questions to clarify scope, stakeholders, and the system(s) involved.
3. Identify and resolve any ambiguous terms or implicit assumptions.
4. Restate the problem back to the user as a concise, structured summary and ask: "Does this accurately capture the problem?"
5. Iterate until the user confirms.
6. Once the problem is confirmed, draw the diagram that best explains the context involved (per **diagram-selection**, usually a C4 context diagram; zoom into flows or interactions with a flowchart or sequence diagram when the problem depends on them), and use it to verify the scope is shared before proceeding.
</define-problem>

<define-decision-drivers>
1. Ask the user: "What are the key factors, constraints, or priorities that will influence this decision?"
2. If the user struggles, suggest categories from **decision-driver-categories** to prompt thinking.
3. Help the user distinguish between hard constraints (must-haves / knock-out criteria) and soft preferences (nice-to-haves).
4. Summarize the drivers in a bullet list and ask the user to confirm or reorder by priority.
5. Once the drivers are confirmed, draw the diagram that best explains the trade-off space (per **diagram-selection**, the decision driver map) so constraints and preferences are visible.
</define-decision-drivers>

<define-considered-options>
1. Ask the user: "What options have you already considered for addressing this problem?"
2. If the user has only one option, brainstorm alternatives together using the prompts in **option-brainstorming-prompts**.
3. For each option, ensure it is concrete and distinct from the others (avoid near-duplicates).
4. Present the final list of options and ask the user to confirm before evaluating any.
</define-considered-options>

<evaluate-options>
1. For each option, ask the user:
   - "What are the main advantages or strengths of this option?"
   - "What are the main disadvantages, risks, or trade-offs?"
2. Map the pros/cons against the decision drivers in a driver-impact table (which drivers are satisfied, which are compromised). Then list the pros and cons as **short, scannable key points** — one sentence each, no analysis or justification. The table handles the analysis; the bullet list just states the key takeaways.
3. If the user wants to evaluate options by their technical implementation — or code investigation evidence (findings from the spike pipeline) is available — apply **detail-options-tech** for each option to produce its tech details (target-state diagrams + code change profile), then present them so pros/cons are judged against the concrete implementation (see **option-tech-details**).
4. Summarize the evaluation of the current option with the driver-impact table and a short Pros/Cons key-points list, then ask for confirmation.
5. After all options are evaluated, draw the diagram that best explains the comparison (per **diagram-selection**, the option comparison matrix with an elimination tree), highlighting any knock-out criteria and why each option was dropped.
6. Guide the user toward a recommendation by asking: "Given the evaluations, which option best satisfies the decision drivers?"
</evaluate-options>

<detail-options-tech>
1. Determine the evidence base: check for investigation findings (e.g., a findings doc from the `conduct-spike` pipeline) and whether the current codebase is accessible.
2. If no evidence base exists but the codebase is accessible, build a lightweight evidence map first (apply the `investigate-code` skill): entry points, key locations with `file:line`, and call chains for the affected flows.
3. For each option, draw its **target-state diagrams**: evolve the current-state C4 view (container/component) as-is → to-be for this option, and add the sequence diagram(s) for the key flow(s) this option changes. Diagrams are option-specific — never reuse another option's diagram.
4. For each option, build its **code change profile**: for every change the option requires, record — location (`file:line` + symbol), current code (quoted from the evidence map), proposed **diff** (git-style diff code block — `diff --git` header, `--- a/` / `+++ b/`, `@@` hunk, `-` / `+` lines — focused on the existing code), and a 1–2 sentence "how to change it". Spell out every change explicitly — never assume the user already knows one. List new files briefly (name + purpose) without diffing them.
5. Ground every entry: each change must trace to an evidence-map entry point or key location; tag confidence **verified / inferred / unverified**; never invent APIs, symbols, or files — if a change needs something the investigation did not establish, mark it unverified and offer to investigate.
6. If no evidence base and no code access: produce architectural-level change profiles, mark every location/scope **unverified**, and recommend a spike (`conduct-spike`) to ground the tech details before relying on them.
7. Present each option's tech details (diagrams + code change profile) and ask whether any need correction or deeper investigation.
8. Keep the confirmed tech details for the ADR — they render as a `#### Tech Details` subsection in each option's evaluation section (see **reference/option-tech-details-guide.md**).
</detail-options-tech>

<compile-adr>
1. Gather all confirmed outputs from the preceding capabilities: problem statement, decision drivers, considered options, and evaluations.
2. Prompt the user for metadata: preferred title, owners, and status (draft | adopt | declined | superseded).
3. Load **reference/adr-template.md** and populate the template with all collected information, using the user's recommended option as "Chosen option" with a synthesized justification. Include each option's `#### Tech Details` subsection when tech details were provided (see **option-tech-details**).
4. Draw a C4/flowchart view of the target state with the chosen option integrated (per **diagram-selection**), and embed it alongside the session's other diagrams in the Context and Decision Outcome sections.
5. Fill in the Consequences section based on the evaluated pros/cons and risks discussed.
6. Verify the completed ADR against this quality checklist:
   - [ ] Problem statement is clear, scoped, and unambiguous
   - [ ] Decision drivers include both hard constraints and soft preferences
   - [ ] At least 2 distinct options were evaluated
   - [ ] Each option has pros/cons explicitly tied to decision drivers
   - [ ] Each option with provided tech details carries a `#### Tech Details` subsection (diagrams + code changes)
   - [ ] Chosen option justification references specific drivers
   - [ ] Consequences section addresses risks and positive impacts
   - [ ] Context and solution are visualized with diagrams (context diagram + target-state C4/flowchart view)
   - [ ] Metadata (title, owners, status) is populated
   - [ ] Every section opens with a bolded one-line takeaway (BLUF)
   - [ ] No sentence exceeds 20 words; no banned phrases (see **concise-writing**)
   - [ ] Pros/cons and consequences are one-claim bullets, no justification
7. Present the completed ADR to the user for final review and ask: "Would you like to adjust any section before saving?"
</compile-adr>

<sync-diagrams>
1. After the user confirms a new finding or correction (revised problem, changed decision drivers, new or removed option, updated evaluation, different chosen option, corrected fact), identify every diagram drawn earlier in the session.
2. For each diagram, decide whether the change affects any element, relationship, flow, or decision it depicts. Leave unaffected diagrams untouched.
3. For each affected diagram, produce the updated version that reflects the latest confirmed state, and state in one line what changed and why.
4. For any new context introduced by the change that no existing diagram covers, draw a new diagram per **diagram-selection** (e.g., a new flow, a zoomed level, an edge-case path) and add it to the session alongside the existing diagrams.
5. Cross-check the full diagram set against the confirmed ADR content: every confirmed fact is represented in at least one diagram, and no diagram contradicts the latest confirmed state.
6. Present the updated and new diagrams together with the revised ADR content, and note which diagrams changed so the user can review the delta.
</sync-diagrams>

</capabilities>

<rules>

<rule>When the user initiates an ADR session, apply **define-problem** to establish a clear problem statement.</rule>
<rule>After the problem is confirmed, apply **define-decision-drivers** to identify the factors that will guide the decision.</rule>
<rule>After decision drivers are confirmed, apply **define-considered-options** to enumerate all viable options.</rule>
<rule>After options are confirmed, apply **evaluate-options** to assess each option's pros and cons against the decision drivers.</rule>
<rule>After all options are evaluated and a recommendation is chosen, apply **compile-adr** to produce the final ADR document using the template.</rule>

<rule>If the user submits a new option mid-evaluation, apply **evaluate-options** to assess it and integrate it into the comparison, then apply **sync-diagrams** to update the comparison matrix and elimination tree.</rule>
<rule>If the user revises the problem or decision drivers at any point, re-apply the affected downstream capabilities to keep the ADR consistent, then apply **sync-diagrams** to update every affected diagram.</rule>
<rule>After each user confirmation, update any in-progress ADR draft so nothing is lost.</rule>
<rule>When the user corrects previously confirmed content or reveals new context at any point (e.g., a new option, a revised driver, a changed chosen option, a newly discovered flow), apply **sync-diagrams** to update the affected diagrams and add new diagrams to explain the new context.</rule>
<rule>Whenever explaining context or a solution during any capability, proactively draw the matching diagram from **diagram-selection** — do not wait for the user to ask.</rule>

<rule>When the user wants to evaluate options by their technical implementation — or asks for diagrams, code diffs, or change locations per option — apply **detail-options-tech** for each option during **evaluate-options**.</rule>

</rules>
