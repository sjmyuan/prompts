# Extraction Playbook — extract-and-refine-capability detail

Apply when `extract-and-refine-capability` routes a candidate to the text path or code path. This file holds the full per-step guidance; the capability in SKILL.md links here.

## Text path — described procedures (signal #12)

Steps explicit in text (chat message, Slack thread, document). The procedure is read, not inferred.

1. **Locate the procedure in text**: ordered language (first/then/next/finally), imperative instructions (you need to/make sure to/always), checklist formatting, conditional branches ("if this is a hotfix, also…"), tool/script invocations.
2. **Scope the task**: goal (what does this accomplish?), trigger condition (when would someone do this?), intended audience.
3. **Extract ordered steps**: imperative verb phrases, preserve order, remove filler, note dependencies and branches.
4. **Identify parameters**: constants (team conventions) become steps; variants (values changing per instance) become parameters with documented type/format.
5. **Assess confidence**: Tentative (single description from one source) or Confirmed (described independently 2+ times, or explicitly "the standard way").
6. **Apply quality checks**: load reference/capability-quality-checklist.md — Reusable, Non-obvious, Complete, Team-specific. Tentative does NOT cause rejection.
7. **Format as a capability**: load reference/capability-format-template.md.

## Code path — implementation recipes (signal #13)

Steps inferred from code changes (which repos/files were touched, in what order). The procedure is deduced, not read. The candidate already carries raw evidence; if missing, return to the source PR(s).

1. **Gather the raw evidence**: repo map, per-repo file list and change order, dependency order between repos.
2. **Map the per-repo change sequence**: files modified/created in order; identify logical phases (e.g., "API endpoint → DB helper → tests").
3. **Map cross-repo orchestration** (multi-repo): which repo first, dependency order, deploy-ordering constraints.
4. **Check generalizability**: would a similar task follow the same repos/files/change types? If domain-specific but structurally general, capture both.
5. **Determine the extraction level**: single repo → one repo-level capability. Multiple repos → repo-level capabilities per repo PLUS a cross-repo orchestration capability referencing them as sub-steps.
6. **Assess confidence and compare instances** (2+ PRs): Tentative (1 PR) or Confirmed (2+); compute per-step hit rate; identify always-present vs conditional steps.
7. **Apply quality checks** (as text-path step 6); for cross-repo, verify inter-repo dependencies are clear.
8. **Format as capability / set**: load reference/capability-format-template.md; multi-repo → one per repo plus orchestration.

## Refine phase — overlapping capabilities

Run only when an overlapping capability already exists in the target.

1. **Load existing context**: read the target file for capabilities covering related tasks; check overlaps at repo and cross-repo level.
2. **Compare existing vs new**: identical steps (core invariant), similar-but-different (unifiable with parameters), unique steps (conditional branches).
3. **Identify the abstraction**: replace concrete values with parameters, merge similar steps, add conditional branches; cover all known instances without over-generalizing.
4. **Preserve variant knowledge**: keep meaningful variants as sub-cases with concrete values; don't force unification.
5. **Validate the abstraction**: verify each original instance is derivable by filling parameters, nothing lost.
6. **Produce the refined capability**: template + evolution note + parameter table showing each parameter with all known variant values. Mark as replacing (not duplicating) the existing capability.
