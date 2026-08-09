# Questioning Dimensions Rubric

Use with **question-the-result** to probe each claim across all six dimensions. Apply every dimension that fits — a claim may fail on several at once.

| Dimension | What it probes | Sample questions |
|---|---|---|
| **Completeness** | Coverage of the full question — missing paths, cases, edge cases, fallbacks, side effects | Which parts of the original request are unaddressed? Which branches, paths, or edge cases are missing? What fallback or error paths were not considered? Which downstream consumers were not checked? |
| **Correctness** | Factual accuracy against primary sources | Does the claim match code/docs/data/logs? Are cited file:line references accurate? Is the conclusion supported by the cited evidence, or could it be misinterpreted? |
| **Ambiguity** | Precision and unambiguity of wording | Which terms are vague or overloaded? Do nouns ("it", "the service", "the system") refer to one thing? Are numbers, units, timeframes, and scope explicit? Would two readers reach different conclusions? |
| **Consistency** | Self-agreement and agreement with known facts | Does the result contradict itself? Does it agree with other results from the same or other agents? Are all statements mutually consistent? |
| **Evidence** | Grounding of every claim | Which claims lack a source? Which sources are secondary (re-stated) rather than primary? Is anything asserted without a verifiable basis? |
| **Assumptions** | Silent premises the result depends on | Which assumptions, if false, would invalidate the result? Are they stated or silently baked in? Are they verifiable? |

## Prioritization

Order challenges by impact, not by count:

- **Impact** — what breaks if the claim is wrong (data loss, security, wrong decision, downstream rework)
- **Likelihood** — how plausible it is that the claim is wrong (unverified, secondary source, hand-waved, dead code)
- **Scope** — how much of the result depends on the challenged claim

High-impact + plausible = verify first. Low-impact + implausible = note, don't block.
