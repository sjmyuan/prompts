# Modify Existing SVG — Detailed Steps

Applies **modify-existing-svg** in the svg-editor skill.

**Steps**:

1. **Parse and understand the existing SVG**: Read the SVG XML and identify all significant elements: `<rect>`, `<circle>`, `<ellipse>`, `<polygon>`, `<path>`, `<text>`, `<line>`, `<defs>`, `<g>`, `<marker>`. Note the current `viewBox`, color palette, font choices, layout structure, and any existing `<defs>` definitions.

2. **Clarify the user's modification request**: Determine exactly what the user wants to change:
   - **Style changes**: Colors, borders, fonts, stroke widths, opacity, gradients
   - **Content changes**: Text labels, titles, annotations, data values
   - **Structural changes**: Add new shapes/nodes, remove existing elements, reorder elements (z-index)
   - **Layout changes**: Resize, reposition, realign existing elements
   - **Connection changes**: Add/remove/reroute connections, change line styles (solid/dashed), update arrow markers

3. **Plan modifications systematically**: Before editing, create a modification plan:
   - List each element to modify with its target change
   - For additions, determine placement using `<svg-layout-principles>` from SKILL.md (spacing, alignment, overlap avoidance)
   - For removals, identify all dependent elements (connections, labels attached to the removed element) that also need removal or re-routing
   - For style changes, reference `<color-palettes>` from SKILL.md to maintain visual consistency
   - Ensure the `viewBox` is still adequate after all changes; expand if needed

4. **Apply modifications while preserving SVG integrity**:
   - Preserve all existing `<defs>` definitions unless specifically asked to change them
   - Preserve existing `<g>` grouping structure unless the user requests restructuring
   - When changing colors, update both fills and strokes consistently
   - When changing text, recompute shape sizes if needed using `<text-sizing>` rules from SKILL.md
   - When adding new elements, apply `<connection-routing>` from SKILL.md for any new connections
   - When removing elements, also remove any orphaned connections that referenced the removed element

5. **Verify the result**: After all modifications:
   - Check that no new overlaps were introduced (use `<svg-layout-principles>` overlap avoidance rules)
   - Check that all connection lines still connect cleanly to their target shapes
   - Check that all `<marker>` references (`marker-end`, `marker-start`, `marker-mid`) point to valid `<marker>` definitions
   - Check that text fits within its parent shape (or update shape size)
   - Verify the `viewBox` contains all elements with adequate padding
   - Ensure the modified SVG remains valid XML

6. **Output the modified SVG**: Produce the complete corrected SVG with all modifications applied. If the changes are extensive, include a brief summary of what was changed.
