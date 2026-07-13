# Example: Machine Learning Pipeline Concept Diagram

**Scenario**: A user asks to create a concept diagram explaining an ML pipeline, from data collection to model deployment.

**Trigger**: "Create a concept diagram for a machine learning pipeline showing Data Collection → Data Preprocessing → Feature Engineering → Model Training → Model Evaluation → Model Deployment, with the central concept being 'ML Pipeline'."

**Applies**: **create-scripted-diagram** (concept variant)

---

## Input

Create a concept diagram for a machine learning pipeline:
- Central concept: "ML Pipeline"
- Level 1 nodes (clockwise from top): Data Collection, Data Preprocessing, Feature Engineering, Model Training, Model Evaluation, Model Deployment
- Each Level 1 node has 1-2 sub-nodes

## Output

```svg
<svg viewBox="0 0 800 700" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#78909C"/>
    </marker>
    <filter id="shadow-center" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="2" dy="3" stdDeviation="4" flood-color="#1565C0" flood-opacity="0.3"/>
    </filter>
    <filter id="shadow-node" x="-5%" y="-5%" width="120%" height="120%">
      <feDropShadow dx="1" dy="2" stdDeviation="2" flood-color="#000000" flood-opacity="0.1"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="800" height="700" fill="#FFFFFF"/>

  <!-- ========== CENTRAL CONCEPT ========== -->
  <circle cx="400" cy="350" r="55" fill="#E3F2FD" stroke="#1565C0" stroke-width="3" filter="url(#shadow-center)"/>
  <text x="400" y="342" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="15" fill="#1565C0" font-weight="bold">ML</text>
  <text x="400" y="360" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="15" fill="#1565C0" font-weight="bold">Pipeline</text>

  <!-- ========== LEVEL 1 NODES (6 nodes around center) ========== -->
  <!-- Positions calculated at 60° intervals, radius=140px from center (400,350) -->

  <!-- Node 1: Data Collection (top, 270°) -->
  <rect x="340" y="150" width="120" height="42" rx="6" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1.5" filter="url(#shadow-node)"/>
  <text x="400" y="175" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="12" fill="#212121" font-weight="bold">Data Collection</text>
  <!-- Connection: center → node1 -->
  <path d="M 400 295 C 400 250, 400 220, 400 192" stroke="#78909C" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>

  <!-- Node 2: Data Preprocessing (top-right, 330°) -->
  <rect x="540" y="215" width="140" height="42" rx="6" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1.5" filter="url(#shadow-node)"/>
  <text x="610" y="240" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="12" fill="#212121" font-weight="bold">Data Preprocessing</text>
  <!-- Connection: center → node2 -->
  <path d="M 440 310 C 490 280, 540 260, 570 250" stroke="#78909C" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>

  <!-- Node 3: Feature Engineering (bottom-right, 30°) -->
  <rect x="540" y="435" width="140" height="42" rx="6" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1.5" filter="url(#shadow-node)"/>
  <text x="610" y="460" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="12" fill="#212121" font-weight="bold">Feature Engineering</text>
  <!-- Connection: center → node3 -->
  <path d="M 440 395 C 490 420, 530 440, 560 450" stroke="#78909C" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>

  <!-- Node 4: Model Training (bottom, 90°) -->
  <rect x="345" y="500" width="110" height="42" rx="6" fill="#FFF3E0" stroke="#E65100" stroke-width="1.5" filter="url(#shadow-node)"/>
  <text x="400" y="525" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="12" fill="#212121" font-weight="bold">Model Training</text>
  <!-- Connection: center → node4 -->
  <path d="M 400 405 C 400 440, 400 470, 400 500" stroke="#78909C" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>

  <!-- Node 5: Model Evaluation (bottom-left, 150°) -->
  <rect x="120" y="435" width="130" height="42" rx="6" fill="#FFF3E0" stroke="#E65100" stroke-width="1.5" filter="url(#shadow-node)"/>
  <text x="185" y="460" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="12" fill="#212121" font-weight="bold">Model Evaluation</text>
  <!-- Connection: center → node5 -->
  <path d="M 355 395 C 310 420, 260 440, 230 450" stroke="#78909C" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>

  <!-- Node 6: Model Deployment (top-left, 210°) -->
  <rect x="110" y="215" width="140" height="42" rx="6" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1.5" filter="url(#shadow-node)"/>
  <text x="180" y="240" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="12" fill="#212121" font-weight="bold">Model Deployment</text>
  <!-- Connection: center → node6 -->
  <path d="M 355 310 C 310 280, 260 260, 230 250" stroke="#78909C" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>

  <!-- ========== LEVEL 2 NODES ========== -->

  <!-- Data Collection sub-nodes -->
  <rect x="300" y="100" width="90" height="32" rx="4" fill="#F1F8E9" stroke="#558B2F" stroke-width="1" filter="url(#shadow-node)"/>
  <text x="345" y="120" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="10" fill="#33691E">APIs</text>
  <path d="M 370 132 C 370 140, 380 145, 390 150" stroke="#B0BEC5" stroke-width="1" fill="none" marker-end="url(#arrow)"/>

  <rect x="440" y="100" width="90" height="32" rx="4" fill="#F1F8E9" stroke="#558B2F" stroke-width="1" filter="url(#shadow-node)"/>
  <text x="485" y="120" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="10" fill="#33691E">Databases</text>
  <path d="M 470 132 C 460 140, 450 145, 430 150" stroke="#B0BEC5" stroke-width="1" fill="none" marker-end="url(#arrow)"/>

  <!-- Data Preprocessing sub-nodes -->
  <rect x="600" y="170" width="100" height="32" rx="4" fill="#F1F8E9" stroke="#558B2F" stroke-width="1" filter="url(#shadow-node)"/>
  <text x="650" y="190" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="10" fill="#33691E">Clean &amp; Transform</text>
  <path d="M 630 205 C 625 210, 620 215, 615 218" stroke="#B0BEC5" stroke-width="1" fill="none" marker-end="url(#arrow)"/>

  <!-- Feature Engineering sub-nodes -->
  <rect x="610" y="390" width="100" height="32" rx="4" fill="#F1F8E9" stroke="#558B2F" stroke-width="1" filter="url(#shadow-node)"/>
  <text x="660" y="410" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="10" fill="#33691E">Feature Selection</text>
  <path d="M 640 420 C 630 425, 620 430, 610 435" stroke="#B0BEC5" stroke-width="1" fill="none" marker-end="url(#arrow)"/>

  <!-- Model Training sub-nodes -->
  <rect x="490" y="530" width="120" height="32" rx="4" fill="#FFF8E1" stroke="#F57F17" stroke-width="1" filter="url(#shadow-node)"/>
  <text x="550" y="550" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="10" fill="#E65100">Hyperparameter Tuning</text>
  <path d="M 490 545 C 470 540, 450 535, 455 530" stroke="#B0BEC5" stroke-width="1" fill="none" marker-end="url(#arrow)"/>

  <!-- Model Evaluation sub-nodes -->
  <rect x="60" y="490" width="120" height="32" rx="4" fill="#FFF8E1" stroke="#F57F17" stroke-width="1" filter="url(#shadow-node)"/>
  <text x="120" y="510" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="10" fill="#E65100">Cross-Validation</text>
  <path d="M 140 480 C 155 475, 165 465, 175 455" stroke="#B0BEC5" stroke-width="1" fill="none" marker-end="url(#arrow)"/>

  <!-- Model Deployment sub-nodes -->
  <rect x="50" y="170" width="120" height="32" rx="4" fill="#F1F8E9" stroke="#558B2F" stroke-width="1" filter="url(#shadow-node)"/>
  <text x="110" y="190" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="10" fill="#33691E">REST API / Docker</text>
  <path d="M 130 205 C 145 210, 160 215, 180 218" stroke="#B0BEC5" stroke-width="1" fill="none" marker-end="url(#arrow)"/>

  <!-- ========== FLOW ARROWS between Level 1 nodes (showing pipeline direction) ========== -->
  <!-- Data Collection → Data Preprocessing -->
  <path d="M 460 175 C 500 190, 520 200, 540 220" stroke="#B0BEC5" stroke-width="1.5" stroke-dasharray="4,3" fill="none" marker-end="url(#arrow)"/>

  <!-- Data Preprocessing → Feature Engineering -->
  <path d="M 620 260 C 620 340, 620 380, 610 435" stroke="#B0BEC5" stroke-width="1.5" stroke-dasharray="4,3" fill="none" marker-end="url(#arrow)"/>

  <!-- Feature Engineering → Model Training -->
  <path d="M 540 460 C 500 480, 480 490, 455 505" stroke="#B0BEC5" stroke-width="1.5" stroke-dasharray="4,3" fill="none" marker-end="url(#arrow)"/>

  <!-- Model Training → Model Evaluation -->
  <path d="M 345 525 C 310 530, 280 530, 250 520" stroke="#B0BEC5" stroke-width="1.5" stroke-dasharray="4,3" fill="none" marker-end="url(#arrow)"/>

  <!-- Model Evaluation → Model Deployment -->
  <path d="M 160 430 C 140 370, 140 320, 160 260" stroke="#B0BEC5" stroke-width="1.5" stroke-dasharray="4,3" fill="none" marker-end="url(#arrow)"/>

  <!-- ========== TITLE ========== -->
  <text x="400" y="620" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#757575" font-style="italic">Machine Learning Pipeline — End-to-End Workflow</text>

  <!-- Legend -->
  <rect x="280" y="640" width="12" height="12" rx="2" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1"/>
  <text x="298" y="650" font-family="Arial, sans-serif" font-size="11" fill="#424242">Data Stage</text>
  <rect x="420" y="640" width="12" height="12" rx="2" fill="#FFF3E0" stroke="#E65100" stroke-width="1"/>
  <text x="438" y="650" font-family="Arial, sans-serif" font-size="11" fill="#424242">Model Stage</text>
  <path d="M 555 646 L 585 646" stroke="#B0BEC5" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="593" y="650" font-family="Arial, sans-serif" font-size="11" fill="#424242">Pipeline Flow</text>
</svg>
```
