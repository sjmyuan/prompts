---
name: write-solution-doc
description: Produce comprehensive solution documentation with C4 diagrams, sequence/flowchart diagrams, API contracts, RAID analysis, and RACI matrices. Use when documenting, writing, creating, or authoring a finalized solution decision, solution architecture, or technical solution document.
---

<when-to-use-this-skill>
- User wants to document a finalized solution decision
- User needs to create a solution architecture document
- User wants to produce C4 diagrams (C2/C3), sequence diagrams, or flowcharts for a system
- User needs to define API/event schemas for a solution's components
- User wants to perform RAID analysis (Risks, Assumptions, Issues, Dependencies)
- User wants to create a RACI matrix for solution ownership
- User wants to compile a complete, multi-section solution document
</when-to-use-this-skill>

<knowledge>

<solution-doc-structure>
A complete solution document consists of the following sections, produced in order:
1. **Business Context & Solution Background** — Why this solution exists, what problem it solves, and the decision rationale.
2. **System Topology (C4 Model)** — C2 (Container) and C3 (Component) diagrams showing the system landscape.
3. **Interaction Details** — Sequence diagrams (for runtime message flows between components) and/or flowcharts (for process logic, decision branches, and business workflows). Choose the appropriate diagram type per scenario or combine both when needed.
4. **API / Event Schema** — Contract definitions between components (REST APIs, async events, gRPC, etc.).
5. **Related Documents** — References to design docs, RFCs, ADRs, or external specifications.
6. **External Dependencies** — External systems/services, their owning teams, and contact persons.
7. **Maintainers** — Owning team and contact person for each component in the solution.
8. **RAID Analysis** — Risks, Assumptions, Issues, and Dependencies.
9. **RACI Matrix** — Responsible, Accountable, Consulted, and Informed parties.
</solution-doc-structure>

<c4-model>
The C4 model provides a hierarchical approach to software architecture diagrams:
- **C2 (Container Diagram)**: Shows the high-level technical building blocks — applications, data stores, microservices, etc. — and how they interact. Think "docker-compose" level.
- **C3 (Component Diagram)**: Zooms into a single container to show its internal components and their interactions. Think "Spring components" or "React component tree" level.

Use PlantUML with the C4-PlantUML macros/snippets (`!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml` etc.) for C4 diagrams. Fall back to vanilla PlantUML if C4 macros are not available.
</c4-model>

<diagram-selection-guide>
Use the following decision matrix to choose the right diagram type for each interaction scenario:

| Scenario | Recommended Diagram | Rationale |
|---|---|---|
| Runtime message passing between services/components (e.g., API calls, event publishing, request-response chains) | **Sequence Diagram** | Shows participants, message ordering, activation bars, and lifelines — best for temporal interaction flows |
| Business process with decision branches and conditional paths (e.g., order approval workflow, refund eligibility logic, state transitions) | **Flowchart** | Shows decision diamonds, branching paths, and process steps — best for logic and control flow |
| Data pipeline with transformation stages and branching (e.g., ETL steps, data routing rules, enrichment logic) | **Flowchart** | Pipeline stages are process steps; routing rules are decision nodes — naturally fits flowchart syntax |
| Multi-participant orchestration with both runtime calls AND decision logic (e.g., saga orchestration with compensating actions, complex checkout flow) | **Both** — sequence diagram for the happy-path call chain + flowchart for the decision/compensation logic | Use sequence to show who-calls-whom, flowchart to show what-decisions-are-made |
| State machine transitions (e.g., order status lifecycle, user onboarding states) | **Flowchart** (state diagram style) | States as nodes, transitions as arrows with conditions — flowchart is the simplest PlantUML option for this |
| Algorithm or processing logic within a single component (e.g., rate limiting algorithm, caching strategy) | **Flowchart** | No cross-component participants — purely internal logic flow |

**Decision rule**: If the primary question is "who talks to whom and in what order?" → use a sequence diagram. If the primary question is "what decisions are made and what paths exist?" → use a flowchart. When both questions matter, produce both diagrams.
</diagram-selection-guide>

<plantuml-standards>
PlantUML diagram conventions and formatting rules for all diagram types (C4, sequence, flowchart, etc.). Load **reference/plantuml-standards.md** for the full standards.
</plantuml-standards>

<api-design-standards>
API and event schema design conventions. Load **reference/api-design-standards.md** for the full standards.
</api-design-standards>

<raid-framework>
RAID analysis framework. Load **reference/raid-framework.md** for the full framework.
</raid-framework>

<raci-framework>
RACI responsibility assignment matrix. Load **reference/raci-framework.md** for the full framework.
</raci-framework>

<bilingual-support>
The assistant supports both English and Chinese (中文) output:
- Detect the user's language from their initial input and respond in that language.
- Allow the user to switch languages at any point (e.g., "请用中文输出" or "switch to English").
- Diagram labels can be in either language based on audience preference.
- Technical terms (API, RAID, RACI, C4, PlantUML) remain in English unless the user explicitly requests translation.
</bilingual-support>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| User wants to see a complete end-to-end solution document workflow | Full walkthrough of all 10 capabilities producing a final solution document | [examples/full-solution-document.md](examples/full-solution-document.md) |
| User focuses on producing C4, sequence, and flowchart diagrams | Diagram-heavy workflow with C2, C3, sequence diagram, and flowchart outputs | [examples/c4-and-interaction-diagrams.md](examples/c4-and-interaction-diagrams.md) |
| User needs API/event contract definitions | Detailed API schema and event schema design output | [examples/api-contracts.md](examples/api-contracts.md) |
| User needs to list related documents, external deps, and maintainers | Document-listing and dependency-tracking workflow | [examples/dependencies-and-maintainers.md](examples/dependencies-and-maintainers.md) |
| Writing PlantUML diagrams (C4, sequence, flowchart) | Diagram syntax, formatting rules, and conventions for all diagram types | [reference/plantuml-standards.md](reference/plantuml-standards.md) |
| Designing API/event contracts | REST, gRPC, and async event schema conventions | [reference/api-design-standards.md](reference/api-design-standards.md) |
| Performing RAID analysis | RAID framework definition and item schema | [reference/raid-framework.md](reference/raid-framework.md) |
| Building a RACI matrix | RACI framework definition and table format | [reference/raci-framework.md](reference/raci-framework.md) |

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
3. Produce a C2 Container diagram in PlantUML using C4-PlantUML macros with a brief explanation.
4. Ask the user to confirm the C2 diagram, then zoom into the most critical container to produce a C3 Component diagram.
5. Produce the C3 Component diagram in PlantUML with a brief explanation.
6. Ask the user to confirm. Offer to produce additional C3 diagrams for other containers if needed.
7. Refine diagrams based on user feedback until confirmed.
</draw-c4-topology>

<draw-interaction-diagrams>
1. Based on confirmed C4 topology, identify the key interaction flows that need documenting.
2. For each flow, consult the **diagram-selection-guide** in `<knowledge>` to decide whether a sequence diagram, flowchart, or both are appropriate. If unsure, explain the trade-off and ask the user.
3. Ask 3–8 clarifying questions, one at a time, about:
   - Which scenarios/flows are most critical to document.
   - For sequence diagrams: the exact sequence of calls/messages between components, synchronous vs. asynchronous interactions, error and edge-case flows.
   - For flowcharts: the decision points, branching conditions, process steps, and start/end states.
4. Produce one diagram per critical flow in PlantUML, choosing the appropriate type per the selection guide.
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
1. Compile all confirmed sections into a single, well-organized Markdown document following this structure:

```
# Solution Document: [Solution Name]

## 1. Business Context & Solution Background
[Context and background summary]

## 2. System Topology (C4 Model)
### 2.1 C2 — Container Diagram
[PlantUML diagram + explanation]
### 2.2 C3 — Component Diagram(s)
[PlantUML diagram(s) + explanation]

## 3. Interaction Details
[One subsection per critical flow with PlantUML diagram(s) + explanation. Use sequence diagrams for runtime message flows, flowcharts for process logic/decision branches, or both when needed.]

## 4. API / Event Schema
[Structured schema definitions]

## 5. Related Documents
[Table of related documents]

## 6. External Dependencies
[Table of external dependencies with teams and contacts]

## 7. Maintainers
[Table of components with maintainer teams and contacts]

## 8. RAID Analysis
[RAID table with Risks, Assumptions, Issues, Dependencies]

## 9. RACI Matrix
[RACI matrix table]
```

2. Use clear heading hierarchy, tables for structured data, and fenced code blocks for PlantUML and JSON/YAML schemas.
3. For any section that was explicitly skipped, mark it as `[Skipped]`.
4. Ensure all PlantUML diagrams use correct syntax and are renderable.
5. Match the user's language preference (English or Chinese) for explanatory text.
6. Present the final document and offer to refine any section.
</structure-solution-doc>

</capabilities>

<rules>
<rule>When the user provides a solution decision to document → begin with **clarify-business-context** to gather background and detect the user's language.</rule>

<rule>Follow the documentation sequence strictly unless the user explicitly requests a different order or asks to skip a section. The default sequence is: clarify-business-context → draw-c4-topology → draw-interaction-diagrams → design-api-event-schema → list-related-documents → list-external-dependencies → list-maintainers → list-raids → list-raci → structure-solution-doc.</rule>

<rule>Always ask questions one at a time and wait for the user's response before proceeding to the next question or capability. Never batch multiple questions together unless the user explicitly requests it.</rule>

<rule>After each capability's output, pause and ask the user to confirm before proceeding to the next capability. On receiving feedback, refine the current output until the user confirms satisfaction.</rule>

<rule>When the user says "looks good", "confirmed", "approved", "proceed", "next", or similar confirmations, move on to the next capability in the sequence. Do not skip capabilities unless the user explicitly asks to.</rule>

<rule>When the user says "skip [section name]" or "skip [capability name]", skip that capability entirely and proceed to the next one. Mark the skipped section as "[Skipped]" in the final document.</rule>

<rule>If the user requests to jump to a specific capability (e.g., "let's go to RAID"), skip ahead to that capability and continue the sequence from there.</rule>

<rule>When the user says "draft all" or "generate full document", skip the iterative confirmation loop and produce all sections at once as a draft using structure-solution-doc, then offer to refine any section.</rule>

<rule>If the user provides pre-existing content for any section, incorporate it directly into the relevant capability instead of re-gathering that information. Confirm understanding of the provided content before proceeding.</rule>

<rule>For PlantUML diagrams, always provide the complete, renderable PlantUML code inside a fenced code block with `plantuml` language tag. Include both the diagram code and a written explanation.</rule>

<rule>When the user switches language mid-session (e.g., "请用中文"), immediately switch all subsequent output to the requested language while preserving already-confirmed content in its original language.</rule>
</rules>
