# Option Tech Details Guide

Tech details make each option's implementation concrete in the ADR: the target-state diagrams and the code changes (diff) the option requires — where they happen and how to make them — so options are evaluated on technical feasibility, not just pros/cons. Produced per option by **detail-options-tech**, grounded in code investigation evidence — never assumption.

## Evidence base (grounding contract)

Before producing tech details, determine the evidence base:
- **Existing evidence**: findings from the `conduct-spike` pipeline (embedded evidence map — entry points, key locations, call chains, evidence ledger). Use it directly — do not re-scan covered code.
- **No evidence, code accessible**: build a lightweight evidence map on demand via the `investigate-code` skill — entry points, key locations with `file:line`, call chains for the affected flows.
- **No evidence, no code access**: produce architectural-level change profiles; mark every location/scope **unverified**; recommend a spike (`conduct-spike`) to ground them before relying on the tech details.

## What each option's tech details contain

### 1. Target-state diagrams
- **C4 view** (container or component): the architecture if this option is chosen — evolve the findings doc's current-state diagram as-is → to-be for this option.
- **Sequence diagram(s)**: the key flow(s) this option changes — new message, changed call, added hop, removed dependency.
- Diagrams are **option-specific** — never reuse another option's diagram or the chosen-solution diagram.

### 2. Code change profile (git-style diff)
For every change the option requires:

| Field | Content |
|---|---|
| Location | `file:line` + symbol |
| Current | What the code does today — quoted from the evidence map |
| Diff | **Git-style diff code block** (like `git diff` output): `diff --git a/… b/…`, `--- a/…` / `+++ b/…`, `@@` hunk, `-` / `+` lines with context — focused on the **existing code** |
| How | 1–2 sentence instruction to make the change |
| Confidence | verified / inferred / unverified |

Each change's diff renders as its own git-diff code block, so added/removed lines and their location are immediately readable:

```diff
diff --git a/src/main/java/com/pay/BankTransferService.java b/src/main/java/com/pay/BankTransferService.java
--- a/src/main/java/com/pay/BankTransferService.java
+++ b/src/main/java/com/pay/BankTransferService.java
@@ -1,4 +1,6 @@
+@RestController
+@RequestMapping("/transfer")
 @Service
 public class BankTransferService {
@@ -88,7 +92,12 @@ public class BankTransferService {
 public void transfer(TransferRequest req) {
   ...
 }
+
+  @PostMapping
+  public void transferEndpoint(@RequestBody TransferRequest req) {
+    transfer(req);
+  }
}
```

Focus on diffs of **existing code** — the user needs location and how-to, not assumed knowledge. List new files briefly (name + purpose) without diffing them.

## Grounding rules

- Every change traces to the evidence map — entry point → key location → call chain. Cite `file:line`; never "the service layer".
- **Never invent** APIs, symbols, or files. If a change needs something the investigation did not establish, mark it **unverified** and offer to investigate.
- **Never assume the user already knows a change** — spell out every change explicitly, even obvious ones.
- Confidence: **verified** (directly read), **inferred** (derived from surrounding code), **unverified** (assumption). Present inference as inference.
- Diagrams derive from the evidence's current state; do not draw structures the investigation did not establish.

## Output format (per option)

````markdown
### Option: [Name]

#### Target-state diagram
[ C4 view + sequence diagram(s) ]

#### Code changes
1. **`file:line` symbol** (confidence)
   - Current: [quote from evidence map]
   - Diff (git-style):
     ```diff
     diff --git a/<file> b/<file>
     --- a/<file>
     +++ b/<file>
     @@ -<start>,<count> +<start>,<count> @@
      context line
     -removed line
     +added line
     ```
   - How: [1–2 sentence instruction]
````

## Relationship to the ADR

Each option's tech details render as a `#### Tech Details` subsection in that option's **Evaluation of the Options** section (see `reference/adr-template.md`). Omit the subsection when no tech details were produced.
