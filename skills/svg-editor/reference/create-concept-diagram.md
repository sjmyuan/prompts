# Create Concept Diagram — Detailed Steps

Applies **create-concept-diagram** in the svg-editor skill.

**Steps**:
1. **Identify the central concept and branches**: Determine the core topic (center) and related sub-concepts. Organize into ≤3 hierarchical levels.
2. **Build JSON for compute_all.py**: Use `diagram_type: "concept"`. Mark the central node with `"role": "central"`. Set branch nodes with no special role — they are distributed radially.
3. **Run compute_all.py**: Execute `python3 scripts/compute_all.py '<json>'`. The script handles radial layout, bezier paths, labels, and viewBox.
4. **Review validation**: Check `validation.all_clear`. If overlaps exist, adjust node count or let the force-directed resolver handle it.
5. **Assemble SVG**: Use script output SVG fragments (`svg_shape`, `svg_line`, `svg_label`, `svg_markers`, `svg_title_bar`). For concept diagrams, edges use bezier curves (set automatically when `diagram_type: "concept"`).
6. **Output**: Return raw, valid SVG code with no surrounding explanation.
