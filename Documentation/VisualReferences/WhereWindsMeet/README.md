# WHERE WINDS MEET — VISUAL PRESENTATION & ATMOSPHERIC BENCHMARKS

## 1. Purpose & Scope

This directory contains visual presentation benchmarks derived from *Where Winds Meet* (Everstone Studio). These references serve exclusively to guide the **cinematic rendering quality, environmental composition, atmospheric depth, and exploration feel** in Unreal Engine 5.8.

> [!WARNING]
> **CRITICAL ART DIRECTION BOUNDARY**:
> These references are used **ONLY** for environmental rendering technique, atmospheric depth, foliage shading, and camera presentation. **Do not copy Chinese fantasy architecture, oriental pagodas, or mythological props into the University of Dhaka environment.** The architecture of SparkVision remains 100% historically and geographically authentic to Bangladesh and Dhaka University.

---

## 2. Targeted Presentation Elements

### 2.1 Atmospheric Depth & Volumetric Lighting
* **Multi-Layered Aerial Perspective**: Using Unreal Engine 5.8 Exponential Height Fog and Local Volumetric Fog to establish clear distance separation between foreground landmarks (Curzon Hall), mid-ground roads (Doyel Chattar), and distant academic wings.
* **Sunbeam & God-Ray Dispersion**: Subtle volumetric light scattering filtering through dense tree branches onto paved exploration pathways.

### 2.2 Vegetation Density, Wind & Natural Interaction
* **Foliage Shading Quality**: Two-sided transmission materials that allow sunlight to illuminate leaves from behind, preventing foliage from appearing like flat plastic cards.
* **Organic Ground Scatter**: Natural blending between lawns, wild grass tufts, fallen leaves, and paved road edges.

### 2.3 Environmental Scene Composition
* **Scenic Exploration Vistas**: Framing paths and gateways so that landmarks peek through arches, foliage, or road bends, guiding the player forward naturally without artificial UI compass clutter.

### 2.4 Third-Person Exploration Framing
* **Camera Distance & FOV**: Framing third-person exploration with an intimate yet expansive camera distance, allowing the player character to ground the scale against monumental historical architecture.

---

## 3. Current Status

* **Status**: `IN PROGRESS`
* **Evidence**: Volumetric fog and directional sun lighting active in `LV_Campus_Blockout`; verified via `Phase2_Curzon_CinematicAngled_Daylight.png`.
* **Remaining Tasks**:
  - Implement dynamic wind flutter vertex shader on tree leaf clusters (`SM_Campus_Tree_Hero`).
  - Fine-tune distance fog falloff across the 1.5 km expanse from Curzon Hall to TSC.
