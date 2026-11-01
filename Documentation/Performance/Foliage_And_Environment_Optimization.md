# SparkVision — Foliage and Environment Optimization Report
## Campus Flora, Natural Proportions, and Eco-Zone Management

---

## 1. Executive Summary

A core visual pillar of the University of Dhaka campus is its lush tropical vegetation—including tall Royal Palms flanking Curzon Hall, the riparian ecology around the Curzon pond, shade-giving Banyan and Rain trees along The Mall and Fuller Road, and flowering shrubs at Hakim Chattar and TSC.

The optimization strategy **did not remove or thin out vegetation**. Instead, it focused on:
1. **Distance-Based Culling**: Setting small-foliage culling thresholds (`foliage.MinimumScreenSize=0.005`, `grass.CullDistanceScale=0.85`) while keeping large landmark canopy trees visible at infinite horizon.
2. **LOD Distance Scaling**: Applying `foliage.LODDistanceScale=1.15` to transition distant foliage to lighter LOD representations smoothly.
3. **Shadow Invalidation Protection**: Disabling per-frame VSM shadow invalidation on wind deformation (`r.Shadow.Virtual.Cache.InvalidateOnWorldPositionOffset=0`).

---

## 2. Key Ecological Zones Preserved

| Ecological Zone | Vegetation Types | Optimization Approach |
| :--- | :--- | :--- |
| **Curzon South Portico** | Royal Palms (*Roystonea regia*), manicured hedge borders | Static instances with cached VSM shadows; cast shadows onto portal facade preserved |
| **Curzon Pond Basin** | Weeping Willows, Blooming Pink Lagerstroemia, Reeds, Water Lilies | Clustered actors; reflections handled via Lumen screen-tracing rather than planar capture cameras |
| **The Mall & Kala Bhaban** | Large Banyan trees (*Ficus benghalensis*), Rain trees (*Albizia saman*) | High-altitude canopy meshes with simplified collision capsules |
| **Doyel Chattar & Shaheed Minar** | Shrub borders, perimeter trees, manicured grass | Standardized instanced static meshes with unified material instances |

---

## 3. Draw Call & Instance Management

- **Instanced Static Meshes (ISM)**: Replaced individual actor overhead with grouped instances for repeated props (hedges, lampposts, curb segments).
- **Collision Optimization**: Small decorative vegetation (reeds, lilies, lawn flowers) has collision disabled (`NoCollision`), removing unnecessary raycasts and physics broadphase overhead.
- **Canopy Distance Fields**: Foliage utilizes two-sided distance field generation for accurate ambient shadowing under dense tree canopies without requiring per-leaf ray tracing.

---

## 4. Verification

Render captures (`Visual_After/P01_Curzon_Hero.png` and `Visual_After/P02_Living_Campus_Greenery.png`) prove that tree density, palm heights, pond foliage, and ground greenery remain visually identical to previous environmental milestones.
