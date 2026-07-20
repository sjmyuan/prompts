# Modify Existing SVG — Reference

Applies **modify-existing-svg** in the edit-svg skill.

This reference covers modification types and the PPT upgrade workflow.

## Modification Types

| Type | Examples | Approach |
|---|---|---|
| Style | Colors, borders, fonts, gradients | Use `colors.PPT_PALETTE` consistently |
| Content | Text labels, titles, annotations | Call `svg_builder.get_shape_dimensions()` for new text sizes |
| Structural | Add/remove/reorder elements | Compute new positions via scripts, remove orphaned connections |
| Layout | Resize, reposition, realign | Run `graph_layout.resolve_overlaps()`, `compute_viewbox()` |
| Connections | Add/remove/reroute | Use `routing.orthogonal_path()`, `connection_endpoints()` |

## PPT Upgrade Workflow

When upgrading an existing SVG to PPT quality:

1. Generate PPT defs: `colors.get_shadow_filter()` + `colors.get_gradient_defs()`
2. Generate title bar: `svg_builder.generate_title_bar()`
3. Offset all existing y-coordinates via script
4. Upgrade font-family: `svg_builder.get_default_font_stack()`
5. Re-run **Generate SVG elements** with `ppt_mode=True`
6. Switch to 16:9 viewBox (960×540) if needed
7. Verify contrast: `colors.wcag_aa_check()`

## Detection & Correction Functions

| Area | Detection | Correction |
|---|---|---|
| Element overlap | `geometry.find_overlapping(bboxes, margin=10)` | `graph_layout.resolve_overlaps(nodes, margin=20)` |
| Path intersections | `routing.detect_intersections(paths, obstacles)` | `routing.orthogonal_path()` with obstacle avoidance |
| Endpoint validity | `routing.endpoint_valid(src_pt, dst_pt, src_bbox, dst_bbox)` | Re-route via `route_with_port_allocation()` |
| ViewBox clipping | — | `graph_layout.compute_viewbox(bboxes, padding=40)` |

## Workflow

1. Parse SVG → extract bounding boxes and paths
2. Detect overlaps and issues via detection functions
3. Fix issues via correction functions
4. Re-generate SVG fragments with corrected positions
5. Re-validate until clean
6. Assemble and output

## Verification Checklist

- [ ] No overlaps: `geometry.overlap()`
- [ ] Valid connections: `routing.endpoint_valid()`
- [ ] WCAG AA contrast: `colors.wcag_aa_check()`
- [ ] No viewBox overflow: `graph_layout.compute_viewbox()`
