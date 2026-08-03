# Example: Structured Code Reference for Payment Service Migration

**Scenario**: After the 4-area parallel investigation in `examples/multi-agent-investigation.md`, the orchestrator merges each sub-agent's returned per-area code reference into one consolidated map. The same document is then included in every later sub-agent brief (ADR drafting, deep-dive) so no agent re-scans code.

**Applies**: `investigate-per-area` (collect per-area references) → `compile-code-reference`

**What makes this distinct**: This example shows the full 7-section structure and how searched-negatives and confidence tags prevent redundant scanning.

---

## Code Reference: Payment Service Migration

### 1. Scope
- Repos: `payment-service` (monolith), `infra-configs` (K8s/Kong/GitHub Actions)
- Areas: service decomposition, inter-service communication, database decomposition, migration strategy
- Last updated: 2026-08-03

### 2. Entry Points
| Area | Entry point (file:line) | Trigger | Purpose |
|---|---|---|---|
| Service decomposition | `controller/PaymentController.java:42` | `POST /api/payments` | Single HTTP entry for all payment types |
| Inter-service communication | `service/PaymentOrchestrator.java:88` | New payment request | Coordinates CreditCard/BankTransfer/Wallet flows |
| Database decomposition | `repository/TransactionRepository.java:31` | Any payment persistence | Shared `transactions` table access |
| Migration strategy | `k8s/payment-deployment.yaml:12` | Deploy | 3-replica monolith pod spec |
| Migration strategy | `.github/workflows/deploy.yml:24` | CI/CD | Canary deploy pipeline |

### 3. Key Code Locations
| Area | File:line | Symbol | Role | Why it matters |
|---|---|---|---|---|
| Service decomposition | `domain/CreditCardPayment.java:15` | `CreditCardPayment` | One of 3 payment domains | Boundary candidate |
| Service decomposition | `service/PaymentOrchestrator.java:88` | `PaymentOrchestrator` | 1200-line central coordinator | Couples all payment types |
| Service decomposition | `service/CreditCardService.java:63` | `CreditCardService` | Imports bank-transfer domain objects | Tight-coupling evidence |
| Communication | `adapter/WalletGrpcClient.java:41` | `WalletGrpcClient` | gRPC call to wallet provider | External integration point |
| Communication | `adapter/LegacyAcquirerSoapClient.java:77` | `LegacyAcquirerSoapClient` | SOAP call to legacy acquirer | Must-maintain integration |
| Database | `db/schema.sql:201` | `transactions` table | Shared across payment types | Decomposition blocker |
| Database | `db/stored-procs/settlement.sql:1` | settlement procedures | 12 procs, 2000+ lines | Migration blocker |
| Migration | `kong/kong.yml:34` | `/api/payments/*` route | Single upstream to monolith | No traffic splitting |

### 4. Call Chains
**Flow: Wallet payment request**
1. `controller/PaymentController.java:42` — routes request by payment type
2. `service/PaymentOrchestrator.java:88` — `process()` dispatches to wallet flow
3. `service/WalletPaymentService.java:120` — `charge()` validates + calls wallet provider
4. `adapter/WalletGrpcClient.java:41` — sends gRPC `ChargeRequest` to wallet provider
5. `repository/TransactionRepository.java:31` — `save()` writes `transactions` row
6. `service/PaymentOrchestrator.java:140` — `settle()` calls stored proc `sp_settle`

**Flow: CI/CD deploy (migration area)**
1. `.github/workflows/deploy.yml:24` — on push to main → build
2. `.github/workflows/deploy.yml:40` — canary 10% rollout
3. `k8s/payment-deployment.yaml:12` — 3 replicas, no traffic-split labels

### 5. Evidence Ledger
| Claim / Question | Verdict | Evidence (file:line) | Confidence |
|---|---|---|---|
| Is there a circuit breaker around external calls? | No | `grep "CircuitBreaker\|Resilience4j\|fallback"` across `payment-service` — no matches | Verified (negative) |
| Are all internal calls in-process? | Yes | `PaymentOrchestrator.java:88` calls services directly; no internal HTTP client found | Verified |
| Does `transactions` hold all payment types? | Yes | `db/schema.sql:201` — no payment-type discriminator at table level | Verified |
| Can Kong split traffic? | Unknown | `kong/kong.yml:34` — single upstream, no weighted upstreams | Inferred |
| Team has async messaging experience? | N/A | from user conversation, not code | Unverified |

### 6. Cross-Area Dependencies
| From | To | Coupling (file:line) |
|---|---|---|
| Service decomposition | Database decomposition | `PaymentOrchestrator.java:88` → `TransactionRepository.java:31` — every payment type writes shared `transactions` |
| Inter-service communication | Migration strategy | `kong/kong.yml:34` single upstream — no routing for strangler-fig step-down |
| Service decomposition | Inter-service communication | `CreditCardService.java:63` imports bank-transfer domain — decomposition must sever this first |

### 7. Searched-Negatives & Gaps
| Area | Search performed | Result | Next step |
|---|---|---|---|
| Communication | `grep -ri "kafka\|rabbit\|mq"` in `payment-service` | No message broker usage | Prototype async feasibility (direction D2) |
| Migration | `grep -ri "featureflag\|trafficsplit"` in `infra-configs` | None found | Verify Kong weighted-upstream capability in docs |
| Service decomposition | Search for `*Module` / bounded-context markers | None — package-by-layer only | Deep-dive into domain import graph (D1) |

---

## Passing the Code Reference to Sub-Agents

When the orchestrator later dispatches ADR drafting, each brief includes its area's slice:

```
Produce ADR for: Service Decomposition Boundaries
Code reference: code-reference-payment-migration.md §3 (key locations), §5 (evidence), §6 (coupling)
Do not re-scan covered code — verify only inferred/unverified claims or marked gaps.
[Decision drivers, options, assumed solution as in multi-agent-investigation.md]
```

Sub-agents start from the map's entry points and call chains, treat **verified** claims as settled, and return any new locations they find so the map keeps growing.
