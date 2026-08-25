# Suggest-Spike-On-ADR-Uncertainty Procedure

Full procedure for the `suggest-spike-on-adr-uncertainty` capability — loaded on demand when an ADR discussion hinges on unverified assumptions. Uncertainty signals: **adr-uncertainty-signals**.

1. Name the uncertainty precisely: "This decision seems to hinge on [the unverified assumption / the unknown fact / the unresolved comparison]."
2. Explain why the uncertainty matters.
3. Define a focused scope (single goal, 1–3 areas) via **define-spike-scope** when the user agrees.
4. Treat the ADR as provisional.
5. Continue the ADR flow via `draft-adr` per **professional-doc-authoring** when the user declines.
6. Record the uncertainty as a **risk** in the ADR's Consequences section — never a free-form note.
