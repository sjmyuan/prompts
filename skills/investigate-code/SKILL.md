---
name: investigate-code
description: Investigate codebases to answer questions about functionality, architecture, and cross-system dependencies. Use when investigating, understanding, tracing, analyzing, visualizing, discovering patterns in, or documenting how code works.
---

<when-to-use-this-skill>
- User asks questions about existing code (how it works, why it's designed that way, where things live)
- User wants to understand a feature, component, or system implementation
- User needs to trace control flow, data flow, or dependencies through the codebase
- User wants to investigate code across multiple repositories and their interactions
- User wants to visualize architecture with C4 diagrams, sequence diagrams, or call stack traces
- User wants to discover implementation patterns or detect inconsistencies across the codebase
- User is conducting a spike investigation (via the `conduct-spike` skill) and needs current-state investigation of an area
</when-to-use-this-skill>

<knowledge>

<search-strategies>
| Strategy | Use for |
|---|---|
| **Semantic search** | Conceptual queries, high-level patterns |
| **Grep search** | Exact strings, function/class names, identifiers |
| **File search** | Partial file names, known directory structures |
</search-strategies>
<multi-repo-discovery>
Discover cross-repo dependencies:

| Strategy | What to look for |
|---|---|
| **Configuration analysis** | Service discovery configs, docker-compose, Kubernetes manifests |
| **HTTP client search** | `RestTemplate`, `WebClient`, `FeignClient`, `axios`, `fetch` with hostnames |
| **Event topology** | `@KafkaListener`, `@RabbitListener`, `publish()`, `topic()` |
| **Dependency manifests** | `pom.xml`, `build.gradle`, `package.json`, `go.mod` for internal packages |
| **API contracts** | OpenAPI/Swagger specs, Protobuf files, GraphQL schemas |
</multi-repo-discovery>
<diagram-conventions>
Choose the most appropriate diagram type for what you're explaining: C4 for architecture, sequence for interactions, flowchart for decision logic, state diagram for lifecycles, class/ER for data models. Draw all diagrams with Mermaid — use native `C4Container`/`C4Component` for C4. See [reference/diagram-quick-reference.md](reference/diagram-quick-reference.md) for syntax quick-reference, [reference/c4-model-conventions.md](reference/c4-model-conventions.md) for C4 element types and layout, and [reference/sequence-diagram-conventions.md](reference/sequence-diagram-conventions.md) for sequence diagram patterns.
</diagram-conventions>
<progressive-disclosure-levels>
Guide investigations from high-level to detail: C2 Container ("What systems exist?") → C3 Component ("What's inside?") → Sequence/Flowchart ("What's the message order or decision logic?") → Call Stack ("What happens in this method?"). Supplement with state diagrams (lifecycles), class diagrams (data models), or other types whenever they clarify the explanation better than the default level. Start at the level matching user familiarity — Level 1 for unfamiliar systems, Level 3-4 for specific flows.
</progressive-disclosure-levels>
<pattern-discovery-heuristics>
Search for similar implementations (priority order):

1. **Package naming** — Sibling packages often follow the same pattern
2. **Suffix matching** — `*Controller`, `*Orchestrator`, `*Adapter`, `*Repository`
3. **Interface implementations** — All classes implementing the same interface
4. **Annotation presence** — Classes sharing the same annotations
5. **Dependency mirroring** — Services calling the same adapters or siblings

See [reference/pattern-discovery-strategies.md](reference/pattern-discovery-strategies.md) for the structural fingerprint format and inconsistency severity levels.
</pattern-discovery-heuristics>
<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Conducting a typical investigation (any question type) | End-to-end example with clarification, discovery, tracing, and synthesis | [examples/investigation-workflow.md](examples/investigation-workflow.md) |
| Needing a Mermaid syntax quick-reference for any diagram type | C2/C3/Sequence syntax cheat-sheet | [reference/diagram-quick-reference.md](reference/diagram-quick-reference.md) |
| Drawing C2 or C3 diagrams | Full element types, boundaries, `C4Container`/`C4Component` patterns | [reference/c4-model-conventions.md](reference/c4-model-conventions.md) |
| Drawing sequence diagrams | Message numbering, Mermaid syntax, cross-reference conventions | [reference/sequence-diagram-conventions.md](reference/sequence-diagram-conventions.md) |
| Tracing method-level call stacks | Frame format, cross-repo annotation, correlation with sequence diagrams | [reference/call-stack-trace-conventions.md](reference/call-stack-trace-conventions.md) |
| Discovering patterns or detecting inconsistencies | Structural fingerprint format, comparison matrix, severity levels | [reference/pattern-discovery-strategies.md](reference/pattern-discovery-strategies.md) |
| Investigating across multiple repos | Dependency matrix, C2 diagram, cross-repo call traces | [examples/multi-repo-dependency.md](examples/multi-repo-dependency.md) |
| Running a progressive zoom-in (C2→C3→sequence→call stack) | End-to-end example with all four levels | [examples/progressive-zoom-in.md](examples/progressive-zoom-in.md) |
| Compiling findings into a markdown report | Full report structure with all sections | [examples/markdown-report.md](examples/markdown-report.md) |
| Finding similar features or flagging inconsistent patterns | End-to-end pattern discovery with inconsistency detection | [examples/pattern-discovery.md](examples/pattern-discovery.md) |
</context-loading-guide>

</knowledge>

<capabilities>

<investigate-codebase>
1. **Clarify the question**: If ambiguous or broad (e.g., "How does auth work?"), ask the user to specify system, scope, or depth. For simple direct questions (e.g., "Where is `UserService` defined?"), skip to step 2.
2. **Discover relevant code**: Use semantic search, grep, and file search (see search-strategies) to locate entry points, key classes, and configuration.
3. **Trace control and data flow**: Follow entry points through the call chain — identify each component's role, how data transforms at each step, and how errors are handled.
4. **Analyze dependencies**: List external libraries, internal module dependencies, service integrations, and configuration dependencies.
5. **Extract structural fingerprint**: Note the feature's layer chain (e.g., Controller → Orchestrator → Service → Adapter), stereotypes, and external interactions. This feeds into discover-implementation-patterns.
6. **Synthesize findings**: Present a coherent narrative — direct answer first, then supporting evidence with file:line references, key design decisions, and areas needing deeper investigation.
7. **Validate**: Verify that all file:line references are accurate by checking the workspace, and that the narrative answers the original question directly.
</investigate-codebase>

<analyze-cross-repo-dependencies>
1. **Identify repositories**: Determine which repos are involved from user input, workspace structure, or directory layout.
2. **Discover interfaces per repo**: For each repo, find REST endpoints, event publishers/consumers, gRPC services, and shared library dependencies.
3. **Build dependency matrix**: For each repo pair, determine direction (who calls whom), protocol (HTTP/Kafka/gRPC/DB), endpoints/topics, and error handling patterns.
4. **Present the matrix**: Use a table with Source, Target, Protocol, Direction, Details columns. Highlight synchronous dependencies (potential failure cascades) vs. asynchronous (resilient).
5. **Offer visualization**: Ask if the user wants a C2 container diagram via draw-c4-diagram.
6. **Validate**: Verify that every dependency direction in the matrix matches the actual code — confirm the HTTP client, event publisher, or DB connection exists in the source repo.
</analyze-cross-repo-dependencies>

<draw-c4-diagram>
1. **Determine level**: C2 (Container) for system landscape across repos; C3 (Component) to zoom into one container's internals.
2. **Load conventions**: Load [reference/c4-model-conventions.md](reference/c4-model-conventions.md).
3. **Define content**: List all elements (containers/components, databases, external systems, actors) and connections with protocol labels.
4. **Create Mermaid**: Use `C4Container` for C2 and `C4Component` for C3. For C3, wrap components in a `Container_Boundary()`; for C2, group containers with `System_Boundary()`. Label connections with protocols (e.g., `Rel(a, b, "POST /payments", "HTTPS")`).
5. **Render and explain**: Present the Mermaid source, then describe each element's role and key connections.
6. **Offer next level**: For C2, ask which container to zoom into (C3). For C3, ask which interaction to sequence-diagram.
7. **Validate**: Verify that every container and connection in the diagram appears in the dependency matrix, and that connection labels include protocol and endpoint.
</draw-c4-diagram>

<draw-sequence-diagram>
1. **Select the operation**: Based on user choice or the key interaction from the C2/C3 diagram.
2. **Load conventions**: Load [reference/sequence-diagram-conventions.md](reference/sequence-diagram-conventions.md).
3. **Trace the message flow**: Identify all participants, message order with method signatures, sync vs. async calls, and return values.
4. **Create Mermaid**: Use `sequenceDiagram` syntax. Number messages sequentially for call-stack cross-referencing. Use `->>` for sync, `-->>` for async and returns. Add `alt/loop/par` blocks for branching.
5. **Render and explain**: Walk through numbered messages highlighting key interactions.
6. **Offer method detail**: Ask which message to trace at the call-stack level via trace-call-stack.
7. **Validate**: Verify that message numbers are sequential, return arrows exist for every call, and all participants match containers from the C2/C3 diagram.
</draw-sequence-diagram>

<trace-call-stack>
1. **Select the target method**: Based on user choice or the most critical method from the sequence diagram.
2. **Load conventions**: Load [reference/call-stack-trace-conventions.md](reference/call-stack-trace-conventions.md).
3. **Trace the call chain**: Starting from the target method, follow depth-first. Record for each method: file path + line, full signature, parameter values, return value, 2-5 lines of relevant code, and side effects.
4. **Format the trace**: Use depth-indexed `[N]` numbering, tree branches (`├─→`, `╰─→`) for hierarchy, `[repo: name]` for cross-repo calls. Match frame numbers to the sequence diagram message numbers.
5. **Present insights**: Highlight key logic, error handling, and design decisions found in the trace.
6. **Validate**: Verify that every frame `[N]` has a matching message number in the corresponding sequence diagram, and that all file paths are verifiable in the workspace.
</trace-call-stack>

<discover-implementation-patterns>
1. **Extract structural fingerprint**: From the already-investigated feature, capture: entry point type, layer chain, stereotypes, external interactions, error handling, and configuration.
2. **Search for similar features**: Apply pattern-discovery-heuristics — start with naming conventions, then annotation/interface patterns, then structural similarity.
3. **Compare each candidate**: Classify as match (same structure), variant (same layers, different tech/approach), or mismatch (different structure).
4. **Synthesize findings**: If all match → present unified pattern with the current feature as canonical example. If variants exist → flag inconsistency explicitly: "⚠️ Inconsistency: N different patterns found." List each variant with structural differences and affected files.
5. **Recommend**: If inconsistency found, suggest standardization. If unique pattern, state so.
6. **Validate**: Verify that each comparison candidate's structural fingerprint is complete (all 6 dimensions: entry point, layer chain, stereotypes, external interactions, error handling, configuration), and that inconsistency classifications (match/variant/mismatch) are justified by the evidence.
</discover-implementation-patterns>

<compile-markdown-report>
1. **Determine scope**: Ask if user wants all levels or a subset.
2. **Load example**: Load [examples/markdown-report.md](examples/markdown-report.md) for structure reference.
3. **Assemble sections**: System overview (C2 + dependency matrix) → Component internals (C3 per container) → Interaction flows (sequence diagrams) → Method details (call stacks) → Key decisions → Edge cases → Next steps.
4. **Embed diagrams**: Mermaid source blocks with brief text descriptions.
5. **Validate**: Ensure all file paths and line numbers are accurate, and every investigation level is represented.
</compile-markdown-report>

</capabilities>

<rules>
<rule> When the user asks a question about existing code, apply investigate-codebase. First clarify if the question is ambiguous; skip directly to investigation for simple, direct questions. </rule>
<rule> When the question spans multiple repositories or the user asks about cross-system dependencies, apply analyze-cross-repo-dependencies before any diagramming. </rule>
<rule> When the user wants to see system architecture, container internals, or how systems/components connect, apply draw-c4-diagram at the appropriate level (C2 for landscape, C3 for internals). </rule>
<rule> When the user wants to see exact message ordering or interaction flow for an operation, apply draw-sequence-diagram. </rule>
<rule> When the user wants method-level implementation details or code walkthrough, apply trace-call-stack. Correlate frame numbers with any existing sequence diagram. </rule>
<rule> When the user wants a guided tour from high-level down to method detail, apply levels in sequence: draw-c4-diagram (C2) → draw-c4-diagram (C3) → draw-sequence-diagram → trace-call-stack. Start at the level matching user familiarity — do not always start at C2. </rule>
<rule> When the user asks how a type of feature works generally, or wants to know if similar features follow a consistent pattern, apply investigate-codebase on one example, then apply discover-implementation-patterns to find and compare all similar implementations. </rule>
<rule> When the user asks for a document, report, or all findings compiled, apply compile-markdown-report after completing the relevant investigation capabilities. </rule>
</rules>

