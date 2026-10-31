# CURRENT GAME SCREENSHOTS & VIEWPORT CAPTURES

## 1. Purpose & Standards

This directory stores in-engine screenshots captured directly from active Unreal Engine 5.8 editor sessions and Play-In-Editor (PIE) runs of **SparkVision: University of Dhaka**.

These captures reflect the **work-in-progress state** of the actual game and serve as the direct visual evidence compared against our authentic reference photography and cinematic benchmarks.

---

## 2. Naming Conventions

All screenshots deposited here must follow strict, descriptive naming conventions:

```text
[Milestone]_[Landmark/Zone]_[CameraView]_[LightingPass].png
```

### Approved Filename Patterns:
* `Baseline_Curzon_Entrance.png` — Curzon Hall central portico from south promenade approach.
* `Baseline_Campus_Aerial.png` — High-altitude top-down or 45° angled campus wide view.
* `Baseline_Courtyard.png` — Curzon Hall inner quadrangle lawn and veranda perspective.
* `Baseline_PlayerView.png` — Third-person eye-level camera view behind player pawn.
* `Phase2_Curzon_FrontFacade_Daylight.png` — Frontal daylight render of hero Curzon facade.
* `Phase2_Curzon_FrontFacade_GoldenHour.png` — Golden-hour lighting render of Curzon facade.
* `PIE_Live_Gameplay_Verified.png` — In-viewport active player possession and collision capture.

---

## 3. Capture Protocol via Unreal MCP

To guarantee reproducible, scientific visual comparisons, screenshots are captured using the programmatic **Unreal MCP** toolset:
- **Toolset**: `EditorToolset.EditorAppToolset`
- **Method**: `CaptureViewport` (with exact camera location, rotator, and FOV) or `CaptureEditorImage`
- **Resolution**: Native 1920×1080 or viewport native aspect ratio.
- **Gizmos & Overlays**: `bShowUI: false` (clean gameplay rendering without editor widgets).

---

## 4. Current Status

* **Status**: `COMPLETED`
* **Evidence**: Over 15 active captures recorded, including `PIE_Live_Gameplay_Verified.png` and `TopDown_Campus_Corrected_UTM46N.png`.
* **Remaining Tasks**:
  - Automatically copy all programmatic viewport captures from `Scripts/capture_scene_views.py` directly into this folder during continuous integration.
