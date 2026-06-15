# SVG Editor Computation Scripts
#
# All layout calculations (overlap detection, connection routing,
# label positioning, contrast validation) are done via Python scripts,
# not by AI reasoning.
#
# Usage from agent:
#   python3 scripts/compute_all.py '<json_description>'
#
# Modules:
#   geometry.py  - Bbox/point math, overlap detection, intersections
#   routing.py   - Orthogonal/bezier path computation, endpoint validation
#   layout.py    - Grid/radial layout, force-directed overlap resolution, viewBox
#   labeling.py  - Label placement on connection paths
#   colors.py    - WCAG contrast ratio, PPT palette, gradient/shadow defs
#   compute_all.py - Main orchestrator: JSON in, JSON out
