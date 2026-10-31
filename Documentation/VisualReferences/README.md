# SPARKVISION — VISUAL REFERENCE LIBRARY & ARTISTIC BENCHMARKING GUIDE

## 1. Purpose & Scope

The **Visual Reference Library** establishes the artistic, historical, and architectural criteria for *SparkVision: University of Dhaka*. It provides environment artists, level designers, and technical artists with clear, authenticated visual baselines to ensure fidelity to the real University of Dhaka campus while achieving world-class cinematic quality.

---

## 2. Core Art Philosophy: Ground Truth vs. Presentation Inspiration

A strict separation governs the two categories of visual references used in SparkVision:

> [!IMPORTANT]
> **Real University of Dhaka photographs determine GEOGRAPHY and ARCHITECTURE.**
> We do not invent architectural styles, fantasy towers, or unhistorical geometry. Real photographic, archival, and cartographic evidence dictates building footprints, rooflines, brickwork, ornamentation, and compound layout.

> [!TIP]
> **Commercial game screenshots (*Where Winds Meet*, *Ghost of Tsushima*) provide VISUAL PRESENTATION INSPIRATION.**
> We reference these games solely for environment depth, atmospheric layering, natural lighting, organic foliage variation, wind dynamics, and third-person camera composition. Commercial fantasy architecture must **never** be copied into the University of Dhaka environment.

---

## 3. The 9-Step Visual Reference Workflow

All environment art and architectural assets must pass through this disciplined visual comparison pipeline:

1. **Add authentic University of Dhaka photographs** to the appropriate subfolder (`DU_Architecture/` or `DU_Environment/`).
2. **Add *Where Winds Meet* and *Ghost of Tsushima* screenshots** for atmospheric and lighting presentation references, strictly respecting fair-use and internal developmental guidelines.
3. **Record source, URL, and permission data** in [`ReferenceSources.md`](file:///Users/atiaoishi/Downloads/sparkvision/Documentation/VisualReferences/ReferenceSources.md).
4. **Keep current game screenshots separate** from external references inside [`CurrentGameScreenshots/`](file:///Users/atiaoishi/Downloads/sparkvision/Documentation/VisualReferences/CurrentGameScreenshots).
5. **Capture new in-engine screenshots from fixed, calibrated camera positions** (e.g., front facade, 45° angled aerial, third-person player eye level).
6. **Compare the actual running Unreal Engine game against appropriate reference photos and composition benchmarks**.
7. **Record identified visual gaps** (e.g., missing cornice trim, inaccurate arch cusping, insufficient tree canopy density, excessive ground flatness).
8. **Implement targeted corrections** in Blender, material instances, or level actor transforms and re-validate via Unreal MCP.
9. **Promote only verified, peer-reviewed screenshots** into [`ApprovedVisualBaselines/`](file:///Users/atiaoishi/Downloads/sparkvision/Documentation/VisualReferences/ApprovedVisualBaselines) as permanent regression baselines.

---

## 4. Subdirectory Structure

* [`DU_Architecture/`](file:///Users/atiaoishi/Downloads/sparkvision/Documentation/VisualReferences/DU_Architecture/README.md): Authentic photos of Curzon Hall, Shaheed Minar, TSC, Central Library, Aparajeyo Bangla, arches, columns, and chhatris.
* [`DU_Environment/`](file:///Users/atiaoishi/Downloads/sparkvision/Documentation/VisualReferences/DU_Environment/README.md): Authentic photos of campus roads, botanical gardens, heritage lamps, colonial benches, and courtyards.
* [`WhereWindsMeet/`](file:///Users/atiaoishi/Downloads/sparkvision/Documentation/VisualReferences/WhereWindsMeet/README.md): Presentation references for atmospheric depth, weather, lighting, and third-person exploration.
* [`GhostOfTsushima/`](file:///Users/atiaoishi/Downloads/sparkvision/Documentation/VisualReferences/GhostOfTsushima/README.md): Presentation references for landscape composition, dramatic golden-hour sunlight, and foreground/background framing.
* [`CurrentGameScreenshots/`](file:///Users/atiaoishi/Downloads/sparkvision/Documentation/VisualReferences/CurrentGameScreenshots/README.md): Real-time screenshots captured from the running Unreal Engine 5.8 editor.
* [`ApprovedVisualBaselines/`](file:///Users/atiaoishi/Downloads/sparkvision/Documentation/VisualReferences/ApprovedVisualBaselines/README.md): Locked visual baselines representing milestone-approved quality gates.

---

## 5. Current Status

* **Status**: `COMPLETED`
* **Evidence**: Repository structure established; workflow active across Phase 2 (Curzon Hall Hero) and Phase 3 (Full Campus).
* **Remaining Tasks**:
  - Ingest high-resolution archival photos from Dhaka University Library and National Archives.
  - Establish automated screenshot comparison scripts in `Testing/VisualRegressionTests.md`.
