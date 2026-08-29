# Example: Brainstorm Alternative Algorithm Approaches

**Scenario**: The user proposes a linear scan for "search for a target in a rotated sorted array."
The assistant runs **brainstorm-algorithms** to propose paradigm-different alternatives and compare trade-offs.

**Applies**: **brainstorm-algorithms**

## Input / Context

User approach: linear scan — O(n). Constraint: n up to 10⁵.

## Expected Output

Alternative approaches with core idea, pros, and cons:

**1. Linear Scan (user's proposal)** — Core idea: check every element in turn.
- Pros: trivial to implement; makes no assumptions.
- Cons: O(n); ignores the sorted-rotated structure.

**2. Binary Search** — Core idea: the rotation splits the array into two sorted halves; compare `mid` with `left` to decide which half to keep, then recurse.
- Pros: O(log n); optimal for sorted input.
- Cons: fiddly boundary conditions for pivot and rotation direction.

**3. Find Pivot Then Binary Search** — Core idea: locate the rotation point with a binary search, then binary-search the appropriate half.
- Pros: clean two-phase reasoning; each phase is standard.
- Cons: two passes; slightly more code.

**Recommendation**: Binary search (option 2) — O(log n) fits the n ≤ 10⁵ constraint; option 3 is the fallback if the user finds option 2 hard to reason about.

**Confirmation**: "Which direction do you want to pursue?"
