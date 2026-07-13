# Analyze and Fix Layout — Detailed Steps

Applies **analyze-and-fix-layout** in the edit-svg skill.

**🔴 Before starting**: Read the zero-tolerance rule in [reference/computation-snippets.md](computation-snippets.md). All layout fixes MUST be computed by scripts, not by manual coordinate tweaks.

**Steps**:
0. **No manual coordinate tweaks**. Every position adjustment, path re-route, and viewBox expansion MUST come from script execution. Never "nudge" coordinates manually.
1. **Parse the SVG**: Read the SVG XML, extract bounding boxes and connection paths from all significant elements.
2. **Reconstruct node/edge data**: Map SVG shapes to node types, paths to edges.
3. **Detect overlaps via snippet**: Run overlap validation from [reference/computation-snippets.md](computation-snippets.md). **Do NOT visually estimate overlaps.**
4. **Validate connections via snippet**: Run `routing.detect_intersections()`. **Do NOT manually trace paths.**
5. **Fix issues via scripts — never manually**:
   - **Overlaps**: Run `graph_layout.resolve_overlaps()`. **Do NOT manually shift coordinates.**
   - **Line-shape intersections**: Re-route via `routing.orthogonal_path()` with obstacle avoidance. **Do NOT manually adjust path strings.**
   - **Endpoint issues**: Use `routing.endpoint_valid()`. **Do NOT manually adjust endpoint coordinates.**
   - **ViewBox clipping**: Run `graph_layout.compute_viewbox()` with expanded dimensions. **Do NOT manually compute viewBox.**
6. **Regenerate SVG fragments via script**: Re-run **Generate SVG elements** snippet with corrected positions. **Do NOT manually edit SVG attributes.**
7. **Validate via script**: Re-run overlap and endpoint checks until clean.
8. **Assemble and output** corrected SVG following the **SVG assembly pattern** in [reference/computation-snippets.md](computation-snippets.md).
