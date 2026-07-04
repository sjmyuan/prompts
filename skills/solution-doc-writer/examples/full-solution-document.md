# Example: Full Solution Document Workflow

**Scenario**: A user has a finalized solution decision for migrating their monolithic e-commerce platform to a microservices architecture and wants to produce a complete solution document covering all nine sections. The user starts from scratch with no pre-existing content.

**Applies**: Capabilities 1, 2, and 10 in detail, with truncated output for capabilities 3–9 — demonstrates the end-to-end sequencing pattern.

---

## Input (User's Initial Prompt)

> We've decided to migrate our legacy monolithic e-commerce platform (MonolithMart) to a microservices architecture. The new system is called "ShopMesh". We chose this because the monolith can't scale for our growing order volume (10x growth in 2 years), and different teams want to deploy independently. Key constraints: must be live before Black Friday (5 months), must comply with PCI-DSS for payments, and we can't have more than 30 minutes downtime during the migration. Can you help me write the solution document?

---

## Capability 1: clarify-business-context

**Assistant output** (step by step, one question at a time):

> **Q1**: Who are the key stakeholders for ShopMesh? (e.g., product owners, engineering leads, business sponsors)

*User answers: VP of Engineering is the sponsor, 3 engineering teams (Orders, Catalog, Payments), Product Manager: Sarah Chen*

> **Q2**: What is the scope boundary? Which parts of MonolithMart are being migrated to ShopMesh, and what stays on the monolith?

*User answers: Orders, Catalog, and Payments move to ShopMesh. User accounts, reviews, and recommendations stay on MonolithMart for now.*

> **Q3**: What alternative solutions were considered and why was microservices chosen?

*User answers: Considered modular monolith and vertical scaling. Microservices chosen for independent deployability and team autonomy.*

[...continues through 5-7 more questions about constraints, end users, success criteria...]

**Summary output**:

> Here's my understanding of the business context:
>
> **Problem**: MonolithMart cannot scale to handle 10x order volume growth. Teams are blocked on each other's deployment schedules.
>
> **Solution**: ShopMesh — microservices for Orders, Catalog, Payments. User accounts, reviews, recommendations remain on MonolithMart.
>
> **Decision Rationale**: Microservices chosen over modular monolith and vertical scaling for independent deployability and team autonomy.
>
> **Constraints**: Live before Black Friday (5 months), PCI-DSS compliance, ≤30min downtime during migration.
>
> **Stakeholders**: VP Eng (sponsor), 3 eng teams, PM Sarah Chen.
>
> Does this summary look correct? Shall I proceed to system topology?

---

## Capability 2: draw-c4-topology

**After Q&A about participating systems, communication patterns, external systems...**

**C2 Container Diagram output**:

```plantuml
@startuml ShopMesh C2 Container
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

Person(customer, "Customer", "Online shopper")
Person(admin, "Admin", "Store administrator")

System_Boundary(shopmesh, "ShopMesh") {
    Container(order_svc, "Order Service", "Go", "Manages order lifecycle")
    Container(catalog_svc, "Catalog Service", "Go", "Product catalog and inventory")
    Container(payment_svc, "Payment Service", "Java", "Payment processing (PCI-DSS)")
    ContainerDb(order_db, "Order DB", "PostgreSQL", "Order data")
    ContainerDb(catalog_db, "Catalog DB", "PostgreSQL", "Product and inventory data")
    ContainerDb(payment_db, "Payment DB", "PostgreSQL", "Payment records (encrypted)")
    Container(api_gw, "API Gateway", "Kong", "Routes, auth, rate limiting")
}

System_Ext(monomart, "MonolithMart", "Legacy monolith (accounts, reviews, recs)")
System_Ext(pay_gw, "Payment Gateway", "Stripe")
System_Ext(notify, "Notification Service", "SendGrid")

Rel(customer, api_gw, "HTTPS", "shops")
Rel(admin, api_gw, "HTTPS", "manages")
Rel(api_gw, order_svc, "gRPC")
Rel(api_gw, catalog_svc, "gRPC")
Rel(api_gw, payment_svc, "gRPC")
Rel(order_svc, order_db, "SQL")
Rel(catalog_svc, catalog_db, "SQL")
Rel(payment_svc, payment_db, "SQL")
Rel(order_svc, catalog_svc, "gRPC", "checks inventory")
Rel(order_svc, payment_svc, "gRPC", "processes payment")
Rel(payment_svc, pay_gw, "HTTPS", "charges")
Rel(order_svc, notify, "AMQP", "sends confirmations")
Rel(order_svc, monomart, "REST", "syncs account data")
Rel(catalog_svc, monomart, "REST", "syncs reviews")

@enduml
```

> **C2 Explanation**: ShopMesh has three microservices — Order, Catalog, and Payment — behind a Kong API Gateway. Each service owns its own PostgreSQL database. The Order service orchestrates checkout by calling Catalog (inventory check) and Payment (charge). Async notifications go through RabbitMQ to SendGrid. The legacy MonolithMart is called for account data and reviews.

[...user confirms, then C3 diagram for Order Service follows...]

---

## Capability 10: structure-solution-doc

**After all 9 capabilities confirmed, the final compilation:**

```markdown
# Solution Document: ShopMesh

## 1. Business Context & Solution Background

MonolithMart, our legacy e-commerce monolith, can no longer scale to meet 10x order volume growth projected over the next two years. ...

## 2. System Topology (C4 Model)

### 2.1 C2 — Container Diagram

[C2 PlantUML code + explanation]

### 2.2 C3 — Component Diagram: Order Service

[C3 PlantUML code + explanation]

## 3. Interaction Details (Sequence Diagrams)

### 3.1 Checkout Flow

[Sequence diagram + explanation]

### 3.2 Inventory Sync Flow

[Sequence diagram + explanation]

## 4. API / Event Schema

### 4.1 Order Service — Create Order

| Field | Value |
|---|---|
| Endpoint | `POST /api/v1/orders` |
| Auth | OAuth2 Bearer token |
| ... | ... |

## 5. Related Documents

| Title | Type | Link | Relevance |
|---|---|---|---|
| MonolithMart Architecture RFC | RFC | ... | Current system design |
| ... | ... | ... | ... |

## 6. External Dependencies

| System | Team | Contact | SLA | Fallback |
|---|---|---|---|---|
| Stripe | Payments Infra | ... | 99.99% | ... |
| ... | ... | ... | ... | ... |

## 7. Maintainers

| Component | Team | Primary Contact | Backup |
|---|---|---|---|
| Order Service | Orders Team | ... | ... |
| ... | ... | ... | ... |

## 8. RAID Analysis

### Risks

| ID | Description | Impact | Probability | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| R1 | Stripe API v2 deprecation before launch | High | Medium | ... | ... | ... |

[... full RAID table ...]

## 9. RACI Matrix

| Task / Decision | Orders Team | Catalog Team | Payments Team | Platform | PM |
|---|---|---|---|---|---|
| Define API contracts | R | R | R | C | I |
| Implement order service | R | I | C | C | I |
| ... | ... | ... | ... | ... | ... |
```

> The complete solution document is above. Would you like me to refine any section?
