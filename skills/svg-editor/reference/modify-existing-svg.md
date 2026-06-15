# Modify Existing SVG — Detailed Steps

Applies **modify-existing-svg** and **upgrade-to-ppt-quality** in the svg-editor skill.

Before starting, load the following knowledge sections from SKILL.md for reference:
- `<ppt-design-requirements>` — PPT-quality standards for slide-ready output
- `<color-palettes>` — PPT Professional palette (default) and Basic palette
- `<svg-element-reference>` — PPT-quality SVG patterns with drop shadows and gradients
- `<svg-layout-principles>` — canvas, spacing, alignment, and overlap avoidance
- `<text-sizing>` — text and shape sizing with PPT typography defaults
- `<viewbox-strategy>` — PPT standard 16:9 viewBox (960×540) as default

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
   - When changing colors, update both fills and strokes consistently, defaulting to the PPT Professional palette from `<color-palettes>`
   - When changing text, recompute shape sizes if needed using `<text-sizing>` rules from SKILL.md
   - When adding new elements, apply `<connection-routing>` from SKILL.md for any new connections
   - When removing elements, also remove any orphaned connections that referenced the removed element
   - **PPT upgrade steps** (apply when user wants PPT quality):
     a. Insert `<filter id="shadow">` with `feDropShadow` in `<defs>` (see `<svg-element-reference>`)
     b. Add `<linearGradient>` definitions for shape fills matching PPT Professional palette
     c. Add a title bar: `<rect>` at y=0, full width, 60px height, `#1A73E8` fill, with shadow and white bold title text
     d. Offset all existing y-coordinates by +60px to make room for the title bar
     e. Upgrade font-family to `Segoe UI, -apple-system, Helvetica Neue, Arial, sans-serif`
     f. Apply `filter="url(#shadow)"` to key shapes, increase `rx`/`ry` to 6–8px
     g. Switch to 16:9 viewBox (`960×540`) if not already PPT-compatible
     h. Verify contrast ≥4.5:1 per `<ppt-design-requirements>`

5. **Verify the result**: After all modifications:
   - Check that no new overlaps were introduced (use `<svg-layout-principles>` overlap avoidance rules)
   - Check that all connection lines still connect cleanly to their target shapes
   - Check that all `<marker>` references (`marker-end`, `marker-start`, `marker-mid`) point to valid `<marker>` definitions
   - Check that text fits within its parent shape (or update shape size)
   - Verify the `viewBox` contains all elements with adequate padding
   - Ensure the modified SVG remains valid XML

6. **Output the modified SVG**: Produce the complete corrected SVG with all modifications applied. If the changes are extensive, include a brief summary of what was changed.
