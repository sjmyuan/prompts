# Create Architecture Diagram — Detailed Steps

Applies **create-architecture-diagram** in the svg-editor skill.

**Steps**:
1. **Identify tiers and components**: Group components into horizontal tiers/layers (e.g., Client → API → Service → Database → External). Identify which components communicate and the direction of communication.
2. **Plan the layer layout**:
   - Each layer is a horizontal band spanning the full diagram width.
   - Layer height = max(component height within layer) + 30px padding top/bottom.
   - Within each layer, distribute components horizontally with equal spacing. Minimum gap between adjacent components = 60px to leave room for vertical connection lines passing between them.
   - Layer-to-layer gap = 60–80px (edge-to-edge) to ensure connection lines have room for arrowheads and labels. Reference `<svg-layout-principles>` corridor spacing: minimum 40px + extra for labels and bends.
3. **Position components**:
   - Component boxes: width = 140–180px, height = 50–60px for services; width = 120px, height = 40px for smaller items.
   - Draw a subtle background `<rect>` for each layer band using a light fill (e.g., `#F5F5F5`). Add a small header label for the layer name.
   - Use `<svg-layout-principles>` from SKILL.md for spacing validation.
4. **Draw connections**:
   - Use curved bezier paths for inter-layer connections (S-curves) and orthogonal paths for intra-layer connections.
   - Communication direction left-to-right or top-to-bottom as appropriate.
   - Apply `<connection-routing>` from SKILL.md for clean line routing.
5. **Add labels**:
   - Component names inside boxes. Layer names in the layer header band.
   - For connections, add protocol or data-flow labels at midpoints.
6. **Add decorations**:
   - Optional: cloud shape for external systems (use overlapping `<circle>` and `<path>` elements).
   - Optional: database cylinder shape for storage tiers (ellipse top + rect body + ellipse bottom).
   - Optional: container bounding box (dashed `<rect>`) enclosing grouped components.
7. **Set viewBox** and output raw SVG.
