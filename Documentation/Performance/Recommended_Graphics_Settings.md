# SparkVision — Recommended Graphics Settings
## Multi-Tier Hardware Presets for Apple Silicon M4 and Workstations

---

## 1. Overview of Built-In Scalability Presets

SparkVision includes three finely tuned scalability profiles in `Config/DefaultScalability.ini`:

| Preset Tier | Profile Key | Target Framerate | Hardware Recommendation | Key Visual Characteristics |
| :--- | :--- | :--- | :--- | :--- |
| **Optimized** | `@1` (Balanced) | **60 FPS** | MacBook Air M4 (Battery / Cool Mode) | Software Lumen, 1,536 VSM pages, 60% foliage density, 250 MB RenderTarget pool |
| **High Quality** | `@2` (Default) | **45 – 60 FPS** | MacBook Air M4 (AC Power Connected) | Full Software Lumen, 2,048 VSM pages, 75% foliage density, 300 MB RenderTarget pool |
| **Cinematic** | `@3` (Fidelity) | **30 FPS / Screenshots** | M4 Pro / Max or Desktop Workstations | High-resolution Lumen, 3,072 VSM pages, 100% foliage density, 400 MB RenderTarget pool |

---

## 2. Default Configuration (`Config/DefaultEngine.ini`)

By default, the project runs on **High Quality (`@2`)** with:

```ini
[SystemSettings]
; 1. Texture Streaming & Memory Pool Clamping
r.TextureStreaming=1
r.Streaming.PoolSize=1000
r.Streaming.LimitPoolSizeToVRAM=1

; 2. Lumen Software Ray Tracing
r.Lumen.HardwareRayTracing=0
r.Lumen.TraceMeshSDFs=1

; 3. Virtual Shadow Map Memory Optimization
r.Shadow.Virtual.ResolutionLodBiasDirectional=1
r.Shadow.Virtual.MaxPhysicalPages=2048
r.Shadow.Virtual.Clipmap.MinPageAddressBits=4
r.Shadow.Virtual.Cache.InvalidateOnWorldPositionOffset=0
r.Shadow.Virtual.Cache.WPOThreshold=2.0

; 4. Dynamic Super Resolution & Temporal Antialiasing
r.TemporalAA.Upsampling=1
r.ScreenPercentage=80
r.TSR.History.ScreenPercentage=100

; 5. Lumen Frame Pacing & Surface Cache Throttling
r.LumenScene.Radiosity.UpdateFactor=0.25
r.LumenScene.SurfaceCache.UpdateFactor=0.25

; 6. Foliage & Undergrowth Distance Culling
foliage.MinimumScreenSize=0.005
foliage.LODDistanceScale=1.15
grass.CullDistanceScale=0.85
```

---

## 3. Switching Presets In-Game

To switch presets at runtime via the in-game developer console or UI:

- **Optimized (60 FPS Target)**:
  `sg.ViewDistanceQuality 1` | `sg.ShadowQuality 1` | `sg.PostProcessQuality 1` | `sg.TextureQuality 1` | `sg.EffectsQuality 1` | `sg.FoliageQuality 1` | `sg.ShadingQuality 1`
- **High Quality (Default)**:
  `sg.ViewDistanceQuality 2` | `sg.ShadowQuality 2` | `sg.PostProcessQuality 2` | `sg.TextureQuality 2` | `sg.EffectsQuality 2` | `sg.FoliageQuality 2` | `sg.ShadingQuality 2`
- **Cinematic (Screenshot Mode)**:
  `sg.ViewDistanceQuality 3` | `sg.ShadowQuality 3` | `sg.PostProcessQuality 3` | `sg.TextureQuality 3` | `sg.EffectsQuality 3` | `sg.FoliageQuality 3` | `sg.ShadingQuality 3`
