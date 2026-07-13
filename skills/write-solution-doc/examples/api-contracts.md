# Example: API Contracts and Event Schemas Focus

**Scenario**: A user has finalized the C4 topology and sequence diagrams for an "InventorySync" solution. They now need detailed API contracts and event schemas defined. The solution involves REST APIs (between services) and async events (for inventory change propagation).

**Applies**: `design-api-event-schema` — demonstrates REST API and async event schema design with authentication, error handling, and versioning.

---

## Input (User's Prompt)

> Our InventorySync solution has:
> - **Inventory Service** (REST API consumed by Order Service for stock checks, and by Admin Dashboard for CRUD)
> - **Warehouse Service** (receives async events when inventory changes)
> - Communication: Order Service calls Inventory Service via REST. Inventory changes are published as Kafka events. Warehouse Service consumes those events.
> 
> I need API contracts for the Inventory Service's REST endpoints and event schemas for the Kafka topics.

---

## Capability 4: design-api-event-schema

**Q1**: What API style/format do you prefer for REST? JSON, Protobuf, or something else?

*User answers: JSON with standard REST conventions.*

**Q2**: What authentication method should the Inventory Service endpoints use?

*User answers: OAuth2 with JWT Bearer tokens, scoped by service. Order Service gets `inventory:read`, Admin Dashboard gets `inventory:write`.*

**Q3**: Do you need pagination for list endpoints?

*User answers: Yes, cursor-based pagination for the products list endpoint (potentially thousands of SKUs).*

**Q4**: Any rate limiting requirements?

*User answers: Order Service can call up to 1000 req/s. Admin Dashboard limited to 100 req/s.*

**Q5**: For the Kafka events, do you have a schema versioning strategy in mind?

*User answers: We use Confluent Schema Registry with Avro. Backward-compatible changes only. Breaking changes get a new topic with a version suffix.*

**Q6**: What's your dead-letter queue strategy for failed events?

*User answers: Failed events go to a `inventory.dlq` topic after 3 retries. Ops team monitors that topic.*

---

### Output: REST API Contracts

#### 1. Check Stock (Order Service → Inventory Service)

| Field | Value |
|---|---|
| **Endpoint** | `GET /api/v1/inventory/stock` |
| **Auth** | OAuth2 Bearer token (scope: `inventory:read`) |
| **Rate Limit** | 1000 req/s per service account |
| **Description** | Batch check stock availability for multiple SKUs |

**Request**:
```json
{
  "skus": ["SKU-001", "SKU-002", "SKU-003"],
  "warehouse_id": "WH-US-EAST-1"
}
```

| Param | Type | Required | Validation |
|---|---|---|---|
| `skus` | `string[]` | Yes | 1–100 items, alphanumeric + hyphens |
| `warehouse_id` | `string` | No | If omitted, checks all warehouses |

**Response (200)**:
```json
{
  "results": [
    {
      "sku": "SKU-001",
      "available": 42,
      "reserved": 5,
      "warehouse_id": "WH-US-EAST-1",
      "last_updated": "2026-07-04T10:30:00Z"
    },
    {
      "sku": "SKU-002",
      "available": 0,
      "reserved": 0,
      "warehouse_id": "WH-US-EAST-1",
      "last_updated": "2026-07-04T09:15:00Z"
    }
  ]
}
```

**Error Responses**:

| Status | Code | Body |
|---|---|---|
| 400 | `INVALID_SKUS` | `{"error":"INVALID_SKUS","message":"SKU-XXX is not a valid format","details":["SKU-XXX"]}` |
| 401 | `UNAUTHORIZED` | `{"error":"UNAUTHORIZED","message":"Invalid or expired token"}` |
| 403 | `INSUFFICIENT_SCOPE` | `{"error":"INSUFFICIENT_SCOPE","message":"Token lacks inventory:read scope"}` |
| 429 | `RATE_LIMITED` | `{"error":"RATE_LIMITED","message":"Too many requests","retry_after":30}` |

---

#### 2. Update Inventory (Admin Dashboard → Inventory Service)

| Field | Value |
|---|---|
| **Endpoint** | `PATCH /api/v1/inventory/products/{sku}` |
| **Auth** | OAuth2 Bearer token (scope: `inventory:write`) |
| **Rate Limit** | 100 req/s per user |
| **Idempotency** | `Idempotency-Key` header required |

**Request**:
```json
{
  "quantity_delta": -5,
  "reason": "ORDER_FULFILLED",
  "order_id": "ORD-12345"
}
```

| Param | Type | Required | Validation |
|---|---|---|---|
| `quantity_delta` | `int` | Yes | Non-zero, -10000 to 10000 |
| `reason` | `string` | Yes | Enum: `ORDER_FULFILLED`, `RESTOCK`, `DAMAGED`, `CORRECTION` |
| `order_id` | `string` | Conditional | Required when reason is `ORDER_FULFILLED` |

**Response (200)**:
```json
{
  "sku": "SKU-001",
  "previous_quantity": 42,
  "new_quantity": 37,
  "delta": -5,
  "reason": "ORDER_FULFILLED",
  "updated_at": "2026-07-04T11:00:00Z"
}
```

---

#### 3. List Products (Admin Dashboard → Inventory Service)

| Field | Value |
|---|---|
| **Endpoint** | `GET /api/v1/inventory/products` |
| **Auth** | OAuth2 Bearer token (scope: `inventory:write` or `inventory:read`) |
| **Pagination** | Cursor-based (`?cursor=xxx&limit=50`) |
| **Rate Limit** | 100 req/s |

**Request**: `GET /api/v1/inventory/products?cursor=eyJza3UiOiJTS1UtMDUwIn0&limit=50`

**Response (200)**:
```json
{
  "data": [
    {
      "sku": "SKU-001",
      "name": "Widget Pro",
      "quantity": 37,
      "warehouse_id": "WH-US-EAST-1",
      "updated_at": "2026-07-04T11:00:00Z"
    }
  ],
  "pagination": {
    "next_cursor": "eyJza3UiOiJTS1UtMDUxIn0",
    "has_more": true,
    "limit": 50
  }
}
```

---

### Output: Event Schemas (Kafka + Avro)

#### Topic: `inventory.changed.v1`

| Field | Value |
|---|---|
| **Topic** | `inventory.changed.v1` |
| **Schema Registry** | Confluent Schema Registry |
| **Format** | Avro |
| **Partitioning Key** | `sku` (ensures ordering per product) |
| **DLQ** | `inventory.dlq` after 3 retries |
| **Versioning** | Backward-compatible changes on same topic. Breaking changes → new topic `inventory.changed.v2` |

**Avro Schema** (`inventory.changed.v1-value.avsc`):
```json
{
  "type": "record",
  "name": "InventoryChanged",
  "namespace": "com.inventorysync.events",
  "fields": [
    {
      "name": "event_id",
      "type": "string",
      "doc": "UUID v4 for deduplication"
    },
    {
      "name": "event_type",
      "type": {
        "type": "enum",
        "name": "InventoryEventType",
        "symbols": ["STOCK_DECREASED", "STOCK_INCREASED", "OUT_OF_STOCK", "BACK_IN_STOCK"]
      },
      "doc": "Derived from quantity_delta and thresholds"
    },
    {
      "name": "sku",
      "type": "string"
    },
    {
      "name": "warehouse_id",
      "type": "string"
    },
    {
      "name": "previous_quantity",
      "type": "int"
    },
    {
      "name": "new_quantity",
      "type": "int"
    },
    {
      "name": "delta",
      "type": "int"
    },
    {
      "name": "reason",
      "type": {
        "type": "enum",
        "name": "ChangeReason",
        "symbols": ["ORDER_FULFILLED", "RESTOCK", "DAMAGED", "CORRECTION"]
      }
    },
    {
      "name": "timestamp",
      "type": "long",
      "logicalType": "timestamp-millis"
    },
    {
      "name": "schema_version",
      "type": "string",
      "default": "1.0.0"
    }
  ]
}
```

**Consumer: Warehouse Service**

| Concern | Strategy |
|---|---|
| **Idempotency** | Deduplicate on `event_id` (UUID v4), store processed IDs in Redis with 7-day TTL |
| **Ordering** | Consume by `sku` partition — per-product ordering guaranteed |
| **Backpressure** | Consumer pause on partition if processing lag > 10,000 messages |
| **Error Handling** | 3 retries with exponential backoff, then DLQ. Alert Ops team on DLQ messages. |
