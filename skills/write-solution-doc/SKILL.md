---
name: write-solution-doc
description: Produce solution documentation with C4 diagrams, sequence/flowchart diagrams, API contracts, RAID analysis, and RACI matrices. Use when documenting, writing, or authoring a solution decision, architecture, or technical document; producing C4/sequence/flowchart diagrams; defining API/event schemas; performing RAID analysis; creating RACI matrices; or compiling a multi-section solution document.
---

<when-to-use-this-skill>
- User wants to document a finalized solution decision
- User needs to create a solution architecture document
- User wants to produce C4 diagrams (C2/C3), sequence diagrams, or flowcharts for a system
- User needs to define API/event schemas for a solution's components
- User wants to perform RAID analysis (Risks, Assumptions, Issues, Dependencies)
- User wants to create a RACI matrix for solution ownership
- User wants to compile a complete, multi-section solution document
- User is conducting a spike investigation (via the `conduct-spike` skill) and needs a solution document or current-state findings documents compiled
</when-to-use-this-skill>

<knowledge>

<solution-doc-structure>
A complete solution document has 9 sections, produced in order: Business Context & Solution Background, System Topology (C2/C3), Interaction Details, API / Event Schema, Related Documents, External Dependencies, Maintainers, RAID Analysis, RACI Matrix. See **reference/solution-doc-structure.md** for the full section-by-section description and the Markdown template.
</solution-doc-structure>

<current-state-mode>
The same 9-section format also documents the **current state** (as-is findings docs) and supports compiling a **target-state** document from a current-state baseline. Load **reference/current-state-mode.md** when producing a current-state document or evolving a baseline as-is → to-be.
</current-state-mode>

<c4-model>
The C4 model provides a hierarchical approach to software architecture diagrams:
- **C2 (Container Diagram)**: Shows the high-level technical building blocks — applications, data stores, microservices, etc. — and how they interact. Think "docker-compose" level.
- **C3 (Component Diagram)**: Zooms into a single container to show its internal components and their interactions. Think "Spring components" or "React component tree" level.

Draw all diagrams with Mermaid. Use Mermaid's native C4 diagram types for architecture: `C4Context` (context), `C4Container` (C2), and `C4Component` (C3), with C4-PlantUML-compatible syntax (`Person`, `System`, `Container`, `ContainerDb`, `Component`, `System_Boundary`, `Container_Boundary`, `Rel`). See **reference/mermaid-standards.md** for the full syntax and snippets.
</c4-model>

<diagram-selection-guide>
Choose the diagram type by scenario: runtime message passing → **sequence diagram**; business process / decision branches / data pipeline → **flowchart**; orchestration with both calls AND decisions → **both**; pure state lifecycle → **state diagram** (`stateDiagram-v2`). If the question is "who talks to whom, in what order?" → sequence; "what decisions and paths exist?" → flowchart. Accept and normalize existing diagrams from other sources. See **reference/diagram-selection-guide.md** for the full decision matrix and interop rules.
</diagram-selection-guide>

<mermaid-standards>
Mermaid diagram conventions and formatting rules for all diagram types (C4, sequence, flowchart, state diagram). Load **reference/mermaid-standards.md** for the full standards.
</mermaid-standards>

<api-design-standards>
API and event schema design should include: **endpoint/topic name** + HTTP method (or channel/queue); **request/response or event payload schema** (JSON, Protobuf, or Avro); **authentication & authorization** (OAuth2, API Key, mTLS); **error handling** conventions (status codes, error body); **rate limiting, pagination, idempotency** where relevant; for async events: schema versioning, DLQ handling, ordering guarantees.
</api-design-standards>

<raid-framework>
RAID = **Risks** (future events that could negatively impact the solution), **Assumptions** (believed true, not yet validated), **Issues** (current problems or blockers), **Dependencies** (external factors or teams the solution relies on). Each item: ID, Category, Description, Impact (H/M/L), Probability (H/M/L, Risks only), Mitigation/Resolution, Owner. Present as a structured table.
</raid-framework>

<raci-framework>
RACI = **R**esponsible (does the work), **A**ccountable (ultimately answerable — only ONE per task), **C**onsulted (two-way input), **I**nformed (kept up-to-date, one-way). Present as a matrix table: tasks as rows, teams/roles as columns, R/A/C/I in cells.
</raci-framework>

<bilingual-support>
The assistant supports both English and Chinese (中文) output:
- Detect the user's language from their initial input and respond in that language.
- Allow the user to switch languages at any point (e.g., "请用中文输出" or "switch to English").
- Diagram labels can be in either language based on audience preference.
- Technical terms (API, RAID, RACI, C4, Mermaid) remain in English unless the user explicitly requests translation.
</bilingual-support>

<concise-writing>
All solution-doc prose follows BLUF (conclusion first), hard caps, atomic bullets, diagrams-and-tables-over-prose, and single-source-of-truth. Every heading's first line is a bolded one-line takeaway; no banned phrases; every sentence passes the reader-anchored "so what?" test — it must add a fact a reader needs to understand, implement, or maintain the solution. Finish with a delete-by-default pass (cut ~20%) before presenting. Load **reference/writing-style.md** for the full rules (caps table, banned-phrase list, sentence surgery).
</concise-writing>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| User wants to see a complete end-to-end solution document workflow | Full walkthrough of all capabilities producing a final solution document | [examples/full-solution-document.md](examples/full-solution-document.md) |
| User focuses on producing C4, sequence, and flowchart diagrams | Diagram-heavy workflow with C2, C3, sequence diagram, and flowchart outputs | [examples/c4-and-interaction-diagrams.md](examples/c4-and-interaction-diagrams.md) |
| User needs API/event contract definitions | Detailed API schema and event schema design output | [examples/api-contracts.md](examples/api-contracts.md) |
| User needs to list related documents, external deps, and maintainers | Document-listing and dependency-tracking workflow | [examples/dependencies-and-maintainers.md](examples/dependencies-and-maintainers.md) |
| Writing Mermaid diagrams (C4, sequence, flowchart) | Diagram syntax, formatting rules, and conventions for all diagram types | [reference/mermaid-standards.md](reference/mermaid-standards.md) |
| Choosing the right diagram type for an interaction, or normalizing existing diagrams | Full decision matrix, interop rules, and decision rule | [reference/diagram-selection-guide.md](reference/diagram-selection-guide.md) |
| Compiling the final document or recalling section order | 9-section description and Markdown template | [reference/solution-doc-structure.md](reference/solution-doc-structure.md) |
| Producing a current-state (as-is) document, or evolving a current-state baseline into a target-state (to-be) document | Current-state mode and baseline-input rules — diagram labeling, RAID/RACI substitution, as-is → to-be evolution | [reference/current-state-mode.md](reference/current-state-mode.md) |
| Writing or reviewing any solution-doc prose | BLUF rules, sentence/paragraph caps, banned-phrase list, atomic bullets, single source of truth, reader-anchored "so what?" test | [reference/writing-style.md](reference/writing-style.md) |
| User corrects content or new findings emerge mid-session and diagrams need to stay current | Walkthrough of **sync-diagrams** updating affected diagrams and adding new ones | [examples/diagram-sync.md](examples/diagram-sync.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<clarify-business-context>
1. Detect the user's language (English or Chinese) from their initial input and respond in that language.
2. Ask 3–10 targeted questions, one at a time, to understand the business context and solution background.
3. Key areas to probe:
   - What problem does this solution solve?
   - What alternative solutions were considered and why was this one chosen?
   - What are the key business constraints (timeline, budget, compliance, etc.)?
   - Who are the key stakeholders and end users?
   - What is the scope boundary — what is explicitly in and out of scope?
4. Wait for the user's response before asking the next question.
5. Summarize the gathered context and ask the user to confirm before moving to the next capability.
6. If the user provides pre-existing business context content, incorporate it directly instead of re-gathering and confirm understanding.
</clarify-business-context>

<draw-c4-topology>
1. Based on confirmed business context, identify the containers (C2 level) involved in the solution.
2. Ask 3–8 clarifying questions, one at a time, about:
   - Which systems/services/applications participate in the solution.
   - How they communicate (sync HTTP, async messaging, gRPC, etc.).
   - External systems and users that interact with the solution.
3. Produce a C2 Container diagram in Mermaid (`C4Container`) with a brief explanation.
4. Ask the user to confirm the C2 diagram, then zoom into the most critical container to produce a C3 Component diagram.
5. Produce the C3 Component diagram in Mermaid (`C4Component`) with a brief explanation.
6. Ask the user to confirm. Offer to produce additional C3 diagrams for other containers if needed.
7. Refine diagrams based on user feedback until confirmed.
</draw-c4-topology>

<draw-interaction-diagrams>
1. Based on confirmed C4 topology, identify the key interaction flows that need documenting.
2. For each flow, consult the **diagram-selection-guide** to decide whether a sequence diagram, flowchart, or both are appropriate. If unsure, explain the trade-off and ask the user.
3. Ask 3–8 clarifying questions, one at a time, about:
   - Which scenarios/flows are most critical to document.
   - For sequence diagrams: the exact sequence of calls/messages between components, synchronous vs. asynchronous interactions, error and edge-case flows.
   - For flowcharts: the decision points, branching conditions, process steps, and start/end states.
4. Produce one diagram per critical flow in Mermaid, choosing the appropriate type per the selection guide.
5. **Sequence diagram requirements**: clearly show participants, message ordering, activation bars, and notes for important details.
6. **Flowchart requirements**: clearly show start/stop nodes, process steps (rectangles), decision nodes (diamonds), and labeled arrows for each branch condition.
7. Ask the user to confirm each diagram. Refine based on feedback.
</draw-interaction-diagrams>

<design-api-event-schema>
1. For each interaction identified in the sequence diagrams, define the API contract or event schema.
2. Ask 3–8 clarifying questions, one at a time, about:
   - Preferred API style (REST, gRPC, GraphQL, async messaging).
   - Required fields, data types, validation rules.
   - Authentication and authorization requirements.
   - Rate limiting, pagination, or idempotency needs.
3. Document each API/event with: endpoint/topic, method, request schema, response schema, auth method, and error codes.
4. For event schemas: include schema versioning strategy and dead-letter queue handling.
5. Present schemas in structured tables or code block format.
6. Ask the user to confirm each schema. Refine based on feedback.
</design-api-event-schema>

<list-related-documents>
1. Ask 2–5 questions, one at a time, to identify related documents:
   - Design docs, RFCs, ADRs (Architecture Decision Records).
   - External API documentation or vendor specs.
   - Regulatory/compliance documents.
   - Previous solution documents for related systems.
2. List each document with: title, type (RFC/ADR/Design/External), link or path, and a one-line description of relevance.
3. Present as a structured table.
4. Ask the user to confirm the list.
</list-related-documents>

<list-external-dependencies>
1. Based on the C4 diagrams and interactions, identify all external systems/services the solution depends on.
2. For each external dependency, ask the user to provide:
   - System/service name and description.
   - Owning team or organization.
   - Primary contact person and their contact info (email, Slack, etc.).
   - SLA or availability expectations.
   - Fallback/mitigation if the dependency is unavailable.
3. Present as a structured table.
4. Ask the user to confirm. Allow adding or removing dependencies.
</list-external-dependencies>

<list-maintainers>
1. For each component (container or internal component) in the solution, identify:
   - Component name.
   - Owning/maintainer team.
   - Primary contact person and contact info.
   - Secondary contact (backup).
2. Present as a structured table.
3. Ask the user to confirm. Allow edits.
</list-maintainers>

<list-raids>
1. Analyze the solution to identify Risks, Assumptions, Issues, and Dependencies across all four RAID categories.
2. For each category, ask 3–5 targeted questions, one at a time, to help the user think through items they may have missed.
3. Example probes:
   - Risks: "What happens if the primary database is unavailable?", "What if the third-party API rate-limits us?"
   - Assumptions: "Are we assuming the upstream service will always return data in <100ms?", "Are we assuming a specific deployment environment?"
   - Issues: "Are there any unresolved technical disagreements?", "Are there any missing API specifications?"
   - Dependencies: "Do we depend on another team's delivery before we can go live?"
4. Document each RAID item with: ID, Category, Description, Impact (H/M/L), Probability (H/M/L, for Risks), Mitigation/Resolution, Owner, and Status.
5. Present as a structured table with one section per RAID category.
6. Ask the user to confirm. Allow edits.
</list-raids>

<list-raci>
1. Identify all key tasks, decisions, and deliverables across the solution lifecycle (design, implementation, testing, deployment, operations).
2. Identify all teams/roles involved in the solution.
3. Ask 3–8 clarifying questions, one at a time, to assign R/A/C/I for each task.
4. Remind the user: only ONE "A" (Accountable) per row.
5. Present as a matrix table with tasks as rows and teams/roles as columns, with R/A/C/I values in cells.
6. Ask the user to confirm. Allow edits.
</list-raci>

<structure-solution-doc>
1. Load **reference/solution-doc-structure.md** and compile all confirmed sections into a single, well-organized Markdown document following its template (apply **concise-writing** throughout).
2. Under every heading, the first line is a bolded one-line takeaway (≤15 words). Tables and diagrams carry the detail; prose only summarizes in one line.
3. Use tables for structured data and fenced code blocks for Mermaid diagrams and JSON/YAML schemas. Never restate what a table or diagram shows.
4. For any section that was explicitly skipped, mark it as `[Skipped]`.
5. Ensure all Mermaid diagrams use correct syntax and are renderable.
6. Match the user's language preference (English or Chinese) for explanatory text.
7. Run the concise check (see **concise-writing**): no sentence >20 words, no banned phrases, every bullet is one claim, every heading has a takeaway line, no fact restated (single source of truth), delete-by-default pass run (~20% cut).
8. Present the final document and offer to refine any section.
</structure-solution-doc>

<sync-diagrams>
1. After the user confirms a new finding or correction (changed topology, added or removed container/component, corrected interaction flow, revised schema, new dependency or edge case), identify every diagram produced earlier in the session.
2. For each diagram, decide whether the change affects any element, relationship, message, branch, or section it depicts. Leave unaffected diagrams untouched.
3. For each affected diagram, produce the updated version reflecting the latest confirmed state, and state in one line what changed and why.
4. For any new context introduced by the change that no existing diagram covers, draw a new diagram per **diagram-selection-guide** (e.g., a new flow, a zoom into a container, a new error path) and add it to the document section it belongs to.
5. Cross-check the full diagram set against the confirmed sections: every confirmed architectural fact is represented in at least one diagram, and no diagram contradicts the latest confirmed state.
6. Present the updated and new diagrams together with the revised section content, and note which diagrams changed so the user can review the delta.
</sync-diagrams>

</capabilities>

<rules>
<rule>When the user provides a solution decision to document → begin with **clarify-business-context** to gather background and detect the user's language.</rule>

<rule>Follow the documentation sequence strictly unless the user explicitly requests a different order or asks to skip a section. The default sequence is: clarify-business-context → draw-c4-topology → draw-interaction-diagrams → design-api-event-schema → list-related-documents → list-external-dependencies → list-maintainers → list-raids → list-raci → structure-solution-doc. **sync-diagrams** is cross-cutting — it is not part of the sequence and applies on any correction or new finding.</rule>

<rule>When feedback on a capability's output changes any confirmed content → apply **sync-diagrams** to keep the diagrams current before continuing the sequence.</rule>

<rule>When the user provides existing diagrams or documented architecture → incorporate them directly into the relevant capability instead of redrawing. Confirm understanding and ask whether to reuse as-is, modify for the target state, or produce new diagrams alongside existing ones.</rule>

<rule>When the user corrects or revises any previously confirmed content (topology, interactions, schemas, dependencies, or sections) → apply **sync-diagrams** to update the affected diagrams and add new diagrams for newly revealed context before continuing the sequence.</rule>

<rule>When new findings emerge mid-session (a new component, a changed integration, a new edge case or flow) → apply **sync-diagrams** to keep all existing diagrams current and add new diagrams to explain the new context.</rule>

<rule>When the user says "looks good", "confirmed", "approved", "proceed", "next", or similar confirmations, move on to the next capability in the sequence. Do not skip capabilities unless the user explicitly asks to.</rule>

<rule>When the user says "skip [section name]" or "skip [capability name]", skip that capability entirely and proceed to the next one. Mark the skipped section as "[Skipped]" in the final document.</rule>

<rule>If the user requests to jump to a specific capability (e.g., "let's go to RAID"), skip ahead to that capability and continue the sequence from there.</rule>

<rule>When the user says "draft all" or "generate full document", skip the iterative confirmation loop and produce all sections at once as a draft using structure-solution-doc, then offer to refine any section.</rule>

<rule>If the user provides pre-existing content for any section, incorporate it directly into the relevant capability instead of re-gathering that information. Confirm understanding of the provided content before proceeding.</rule>

<rule>When the user switches language mid-session (e.g., "请用中文"), immediately switch all subsequent output to the requested language while preserving already-confirmed content in its original language.</rule>
</rules>
