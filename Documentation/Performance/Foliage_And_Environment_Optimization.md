# SparkVision — Foliage and Environment Optimization Report
## Campus Flora, Natural Proportions, and Eco-Zone Management

---

## 1. Executive Summary

A core visual pillar of the University of Dhaka campus is its lush tropical vegetation—including tall Royal Palms flanking Curzon Hall, the riparian ecology around the Curzon pond, shade-giving Banyan and Rain trees along The Mall and Fuller Road, and flowering shrubs at Hakim Chattar and TSC.

The optimization strategy **did not remove or thin out vegetation**. Instead, it focused on:
1. **Hierarchical Instancing**: Utilizing Nanite static mesh representation where supported and instanced static mesh components.
2. **Culling Distance Calibration**: Setting aggressive small-foliage culling thresholds (`r.WireframeCullThreshold=5.0`) while keeping large landmark canopy trees visible at infinite horizon.
3. **Shadow Optimization**: Using Virtual Shadow Maps with page caching so static foliage does not force per-frame shadow map redrawing.

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

Render captures (`POST_OPT_CURZON_HERO.png` and `POST_OPT_CURZON_POND.png`) prove that tree density, palm heights, pond foliage, and ground greenery remain visually identical to previous environmental milestones (`e86f6f0`).
