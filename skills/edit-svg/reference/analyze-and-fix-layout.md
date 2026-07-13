# Analyze and Fix Layout — Reference

Applies **modify-existing-svg** in the edit-svg skill.

Layout fixes are handled by the consolidated **modify-existing-svg** capability. This reference provides the specific detection and correction functions.

## Detection Functions

| Issue | Function |
|---|---|
| Element overlap | `geometry.find_overlapping(bboxes, margin=10)` |
| Path intersections | `routing.detect_intersections(paths, obstacles)` |
| Endpoint validity | `routing.endpoint_valid(src_pt, dst_pt, src_bbox, dst_bbox)` |

## Correction Functions

| Issue | Function |
|---|---|
| Overlapping elements | `graph_layout.resolve_overlaps(nodes, margin=20)` |
| Line-shape intersections | `routing.orthogonal_path(src_pt, dst_pt, src_side, dst_side, obstacles=[])` |
| ViewBox clipping | `graph_layout.compute_viewbox(bboxes, padding=40)` |

## Workflow

1. Parse SVG → extract bounding boxes and paths
2. Detect overlaps and intersection issues via detection functions
3. Fix issues via correction functions
4. Re-generate SVG fragments with corrected positions
5. Re-validate until clean
6. Assemble and output
