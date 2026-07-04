# Example: Related Documents, External Dependencies, and Maintainers

**Scenario**: A user has finalized the C4 topology, sequence diagrams, and API contracts for a "PayBridge" payment orchestration solution. They now need to document related documents, external dependencies, and component maintainers. The user has a complex dependency landscape with multiple third-party payment providers.

**Applies**: `list-related-documents`, `list-external-dependencies`, and `list-maintainers` — demonstrates the document-listing and dependency-tracking workflows.

---

## Input (User's Prompt)

> We've finished sections 1–4 for PayBridge — our payment orchestration layer that routes transactions across Stripe, Adyen, and PayPal. Now I need the related documents, external dependencies list, and maintainers table. We have RFCs from each payment provider's integration, our internal PCI-DSS compliance docs, and a migration design doc from our old monolith. For external deps, besides the three payment gateways, we depend on our bank's FX rate API and a fraud detection SaaS vendor (Sift). Four teams are involved: Payments Platform, SRE, Compliance, and Fraud.

---

## Capability 5: list-related-documents

**Q1**: Besides the payment provider RFCs, any other design docs or ADRs that influenced PayBridge?

*User answers: We have an ADR for why we chose orchestration over direct integration. Also a design doc for the idempotency key strategy, since we need exactly-once payment processing.*

**Q2**: Any compliance or regulatory documents tied to this solution?

*User answers: Yes — our PCI-DSS Level 1 compliance attestation, and a PSD2/SCA readiness assessment from our compliance consultant.*

**Q3**: Are there external vendor docs you want to reference (API docs, SLA agreements)?

*User answers: Stripe API reference, Adyen integration guide, PayPal REST API docs, and Sift Science API docs. Also our bank's FX rate API spec.*

---

### Output: Related Documents

| Title | Type | Link / Path | Relevance |
|---|---|---|---|
| PayBridge Orchestration ADR | ADR | `docs/adr/012-paybridge-orchestration.md` | Decision to use orchestration pattern over direct PSP integration |
| Idempotency Key Strategy | Design | `docs/design/idempotency-keys.md` | Exactly-once payment semantics across multiple PSPs |
| PCI-DSS Level 1 Attestation | Compliance | `compliance/pci-dss-2026.pdf` | PCI compliance evidence for card data handling |
| PSD2/SCA Readiness Assessment | Compliance | `compliance/psd2-sca-2026.pdf` | Strong Customer Authentication requirements |
| Stripe API Reference | External | `https://docs.stripe.com/api` | Stripe payment intent and refund APIs |
| Adyen Integration Guide | External | `https://docs.adyen.com/api` | Adyen checkout and payout APIs |
| PayPal REST API Docs | External | `https://developer.paypal.com/docs/api` | PayPal orders and subscriptions APIs |
| Sift Science API Docs | External | `https://sift.com/developers/docs` | Fraud detection scoring API |
| Bank FX Rate API Spec | External | `internal/fx-rate-api-v2.yaml` | Real-time currency conversion rates |

---

## Capability 6: list-external-dependencies

**Q1**: For Stripe — who owns the account and what's the SLA?

*User answers: Payments Platform owns the Stripe account. Stripe SLA is 99.95%. Primary contact: payments-team@company.com. Fallback: if Stripe is down, we auto-retry with exponential backoff and queue payments for later processing.*

**Q2**: Same details for Adyen and PayPal?

*User answers: Adyen and PayPal are also under Payments Platform. Adyen SLA is 99.9%, PayPal is 99.95%. Same contacts and fallback strategy.*

**Q3**: Tell me about the bank FX rate API dependency.

*User answers: That's owned by our Treasury team (treasury@company.com). SLA is 99.5% during forex market hours, lower outside. Contact: Lisa Chen (lchen@). Fallback: cache last-known rates for up to 1 hour; if cache expired, block non-USD transactions until API recovers.*

**Q4**: And Sift for fraud detection?

*User answers: Sift is managed by our Fraud team (fraud@company.com). Sift's SLA is 99.9%. Primary contact: Mark Torres (mtorres@). Fallback: if Sift is unavailable, we use a rule-based scoring fallback (amount thresholds, velocity checks) with elevated manual review.*

---

### Output: External Dependencies

| System | Description | Owning Team | Contact | SLA | Fallback |
|---|---|---|---|---|---|
| Stripe | Primary payment processor (cards, wallets) | Payments Platform | payments-team@company.com | 99.95% | Retry with exponential backoff; queue payments |
| Adyen | Secondary payment processor (EU markets) | Payments Platform | payments-team@company.com | 99.9% | Same as Stripe fallback |
| PayPal | Tertiary payment processor (digital wallets) | Payments Platform | payments-team@company.com | 99.95% | Same as Stripe fallback |
| Bank FX Rate API | Real-time currency conversion rates | Treasury | Lisa Chen (lchen@company.com) | 99.5% (market hours) | Cache rates up to 1h; block non-USD if expired |
| Sift Science | ML-based fraud detection scoring | Fraud | Mark Torres (mtorres@company.com) | 99.9% | Rule-based fallback (amount thresholds, velocity) |

---

## Capability 7: list-maintainers

**Q1**: Which team owns the PayBridge Orchestrator (the core routing engine)?

*User answers: Payments Platform team. Primary contact: Alex Kim (akim@). Backup: Sarah Wu (swu@).*

**Q2**: And the PSP Adapters (Stripe, Adyen, PayPal connectors)?

*User answers: Payments Platform again — same contacts.*

**Q3**: What about the Fraud Integration component and the FX Rate component?

*User answers: Fraud Integration is owned by the Fraud team — primary: Mark Torres (mtorres@), backup: Nina Patel (npatel@). FX Rate component is owned by Payments Platform — same contacts.*

**Q4**: Infrastructure and deployment ownership?

*User answers: SRE owns the Kubernetes cluster, CI/CD pipelines, and monitoring. Primary: Diego Ramos (dramos@), backup: SRE on-call rotation.*

**Q5**: Any shared ownership on the idempotency store (Redis)?

*User answers: Redis is managed by SRE, but Payments Platform owns the data model and key schema.*

---

### Output: Maintainers

| Component | Owning Team | Primary Contact | Secondary Contact |
|---|---|---|---|
| PayBridge Orchestrator | Payments Platform | Alex Kim (akim@company.com) | Sarah Wu (swu@company.com) |
| Stripe Adapter | Payments Platform | Alex Kim (akim@company.com) | Sarah Wu (swu@company.com) |
| Adyen Adapter | Payments Platform | Alex Kim (akim@company.com) | Sarah Wu (swu@company.com) |
| PayPal Adapter | Payments Platform | Alex Kim (akim@company.com) | Sarah Wu (swu@company.com) |
| Fraud Integration | Fraud | Mark Torres (mtorres@company.com) | Nina Patel (npatel@company.com) |
| FX Rate Component | Payments Platform | Alex Kim (akim@company.com) | Sarah Wu (swu@company.com) |
| Idempotency Store (Redis) | SRE (infra) / Payments (schema) | Diego Ramos (dramos@company.com) | SRE on-call |
| Kubernetes + CI/CD | SRE | Diego Ramos (dramos@company.com) | SRE on-call |
