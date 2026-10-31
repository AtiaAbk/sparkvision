# SPARKVISION — VISUAL REGRESSION & BENCHMARKING SUITE

## 1. Title & Executive Purpose

* **Document**: `VisualRegressionTests.md`
* **Purpose**: Defines reproducible camera transforms, programmatic capture procedures, and image comparison tolerance thresholds to prevent visual regressions across milestones.

---

## 2. Standard Benchmark Camera Transforms

To eliminate subjective viewpoint variations, visual regression tests use fixed camera coordinates via Unreal MCP:

| Benchmark View ID | Camera Location (X, Y, Z in cm) | Camera Rotation (Pitch, Yaw, Roll) | FOV | Benchmark Target |
| :--- | :--- | :--- | :---: | :--- |
| **VR-CAM-01 (Front Facade)** | `(-6500.0, 0.0, 650.0)` | `(-2.0, 0.0, 0.0)` | $75.0^\circ$ | Curzon Hall central portico & symmetrical wings |
| **VR-CAM-02 (45° Angled Aerial)** | `(-8000.0, -5000.0, 3200.0)` | `(-22.0, 30.0, 0.0)` | $80.0^\circ$ | Curzon courtyard, corner towers, and roofline |
| **VR-CAM-03 (Player Eye Level)** | `(-3500.0, 0.0, 200.0)` | `(0.0, 0.0, 0.0)` | $90.0^\circ$ | Player spawn perspective and promenade framing |
| **VR-CAM-04 (Campus Top-Down)** | `(20000.0, -80000.0, 150000.0)` | `(-90.0, 0.0, 0.0)` | $90.0^\circ$ | Campus wide road network and landmark alignment |

---

## 3. Execution & Automated Comparison Workflow

1. **Trigger Script**: Run `python3 Scripts/capture_scene_views.py`.
2. **Viewport Capture**: Unreal MCP dispatches `EditorAppToolset.CaptureViewport` with each fixed transform.
3. **Diff Analysis**: Python script computes Mean Squared Error (MSE) and Structural Similarity Index (SSIM) against `Documentation/VisualReferences/ApprovedVisualBaselines/`.
4. **Tolerance**: If $\text{SSIM} < 0.95$ on static architecture, the test flags a regression for artist inspection.

---

## 4. Current Status

* **Status**: `COMPLETED`
* **Evidence**:
  - Script `Scripts/capture_scene_views.py` operational; captures stored in `Documentation/Screenshots/`.
* **Remaining Tasks**:
  - Implement automated pixel-diff heatmap generation for flagged regressions.
