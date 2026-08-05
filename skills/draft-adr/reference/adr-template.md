# ADR Template

When producing the final ADR document, use the exact structure below. Wrap placeholders in `{{ }}` and fill them in based on the discussion with the user.

````markdown
# YYYY-MM-DD-{{TITLE}}

* Status: {{STATUS:draft | adopt | declined | superseded}}
* Owners: [ Who started and drives the ADR ]
* Date: {{DATE}}

## Context and Problem Statement

[ Describe the context and problem statement, e.g. in free form using two to three sentences. You may want to articulate the problem in form of a question. ]

![Context diagram: system(s) in scope, actors, and external dependencies]({{DIAGRAM:context}})
[ Embed the C4 context diagram drawn during define-problem, plus any flowchart or sequence diagram used to zoom into the context. For architecture diagrams use C4 Models see https://c4model.com ]

## Decision Outcome

Chosen option: "[ option 1 ]", because [ justification e.g. only option which meets k.o. criterion of decision driver 1 | which resolves issue | comes out best (see below) | ... ].

![C4/flowchart: target state with the chosen option integrated into the context]({{DIAGRAM:solution}})
[ Embed the target-state C4/flowchart view drawn during compile-adr. ]

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

![Option comparison matrix: drivers × options with knock-out highlights]({{DIAGRAM:comparison-matrix}})
[ Embed the option comparison matrix / elimination tree drawn during evaluate-options. ]

## Evaluation of the Options <!-- required -->

### [ option 1 ]

[ example | description | pointer to more information | scenario | strengths | impact | ... ] <!-- required -->

#### Tech Details <!-- optional: include when tech details were provided from a spike's code investigation -->

[ Target-state diagram(s) for this option: C4 view + sequence diagram(s) showing the flow this option changes. ]

**Code changes** (grounded in the code reference — `file:line`, one git-style diff block per change):

1. `file:line` symbol (confidence: verified / inferred / unverified) — [how to change it]

```diff
diff --git a/<file> b/<file>
--- a/<file>
+++ b/<file>
@@ -<start>,<count> +<start>,<count> @@
 context line
-removed line
+added line
```

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
#### Tech Details <!-- optional: include when tech details were provided from a spike's code investigation -->

[ Target-state diagram(s) for this option: C4 view + sequence diagram(s) showing the flow this option changes. ]

**Code changes** (grounded in the code reference — `file:line`, one git-style diff block per change):

1. `file:line` symbol (confidence: verified / inferred / unverified) — [how to change it]

```diff
diff --git a/<file> b/<file>
--- a/<file>
+++ b/<file>
@@ -<start>,<count> +<start>,<count> @@
 context line
-removed line
+added line
```

#### Pros

* Good, because [ argument 1 ]
* Good, because [ argument 2 ]
* ... <!-- number of pros can vary -->

#### Cons

* Bad, because [ argument 3 ]
* Bad, because [ argument 4 ]
* ... <!-- number of cons can vary -->

## References <!-- optional -->
````
