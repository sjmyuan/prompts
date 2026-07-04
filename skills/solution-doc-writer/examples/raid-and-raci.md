# Example: RAID Analysis and RACI Matrix Focus

**Scenario**: A user has completed all other sections of their solution document for "DataBridge" (an internal data pipeline migration from batch ETL to CDC streaming). They now need RAID analysis and a RACI matrix. The user is new to these frameworks and needs guidance.

**Applies**: `list-raids` and `list-raci` — demonstrates governance/ownership sections with guided questioning for a user unfamiliar with RAID/RACI.

---

## Input (User's Prompt)

> We've finished sections 1–7 for DataBridge — the CDC-based data pipeline replacing our nightly batch ETL. Now I need the RAID analysis and RACI matrix. I'm not super familiar with RAID, so please walk me through it. Our setup: Kafka Connect for CDC, Flink for stream processing, writing to Snowflake. Three teams involved: Data Platform (owns Kafka/Flink), Analytics (owns data models in Snowflake), and SRE (owns deployment and monitoring). We go live in 6 weeks.

---

## Capability 8: list-raids

**Assistant starts with Risks category...**

> Let's start with **Risks** — potential future events that could negatively impact DataBridge.
>
> **Q1**: What happens if the source database's CDC logs grow faster than Kafka Connect can consume them?

*User answers: We could lose data if the WAL gets recycled before we read it. Our mitigation is to monitor lag and scale Kafka Connect workers, but we haven't load-tested the peak volume yet.*

> **Q2**: What if Snowflake has an outage during business hours when analysts expect fresh data?

*User answers: They'd fall back to the old batch ETL, which we plan to keep running in parallel for the first 2 weeks. But after that, we decommission it.*

> **Q3**: Any risks around the Flink job state or checkpointing?

*User answers: If the Flink job fails and checkpoints are corrupted, we'd have to replay from the beginning of the Kafka topic. Our retention is 7 days, so we have some buffer.*

[...continues with Assumptions, Issues, Dependencies...]

**Q4 (Assumptions)**: Are you assuming anything about the source database's availability or schema stability?

*User answers: We're assuming no schema changes in the source tables during the 6-week rollout. The upstream team has verbally agreed but there's no formal freeze.*

**Q5 (Issues)**: Are there any unresolved disagreements or blockers right now?

*User answers: Yes — SRE wants to deploy on Kubernetes, but Data Platform wants to keep Flink on its own VMs for performance. This hasn't been resolved yet. Also, the Analytics team hasn't finalized the target Snowflake schema for the new streaming tables.*

**Q6 (Dependencies)**: Do you depend on other teams delivering something before your go-live?

*User answers: We need the SRE team to provision 3 new Kafka brokers and set up monitoring dashboards. We also depend on the source database team enabling logical replication (they said it'll be done next week).*

---

### Output: RAID Table

> Here's the compiled RAID analysis. Please review and suggest any additions or changes.

#### Risks

| ID | Description | Impact | Probability | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| R1 | Source DB WAL growth outpaces Kafka Connect consumption, causing data loss | High | Medium | Monitor lag with Datadog alerts; auto-scale Connect workers; keep batch ETL as fallback for first 2 weeks | Data Platform | Open |
| R2 | Snowflake outage during business hours after batch ETL decommissioned | High | Low | Keep batch ETL running for 2-week parallel period; document manual failover procedure | SRE | Open |
| R3 | Flink checkpoint corruption requiring full Kafka topic replay | Medium | Low | Validate checkpoints on restart; 7-day Kafka retention provides replay window; test disaster recovery scenario before go-live | Data Platform | Open |
| R4 | Source DB schema change breaks CDC parsing during rollout | Medium | Medium | Negotiate formal schema freeze with upstream team; add schema compatibility checks in CI pipeline | Data Platform | Open |

#### Assumptions

| ID | Description | Impact | Mitigation / Validation | Owner | Status |
|---|---|---|---|---|---|
| A1 | Source database tables will not undergo schema changes during 6-week rollout | High | Obtain formal schema freeze commitment from upstream team before go-live; add schema evolution handling in Kafka Connect config | Data Platform | Needs Validation |
| A2 | Peak CDC event volume will stay within tested throughput (50K events/sec) | High | Load test with 2x peak volume before go-live; document auto-scaling thresholds | Data Platform | Needs Validation |
| A3 | Analytics team can adapt to near-real-time data instead of daily batch cadence | Low | Conduct training session; provide SLA dashboard showing data freshness | Analytics | Validated |

#### Issues

| ID | Description | Impact | Resolution Plan | Owner | Status |
|---|---|---|---|---|---|
| I1 | SRE wants Kubernetes deployment for Flink; Data Platform wants dedicated VMs for performance | Medium | Schedule architecture review meeting this week; benchmark both options; escalate to CTO if unresolved by Friday | SRE / Data Platform | Blocked |
| I2 | Analytics team has not finalized target Snowflake schema for streaming tables | High | Analytics team to deliver draft schema by end of week; Data Platform to review compatibility with Flink sinks | Analytics | In Progress |

#### Dependencies

| ID | Description | Impact | Owner / Team | Expected Date | Status |
|---|---|---|---|---|---|
| D1 | SRE provisions 3 new Kafka brokers and configures monitoring dashboards | High | SRE | 2 weeks | Pending |
| D2 | Source database team enables logical replication (pgoutput plugin) | High | DB Ops Team | Next week | Committed |
| D3 | Analytics team delivers final Snowflake schema for streaming tables | High | Analytics | End of week | In Progress |

---

## Capability 9: list-raci

**Assistant identifies tasks and teams, then assigns RACI...**

> Now let's build the RACI matrix. I've identified key tasks across the DataBridge lifecycle. Let me walk through each one and assign R/A/C/I.
>
> **Q1**: For "Define CDC pipeline architecture" — who is Responsible (does the work) and who is Accountable (the single person ultimately answerable)?

*User answers: Responsible: Data Platform. Accountable: Data Platform Tech Lead (Li Wei).*

> **Q2**: Who needs to be Consulted for architecture decisions?

*User answers: SRE for infrastructure decisions, Analytics for data model impacts.*

[...continues for each task...]

---

### Output: RACI Matrix

| Task / Decision | Data Platform | Analytics | SRE | PM | DB Ops |
|---|---|---|---|---|---|
| Define CDC pipeline architecture | R/A | C | C | I | C |
| Provision Kafka + Flink infrastructure | C | I | R/A | I | — |
| Configure source DB logical replication | I | — | — | I | R/A |
| Implement Kafka Connect CDC connectors | R/A | — | C | I | C |
| Develop Flink stream processing jobs | R/A | C | — | I | — |
| Design Snowflake target schema | C | R/A | — | I | — |
| Load testing (2x peak volume) | R | C | R | I | — |
| Deployment & go-live | C | I | R/A | I | — |
| Rollback procedure documentation | R | C | R/A | I | — |
| Decommission batch ETL (post go-live) | R | C | I | A | — |

**Legend**: R = Responsible, A = Accountable, C = Consulted, I = Informed, — = Not involved

> A few notes:
> - Data Platform is heavily loaded with R/A on 6 rows — consider delegating "Decommission batch ETL" to Analytics after the transition period.
> - SRE holds A for both infrastructure provisioning and go-live deployment, which is appropriate.
> - DB Ops has a single but critical responsibility (logical replication enablement).
>
> Does this matrix look correct? Any changes needed?
