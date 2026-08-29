# Example: Explain a DP Transition Step by Step

**Scenario**: The user chose dynamic programming for the Longest Increasing Subsequence (LIS) problem but cannot follow the state transition.
The assistant runs **explain-complex-paths** with a step-by-step trace on a tiny example.

**Applies**: **explain-complex-paths**

## Input / Context

Pattern to explain: `dp[i] = 1 + max(dp[j])` for all `j < i` with `nums[j] < nums[i]`. Example input `[3, 1, 2]`.

## Expected Output

Step-by-step trace of the transition:

| Step | i | nums[i] | Candidates j with nums[j] < nums[i] | dp[i] |
|---|---|---|---|---|
| 1 | 0 | 3 | none | 1 |
| 2 | 1 | 1 | none (nums[0] = 3 > 1) | 1 |
| 3 | 2 | 2 | j = 1 (nums[1] = 1 < 2, dp[1] = 1) | 1 + 1 = 2 |

Mermaid diagram of the transition flow:

```mermaid
flowchart LR
    A[nums[i] = 2] --> B[scan all j < i]
    B --> C{nums[j] < nums[i]?}
    C -- yes --> D[candidate = dp[j] + 1]
    C -- no --> E[skip]
    D --> F[dp[i] = max of candidates]
```

**Takeaway**: `dp[i]` means "LIS ending exactly at index i". The transition extends any shorter increasing subsequence that ends with a smaller value.

**Confirmation**: "Can you restate what dp[i] means in your own words?"
