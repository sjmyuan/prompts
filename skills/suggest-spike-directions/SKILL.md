---
name: suggest-spike-directions
description: Suggest next-step investigation directions for a spike after a round completes. Use when suggesting, proposing, or generating next steps, go-deeper/go-broader candidates, or a direction menu for a spike.
---

<when-to-use-this-skill>
- User asks what to investigate next after a spike round completes — "where should we take this spike next?"
- User wants 3 go-deeper / 3 go-broader candidate questions grounded in the round's investigation evidence
- User wants a direction menu to pick the next spike round's scope
- User is unsure what to focus on next after a spike investigation round
- Do NOT load during an active spike round before investigation results exist — `conduct-spike` runs the investigation; this skill only fires after a round's findings are available
</when-to-use-this-skill>

<knowledge>

<spike-direction-input>
This skill is run manually, on request, after a spike round completes. Its input is the round's investigation evidence — the investigation summary, findings doc, or solution doc produced by `conduct-spike` (whichever exists). Read the relevant artifact before generating candidates; never generate suggestions from guesswork.
</spike-direction-input>

<direction-rule>
Always generate exactly 3 go-deeper and 3 go-broader candidates. Every candidate must be grounded in a specific finding from the round — never unanchored. Each candidate is a concrete, answerable question with a 1-sentence rationale.
</direction-rule>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Generating go-deeper / go-broader candidates and the direction menu | Candidate-generation heuristics, go-deeper vs go-broader patterns, quality criteria, anti-patterns, and the direction-menu template | [reference/spike-direction-suggestions-guide.md](reference/spike-direction-suggestions-guide.md) |
| Seeing a worked example — 3 go-deeper + 3 go-broader candidates grounded in investigation evidence | Walkthrough of generating direction candidates after a spike round, with rationale for each | [examples/spike-direction-suggestions.md](examples/spike-direction-suggestions.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<suggest-spike-directions>
1. Load the round's investigation evidence (investigation summary, findings doc, or solution doc) and extract key discoveries: systems identified, constraints measured, surprises found, open questions, boundary touches.
2. Generate 3 go-deeper candidates: concrete, answerable questions narrowing the spike into a specific unresolved detail. Each must reference a specific finding ("We found X, but didn't explore Y"), be investigable (codebase or prototype can answer it), and include a 1-sentence rationale.
3. Generate 3 go-broader candidates: concrete questions expanding the spike to an adjacent concern the user may have missed. Each must reference something the scope excluded or touched, be a genuine decision, and include a 1-sentence rationale.
4. Present as a direction menu using the template in **reference/spike-direction-suggestions-guide.md** (Go Deeper + Go Broader tables: candidate question, evidence anchor, rationale).
5. Ask: "Would you like to pursue any of these directions? Pick one (or more) and I'll start a new spike round. Or if you're satisfied with the current results, we can stop here." A selected direction becomes a new spike scope — hand back to `conduct-spike`'s **define-spike-scope** with it as the goal.
</suggest-spike-directions>

</capabilities>

<rules>
<rule>When the user asks what to investigate next after a spike round completes, apply **suggest-spike-directions** to propose go-deeper / go-broader candidates.</rule>
<rule>When the user wants next-step candidate questions or a direction menu grounded in the round's investigation evidence, apply **suggest-spike-directions**.</rule>
<rule>When the user is unsure what to focus on next after a spike investigation round, apply **suggest-spike-directions** to surface candidate directions from the evidence.</rule>
<rule>When the user explicitly says the investigation is done or already has a clear next step, do NOT apply **suggest-spike-directions** — respect their direction (see the "When to Skip" section of **reference/spike-direction-suggestions-guide.md**).</rule>
<rule>Do NOT apply during an active spike round before investigation results exist — `conduct-spike` runs the investigation first; this skill only fires after a round's findings are available.</rule>
</rules>
