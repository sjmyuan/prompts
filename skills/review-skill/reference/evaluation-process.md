# Output Evaluation Process

A well-structured skill should define an evaluation process to assess the quality of its own output. Look for:

- A dedicated validation or checklist step within a capability that lists criteria for verifying output correctness.
- A separate capability focused on evaluating or self-reviewing the skill's output.
- A reference file containing a quality checklist that the capability instructs the agent to load and apply.
- Explicit success criteria or pass/fail checks defined in the capability steps.

Common patterns:
- "Verify that [output] meets [criteria]" as a step.
- "Load **reference/quality-checklist.md** and apply each criterion".
- A dedicated `<validate-output>` capability with ordered validation steps.

Severity when absent:
- No evaluation step in any capability → 🟡 Minor (output reliability depends entirely on agent discretion).
- No evaluation step AND no examples demonstrating output validation → 🔴 Major (no way to verify output correctness).
