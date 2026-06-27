# Modify Existing SVG — Detailed Steps

Applies **modify-existing-svg** and **upgrade-to-ppt-quality** in the svg-editor skill.

Before starting, load [reference/design-standards.md](design-standards.md) for PPT/layout standards. Read the zero-tolerance rule in [reference/computation-snippets.md](computation-snippets.md) — no manual coordinate math.

**Steps**:

0. **No manual coordinate math for modifications**. When adding, repositioning, or resizing elements, ALL new positions, dimensions, and paths MUST come from script execution. Never manually compute offsets, new coordinates, or path adjustments.

1. **Parse and understand the existing SVG**: Read the SVG XML and identify significant elements: `viewBox`, colors, fonts, structure, `<defs>`.

2. **Clarify modification type**:
   - **Style changes**: Colors, borders, fonts, stroke widths, gradients
   - **Content changes**: Text labels, titles, annotations
   - **Structural changes**: Add/remove/reorder elements
   - **Layout changes**: Resize, reposition, realign
   - **Connection changes**: Add/remove/reroute connections

3. **Plan modifications**: List each target element with its change. For additions, use design-standards spacing rules. For text changes, call `svg_builder.get_shape_dimensions()` **— do NOT manually estimate new dimensions.** Ensure `viewBox` is adequate; expand via `graph_layout.compute_viewbox()` if needed.

4. **Apply modifications via scripts**:
   - Preserve `<defs>` and `<g>` grouping unless asked to change them
   - When changing colors, use `colors.PPT_PALETTE` consistently
   - When changing text, call `svg_builder.get_shape_dimensions()` **— do NOT manually recalculate dimensions**
   - When adding elements, run the **Compute node positions** and **Generate SVG elements** snippets from [reference/computation-snippets.md](computation-snippets.md) **— do NOT manually write new element SVG**
   - When removing elements, also remove orphaned connections
   - **PPT upgrade** (apply when user requests PPT quality):
     a. Generate PPT defs via script: `colors.get_shadow_filter()` + `colors.get_gradient_defs()` **— do NOT write filter/gradient SVG manually**
     b. Generate title bar via script: `svg_builder.generate_title_bar()` **— do NOT write title bar SVG manually**
     c. Offset all existing y-coordinates via script — **do NOT manually add +60 in your reasoning**
     d. Upgrade font-family to `svg_builder.get_default_font_stack()`
     e. Re-run **Generate SVG elements** snippet with `ppt_mode=True` **— do NOT manually add `filter` or `rx`**
     f. Switch to 16:9 viewBox (960×540) if needed
     g. Verify contrast via `colors.wcag_aa_check()`

5. **Verify the result via scripts**:
   - Run `geometry.overlap()` to check new overlaps **— do NOT visually estimate**
   - Run `routing.endpoint_valid()` to check connections
   - Run `colors.wcag_aa_check()` for contrast
   - Run `graph_layout.compute_viewbox()` to ensure no overflow
   - Return the complete, valid SVG
