# Capability Quality Checklist

Apply these checks to every extracted capability before provisioning. Reject capabilities that fail any criterion.

| Criterion | Question | Rejection rule |
|---|---|---|
| **Reusable** | Would someone follow these same steps more than once? | One-off or single-use procedures → reject |
| **Non-obvious** | Would a newcomer figure this out without being told? | Common/generic knowledge → reject |
| **Complete** | Can someone follow these steps end-to-end without missing context? | Missing dependencies or assumed knowledge → flag as incomplete, fill gaps |
| **Team-specific** | Does it encode this team's conventions vs. generic best practice? | Generic best practice that any developer would know → reject; capabilities should capture team-specific conventions |

**Confidence note**: Tentative confidence (single instance) does NOT cause rejection — it just means the capability should be tagged as tentative and revisited when more data arrives.
