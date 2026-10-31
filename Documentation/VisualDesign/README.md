# SPARKVISION — VISUAL DESIGN, ART DIRECTION & TECHNICAL ART SUITE

## 1. Purpose & Scope

This directory contains the visual design guidelines, art direction standards, physical material parameters, lighting configurations, and asset creation pipelines for **SparkVision: University of Dhaka** in **Unreal Engine 5.8**.

Our visual goal is to blend the historical integrity of Dhaka University's 1904 Indo-Saracenic and mid-century modernist architecture with the cinematic environmental quality, organic landscape composition, and atmospheric lighting of *Where Winds Meet* and *Ghost of Tsushima*.

---

## 2. Directory Index

* [`ArtDirection.md`](file:///Users/atiaoishi/Downloads/sparkvision/Documentation/VisualDesign/ArtDirection.md): Color palettes, atmospheric tone, architectural motifs, and cinematic framing principles.
* [`EnvironmentQualityChecklist.md`](file:///Users/atiaoishi/Downloads/sparkvision/Documentation/VisualDesign/EnvironmentQualityChecklist.md): 25-point visual and technical audit checklist applied to every landmark and zone.
* [`MaterialAndLightingGuide.md`](file:///Users/atiaoishi/Downloads/sparkvision/Documentation/VisualDesign/MaterialAndLightingGuide.md): Physically Based Rendering (PBR) values, master material hierarchy, and Lumen/lighting settings.
* [`AssetPipeline.md`](file:///Users/atiaoishi/Downloads/sparkvision/Documentation/VisualDesign/AssetPipeline.md): Blender 5.2.3 LTS modeling, unit scale standards (1m = 100uu), FBX export settings, and Unreal MCP import workflow.

---

## 3. High-Level Art Direction Summary

```text
Historical Ground Truth (DU Architecture) + Cinematic Presentation (WWM & GoT)
├── Palette: Terracotta Red-Brick (#8A2E20), White Sandstone Trim (#E8E0D2), Deep Lush Foliage (#28482A)
├── Lighting: Lumen Dynamic GI, Directional Sun (Golden Hour 3500K / Daylight 5600K), Exponential Fog
├── Materials: Fully Rough/Specular PBR calibrated; zero unphysical glowing or plastic sheens
└── Composition: 3-point depth layering (Foreground foliage/balustrade -> Midground playable road -> Background horizon)
```

---

## 4. Current Status

* **Status**: `COMPLETED`
* **Evidence**:
  - Curzon Hall PBR materials authored and assigned (`MI_Curzon_Brick`, `MI_Curzon_WhiteTrim`, etc.).
  - Daylight and Golden Hour lighting passes rendered and cataloged in `Documentation/Screenshots/`.
* **Remaining Tasks**:
  - Author weather variation profiles (Monsoon overcast, morning mist).
