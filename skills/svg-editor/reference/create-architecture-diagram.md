# Create Architecture Diagram — Detailed Steps

Applies **create-architecture-diagram** in the svg-editor skill.

**Steps**:
1. **Identify tiers and components**: Group components into horizontal tiers/layers (e.g., Client → API → Service → Database → External). Identify communication direction.
2. **Build JSON for compute_all.py**: Use `diagram_type: "architecture"`. Assign `row` for each layer (0=top, 1, 2...) and `col` for components within a layer. Use `type: "process"` for standard service boxes, `type: "data"` for databases.
3. **Run compute_all.py**: Execute `python3 scripts/compute_all.py '<json>'`. The script handles positioning and connection routing.
4. **Review validation**: Check `validation.all_clear`. Adjust row spacing if overlaps are detected.
5. **Assemble SVG**: Use the script's SVG fragments. Additionally:
   - Draw subtle background `<rect>` for each layer band using `PPT_PALETTE["bg_panel"]`. Add layer header labels.
   - Optionally add cloud shapes, database cylinders, or container bounding boxes as decorative elements.
   - Use `svg_shapes.generate_section_panel()` for layer backgrounds.
6. **Output**: Return raw, valid SVG code.
