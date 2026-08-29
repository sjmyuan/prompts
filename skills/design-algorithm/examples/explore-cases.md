# Example: Enumerate All Cases an Algorithm Must Handle

**Scenario**: The clarified problem is "given an array of n−1 numbers from 1..n with exactly one missing, return the missing number."
The assistant runs **explore-cases** to enumerate every input category before design.

**Applies**: **explore-cases**

## Input / Context

Confirmed definition: input is `arr` of n−1 distinct integers from 1..n, exactly one missing; output is the missing integer.

## Expected Output

A confirmed case list by category:

| Category | Case | Expected behavior |
|---|---|---|
| Normal | Missing value in the middle (e.g. 1..5 missing 3) | Return 3 |
| Boundary | Missing 1 (smallest) | Return 1 |
| Boundary | Missing n (largest) | Return n |
| Edge | n = 2 (one element) | Return the other value |
| Edge | n = 1 (empty array) | Return 1 |
| Error | Duplicate values present | Out of scope — problem states distinct |
| Error | Value outside 1..n | Out of scope — reject or clarify |

**Confirmation**: "Are any cases missing?"
