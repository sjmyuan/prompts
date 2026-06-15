# Modify Existing SVG — Detailed Steps

Applies **modify-existing-svg** and **upgrade-to-ppt-quality** in the svg-editor skill.

Before starting, load `<ppt-design-requirements>` and `<svg-layout-principles>` from SKILL.md.

**Steps**:

1. **Parse and understand the existing SVG**: Read the SVG XML and identify all significant elements: `<rect>`, `<circle>`, `<ellipse>`, `<polygon>`, `<path>`, `<text>`, `<line>`, `<defs>`, `<g>`, `<marker>`. Note the current `viewBox`, color palette, font choices, layout structure, and existing `<defs>`.

2. **Clarify the user's modification request**: Determine exactly what changes are needed:
   - **Style changes**: Colors, borders, fonts, stroke widths, gradients
   - **Content changes**: Text labels, titles, annotations, data values
   - **Structural changes**: Add/remove/reorder elements
   - **Layout changes**: Resize, reposition, realign elements
   - **Connection changes**: Add/remove/reroute connections, change line styles

3. **Plan modifications**: Before editing, create a modification plan:
   - List each target element with its change
   - For additions: determine placement using `<svg-layout-principles>` spacing rules
   - For removals: identify dependent elements (connections, labels) that also need removal
   - For style changes: use `colors.PPT_PALETTE` for color consistency
   - For text changes: recompute shape size via `svg_shapes.get_shape_dimensions()`
   - Ensure `viewBox` is still adequate; expand if needed

4. **Apply modifications**:
   - Preserve existing `<defs>` unless asked to change them
   - Preserve `<g>` grouping structure unless user requests restructuring
   - When changing colors, update both fills and strokes consistently from `colors.PPT_PALETTE`
   - When changing text, call `svg_shapes.get_shape_dimensions()` to compute new shape sizes
   - When adding new elements, run `compute_all.py` with updated JSON to compute positions and SVG fragments
   - When removing elements, also remove orphaned connections
   - **PPT upgrade steps** (apply when user requests PPT quality):
     a. Generate PPT defs: `colors.get_shadow_filter()` and `colors.get_gradient_defs()`
     b. Generate title bar: `svg_shapes.generate_title_bar(title, width)`
     c. Offset all existing y-coordinates by +60px for title bar space
     d. Upgrade font-family to `svg_shapes.get_default_font_stack()`
     e. Apply `filter="url(#shadow)"` to key shapes, increase `rx`/`ry` to 6–8px
     f. Switch to 16:9 viewBox (960×540) if not already compatible
     g. Verify contrast ≥4.5:1 via `colors.wcag_aa_check()`

5. **Verify the result**: After all modifications:
   - Check no new overlaps introduced (use `geometry.overlap()`)
   - Check all connections still connect cleanly
   - Check contrast via `colors.wcag_aa_check()`
   - Ensure no elements overflow the viewBox
   - Return the complete, valid SVG
