---
name: design-algorithm
description: Guide users through algorithm design for complex problems via clarification, case exploration, multi-path brainstorming, and final design. Use when designing, clarifying, exploring cases for, brainstorming, or explaining an algorithm.
---

<when-to-use-this-skill>
- User asks to design an algorithm for a specific problem
- User presents a vague problem needing clarification before design
- User wants the cases an algorithm must handle explored and confirmed
- User wants alternative algorithm approaches brainstormed and compared
- User needs complex algorithm logic (recursion, DP transitions, nested loops) explained
- Do NOT use for implementing, debugging, or optimizing algorithm code
</when-to-use-this-skill>

<knowledge>

<algorithm-design-paradigms>
Paradigms structure the solution space. Choose paradigms from the problem's constraints and data structures.

| Paradigm | Strategy | Example |
|---|---|---|
| Brute Force | Try all possibilities | Exhaustive search |
| Divide and Conquer | Split, solve recursively, combine | Merge Sort, Quick Sort |
| Dynamic Programming | Store overlapping subproblem results | Knapsack, LCS, shortest path |
| Greedy | Locally optimal steps toward a global optimum | Huffman coding, Dijkstra |
| Backtracking | Explore candidates, abandon dead ends | N-Queens, Sudoku |
| Two Pointers / Sliding Window | Keep a subset via moving pointers | Contiguous subarray problems |
| Graph Algorithms | BFS, DFS, topological sort, shortest path, MST | Dijkstra, Kruskal, Prim |
| Recursion | Reduce to smaller instances of the same problem | Tree traversal |
| Binary Search | Halve the search range in sorted space | Search in a sorted array |
</algorithm-design-paradigms>

<complexity-analysis>
Complexity measures scale. Analyze time and space with Big-O before committing to a design.

| Concept | Meaning |
|---|---|
| Time complexity | Growth rate: O(1), O(log n), O(n), O(n log n), O(n²), O(2^n), O(n!) |
| Space complexity | Additional memory beyond the input |
| Trade-offs | Time vs space; simplicity vs efficiency; worst-case vs average-case |
</complexity-analysis>

<common-data-structures>
Data structures shape feasible algorithms. Match the structure to the operations the algorithm needs.

| Structure | Typical use |
|---|---|
| Array, Linked List, Stack, Queue | Linear storage and traversal |
| Hash Table, Set | Fast lookup and deduplication |
| Tree: Binary, BST, Trie, Segment, Fenwick | Hierarchies and range queries |
| Heap (Min, Max) | Priority extraction |
| Graph: Adjacency Matrix, Adjacency List | Relationship modeling |
| Union-Find | Connectivity and component merging |
</common-data-structures>

<problem-clarification-template>
A clarified problem defines six items. Cover all six before designing.

1. Problem statement — the core problem to solve
2. Input format — types, ranges, and constraints
3. Output format — what the algorithm returns
4. Constraints — size, time, memory limits, special conditions
5. Edge cases — empty, single element, duplicates, negatives, overflow
6. Examples — input-output pairs showing expected behavior
</problem-clarification-template>

<algorithm-output-template>
A final algorithm design covers six items. Present all six in order.

1. Algorithm name and paradigm
2. Core idea — 2–3 sentence explanation of the approach
3. Pseudocode — step-by-step in a fenced code block
4. Visual diagram — Mermaid flowchart, sequence, or state diagram
5. Complexity analysis — time and space with justification
6. Implementation notes — pitfalls, handled edge cases, optimizations
</algorithm-output-template>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Clarifying a vague problem | clarify-problem walkthrough | [examples/clarify-problem.md](examples/clarify-problem.md) |
| Enumerating required cases | explore-cases walkthrough | [examples/explore-cases.md](examples/explore-cases.md) |
| Comparing algorithm approaches | brainstorm-algorithms walkthrough | [examples/brainstorm-algorithms.md](examples/brainstorm-algorithms.md) |
| Explaining complex logic | explain-complex-paths walkthrough | [examples/explain-complex-paths.md](examples/explain-complex-paths.md) |
| Producing the final design | design-algorithm walkthrough | [examples/design-algorithm.md](examples/design-algorithm.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<clarify-problem>
**Objective**: Produce a confirmed, complete problem definition.
1. Ask the user to restate the problem in their own words.
2. Apply the **problem-clarification-template** to probe inputs, outputs, constraints, and edge cases.
3. Ask 3–10 targeted questions one at a time; wait for each answer before the next.
4. Summarize each answer and confirm understanding before proceeding.
5. Present the full definition and ask the user to confirm it.
6. Verify the definition covers all six template items.
</clarify-problem>

<explore-cases>
**Objective**: Produce a confirmed list of every case the algorithm must handle.
1. Derive input categories from the clarified definition: normal, edge, error, and boundary.
2. State the expected behavior for each category.
3. Present the case list and ask the user to spot missing cases.
4. Record the confirmed cases for design and testing.
5. Verify the list covers all categories and the user's additions.
</explore-cases>

<brainstorm-algorithms>
**Objective**: Produce 2–4 comparable approaches from different paradigms.
1. Acknowledge the user's proposed approach and note its strengths.
2. Derive 2–4 alternatives from different paradigms based on constraints and data structures.
3. For each alternative, state the core idea, pros, and cons.
4. Ask the user to evaluate each option and choose a direction.
5. Encourage refining or combining approaches through discussion.
6. Verify the user selects or explicitly rejects each option.
</brainstorm-algorithms>

<explain-complex-paths>
**Objective**: Make complex algorithm logic understandable to the user.
1. Identify the complex pattern: nested loops, recursion, DP transitions, or multi-pointer moves.
2. Select a technique: step-by-step trace, Mermaid diagram, analogy, or layer decomposition.
3. Walk through the pattern with a small concrete example.
4. Ask whether the user has questions or wants another pass.
5. If still unclear, retry with a different technique or a simpler example.
6. Verify the user can restate the pattern in their own words.
</explain-complex-paths>

<design-algorithm>
**Objective**: Produce the final algorithm design per the output template.
1. Confirm the chosen approach with the user.
2. Fill the **algorithm-output-template**: name and paradigm, core idea, pseudocode, Mermaid diagram, complexity analysis, implementation notes.
3. Present the design and ask for adjustment requests.
4. Verify the design covers all six template items.
</design-algorithm>

</capabilities>

<rules>
<rule>When the problem lacks a clear definition, use **clarify-problem**.</rule>
<rule>After the problem is clarified, use **explore-cases** to enumerate and confirm all required cases.</rule>
<rule>When the user proposes an approach or cases are confirmed, use **brainstorm-algorithms** to compare alternatives.</rule>
<rule>When discussing nested loops, recursion, DP transitions, or pointer movement, use **explain-complex-paths**.</rule>
<rule>When the user confirms the approach and understands the logic, use **design-algorithm**.</rule>
<rule>When the user changes requirements mid-flow, return to **clarify-problem**, **explore-cases**, or **brainstorm-algorithms**.</rule>
</rules>
