# Diagram Guide for ADR Drafting

This guide supports the **diagram-selection** knowledge entry. Load it when actually drawing a diagram for an ADR.

## Proactive Diagramming Principles

- Draw a diagram the moment you explain context or a solution — never wait for the user to ask.
- Choose the diagram type by the context you want to explain, not by which ADR step you are in.
- One diagram = one message. If two messages are needed, draw two diagrams.
- Prefer PlantUML wherever the platform supports it; fall back to Mermaid, SVG, or ASCII when it does not. If a dedicated diagram skill exists, delegate the rendering to it.
- Keep diagrams small: 4–9 nodes for context diagrams; use sub-packages instead of merging messages.

## Zooming In

Start with a C4 context diagram for the big picture, then zoom into the part of the context you are explaining:

- Follow the **C4 levels** for structure: context (level 1) → container (level 2) → component (level 3).
- Use a **flowchart** when the explanation is about a process or workflow — step by step, with decision branches.
- Use a **sequence diagram** when the explanation is about interactions — who calls whom, in what order, and whether calls are synchronous or asynchronous.

The solution architecture of an ADR is itself a C4/flowchart view of the target state: draw it the same way, adding the chosen option as a named system/container and marking what changes because of the decision.

## C4 Context Diagram (Level 1)

Use the C4-PlantUML standard library macros. Include `C4_Context.puml` for context diagrams, `C4_Container.puml` for container diagrams, and `C4_Component.puml` for component diagrams:

| Element | C4-PlantUML macro | Example |
|---|---|---|
| Person (actor) | `Person(alias, "Label", "Description")` | `Person(customer, "Customer", "Places orders")` |
| System in scope | `System(alias, "Label", "Description")` | `System(oms, "Order Management Service", "Handles orders")` |
| External system | `System_Ext(alias, "Label", "Description")` | `System_Ext(ps, "Payment Processor", "Charges payments")` |
| Container | `Container(alias, "Label", "Tech", "Description")` | `Container(api, "API Gateway", "Go", "Ingests orders")` |
| Database / store | `ContainerDb(alias, "Label", "Tech", "Description")` | `ContainerDb(db, "Order DB", "PostgreSQL", "Stores orders")` |
| Component | `Component(alias, "Label", "Tech", "Description")` | `Component(oc, "Order Controller", "REST", "Ingests orders")` |
| Relationship | `Rel(from, to, "Label", "Description")` | `Rel(customer, oms, "places orders")` |
| Grouping | `System_Boundary(alias, "Label") { ... }` / `Container_Boundary(alias, "Label") { ... }` | `System_Boundary(oms, "Order Management Service") { ... }` |

Rules:

- Show the system(s) IN scope as the center of the diagram; keep internal containers/databases out of a level-1 context diagram.
- Show only direct relationships; no message-level detail at this level.
- Label every relationship with what flows across it (data, request, event).

## C4 Container Diagram (Level 2)

- Include `C4_Container.puml`; zoom into a system and place its top-level containers (applications, data stores, microservices) inside a `System_Boundary`.
- Name each container with `Container(alias, "Label", "Tech", "Description")` and note its main technology.
- Connect containers with `Rel` and label what flows between them.

## C4 Component Diagram (Level 3)

- Include `C4_Component.puml`; zoom into a single container with a `Container_Boundary` to show the components inside it (modules, services, libraries).
- Name each component with `Component(alias, "Label", "Tech", "Description")` and give it a one-line responsibility.
- Connect components with `Rel`; keep dependencies pointing in a clean direction.

## Flowchart

- Show the sequence of steps and the decision branches that matter to the explanation.
- Keep each branch readable — extract a second diagram instead of packing in more branches.

## Sequence Diagram

- Name each participant (actor, system, component) as a lifeline.
- Show messages top-to-bottom in time order.
- Use solid arrows for synchronous calls and dashed arrows for asynchronous ones.
- Highlight the interaction that matters for the decision (e.g., a revocation path, a payment flow).

## Decision Driver Map

A tree that separates hard constraints from soft preferences:

- Root: "Decision drivers"
- Branch 1: "Hard constraints (knock-out)" → each must-have driver
- Branch 2: "Soft preferences" → each nice-to-have driver

## Option Comparison Matrix + Elimination Tree

A drivers × options grid using three visual states:

- ✅ satisfies the driver
- ⚠️ partially satisfies / conditional
- ❌ fails the driver (mark knock-out failures prominently)

Pair the matrix with an elimination tree when explaining WHY options were dropped:

- Start node: all considered options
- For each eliminated option: edge labeled with the failing driver → "Eliminated"
- For the chosen option: edge labeled "passes all hard constraints" → "Chosen"

## PlantUML Snippets

### C4 context diagram

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

Person(customer, "Customer", "Places orders and queries history")
System(oms, "Order Management Service", "Handles orders and payments")
System_Ext(ps, "Payment Processor", "Charges payments")
System_Ext(iam, "GCP IAM", "AuthN / authZ")

Rel(customer, oms, "places orders / queries")
Rel(oms, ps, "payment processing")
Rel(oms, iam, "authN / authZ")
@enduml
```

### C4 container diagram

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

Person(customer, "Customer", "Places orders and queries history")

System_Boundary(oms, "Order Management Service") {
    Container(api, "API Gateway", "Go", "Ingests orders")
    Container(svc, "Order Service", "Go", "Business logic")
    ContainerDb(db, "Order DB", "PostgreSQL", "Stores orders")
}

System_Ext(ps, "Payment Processor", "Charges payments")

Rel(customer, api, "HTTPS", "places orders")
Rel(api, svc, "gRPC", "forwards")
Rel(svc, db, "SQL", "reads / writes")
Rel(svc, ps, "HTTPS", "charges")
@enduml
```

### C4 component diagram

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

Container_Boundary(svc, "Order Service") {
    Component(oc, "Order Controller", "REST API", "Ingests orders")
    Component(or, "Order Repository", "DAO", "Queries orders")
    Component(pc, "Payment Client", "HTTP client", "Charges payments")
}

ContainerDb(db, "Order DB", "PostgreSQL", "Stores orders")
System_Ext(ps, "Payment Processor", "Charges payments")

Rel(oc, or, "calls", "queries orders")
Rel(or, db, "SQL", "reads / writes")
Rel(oc, pc, "calls", "charges payment")
Rel(pc, ps, "HTTPS", "payment request")
@enduml
```

### Flowchart (zoom into a flow)

```plantuml
@startuml
start
:Receive order;
if (Validate payment) then (yes)
  :Write to database;
  :Notify customer;
else (no)
  :Reject order;
endif
stop
@enduml
```

### Sequence diagram (zoom into interactions)

```plantuml
@startuml
actor Customer
participant "Order Management Service" as OMS
participant "Payment Processor" as PS

Customer -> OMS : place order
OMS -> PS : charge payment
PS --> OMS : payment result
OMS -> OMS : persist order
@enduml
```

### Decision driver map

```plantuml
@startuml
rectangle "Decision drivers" as Root
rectangle "Hard constraints" as Hard
rectangle "Soft preferences" as Soft
rectangle "ACID transactions" as H1
rectangle "Low cost" as S1

Root --> Hard
Root --> Soft
Hard --> H1
Soft --> S1
@enduml
```

### Elimination tree

```plantuml
@startuml
rectangle "All options" as All
rectangle "Option A" as A
rectangle "Option B" as B
rectangle "Eliminated" as X
rectangle "Chosen: Option C" as W

All --> A
All --> B
A --> X : fails driver X
B --> W : passes all hard constraints
@enduml
```

## Fallback Snippets

When PlantUML is unavailable, render the same content in Mermaid or as ASCII for single-message diagrams.

### Mermaid — C4 context diagram

```mermaid
flowchart LR
    Actor([Actor]) -->|request| Sys[System in scope]
    Sys -->|reads / writes| DB[(Database)]
    Sys -->|calls| Ext[External System]
```

### Mermaid — sequence diagram

```mermaid
sequenceDiagram
    actor Customer
    participant OMS as Order Management Service
    participant PS as Payment Processor
    Customer->>OMS: place order
    OMS->>PS: charge payment
    PS-->>OMS: payment result
```

### ASCII fallback

```
[Customer] --places orders--> [Order Management Service]
[Order Management Service] --reads / writes--> [(Database)]
[Order Management Service] --payment--> [Payment Processor]
```

## Updating and Extending Diagrams

Diagrams are living artifacts of the ADR session: sync them whenever the user confirms a new finding or correction, so the visual record never goes stale.

- **Update in place when the change affects an existing diagram**: keep the same diagram identity (title, aliases, structure) and change only what is affected. State the delta in one line before the updated code block (e.g., "Updated: added the analytics system and its relationship to the OMS").
- **Add a new diagram when the context is genuinely new**: a flow, zoom level, or edge case no existing diagram covers. Give it a distinct title; do not overload an existing diagram with extra branches.
- **Preserve identity**: when updating, keep the same aliases and labels so readers can diff old vs. new easily.
- **Keep the set consistent**: after every change, each confirmed fact appears in at least one diagram, and no diagram contradicts the latest confirmed state. Cross-check the whole set before proceeding.
- **Never leave stale visuals**: if a diagram depicts an obsolete state, update or replace it — do not leave both the old and new versions in the session.

## Cross-References

- Selection logic (which diagram to draw for which context): **diagram-selection** in `SKILL.md`
- When to update vs. add diagrams after corrections: **diagram-sync** in `SKILL.md`
- Where diagrams appear in the final document: `reference/adr-template.md`
