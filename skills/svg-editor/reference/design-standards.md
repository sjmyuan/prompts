# PPT Design Standards & Layout Principles

## PPT Design Requirements

All SVG output must meet professional presentation standards for PPT/Keynote/Google Slides.

- **Dimensions**: 16:9 aspect ratio (`viewBox="0 0 960 540"` default). Diagram fills 60–85% of slide area. Include a **title bar** (bold centered title, `#1A73E8` background, white text).
- **Visual effects**: Drop shadows on key shapes (`colors.get_shadow_filter()`), soft linear gradients for fills (`colors.get_gradient_defs()`), rounded corners (`rx="6"`+).
- **Typography**: `font-family="Segoe UI, -apple-system, Helvetica Neue, Arial, sans-serif"`. Title: 20–22px bold. Body: 14px. Annotations: 11px. Min readable: 10px.
- **Color contrast**: WCAG AA (≥4.5:1) for all text vs background. Light fills with dark text. Validate via `colors.wcag_aa_check()`.
- **Simplicity**: 5–8 main elements per diagram. ≤15 words per shape. Group elements with subtle background panels. Min 40px between groups, 20px within groups.

## SVG Layout Principles

**ZERO-TOLERANCE: All geometric computations MUST be delegated to Python scripts — never compute coordinates, bounding boxes, path strings, or dimensions manually.**

- **Canvas**: `viewBox="0 0 960 540"` default. Leave 20–40px padding.
- **Spacing**: Min 20px gap between adjacent shapes. Group-related: 10–15px internal, 30–40px external.
- **Connection corridor**: Min 40px gap between shapes needing connection lines. Multi-line: 60px+.
- **Line clearance**: Any line bend ≥25px away from any other element's edge.
- **Alignment**: Same-level elements aligned to common baseline. Text centered in shapes.
- **Sizing**: Same semantic type → uniform size. Compute via `svg_builder.get_shape_dimensions()`.
- **Z-order**: Connections before shapes (lines underneath). Text labels on top.
- **Overlap avoidance**: Use `geometry.overlap()` / `geometry.find_overlapping()` — never manually check.
