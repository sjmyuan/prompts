# ADR Template

When producing the final ADR document, use the exact structure below. Wrap placeholders in `{{ }}` and fill them in based on the discussion with the user. Apply the concise writing rules in **reference/writing-style.md** — BLUF takeaway under every heading, caps, no banned phrases.

````markdown
# YYYY-MM-DD-{{TITLE}}

* Status: {{STATUS:draft | adopt | declined | superseded}}
* Owners: [ Who started and drives the ADR ]
* Date: {{DATE}}

## Context and Problem Statement

[ ≤3 sentences, SCQA: Situation → Complication → Question → Answer. Lead with the question this ADR answers. ]

![Context diagram: system(s) in scope, actors, and external dependencies]({{DIAGRAM:context}})
[ Embed the C4 context diagram drawn during define-problem, plus any flowchart or sequence diagram used to zoom into the context. For architecture diagrams use C4 Models see https://c4model.com ]

## Decision Outcome

**Chosen:** "[ option 1 ]" — [ 1-sentence justification tied to a specific driver, e.g. "meets KO driver #1 (ACID); best on cost & team expertise" ].

![C4/flowchart: target state with the chosen option integrated into the context]({{DIAGRAM:solution}})
[ Embed the target-state C4/flowchart view drawn during compile-adr. ]

## Consequences

[ 1-line trade-off takeaway, e.g. "**Trade-off:** self-managed ops for lower cost." ]

### Positive Consequences <!-- optional -->

* [ one claim per bullet, ≤10 words, no justification ]
* ...

### Risks <!-- optional -->

* [ one claim per bullet, ≤10 words ]
* ...

### Security

* [ one claim per bullet, ≤10 words ]
* ...

## Decision Drivers <!-- optional -->

* [ one driver per bullet — a fact, not a sentence ]
* ...

## Considered Options

* [ option 1 ]
* [ option 2 ]
* ...

![Option comparison matrix: drivers × options with knock-out highlights]({{DIAGRAM:comparison-matrix}})
[ Embed the option comparison matrix / elimination tree drawn during evaluate-options. ]

## Evaluation of the Options <!-- required -->

### [ option 1 ]

**Verdict:** [ 1 line: recommended / dropped + which driver decides — ≤15 words ]

[ ≤3 short sentences: what it is, key strengths, key risks ] <!-- required -->

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

* [ one claim per bullet — no justification ]
* ...

#### Cons

* [ one claim per bullet — no justification ]
* ...

### [ option 2 ]

**Verdict:** [ 1 line: recommended / dropped + which driver decides — ≤15 words ]

[ ≤3 short sentences: what it is, key strengths, key risks ] <!-- required -->
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

* [ one claim per bullet — no justification ]
* ...

#### Cons

* [ one claim per bullet — no justification ]
* ...

## References <!-- optional -->
````
