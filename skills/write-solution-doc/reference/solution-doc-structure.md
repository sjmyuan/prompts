# Solution Document Structure

Backs the `<solution-doc-structure>` knowledge entry and the **structure-solution-doc** capability. A complete solution document has 9 sections, produced in order.

## The 9 Sections

1. **Business Context & Solution Background** — Why this solution exists, what problem it solves, and the decision rationale.
2. **System Topology (C4 Model)** — C2 (Container) and C3 (Component) diagrams showing the system landscape.
3. **Interaction Details** — Sequence diagrams (runtime message flows between components) and/or flowcharts (process logic, decision branches, business workflows). Choose per the diagram-selection-guide.
4. **API / Event Schema** — Contract definitions between components (REST APIs, async events, gRPC, etc.).
5. **Related Documents** — References to design docs, RFCs, ADRs, or external specifications.
6. **External Dependencies** — External systems/services, their owning teams, and contact persons.
7. **Maintainers** — Owning team and contact person for each component in the solution.
8. **RAID Analysis** — Risks, Assumptions, Issues, and Dependencies.
9. **RACI Matrix** — Responsible, Accountable, Consulted, and Informed parties.

## Markdown Template

````markdown
# Solution Document: [Solution Name]

## 1. Business Context & Solution Background
**Takeaway:** [ 1 line: problem + why this solution ]

## 2. System Topology (C4 Model)
### 2.1 C2 — Container Diagram
[Mermaid diagram — caption is the 1-line takeaway]
### 2.2 C3 — Component Diagram(s)
[Mermaid diagram(s) — caption is the 1-line takeaway]

## 3. Interaction Details
**Takeaway:** [ 1 line per flow ]
[One subsection per critical flow: diagram + 1-line caption. Use sequence diagrams for runtime message flows, flowcharts for process logic/decision branches, or both when needed.]

## 4. API / Event Schema
[Tables / code blocks — no prose walkthrough]

## 5. Related Documents
[Table]

## 6. External Dependencies
[Table with teams and contacts]

## 7. Maintainers
[Table with maintainer teams and contacts]

## 8. RAID Analysis
[Table — one row per item]

## 9. RACI Matrix
[Matrix table]
````

## Rendering Rules (apply concise-writing)

- Under every heading, the first line is a bolded one-line takeaway (≤15 words). Tables and diagrams carry the detail; prose only summarizes in one line.
- Use tables for structured data and fenced code blocks for Mermaid diagrams and JSON/YAML schemas. Never restate what a table or diagram shows.
- For any section explicitly skipped, mark it as `[Skipped]`.
- Ensure all Mermaid diagrams use correct syntax and are renderable.
