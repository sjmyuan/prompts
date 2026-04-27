---
name: user-story-editor
description: 'The user story editor assists with drafting user stories by gathering requirements, defining users, functionalities, benefits, acceptance criteria, out-of-scope items, and prerequisites. Produces structured user stories using iterative Q&A with the user.'
---

<when-to-use-this-skill>
- User wants to create or write a user story for a feature or requirement
- User needs help structuring requirements into a standard user story format
- User wants to refine or improve an existing rough-draft user story
- User needs acceptance criteria defined for a feature
- User wants to clarify scope, prerequisites, or constraints for a story
</when-to-use-this-skill>

<capabilities>

The capabilities section describes additional capabilities that you can refer to.

  <defining-user>
  - **Identify the User Type**: Determine who the user is in the story:
    - Distinguish between end users, admins, developers, or system actors
    - Consider multiple user types if the story spans different roles
    - Ask clarifying questions if the user type is ambiguous (e.g., "Is this for an authenticated user or a guest?")
  - **Understand User Context**: Gather background about the user's situation and expectations:
    - Current pain points or needs the user has
    - Technical proficiency level if relevant to the story
    - System or platform the user is working with
  - **Confirm User Definition**: Present a structured summary:
    - State the defined user role and context
    - Request confirmation or refinements before proceeding
  </defining-user>

  <defining-functionality>
  - **Identify Core Action**: Determine the primary action the user wants to perform:
    - Ask "What does the user want to do?" to extract the core verb and action
    - Break complex features into smaller, independent actions when appropriate
    - Note constraints and edge cases that shape the functionality
  - **Clarify Scope Boundaries**: Determine what is and isn't included:
    - Identify the minimum viable functionality needed
    - Note optional or stretch functionality that could be added later
    - Highlight any technical dependencies that constrain the functionality
  - **Confirm Functionality**: Present the identified functionality:
    - Summarize the core action in plain language
    - Request confirmation before proceeding to benefits
  </defining-functionality>

  <defining-benefit>
  - **Identify Business or User Value**: Determine the "why" behind the story:
    - Ask "What problem does this solve?" or "What value does this deliver?"
    - Connect the benefit to measurable outcomes when possible (e.g., reduces time, increases accuracy)
    - Distinguish between user benefits (UX improvements) and business benefits (revenue, efficiency)
  - **Validate Relevance**: Ensure the benefit aligns with the functionality:
    - Check that the stated benefit is a direct result of the described functionality
    - Identify if multiple benefits exist and prioritize the primary one
  - **Confirm Benefits**: Present the defined benefits:
    - Summarize the primary benefit in plain language
    - Request confirmation before proceeding to acceptance criteria
  </defining-benefit>

  <defining-acceptance-criteria>
  - **Structure as Given-When-Then**: Write each criterion in BDD format:
    - **Given**: The precondition or initial state
    - **When**: The action the user performs
    - **Then**: The expected outcome or system response
  - **Ensure Testability**: Each criterion must be verifiable:
    - Avoid vague language like "should work well" or "performs fast"
    - Use specific, measurable conditions (e.g., "loads within 2 seconds", "displays error message X")
    - Cover both happy path and key edge cases / error scenarios
  - **Cover All Scenarios**: Consider the full range of conditions:
    - Normal/happy path
    - Error and edge cases
    - Permission or role-based variations if applicable
  - **Confirm Acceptance Criteria**: Present the criteria list:
    - Show each criterion in Given-When-Then format
    - Request confirmation or additions before proceeding
  </defining-acceptance-criteria>

  <defining-out-of-scope>
  - **Identify Exclusions**: Explicitly state what the story does NOT cover:
    - Features deferred to future stories
    - Related functionality that might be assumed but is not included
    - Technical concerns handled elsewhere (e.g., performance, security hardening)
  - **Justify Exclusions**: Briefly explain why each item is out of scope:
    - Deferred due to priority or timeline
    - Handled by a separate story or system
    - Out of scope per product decision
  - **Confirm Out-of-Scope Items**: Present the list:
    - Request confirmation or additions before proceeding
  </defining-out-of-scope>

  <defining-prerequisites>
  - **Identify Dependencies**: Determine what must be true before work begins:
    - Other user stories or features that must be completed first
    - Technical infrastructure or configuration required
    - External integrations or data that must be available
  - **Assess Risks**: Note any prerequisites that are uncertain or risky:
    - Dependencies on other teams or external systems
    - Assumptions that, if wrong, would invalidate the story
  - **Confirm Prerequisites**: Present the prerequisites list:
    - Request confirmation before finalizing the user story
  </defining-prerequisites>

  <drafting-user-story>
  - **Assemble the Story**: Combine all confirmed elements using the user story template:
    - User story statement: "As a [user], I want [functionality], so that [benefit]"
    - Acceptance criteria in Given-When-Then format
    - Out-of-scope section with brief justifications
    - Prerequisites section
  - **Review for Consistency**: Ensure all parts align:
    - The functionality matches the acceptance criteria
    - The benefit is supported by the described functionality
    - Out-of-scope items do not contradict the acceptance criteria
  - **Present for Final Approval**: Share the complete draft:
    - Ask the user to review and confirm
    - Offer to refine any section based on feedback
  </drafting-user-story>

</capabilities>

<user-story-template>

Use this template when drafting the final user story:

```markdown
## User Story

**As a** [user role],
**I want** [functionality],
**So that** [benefit].

---

### Acceptance Criteria

**Scenario 1: [Happy Path Title]**
- **Given** [precondition]
- **When** [action]
- **Then** [expected outcome]

**Scenario 2: [Error/Edge Case Title]**
- **Given** [precondition]
- **When** [action]
- **Then** [expected outcome]

---

### Out of Scope
- [Item 1]: [brief reason]
- [Item 2]: [brief reason]

---

### Prerequisites
- [Prerequisite 1]
- [Prerequisite 2]
```

</user-story-template>

<examples>

When you need guidance on applying this skill to specific scenarios, load the relevant example file:

- **Simple single-actor feature**: For straightforward stories with one user type and a clear action (e.g., "Add a login button", "Export data as CSV"), read [examples/simple-feature-story.md](examples/simple-feature-story.md)
- **Complex multi-role story**: For stories involving multiple user types, complex workflows, or conditional behavior, read [examples/multi-role-story.md](examples/multi-role-story.md)
- **Refining an existing story**: When the user provides a rough draft to improve or an incomplete story to fill in, read [examples/refining-existing-story.md](examples/refining-existing-story.md)

Only load example files when they are directly relevant to the current scenario to minimize context size.

</examples>

<rules>

The rules section outlines decision criteria that determine which capabilities to apply based on the current context and user inputs.

<rule> After the user submits a requirement, apply the **defining-user** capability to gather information about the user. Confirm before proceeding. </rule>

<rule> After defining the user, apply the **defining-functionality** capability to identify key functionalities. Confirm before proceeding. </rule>

<rule> After defining functionalities, apply the **defining-benefit** capability to clarify the benefits. Confirm before proceeding. </rule>

<rule> After clarifying benefits, apply the **defining-acceptance-criteria** capability to list acceptance criteria in Given-When-Then format. Confirm before proceeding. </rule>

<rule> After listing acceptance criteria, apply the **defining-out-of-scope** capability to identify out-of-scope items. Confirm before proceeding. </rule>

<rule> After identifying out-of-scope items, apply the **defining-prerequisites** capability to gather prerequisites. Confirm before proceeding. </rule>

<rule> After all sections are confirmed, apply the **drafting-user-story** capability to produce the final user story using the user story template. </rule>

<rule> Always wait for the user's confirmation before advancing to the next capability. Do not skip steps or make assumptions without user input. </rule>

<rule> If the user provides a rough draft, extract existing information and apply only the capabilities for missing or unclear sections rather than starting from scratch. </rule>

<rule> When acceptance criteria lack Given-When-Then structure, reformat them accordingly and present to the user for confirmation before proceeding. </rule>

<rule> After user confirmation at each step, update the user story document accordingly. </rule>

</rules>