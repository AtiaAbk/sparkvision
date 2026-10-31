# CAMPUS LIVING WORLD DEFECT CORRECTION LOG
**Project**: SparkVision — Level 1 University of Dhaka Digital Twin  
**Tracking Cycle**: Phase 1 Blockout $\rightarrow$ Phase 2 Foliage Audit $\rightarrow$ Phase 3 Living Ecology Reconstruction $\rightarrow$ Final Polish.

---

## 1. Defect Tracking Matrix

| Defect ID | Severity | Subsystem / Component | Defect Description (Legacy Implementation) | Root Cause Analysis | Corrective Action & Verification | Status |
|---|---|---|---|---|---|---|
| **DEF-ENV-001** | CRITICAL | Ecology / Foliage | Large open zones across campus were empty, flat, and devoid of vegetation, resembling a sterile blockout. | Early layout focused exclusively on landmark building placement. | Implemented multi-tier ecological planting plan adding 350+ instanced trees, bamboo groves, and groundcover. | **CLOSED** |
| **DEF-ENV-002** | HIGH | Art Direction | Existing trees were generic uniform green spheres with no resemblance to Bengal delta flora. | Placeholder low-poly assets used during phase 1. | Procedurally modeled 8 bespoke Bangladeshi tree species in Blender (Banyan, Raintree, Krishnachura, Jarul, Neem, Palms, Bamboo). | **CLOSED** |
| **DEF-ENV-003** | HIGH | Water / Ponds | Curzon Pond and Shahidullah Lake were flat opaque blue planes with hard 90° edge clipping against terrain. | Placeholder water volume with untextured default material. | Developed translucent depth-absorbing water shader (`M_Water_CurzonPond`), floating water lilies (*Shapla*), and brick ghats. | **CLOSED** |
| **DEF-ENV-004** | HIGH | Dynamics / Wind | Foliage was completely static with zero wind motion, making the world feel frozen and artificial. | Lack of vertex-offset wind logic in foliage shaders. | Integrated 3-tier hierarchical wind shader (trunk sway, branch swing, leaf flutter) inspired by *Ghost of Tsushima*. | **CLOSED** |
| **DEF-ENV-005** | MEDIUM | Ground / Detail | Ground plane under trees was bare green grass with no fallen leaves, exposed roots, or understory shrubs. | Missing micro-layering decals and undergrowth. | Created gnarled buttress root geometry, fallen Krishnachura petal decals, raintree leaf detritus, and wild fern clusters. | **CLOSED** |
| **DEF-ENV-006** | MEDIUM | Traversal / Collision | Players collided with leaf cards and low branches, causing jarring movement stops. | Foliage collision presets incorrectly set to `BlockAll`. | Changed leaf and branch collision to `NoCollision`; reserved `BlockAll` strictly for main structural trunks. Traversal 100% smooth. | **CLOSED** |
| **DEF-ENV-007** | MEDIUM | Performance | Dense tree scattering caused draw calls to spike to over 6,500 on preliminary test. | Individual StaticMeshActors used instead of instancing. | Converted all tree and plant distributions to Hierarchical Instanced Static Meshes (HISM). Draw calls reduced to $< 950$. | **CLOSED** |
| **DEF-ENV-008** | LOW | Atmosphere / Lighting | Midday lighting was flat white with no atmospheric scattering or sense of tropical Bengal humidity. | Directional light intensity and fog parameters uncalibrated. | Tuned "Golden Afternoon" profile with warm $45,000\text{ Lux}$ sunlight, subtle volumetric fog shafts, and ACES color grading. | **CLOSED** |

---

## 2. Verification Sign-Off
All 8 identified environmental defects have been systematically remediated and verified through in-editor simulation, automated ray-trace collision testing, and camera capture inspections across the entire University of Dhaka world.
