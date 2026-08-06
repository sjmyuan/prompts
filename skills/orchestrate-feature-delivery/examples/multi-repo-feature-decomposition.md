# Example: Multi-Repo Feature Decomposition

**Scenario**: A payment-migration spike just finished. Its change summary lists ~18 change items across `api-gateway`, `order-service`, and `shared-contracts`. The user asks: "Split the spiked work into features, align which can be done in parallel, and give me an index so agents can plan and execute in parallel."

**Applies**: **decompose-change-into-features** → **map-features-to-repos** → **order-feature-delivery** → **produce-delivery-index**

## Input (change summary highlights)

- **New**: `WalletService` in `order-service`; token endpoint in `api-gateway`; shared wallet DTOs + envelope schema in `shared-contracts`
- **Modified**: order flow in `order-service` consumes wallet; gateway route in `api-gateway`
- **Data**: `wallet_ledger` table in `order-service`
- **Retired**: `BankTransferService` in `order-service` (after cutover)

## 1. Decomposition (features)

- **F1 wallet-contracts** — `shared-contracts` only: wallet DTOs + envelope schema. *Small shared change, stays in the first consuming feature.*
- **F2 wallet-service** — `order-service`: `WalletService` + `wallet_ledger` migration + tests.
- **F3 wallet-api-gateway** — `api-gateway`: token endpoint + route.
- **F4 order-wallet-integration** — `order-service` + `api-gateway`: order flow consumes wallet, retire `BankTransferService`.

## 2. Feature × repo matrix

| Feature | api-gateway | order-service | shared-contracts |
|---|---|---|---|
| F1 wallet-contracts | — | — | PR |
| F2 wallet-service | — | PR | — |
| F3 wallet-api-gateway | PR | — | — |
| F4 order-wallet-integration | PR | PR | — |

## 3. Waves

- F1 depends on nothing → **Wave 0**.
- F2 and F3 consume F1's DTOs (contract-first) → **Wave 1, parallel**.
- F4 consumes F2's service and F3's endpoint → **Wave 2**.
- `order-service` hosts F2 then F4 — no file conflict, but its PRs serialize naturally across waves.

**Wave 0**: F1 · **Wave 1 (parallel)**: F2, F3 · **Wave 2**: F4 (after F2 + F3 merge)

## 4. Delivery index (excerpt, initial state)

```markdown
# Delivery Index: Payment Migration

## Summary
4 features · 3 repos · 3 waves · critical path: F1 → F2/F3 → F4

## Spike References
- **Change summary**: docs/spikes/payment-migration/change-summary.md
- **Solution doc**: docs/spikes/payment-migration/solution-doc.md
- **ADRs**: docs/spikes/payment-migration/adr-001-wallet.md · adr-002-cutover.md

## Cell plan status
| Cell | Status | Agent | Plan location |
|---|---|---|---|
| shared-contracts/F1 | unplanned | — | — |
| order-service/F2 | unplanned | — | — |
| api-gateway/F3 | unplanned | — | — |
| order-service/F4 | unplanned | — | — |
| api-gateway/F4 | unplanned | — | — |
```

All 5 cells start **unplanned** → the epic is now driven by **orchestrate-delivery** (see **examples/orchestration-round.md**): wave 0 dispatches `shared-contracts/F1`, then F2/F3 in parallel, then F4.
