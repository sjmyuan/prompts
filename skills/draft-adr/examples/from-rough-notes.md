# Example: Structuring Rough Notes into an ADR

**Scenario**: The user has scattered meeting notes and wants help structuring them into a formal ADR. They don't have a clear problem statement yet — just raw discussion points. This example demonstrates all 5 capabilities starting from unstructured input, with emphasis on **define-problem** (clarifying vague input) and **define-considered-options** (brainstorming when the user hasn't identified clear alternatives).

---

## Capability: define-problem

**User input**:
> We had a discussion about our auth system. Currently using JWT but some folks think we should move to sessions. Not sure what to do. We have a React SPA and a Node backend. Security team is worried about token revocation. Also we need SSO eventually.

**Agent output**:
> That's a helpful starting point. Let me ask a few clarifying questions:
>
> 1. **Scope**: Is this decision about the entire auth mechanism (JWT vs. sessions), or are you also considering specific libraries/providers (e.g., Auth0, Passport.js)?
> 2. **Stakeholders**: Besides the security team, who else is involved? Frontend team? DevOps?
> 3. **Timeline**: Is there a deadline driving this decision, or is it a proactive improvement?
> 4. **SSO**: You mentioned SSO is needed "eventually" — is that a near-term requirement (next 3 months) or longer-term?

**User input**:
> It's about the auth mechanism — JWT vs session-based. Both options would use Passport.js either way. Main stakeholders are the security team and the frontend/backend dev teams. No hard deadline, but we're starting a new feature sprint in 2 weeks and want to settle this. SSO is 6+ months out.

**Agent output**:
> That clarifies things. Let me restate the problem:
>
> **Problem Statement**: We need to decide between JWT-based and session-based authentication for our React SPA + Node.js backend. Both options would use Passport.js for implementation. Key context:
> - The security team is concerned about token revocation capabilities
> - SSO integration is planned but not urgent (6+ months out)
> - Decision needed within 2 weeks before the next feature sprint
>
> Does this accurately capture the problem?

**User confirms**: Yes, that's it.

---

## Capability: define-decision-drivers

**User input**:
> The security team's main concern is being able to revoke access immediately if an account is compromised. The frontend team wants something simple that works well with SPAs. The backend team cares about statelessness for horizontal scaling. Also we're SOC 2 audited, so we need audit logging.

**Agent output**:
> Let me organize these into hard constraints and soft preferences:
>
> **Hard Constraints (must-haves)**:
> 1. Immediate token/session revocation — security team's non-negotiable for compromised accounts
> 2. SOC 2 compliance — audit logging for all auth events
>
> **Soft Preferences (nice-to-haves)**:
> 3. SPA-friendly — works well with React single-page app architecture
> 4. Statelessness — backend team prefers no server-side session state for horizontal scaling
> 5. SSO readiness — should not block future SSO integration
>
> Would you like to reorder or adjust any of these?

**User confirms**: That's correct.

---

## Capability: define-considered-options

**User input**:
> Well, we have JWT now and are considering sessions. Those are the two options.

**Agent output**:
> Two options is a good start. Let me brainstorm a bit more to make sure we're not missing anything:
>
> - **Status quo**: Keep JWT as-is (but this doesn't address the revocation concern — worth including so we can evaluate the cost of doing nothing)
> - **Hybrid approach**: JWT access tokens + a token blacklist/denylist in Redis — gives you revocation without full session state
> - **Opaque tokens**: Use reference/opaque tokens that map to server-side state, similar to sessions but with a token-style interface
>
> Here are the options I'd propose:
>
> 1. **JWT (status quo)** — stateless, current implementation
> 2. **Session-based auth** — server-side sessions with a session cookie
> 3. **JWT + Redis denylist** — keep JWT but add a revocation denylist in Redis
> 4. **Opaque tokens** — reference tokens with server-side state
>
> Would you like to keep all four, or should we narrow the list?

**User input**:
> Let's drop opaque tokens — too similar to sessions. Evaluate the first three.

**Agent confirms**: Three options: JWT (status quo), Sessions, JWT + denylist.

---

## Capability: evaluate-options

*(Abbreviated — same pattern as the database-selection example. Each option is evaluated with Pros/Cons tied back to the 5 decision drivers.)*

**After all evaluations, agent summarizes**:

| Driver | JWT (status quo) | Sessions | JWT + denylist |
|---|---|---|---|
| Immediate revocation | ❌ (knock-out) | ✅ | ✅ |
| SOC 2 audit logging | ⚠️ | ✅ | ✅ |
| SPA-friendly | ✅ | ✅ | ✅ |
| Statelessness | ✅ | ❌ | ⚠️ |
| SSO readiness | ✅ | ⚠️ | ✅ |

> JWT (status quo) is eliminated by the revocation hard constraint. Sessions satisfy all hard constraints but compromise statelessness. JWT + Redis denylist satisfies all hard constraints and strikes the best balance on soft preferences — it preserves most statelessness (Redis is lightweight) and keeps SSO readiness.

**User confirms**: JWT + Redis denylist.

---

## Capability: compile-adr

*(Same pattern as database-selection example — loads reference/adr-template.md, gathers metadata, produces the final ADR document.)*
