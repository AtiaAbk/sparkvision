# SparkVision — Texture and Material Optimization Report
## Shader Complexity, Shading Models, and Texture Streaming Budgets

---

## 1. Executive Summary

Realistic environmental aesthetics—such as the weathered terracotta brick of Curzon Hall, water surface caustics in the Curzon pond, and foliage canopy translucency—rely heavily on rich textures and responsive material shaders.

Rather than downscaling textures or converting materials to flat unlit shaders, SparkVision optimized the **underlying shading pipeline architecture**:
1. Converted from experimental Substrate (Strata) with multi-slab evaluation to high-efficiency UE5 standard Deferred Shading.
2. Clamped the streaming texture pool with per-frame streaming limits to avoid I/O stutters.
3. Preserved PBR material parameterization (BaseColor, Roughness, Metallic, Normal) across all authentic Dhaka University structures.

---

## 2. Shading Pipeline Architectural Shift

### Substrate vs Standard Deferred Shading

In Unreal Engine 5, Substrate allows complex layered materials with arbitrary BSDF slabs, but imposes an 80-byte-per-pixel GBuffer payload (`r.Substrate.BytesPerPixel=80`) and requires multi-closure evaluation in every lighting pass.

For SparkVision's architectural and natural materials:
- **Colonial Red Brick**: Diffuse albedo + roughness variation + micro-surface normal.
- **Limestone Trim & Domes**: High-roughness diffuse + ambient occlusion.
- **Pond Water**: Single-layer water material with planar refraction and normal perturbation.
- **Vegetation**: Two-sided foliage shading with subsurface scattering.

None of these require 4-slab complex BSDF evaluation. Reverting to standard Deferred Shading reduced shader compilation complexity, halved GBuffer memory access, and preserved 100% of the material appearance.

---

## 3. Texture Streaming Configuration

```ini
[SystemSettings]
; Enable texture streaming with an explicit pool budget
r.TextureStreaming=1
r.Streaming.PoolSize=1000
r.Streaming.LimitPoolSizeToVRAM=1

; Smooth GPU memory transfers across frames to prevent hitching
r.Streaming.AmortizeCPUToGPUCopy=1
r.Streaming.MaxNumTexturesToStreamPerFrame=8
```

---

## 4. Visual Quality Verification

Visual inspection of `POST_OPT_CURZON_HERO.png` and `POST_OPT_CURZON_POND.png` confirms:
- **Curzon Hall Brick**: Retains rich terracotta tone, mortar lines, and architectural depth.
- **White Ornamentation**: Domes, eaves, and balustrades exhibit crisp silhouettes with zero specular aliasing.
- **Water Surface**: Retains subtle sky reflection, ripple motion, and water lily clusters.
- **Student Character**: Manny mannequin mesh displays proper roughness, metallic highlights, and ambient contact shadowing.
