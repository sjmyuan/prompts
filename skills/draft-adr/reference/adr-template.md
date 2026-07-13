# ADR Template

When producing the final ADR document, use the exact structure below. Wrap placeholders in `{{ }}` and fill them in based on the discussion with the user.

```markdown
# YYYY-MM-DD-{{TITLE}}

* Status: {{STATUS:draft | adopt | declined | superseded}}
* Owners: [ Who started and drives the ADR ]
* Date: {{DATE}}

## Context and Problem Statement

[ Describe the context and problem statement, e.g. in free form using two to three sentences. You may want to articulate the problem in form of a question. ]
[ For architecture diagrams use C4 Models see https://c4model.com ]

## Decision Outcome

Chosen option: "[ option 1 ]", because [ justification e.g. only option which meets k.o. criterion of decision driver 1 | which resolves issue | comes out best (see below) | ... ].

## Consequences

[ Describe a summary of the consequences of the decision chosen, e.g. in free form using two to three sentences. ] <!-- optional -->

### Positive Consequences <!-- optional -->

* [ improvement of quality attribute satisfaction | follow-up decisions required | strengths | impact | ... ]
* ...

### Risks <!-- optional -->

* [ what should be considered during implementation | risk mitigation | weaknesses | impact | ... ]
* ...

### Security

* [ what should be considered during implementation | Impact on Authorization, Authentication, Audit, Assurance, Availability, Asset Protection, Risk profile, Security controls ]
* ...

## Decision Drivers <!-- optional -->

* [ driver 1 e.g. a force, facing concern, ... ]
* [ driver 2 e.g. a force, facing concern, ... ]
* ...

## Considered Options

* [ option 1 ]
* [ option 2 ]
* ...

## Evaluation of the Options <!-- required -->

### [ option 1 ]

[ example | description | pointer to more information | scenario | strengths | impact | ... ] <!-- required -->

#### Pros

* Good, because [ argument 1 ]
* Good, because [ argument 2 ]
* ... <!-- number of pros can vary -->

#### Cons

* Bad, because [ argument 3 ]
* Bad, because [ argument 4 ]
* ... <!-- number of cons can vary -->

### [ option 2 ]

[ example | description | pointer to more information | scenario | strengths | impact | ... ] <!-- required -->

#### Pros

* Good, because [ argument 1 ]
* Good, because [ argument 2 ]
* ... <!-- number of pros can vary -->

#### Cons

* Bad, because [ argument 3 ]
* Bad, because [ argument 4 ]
* ... <!-- number of cons can vary -->

## References <!-- optional -->
```
