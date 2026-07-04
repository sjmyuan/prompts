---
name: adr-editor
description: Guide users through drafting well-structured ADRs. Use when creating, writing, drafting, or authoring an ADR, documenting decisions, evaluating options, or compiling a record from raw notes.
---

<when-to-use-this-skill>
- User wants to create, write, draft, or author an Architecture Decision Record (ADR)
- User needs to document an architectural or technical decision
- User wants to evaluate and compare architecture options for a decision
- User needs help structuring unstructured thoughts or notes into an ADR format
- User wants to compile a polished ADR document from raw discussion points
</when-to-use-this-skill>

<knowledge>

<about-adr>
An Architecture Decision Record (ADR) captures a significant architectural decision along with its context, options considered, and consequences. It serves as a historical record for the team and future contributors, making the rationale behind decisions transparent and traceable.
</about-adr>

<decision-driver-categories>
When prompting the user for decision drivers, suggest these common categories:
- **Performance**: latency, throughput, resource usage
- **Cost**: licensing, infrastructure, operational, migration
- **Timeline**: delivery deadlines, team availability
- **Team expertise**: existing skills, learning curve, hiring needs
- **Maintainability**: code complexity, debugging, onboarding
- **Security**: compliance, data protection, attack surface
- **Scalability**: horizontal/vertical scaling, future growth
- **Compatibility**: existing systems, ecosystem fit, vendor lock-in

Help the user distinguish between **hard constraints** (must-haves / knock-out criteria) and **soft preferences** (nice-to-haves).
</decision-driver-categories>

<option-brainstorming-prompts>
When the user has only one option, prompt them to consider alternatives from these categories:
- **Do nothing / status quo**: What happens if we don't change anything?
- **Industry-standard approaches**: What do similar teams or companies do?
- **Open-source alternatives**: Are there OSS tools that address this?
- **Build vs. buy**: Should we build it ourselves or purchase a solution?
- **Incremental vs. big-bang**: Can we phase the change, or does it need to be all at once?
</option-brainstorming-prompts>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Compiling the final ADR document (compile-adr capability step 3) | Complete ADR markdown template with all sections and placeholder annotations | [reference/adr-template.md](reference/adr-template.md) |
| User provides a complete, well-formed problem statement and wants to see a full end-to-end walkthrough | Full walkthrough of all 5 capabilities for a database selection decision | [examples/database-selection.md](examples/database-selection.md) |
| User has partial notes or rough ideas and needs help structuring them into an ADR | Full walkthrough of all 5 capabilities starting from unstructured input | [examples/from-rough-notes.md](examples/from-rough-notes.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<define-problem>
1. Ask the user to describe the architectural decision they need to make in 2–3 sentences.
2. If the description is vague, ask follow-up questions to clarify scope, stakeholders, and the system(s) involved.
3. Identify and resolve any ambiguous terms or implicit assumptions.
4. Restate the problem back to the user as a concise, structured summary and ask: "Does this accurately capture the problem?"
5. Iterate until the user confirms.
</define-problem>

<define-decision-drivers>
1. Ask the user: "What are the key factors, constraints, or priorities that will influence this decision?"
2. If the user struggles, suggest categories from **decision-driver-categories** to prompt thinking.
3. Help the user distinguish between hard constraints (must-haves / knock-out criteria) and soft preferences (nice-to-haves).
4. Summarize the drivers in a bullet list and ask the user to confirm or reorder by priority.
</define-decision-drivers>

<define-considered-options>
1. Ask the user: "What options have you already considered for addressing this problem?"
2. If the user has only one option, brainstorm alternatives together using the prompts in **option-brainstorming-prompts**.
3. For each option, ensure it is concrete and distinct from the others (avoid near-duplicates).
4. Present the final list of options and ask the user to confirm before evaluating any.
</define-considered-options>

<evaluate-options>
1. For each option, ask the user:
   - "What are the main advantages or strengths of this option?"
   - "What are the main disadvantages, risks, or trade-offs?"
2. Relate each pro/con back to the decision drivers defined earlier — highlight which drivers are satisfied and which are compromised.
3. Summarize the evaluation of the current option with a Pros/Cons list and ask for confirmation.
4. After all options are evaluated, guide the user toward a recommendation by asking: "Given the evaluations, which option best satisfies the decision drivers?"
</evaluate-options>

<compile-adr>
1. Gather all confirmed outputs from the preceding capabilities: problem statement, decision drivers, considered options, and evaluations.
2. Prompt the user for metadata: preferred title, owners, and status (draft | adopt | declined | superseded).
3. Load **reference/adr-template.md** and populate the template with all collected information, using the user's recommended option as "Chosen option" with a synthesized justification.
4. Fill in the Consequences section based on the evaluated pros/cons and risks discussed.
5. Verify the completed ADR against this quality checklist:
   - [ ] Problem statement is clear, scoped, and unambiguous
   - [ ] Decision drivers include both hard constraints and soft preferences
   - [ ] At least 2 distinct options were evaluated
   - [ ] Each option has pros/cons explicitly tied to decision drivers
   - [ ] Chosen option justification references specific drivers
   - [ ] Consequences section addresses risks and positive impacts
   - [ ] Metadata (title, owners, status) is populated
6. Present the completed ADR to the user for final review and ask: "Would you like to adjust any section before saving?"
</compile-adr>

</capabilities>

<rules>

<rule>When the user initiates an ADR session, apply **define-problem** to establish a clear problem statement.</rule>
<rule>After the problem is confirmed, apply **define-decision-drivers** to identify the factors that will guide the decision.</rule>
<rule>After decision drivers are confirmed, apply **define-considered-options** to enumerate all viable options.</rule>
<rule>After options are confirmed, apply **evaluate-options** to assess each option's pros and cons against the decision drivers.</rule>
<rule>After all options are evaluated and a recommendation is chosen, apply **compile-adr** to produce the final ADR document using the template.</rule>

<rule>If the user submits a new option mid-evaluation, apply **evaluate-options** to assess it and integrate it into the comparison.</rule>
<rule>If the user revises the problem or decision drivers at any point, re-apply the affected downstream capabilities to keep the ADR consistent.</rule>
<rule>After each user confirmation, update any in-progress ADR draft so nothing is lost.</rule>

</rules>
