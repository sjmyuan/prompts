# API Design Standards

API and event schema design should include:
- **Endpoint / Topic name** and HTTP method (for REST) or channel/queue (for events).
- **Request/Response or Event payload schema** in JSON, Protocol Buffers, or Avro as appropriate.
- **Authentication & Authorization** requirements (OAuth2, API Key, mTLS, etc.).
- **Error handling** conventions (status codes, error body format).
- **Rate limiting, pagination, idempotency** considerations where relevant.
- For async events: schema versioning strategy, DLQ handling, ordering guarantees.
