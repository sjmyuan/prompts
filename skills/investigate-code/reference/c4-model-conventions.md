# C4 Model Conventions

## C2 Container Diagram

PlantUML: `!include <C4/C4_Container>`

**Elements**: `Person()` (users/actors, external left), `Container()` (applications/services), `ContainerDb()` (databases, below services), `ContainerQueue()` (message brokers), `System()` (external systems, external right), `System_Boundary()` (group related containers), `Rel(src, tgt, label)` (connections).

**Connection labels**: Include protocol and endpoint — `"POST /payments (HTTPS)"`, `"publishes OrderConfirmed (Kafka)"`, `"JDBC"`.

**Layout**: External actors left, external systems right, databases below services, message brokers between.

## C3 Component Diagram

PlantUML: `!include <C4/C4_Component>`

**Elements**: `Container_Boundary(name, label)` (wraps internal components in dashed box), `Component(name, label, technology, description)` (internal components).

**Layering**: Controllers/listeners (outer ring) → Services/orchestrators (middle) → Domain/repositories (inner). Mark external dependencies with `$external=true`.

**Connection labels**: Same as C2 — include protocol and endpoint.
