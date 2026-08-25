---
name: brainstorm-ideas
description: Facilitate structured brainstorming sessions that generate, evaluate, and refine ideas into actionable plans. Use when brainstorming, defining, exploring, generating, evaluating, refining, or iterating on an idea to reach a goal.
---

<when-to-use-this-skill>
- User wants to brainstorm a rough idea into a concrete, actionable plan
- User wants to define goals or explore challenges for an idea
- User wants to generate, evaluate, or prioritize ideas
- User wants to refine an idea into a stronger, more focused form
</when-to-use-this-skill>

<knowledge>
<brainstorming-principles>
- Great ideas come from asking the right questions, not just producing answers
- Challenging assumptions and visual organization reveal connections and gaps
- Evaluation and prioritization matter as much as generation
</brainstorming-principles>
<questioning-protocol>
- Ask **7 to 100** targeted questions, one at a time, waiting for each response
- Provide possible answers or examples with each question; follow up when an answer is vague
- Stop asking once the idea is clear and the plan is actionable
</questioning-protocol>
<facilitation-techniques>
- Use the user's preferred language; default to the language of their request
- Keep a casual, conversational tone using "we" language
- Use "what if" and "how might we" to explore possibilities
- Use examples and analogies; keep suggestions practical and feasible
</facilitation-techniques>
<adaptive-pacing>
Match session depth to idea maturity and user energy. Details: [reference/adaptive-pacing.md](reference/adaptive-pacing.md)
</adaptive-pacing>
<idea-generation>
Generate 5–7 diverse ideas using thinking techniques and present them as a mind map. Details: [reference/idea-generation.md](reference/idea-generation.md)
</idea-generation>
<idea-evaluation>
Score ideas across value, feasibility, differentiation, scope, and impact. Details: [reference/idea-evaluation.md](reference/idea-evaluation.md)
</idea-evaluation>
<challenging-techniques>
Stress-test ideas with devil's-advocate techniques. Details: [reference/challenging-ideas.md](reference/challenging-ideas.md)
</challenging-techniques>
<plan-output-format>
End the session with a structured, actionable plan. Details: [reference/plan-output-format.md](reference/plan-output-format.md)
</plan-output-format>
<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Running a session on a new, unformed idea | End-to-end walkthrough of the full session | [examples/full-session-example.md](examples/full-session-example.md) |
| Improving a rough existing idea with clear gaps | Walkthrough applying capabilities selectively | [examples/refining-existing-idea.md](examples/refining-existing-idea.md) |
| Brainstorming a process or writing improvement, not a product | Full-session walkthrough on a writing topic | [examples/concise-document-writing.md](examples/concise-document-writing.md) |
| Running a second round on a refined idea | Walkthrough of round-2 iteration and the updated plan | [examples/iterating-on-a-plan.md](examples/iterating-on-a-plan.md) |
</context-loading-guide>
</knowledge>

<capabilities>
<facilitate-session>
**Objective**: Run a structured brainstorm from idea to actionable plan.
1. Set the session mode per **reference/adaptive-pacing.md**.
2. Gather the idea or draft.
3. When a draft exists, extract the clear parts and note the gaps.
4. Apply **clarify-idea**.
5. Apply **identify-goals**.
6. Apply **explore-challenges**.
7. Apply **generate-ideas**.
8. Apply **evaluate-ideas**.
9. Apply **challenge-ideas**.
10. Apply **refine-idea**.
11. Apply **compile-actionable-plan** and present the final plan.
12. Offer **iterate-session** to deepen, combine, or pivot.
</facilitate-session>
<clarify-idea>
**Objective**: Produce a plain-language statement of the user's idea.
1. Ask the user to describe their initial idea or concept.
2. Ask who or what it is for, what it solves, and its current state.
3. Probe unstated assumptions about audience, approach, and scope.
4. Challenge vague statements by asking for concrete examples or success metrics.
5. Restate the idea in one or two sentences.
6. Request confirmation before proceeding.
</clarify-idea>
<identify-goals>
**Objective**: Define the primary objectives and success criteria.
1. Ask what the user wants to achieve with the idea.
2. Ask how they will know it succeeded.
3. Ask which objective matters most when several exist.
4. Summarize the goals.
5. Request confirmation before proceeding.
</identify-goals>
<explore-challenges>
**Objective**: Surface the obstacles the idea faces.
1. Ask what challenges or obstacles the user foresees.
2. Ask about risks, constraints, and dependencies.
3. Ask what could cause the idea to fail.
4. Present the challenge list with impact.
5. Request confirmation before proceeding.
</explore-challenges>
<generate-ideas>
**Objective**: Produce a diverse set of candidate ideas.
1. Generate **5–7 diverse ideas** per **reference/idea-generation.md**.
2. Present the ideas as a mind map per **reference/idea-generation.md**.
3. Request confirmation before proceeding.
</generate-ideas>
<evaluate-ideas>
**Objective**: Objectively score and prioritize the candidates — save the devil's advocate for the next phase.
1. Evaluate each idea across the dimensions per **reference/idea-evaluation.md**.
2. Identify risks, challenges, and trade-offs for each idea.
3. Prioritize the ideas with a simple framework (effort vs impact, MoSCoW).
4. Present the scored and prioritized ideas.
5. Request confirmation before proceeding.
</evaluate-ideas>
<challenge-ideas>
**Objective**: Attack the prioritized ideas as devil's advocate before refining.
1. Play devil's advocate on the top ideas per **reference/challenging-ideas.md**.
2. Question scope creep and push for simpler, more focused solutions.
3. Suggest MVP or phased approaches when scope is too large.
4. Present the stress-tested ideas.
5. Request confirmation before proceeding.
</challenge-ideas>
<refine-idea>
**Objective**: Consolidate the surviving ideas into a single refined idea.
1. Combine the strongest elements from the top ideas.
2. Ask what additional elements would make it more robust or appealing.
3. Ask which elements are essential versus nice-to-have.
4. Present the refined idea statement and its essential elements.
5. Request confirmation before proceeding.
</refine-idea>
<compile-actionable-plan>
**Objective**: Deliver a structured, actionable plan.
1. Summarize the refined idea per **reference/plan-output-format.md**.
2. Map each confirmed challenge to its chosen solution.
3. List the essential components.
4. Write concrete, actionable next steps — no timelines or scheduling.
5. Present the plan per **reference/plan-output-format.md**.
6. Ask the user to review and confirm the plan.
</compile-actionable-plan>
<iterate-session>
**Objective**: Run a second round — deepen, combine, or pivot.
1. Offer round 2 and let the user choose a direction.
2. Re-apply only the phases that direction needs and update the plan.
3. Cap at 1–2 rounds; repeat only if the user asks.
</iterate-session>
</capabilities>

<rules>
<rule>When the user wants to brainstorm an idea into an actionable plan, use **facilitate-session**.</rule>
<rule>When the user provides a rough idea, use **facilitate-session** and apply capabilities only for the gaps.</rule>
<rule>When the user requests one phase in isolation, apply that capability directly.</rule>
<rule>When a plan exists and the user wants to go further, apply **iterate-session**.</rule>
</rules>
