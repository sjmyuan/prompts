# Sequence Diagram Conventions

Use Mermaid `sequenceDiagram` syntax. Every sequence diagram follows the **sequence diagram contract**: one zoom level, traceable participants, contract-accurate messages, and a strict noise budget.

## Mermaid Quick Reference

| Pattern | Syntax |
|---|---|
| Participants | `actor "Name"`, `participant "Name" as "Label"`, `database "Name"` |
| Sync call | `A->>B: N: methodName(params)` (solid arrow) |
| Async/event | `A-)B: N: eventName(data)` (open arrow) |
| Return | `A-->>B: N: return value` (dashed arrow) |
| Activation | `activate A` / `deactivate A` |
| Conditional | `alt / else / end` |
| Loop | `loop N times / end` |
| Parallel | `par / and / end` |
| Note | `Note over A,B: text` |
| Comment | `%% level / purpose declaration` |

## Zoom Level (hard rule)

Every sequence diagram operates at exactly **one** zoom level. Never mix levels in a single diagram — a whole service must not share a diagram with a single class.

| Level | Lifelines are | Messages are |
|---|---|---|
| Container (cross-system) | services / systems | API endpoints, events, protocols |
| Component (cross-module) | modules / interfaces | method calls |
| Code (cross-file / class) | files / classes | method signatures |

Declare the level in a `%%` comment and in the caption, e.g. `%% Level: code — cross-file / class`.

## Participant Naming

Encode the identity path in the lifeline label so the reader always knows **which file / class / system** it is:

- Cross-file / class: `participant Alias as "path/to/file.ts<br/>ClassName"` — **always include the file path**, it is the easiest way to locate the element.
- Show the interface when the role is defined by one: `...<br/>OrderService : IOrderService`
- Group ownership with an alias prefix per system/module (`OMS_*`, `ORD_*`) — Mermaid has no boundary boxes, so the prefix carries the grouping.
- Use types semantically: `actor` = external, `participant` = service/class, `database` = store.

## Message Labels

Messages carry the **real contract**, never prose:
- Method calls: `placeOrder(order)` — real name and params from the code
- API calls: `POST /orders`, `gRPC ReserveStock`
- Events: `publish OrderCreated (Kafka: orders)`

**Events and self-calls carry a short explanation** of their effect, separated by `<br/>`, so the intent is readable without the schema:

```
OrderService->>OrderService: 2: validateOrder(order)<br/>checks stock & discount eligibility
OrderService->>Broker: 3: publish OrderCreated<br/>notifies downstream services
```

Self-calls: show at most **2 per lifeline**; larger internal logic moves to a `Note over` or a flowchart.

## Message Numbering

Number messages sequentially for call-stack cross-referencing. Indentation in labels reflects call depth:

```mermaid
sequenceDiagram
    %% Level: code — cross-file / class
    participant CTRL as "orders/controller.ts<br/>OrderController"
    participant SVC as "orders/service.ts<br/>OrderService : IOrderService"
    participant REPO as "orders/repo.ts<br/>OrderRepository"
    database DB

    CTRL->>SVC: 1: createOrder(dto)
    SVC->>SVC: 2: validateOrder(dto)<br/>checks stock & discount
    SVC->>REPO: 3: save(order)
    REPO->>DB: 4: INSERT orders
    DB-->>REPO: 5: orderId
    REPO-->>SVC: 6: OrderId
    SVC->>CTRL: 7: Order
```

Return messages get their own numbers. Frame numbers in call stack traces must match these numbers.

## Noise Budget

- **4–6 lifelines max**; more → split the flow into multiple diagrams.
- **One diagram = one flow**; error paths in a separate diagram or a single `alt`.
- **Omit returns that carry no data** — show a return only when the next step needs its value.
- Skip `activate` / `deactivate` unless call nesting matters.
- More than 2 structural blocks (`alt` / `loop` / `par`) → extract a flowchart.
