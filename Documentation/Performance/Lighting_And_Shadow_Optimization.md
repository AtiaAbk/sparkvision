# SparkVision — Lighting and Shadow Optimization Report
## Lumen Global Illumination, Virtual Shadow Maps, and Apple Silicon Tuning

---

## 1. Executive Summary

Lighting and shadows create the atmospheric, cinematic feel of SparkVision's Where Winds Meet-inspired visual direction. High-contrast tropical sunlight, deep shadows cast under Mughal-era chhatris, and ambient occlusion along colonnades are critical to the game's identity.

By optimizing the lighting pipeline for Apple Silicon:
- **Software Lumen** replaced Hardware Ray Tracing, utilizing Signed Distance Fields (SDF) and Screen-Space Tracing.
- **Virtual Shadow Maps (VSMs)** were retained for razor-sharp contact shadows, but memory was constrained using page caching and physical page limits.
- **WPO Shadow Cache Invalidation Protection**: Disabled per-frame invalidation on wind-animated foliage (`r.Shadow.Virtual.Cache.InvalidateOnWorldPositionOffset=0`).
- **Lumen Surface Cache Throttling**: Spread radiosity updates across frames (`r.LumenScene.Radiosity.UpdateFactor=0.25`) to eliminate GPU frame time spikes.

---

## 2. Lighting Architecture Details

### A. Software Lumen vs Hardware Ray Tracing

On Apple Silicon M4, hardware ray tracing triggers significant shader execution reordering and BVH building overhead. Software Lumen provides virtually indistinguishable global illumination by combining two complementary techniques:
1. **Screen Traces**: Screen-space depth buffer ray marching handles immediate contact shadows and near-field reflections.
2. **Mesh Distance Fields (SDF)**: Precomputed 3D signed distance fields represent the geometry of Curzon Hall and other campus buildings, allowing fast ray marching through empty space for medium-to-far field indirect bounce lighting.

```ini
; Config/DefaultEngine.ini
r.DynamicGlobalIlluminationMethod=1
r.ReflectionMethod=1
r.Lumen.HardwareRayTracing=False
r.Lumen.TraceMeshSDFs=1
r.GenerateMeshDistanceFields=True
r.DistanceFields.DefaultVoxelDensity=0.200000
```

### B. Virtual Shadow Map (VSM) Memory Tuning & Foliage WPO Protection

VSMs allocate pages on demand as geometry moves or changes. In large open-world maps with wind-animated foliage, WPO previously invalidated shadow pages every frame. Setting `InvalidateOnWorldPositionOffset=0` and clamping the physical page pool to 2,048 pages stabilized GPU frame times:

```ini
[SystemSettings]
r.Shadow.Virtual.ResolutionLodBiasDirectional=1
r.Shadow.Virtual.MaxPhysicalPages=2048
r.Shadow.Virtual.Clipmap.MinPageAddressBits=4
r.Shadow.Virtual.Cache.InvalidateOnWorldPositionOffset=0
r.Shadow.Virtual.Cache.WPOThreshold=2.0
r.Shadow.Virtual.Cache.DeformableMeshes=0
r.Shadow.RadiusThreshold=0.04
r.Shadow.Virtual.NormalBias=0.5
```

### C. Smooth Lumen Frame Pacing

```ini
[SystemSettings]
r.LumenScene.Radiosity.UpdateFactor=0.25
r.LumenScene.SurfaceCache.UpdateFactor=0.25
r.Lumen.ScreenProbeGather.DownsampleFactor=16
r.Lumen.ScreenProbeGather.TracingOctahedronResolution=8
r.Lumen.Reflections.DownsampleFactor=2
r.Lumen.Reflections.SmoothBias=0.10
```

---

## 3. Results & Visual Verification

- In `Visual_After/P01_Curzon_Hero.png`, the palm frond shadows cast sharply onto the reddish facade of the Curzon entrance arch with zero shadow flutter.
- Underneath the portico and recessed doorways, ambient occlusion provides natural soft shading without noise or temporal ghosting.
- In `Visual_After/P04_ThirdPerson_Gameplay.png`, the player pawn and stone portico steps cast clear contact shadows onto the limestone landing.
