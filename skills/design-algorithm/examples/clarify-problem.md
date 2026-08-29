# Example: Clarify a Vague Problem Before Design

**Scenario**: The user asks for "an algorithm to find duplicates in a list" — too vague to design against. The assistant runs **clarify-problem** until the six template items are defined.

**Applies**: **clarify-problem**

## Input / Context

User: "I need an algorithm to find duplicates in a list."

## Expected Output

A confirmed problem definition covering the six template items:

**Problem Statement**: Find every element that appears more than once in an input array.

**Input Format**: An array `nums` of integers, length n (1 ≤ n ≤ 10⁵), each value in [−10⁹, 10⁹].

**Output Format**: A list of integers — every value that appears at least twice, in order of first occurrence.

**Constraints**: n up to 10⁵; values may be negative; no time or memory limit specified.

**Edge Cases**: Empty array; single element; all elements unique; all elements identical; duplicates at the start; duplicates at the end; negative values.

**Examples**:
- `[1, 2, 3]` → `[]`
- `[1, 2, 1, 3, 2]` → `[1, 2]`
- `[-1, -1, 0]` → `[-1]`

**Confirmation**: "Does this definition match your intent?"
