# WHERE WINDS MEET ENVIRONMENTAL BENCHMARK STUDY
**Benchmark Title**: *Where Winds Meet* (Everstone Studio / NetEase)  
**Application Target**: SparkVision — Level 1 University of Dhaka Open-World Environment  
**Comparative Objectives**: Density, Multi-Tier Canopy, Wind Interaction, Micro-Ecology, Visual Depth.

---

## 1. Aesthetic Pillars of *Where Winds Meet*
*Where Winds Meet* achieves exceptional open-world environmental presence not through raw geometric polygon count alone, but through five core technical and artistic principles:

1. **Environmental Layering & Spatial Depth**:
   - The world is never a flat ground plane with scattered tree trunks. It is composed of distinct vertical strata:
     - *Canopy Layer* ($15\text{ m} - 35\text{ m}$): Massive overlapping crowns creating cathedral-like dappled light and volumetric god-rays.
     - *Understory / Sub-Canopy* ($5\text{ m} - 12\text{ m}$): Slender saplings, flowering fruit trees (Krishnachura/Jarul), and arching bamboo clusters.
     - *Shrub & Undergrowth* ($1\text{ m} - 3\text{ m}$): Dense ferns, elephant grass, wild ginger, and blooming shrubs that break player sightlines.
     - *Herbaceous Groundcover* ($0.1\text{ m} - 0.8\text{ m}$): Thick clumpy turf grasses, mosses, creeping vines, and fallen leaf carpets.
2. **Dynamic Wind Responsiveness**:
   - Wind is a living character in the scene. Foliage does not vibrate uniformly; it exhibits hierarchical frequency responses:
     - Trunk & Major Limbs: Low frequency, high inertia sway.
     - Secondary Branches: Medium frequency oscillation.
     - Leaf Clusters & Petals: High frequency flutter with micro-turbulence.
   - Wind gusts generate swirling vortices of loose leaves and petals across paved paths.
3. **Atmospheric Density & Volumetric Light**:
   - Subtle localized height fog, morning moisture haze near water bodies, and dynamic Mie scattering that separates foreground assets from midground landmarks.
4. **Organic Transition Zones**:
   - Nature is never abruptly clipped against stone walls. Foundations feature moss creep, roots breaking through brick pavers, and weeds sprouting in mortar joints.
5. **Ecological Purpose & Believability**:
   - Every vegetation cluster tells a story of moisture, sunlight, soil nutrients, and human cultivation.

---

## 2. Translation Matrix: From Ancient Wuxia to Modern Academic Bengal

| *Where Winds Meet* Benchmark Feature | Dhaka University Equivalent in SparkVision | Implementation Strategy |
|---|---|---|
| **Towering Ancient Pine / Ginkgo Forests** | Ancient Banyan (*Bat Brikkho*) & Massive Raintrees | Sculpted wide-spreading trunks with hanging prop roots and umbrella canopies over Fuller Road and Mall. |
| **Golden & Green Bamboo Groves** | Bengal Bamboo (*Bambusa vulgaris*) Thickets | Dense clumped culm clusters along the Curzon Pond perimeter and Science Library garden buffer. |
| **Wild Mountain Grasslands & Reeds** | Deltaic Reeds, Kashful (*Saccharum spontaneum*), and Dense Bermuda Turf | Multi-height procedural grass blades with vertex-color wind displacement. |
| **Falling Blossom Petals (Peach / Cherry)** | Scarlet Krishnachura (*Delonix regia*) & Lilac Jarul Blooms | GPU particle emitters spawning drift petals across the Curzon fountain plaza and Arts Building promenade. |
| **Wetland Water Margins & Lily Ponds** | Curzon Botanical Pond & Shahidullah Pond Margins | Water surface with translucent shader, subsurface scattering, floating Nymphaea lily pads, and muddy bank transitions. |
| **Wind Audio & Foliage Rustle** | Dual-layer localized wind sound cues modulated by player speed and camera occlusion | FMOD / Unreal Audio attenuation volumes around tree crowns. |
