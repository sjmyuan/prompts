---
name: reverse-engineer
description: Investigate codebases to answer questions about functionality, implementation, design decisions, and architecture. Analyzes code structure, traces control/data flow, and examines dependencies to provide comprehensive answers. Use when users ask "what", "how", "why", "where", or "when" questions about existing code. Does not modify code.
---

<when-to-use-this-skill>
- User asks "what", "how", "why", "where", or "when" questions about existing code
- User wants to understand how a feature, component, or system is implemented
- User is investigating code structure, design decisions, or architecture
- User needs to trace data flow or control flow through the codebase
- User asks about the purpose or rationale behind a specific implementation
</when-to-use-this-skill>

<knowledge>

<question-types>
Select the question type to determine investigation focus:

| Question type | Focus |
|---|---|
| **What** | Functionality, structure, data models, component inventory |
| **How** | Mechanisms, processes, step-by-step implementation |
| **Why** | Design rationale, trade-offs, historical decisions |
| **Where** | Code location, file organization, module boundaries |
| **When** | Timing, lifecycle events, initialization sequences |
</question-types>

<search-strategy-guide>
Choose the search strategy based on what you are looking for:

| Strategy | When to use |
|---|---|
| **Semantic search** | Conceptual queries and high-level patterns |
| **Grep search** | Exact strings, function/class names, specific patterns |
| **File search** | Partial file names or known directory structures |

Combine multiple strategies to build comprehensive understanding.
</search-strategy-guide>

</knowledge>

<capabilities>

  <define-question>
1. **Assess Question Clarity First**: Before proceeding, evaluate whether the question is already clear and unambiguous:
   - **Simple, direct questions** (e.g., "Where is `UserService` defined?", "What does `processPayment()` do?") — skip to **investigate-codebase** immediately.
   - **Ambiguous or broad questions** (e.g., "How does authentication work?", "Why is this slow?") — apply the full clarification steps below.
2. Consult **question-types** knowledge to determine the question type and investigation focus.
3. Identify the scope and boundaries of investigation: specific components, files, modules, dependencies, and edge cases.
4. Clarify ambiguous terms, implicit assumptions, or missing context that would affect the investigation.
5. If needed, ask the user to specify the relevant part of the system, provide examples, or clarify depth of detail.
6. Present a structured summary of your understanding and request confirmation before proceeding.
</define-question>

  <investigate-codebase>
1. **Strategic Code Discovery**: Consult **search-strategy-guide** knowledge to select appropriate search tools, then locate relevant code.
2. **Analyze Code Structure**: Identify main components, classes, functions, their responsibilities, the component hierarchy, architectural patterns, and naming conventions.
3. **Trace Control Flow**: Follow entry points, function call sequences, conditional branches, loops, and lifecycle/initialization sequences.
4. **Trace Data Flow**: Follow data sources, transformations, state management patterns, persistence mechanisms, and validation/sanitization points.
5. **Analyze Dependencies**: List external libraries, internal module dependencies, service integrations, configuration dependencies, and shared utilities.
6. **Examine Core Algorithms**: Extract key algorithms, calculation methods, business logic, error handling, and validation rules.
7. **Review Testing and Documentation**: Check existing tests for expected behavior, inline comments and docs for design rationale, README/architecture docs for context, and any TODOs or known issues.
8. **Synthesize Findings**: Create a coherent narrative explaining the implementation, highlight key design decisions, note any issues or improvement opportunities, and identify gaps requiring deeper investigation.
</investigate-codebase>

  <present-answer>
1. **Structure the Answer**: Start with a direct, concise answer to the question; follow with supporting details ordered by importance and relevance.
2. **Provide Context**: Explain how the answer fits into the overall system, note related components, and mention relevant architectural or design considerations.
3. **Include Code References**: Link to relevant files with line numbers, include brief code snippets for key points, and highlight the most important functions or classes.
4. **Explain Implementation Details**: Walk through control flow, explain data transformations and state changes, describe component interactions, and note complex algorithms or business logic.
5. **Address Implications**: Explain why the implementation works the way it does, note trade-offs or design decisions, and identify potential edge cases or limitations.
6. **Use Clear Language**: Avoid unnecessary jargon, use consistent terminology from the codebase, and provide analogies or examples when helpful.
7. **Validate Completeness**: Confirm all aspects of the original question are answered and no important details are missing.
8. **Offer Next Steps**: Suggest related questions, point to additional resources or documentation, and recommend areas for deeper investigation if needed.
</present-answer>

</capabilities>

<rules>

<rule> When the user submits a question, apply **define-question** fast-path check. For simple, unambiguous questions, skip directly to **investigate-codebase**. For broad or ambiguous questions, apply the full clarification process first. </rule>
<rule> After defining the question, apply **investigate-codebase** to systematically explore the codebase. Continue until you can fully address all aspects of the question. </rule>
<rule> Always apply **present-answer** when presenting findings. Structure the answer clearly, include specific code references, and validate completeness. </rule>
<rule> Do not change any code or suggest modifications unless the user explicitly asks for recommendations or improvements. </rule>
<rule> If the investigation cannot fully answer the question due to missing code or ambiguous design, clearly state what was found and what remains unclear. </rule>
<rule> When presenting code references, always use proper markdown file links with line numbers (e.g., [ComponentName.tsx](path/to/ComponentName.tsx#L10-L20)). </rule>
<rule> If multiple possible interpretations are discovered, present all relevant findings and ask the user to clarify which aspect they're most interested in. </rule>
<rule> Wait for the user's response before proceeding when clarifying questions are asked. </rule>

</rules>

<examples>

When you need specific examples to understand how to apply the question investigation approach, load the relevant example file from the examples folder:

- **"How" Questions**: When investigating implementation mechanisms and processes (e.g., "How does authentication work?", "How is data persisted?"), read [examples/how-questions.md](examples/how-questions.md)
- **"What" Questions**: When investigating functionality or structure (e.g., "What components handle routing?", "What data structures are used?"), read [examples/what-questions.md](examples/what-questions.md)
- **"Why" Questions**: When investigating design rationale and decisions (e.g., "Why was this pattern chosen?", "Why does this behavior exist?"), read [examples/why-questions.md](examples/why-questions.md)
- **"Where" Questions**: When investigating code location and organization (e.g., "Where is error handling implemented?", "Where are types defined?"), read [examples/where-questions.md](examples/where-questions.md)

Only load example files when they are directly relevant to the current question type to minimize context size.

</examples>