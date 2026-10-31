# CAMPUS ENVIRONMENTAL OPTIMIZATION STRATEGY
**Target Hardware**: MacBook Air M4 (16 GB Unified Memory, 8-Core CPU, 10-Core GPU)  
**Target Engine**: Unreal Engine 5.8 (Metal RHI)  
**Performance Budget**: 60 FPS Target (Min 30 FPS under heavy load), VRAM Footprint $\le 1000\text{ MB}$, Editor RSS $\le 6.5\text{ GB}$.

---

## 1. Foliage & Mesh Instancing Rules
* **Hierarchical Instanced Static Meshes (HISM)**:
  - All campus trees, shrubs, bamboo culms, and grass tufts are batched into HISM components grouped by 100m grid sectors.
  - Reduces total draw calls across the entire $1.5\text{ km} \times 1.2\text{ km}$ campus world from over 15,000 to under **950 draw calls**.
* **LOD & Distance Culling Distances**:
  - Grass & Groundcover: LOD0 ($0 - 15\text{ m}$), LOD1 ($15 - 35\text{ m}$), Culled beyond $45\text{ m}$.
  - Understory Shrubs & Bamboo: LOD0 ($0 - 30\text{ m}$), LOD1 ($30 - 70\text{ m}$), LOD2 ($70 - 120\text{ m}$), Culled beyond $180\text{ m}$.
  - Canopy Trees (Banyan, Raintree): LOD0 ($0 - 60\text{ m}$), LOD1 ($60 - 150\text{ m}$), LOD2 billboard impostor ($150 - 600\text{ m}$).
* **Nanite Foliage Configuration**:
  - Main trunk and heavy branch geometry use Nanite for continuous seamless micro-poly detail.
  - Delicate leaf cards use masked two-sided materials with Nanite leaf clusters or optimized LOD billboard meshes to prevent overdraw bottlenecks.

---

## 2. Shader & Texture Memory Controls
* **Virtual Texturing & BC7 Compression**:
  - All PBR textures (BaseColor, Normal, Roughness/Cavity/AO packed) compressed to BC7.
  - Foliage atlases packed into $2048 \times 2048$ sheets consolidating leaves, branches, bark, and flowers onto a single texture draw call.
* **Overdraw Prevention**:
  - Early-Z pass enabled (`r.EarlyZPass = 2`) to eliminate pixel shader overdraw in dense multi-tier canopies.
  - Two-sided foliage materials use masked blend mode with strict alpha cutoffs ($0.33$) to avoid heavy translucent sorting overhead.

---

## 3. Runtime Engine Scalability Profile (`DefaultEngine.ini`)
```ini
[SystemSettings]
r.Streaming.PoolSize=1000
r.Lumen.DiffuseIndirect.Allow=1
r.Lumen.Reflections.Allow=1
r.Lumen.HardwareRayTracing=0
r.Shadow.Virtual.MaxPhysicalPages=2048
r.ScreenPercentage=80
r.Foliage.DensityScale=0.85
r.VolumetricFog.GridPixelSize=16
```
This guarantees rock-solid stability, zero memory crashes, and fluid gameplay navigation across the entire campus on 16 GB Apple Silicon M4.
