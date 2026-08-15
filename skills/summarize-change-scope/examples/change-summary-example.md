# Example: Change Summary for Payment Service Migration

**Scenario**: The user has completed a spike on migrating the payment monolith to microservices and wants to understand the concrete code changes required.

**Applies**: `compile-change-summary`

**What makes this distinct**: Demonstrates the change summary with code access — the current codebase is available, so estimates are concrete and code-path-verified.

---

## User Input

> "The solution doc looks good. Now can you give me a summary of what code actually needs to change? I have the codebase open — feel free to check it."

## Assistant Output

*[compile-change-summary applied — with code access confirmed]*

# Change Summary: Payment Service Microservice Migration

## Area: Service Decomposition Boundaries
### ADR: `adr-service-decomposition-01-split-monolith.md` — payment-type services

### New
- **WalletPaymentService** (Spring Boot microservice): New service extracted from monolith. Handles wallet payment initiation, authorization, settlement, refunds.
  - Scope: ~15–20 Java files (controller, service, repository, domain), ~3K–5K LOC estimated
  - Depends on: `adr-communication-01-service-communication.md`, `adr-database-01-break-up-database.md`
- **BankTransferPaymentService** (Spring Boot): New service for bank transfer payments.
  - Scope: ~20–25 Java files, ~5K–8K LOC estimated
- **CreditCardPaymentService** (Spring Boot): New service for credit card payments.
  - Scope: ~30–35 Java files, ~8K–12K LOC estimated (largest domain)
- **PaymentSharedLib** (Java library): Shared utilities, domain models, and error types used by all three services.
  - Scope: ~10–15 Java files, ~2K–3K LOC estimated
- **Dockerfiles + K8s manifests** for each new service.

### Modified
- **`PaymentOrchestrator.java`** (monolith): Refactor from monolithic coordinator to routing/delegation layer. Replace direct method calls with REST/gRPC calls to new services.
  - Scope: ~1200 lines → ~300 lines (delegation only)
  - Risk: Central coordination point — must preserve transaction ordering guarantees
- **`ApiGatewayConfig.java`**: Add routing rules to direct `/api/payments/wallet/*` → WalletPaymentService, etc.
  - Scope: ~50 lines of new config
- **`application.yml`** (monolith): Add service discovery config, remove hardcoded payment type references.
  - Scope: ~30 lines changed

### Retired
- **Wallet payment domain classes** in monolith: `WalletPaymentService.java`, `WalletPaymentController.java`, `WalletPaymentRepository.java`, and ~10 related domain/DTO classes.
  - When: After WalletPaymentService is live and stable (Strangler Fig phase 1 complete)
- **Bank transfer domain classes**: Similar scope, retired after phase 2.
- **Credit card domain classes**: Retired after phase 3 (final extraction).

---

## Area: Inter-service Communication
### ADR: `adr-communication-01-service-communication.md` — hybrid sync/async

### New
- **Kafka topic definitions**: `payment.initiated`, `payment.authorized`, `payment.settled`, `payment.refunded`
  - Scope: Terraform/Infrastructure-as-Code for topic provisioning
- **Event schemas** (Avro): Define schemas for each event type.
  - Scope: ~4–6 `.avsc` files

### Modified
- **`PaymentOrchestrator.java`**: Add Kafka producer for emitting payment events after each processing step.
  - Scope: ~100 lines added
- **All new services**: Add Kafka consumers for relevant events (e.g., Settlement listens for `payment.authorized`).

### Dependency
- **Apache Kafka** cluster: Provision in infrastructure. Team to adopt Kafka client library (`spring-kafka`).
- **Schema Registry**: For Avro schema evolution.

---

## Area: Database Decomposition
### ADR: `adr-database-01-break-up-database.md` — database per service

### New
- **Per-service databases**: `wallet_db`, `banktransfer_db`, `creditcard_db` — initially schemas within the same PostgreSQL instance, later separate instances.
  - Scope: ~3 DDL migration scripts

### Modified
- **`transactions` table**: Split into per-service tables (`wallet.transactions`, `banktransfer.transactions`, `creditcard.transactions`).
  - Scope: Migration scripts + data migration job
  - Risk: Data integrity during migration — requires dual-write period
- **`accounts` table**: Split similarly. Shared `audit_log` remains as a common table (referenced read-only by all services).

### Data
- **Data migration job**: ETL process to copy existing transaction/account data into per-service tables. Runs incrementally during Strangler Fig phases.
  - Scope: ~1 batch job, ~500 LOC estimated

### Retired
- **12 stored procedures** for settlement logic: Rewrite as application-level logic in each service.
  - Scope: ~2000 lines of PL/pgSQL to retire; ~1500 lines of Java to write

### ADR: `adr-database-02-schema-migration.md` — expand-contract migrations

### Data
- **Expand-contract migration scripts**: additive columns → backfill → drop, shipped with each service as it extracts.
  - Scope: ~3–4 migration scripts + backfill jobs

### Modified
- **Settlement stored procedures**: procedure rewrites follow the phased DB split (aligns with `adr-database-01-break-up-database.md`).
  - Scope: ~2000 lines PL/pgSQL rewritten incrementally

---

## Area: Migration Strategy
### ADR: `adr-migration-01-zero-downtime-migration.md` — strangler fig

### Configuration
- **Kong API Gateway**: Add routing rules with traffic splitting (canary). Route `wallet` traffic to new service progressively (10% → 50% → 100%).
  - Scope: Kong configuration changes (~100 lines)
- **Feature flags**: Introduce feature flag library (e.g., LaunchDarkly or in-house) to toggle between monolith and new service paths.
  - Scope: ~5 feature flags; ~200 LOC integration code
- **CI/CD pipeline** (GitHub Actions): Add build/deploy jobs for each new service.
  - Scope: ~3 new workflow files

---

## Cross-Cutting Concerns

| Concern | Change | Affected Areas |
|---|---|---|
| **Authentication** | All new services must integrate with existing OAuth2 provider. Extract auth interceptor from monolith into `PaymentSharedLib`. | Areas 1, 2 |
| **Logging & monitoring** | Standardize logging format across all services. Add distributed tracing (e.g., OpenTelemetry). | All areas |
| **Error handling** | Define shared error response format and error codes in `PaymentSharedLib`. | All areas |

## Notes

- Estimates are based on current monolith code structure (verified). Actual LOC may vary based on framework boilerplate and test code.
- Data migration is the highest-risk area — recommend a separate spike or proof-of-concept for the dual-write period.
- Stored procedure retirement should happen last (after all services are live) to avoid disrupting existing settlement flows.
- Team has no Kafka experience — budget time for learning and a proof-of-concept before production integration.
