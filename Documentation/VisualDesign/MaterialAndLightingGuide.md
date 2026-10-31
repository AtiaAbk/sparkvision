# SPARKVISION — MATERIAL & LIGHTING IMPLEMENTATION GUIDE

## 1. Title & Executive Purpose

* **Document**: `MaterialAndLightingGuide.md`
* **Purpose**: Details the PBR material hierarchy, master shader networks, Lumen dynamic global illumination parameters, and sun/atmosphere lighting configurations in **Unreal Engine 5.8**.

---

## 2. Master Material Hierarchy

All environment surfaces derive from unified master materials located in `/Game/SparkVision/Materials/`:

```text
M_Master_Opaque (Master PBR Shader)
├── MI_Curzon_Brick             [BaseColor: (0.24, 0.03, 0.02), Roughness: 0.85]
├── MI_Curzon_Brick_Aged        [BaseColor: (0.14, 0.02, 0.01), Roughness: 0.90]
├── MI_Curzon_WhiteTrim         [BaseColor: (0.78, 0.73, 0.61), Roughness: 0.70]
├── MI_Curzon_Wood              [BaseColor: (0.05, 0.02, 0.01), Roughness: 0.65]
├── MI_Curzon_Iron              [BaseColor: (0.01, 0.01, 0.01), Roughness: 0.40, Metallic: 0.85]
├── MI_Campus_Asphalt           [BaseColor: (0.04, 0.04, 0.04), Roughness: 0.88]
└── MI_Campus_LawnGrass         [BaseColor: (0.03, 0.08, 0.03), Roughness: 0.60]

M_Master_Foliage (Subsurface Two-Sided)
└── MI_Tree_Leaves              [BaseColor: (0.02, 0.07, 0.02), SubsurfaceColor: (0.10, 0.25, 0.05)]
```

---

## 3. Lighting Configurations (Daylight & Golden Hour)

Lighting actors are organized inside the `Lighting_Environment` folder in World Outliner:

### 3.1 Daylight Configuration (Clear Afternoon)
* **Directional Light**:
  - Intensity: $75,000\text{ lux}$
  - Light Color: Pure White (`5800 K`)
  - Sun Pitch: $-42.0^\circ$, Sun Yaw: $145.0^\circ$
* **Sky Light**: Real-time Capture enabled, Intensity: $1.0$
* **Exponential Height Fog**: Fog Density = $0.002$, Volumetric Fog enabled with Scattering Distribution = $0.25$

### 3.2 Golden Hour Configuration (Cinematic Benchmark)
* **Directional Light**:
  - Intensity: $45,000\text{ lux}$
  - Light Color: Warm Amber (`3600 K`)
  - Sun Pitch: $-18.0^\circ$, Sun Yaw: $215.0^\circ$
* **PostProcess Volume**:
  - Bloom: Method = Convolution, Intensity = $0.65$
  - White Balance: Temp = $6200\text{ K}$, Tint = $-0.05$
  - Exposure: Min EV100 = $7.0$, Max EV100 = $13.0$

---

## 4. Current Status

* **Status**: `COMPLETED`
* **Evidence**:
  - Verified across multiple captures: `Phase2_Curzon_FrontFacade_Daylight.png` vs. `Phase2_Curzon_FrontFacade_GoldenHour.png`.
* **Remaining Tasks**:
  - Add night illumination profile with volumetric street lamp glows.
