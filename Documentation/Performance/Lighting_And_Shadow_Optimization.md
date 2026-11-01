# SparkVision — Lighting and Shadow Optimization Report
## Lumen Global Illumination, Virtual Shadow Maps, and Apple Silicon Tuning

---

## 1. Executive Summary

Lighting and shadows create the atmospheric, cinematic feel of SparkVision's Where Winds Meet-inspired visual direction. High-contrast tropical sunlight, deep shadows cast under Mughal-era chhatris, and ambient occlusion along colonnades are critical to the game's identity.

By optimizing the lighting pipeline for Apple Silicon:
- **Software Lumen** replaced Hardware Ray Tracing, utilizing Signed Distance Fields (SDF) and Screen-Space Tracing.
- **Virtual Shadow Maps (VSMs)** were retained for razor-sharp contact shadows, but memory was constrained using page caching and physical page limits.
- **Directional Light Cascades**: Enabled CSM caching so that non-moving campus architecture does not trigger shadow map redraws.

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

### B. Virtual Shadow Map (VSM) Memory Tuning

VSMs allocate pages on demand as geometry moves or changes. In large open-world maps, this can lead to memory fragmentation. By clamping the physical page pool to 2,048 pages and setting a resolution LOD bias of 1 for the directional sun light, VSM memory footprint was halved without softening critical contact shadows:

```ini
[SystemSettings]
r.Shadow.Virtual.ResolutionLodBiasDirectional=1
r.Shadow.Virtual.MaxPhysicalPages=2048
r.Shadow.Virtual.Clipmap.MinPageAddressBits=4
r.Shadow.CSMCaching=1
```

---

## 3. Results & Visual Verification

- In `POST_OPT_CURZON_HERO.png`, the palm frond shadows cast sharply onto the reddish facade of the Curzon entrance arch.
- Underneath the portico and recessed doorways, ambient occlusion provides natural soft shading without noise or temporal ghosting.
- In `POST_OPT_GAMEPLAY_TRAVERSAL.png`, the student NPC and Archive Terminal cast clear contact shadows onto the limestone steps.
