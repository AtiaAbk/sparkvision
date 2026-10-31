# CAMPUS CANOPY LAYERING & FOREST FLOOR DYNAMICS
**Project**: SparkVision — Level 1 University of Dhaka Digital Twin  
**Aesthetic Benchmark**: *Where Winds Meet* Depth & Environmental Storytelling  
**Scope**: Vertical Ecological Strata, Sunlight Filtration, Root Systems & Soil Mechanics.

---

## 1. The Four-Tier Canopy Architecture

```
[Tier 1: Emergent Upper Canopy (25m - 35m)]   === Raintree (Albizia) & Banyan (Ficus) ===
                        \                   /
[Tier 2: Intermediate Sub-Canopy (10m - 18m)] === Krishnachura, Radhachura, Jarul, Neem ===
                        \                   /
[Tier 3: Shrub & Bamboo Understory (2m - 8m)] === Bengal Bamboo, Ferns, Bougainvillea ===
                        \                   /
[Tier 4: Forest Floor & Groundcover (0m - 1m)]=== Turf, Moss, Leaf Detritus, Exposed Roots ===
```

### Tier 1: Emergent Upper Canopy ($25\text{ m} - 35\text{ m}$)
* Dominated by massive century-old Raintrees and expansive Banyans.
* Creates the grand overhead ceiling that filters harsh tropical sunlight into soft, cinematic, dappled lighting pools.
* Hosts high-canopy wildlife (crows, bats at twilight).

### Tier 2: Intermediate Sub-Canopy ($10\text{ m} - 18\text{ m}$)
* Dominated by flowering ornamental and fruit trees: flaming red Krishnachura, golden Radhachura, lilac Jarul, and fragrant Mango trees.
* Provides midground visual interest and bursts of vibrant color that break the monotony of green and grey.

### Tier 3: Shrub & Bamboo Understory ($2\text{ m} - 8\text{ m}$)
* Dense bamboo thickets, flowering bougainvillea hedges, and wild lime shrubs.
* Directs player pathfinding, blocks distant sightlines to create a sense of mystery and discovery, and frames architectural views.

### Tier 4: Forest Floor & Groundcover ($0\text{ m} - 1\text{ m}$)
* Gnarled buttress roots breaking through red brick walkways.
* Thick carpets of fallen leaves, dead twigs, and dropped seed pods.
* Dark rich alluvium soil with patchworks of green moss, maidenhair ferns, and wild clover.

---

## 2. Dynamic Lighting & Volumetric God-Rays
* **Unreal Engine 5.8 Lumen & Volumetric Fog Calibration**:
  - `VolumetricFog = 1` with `FogDensity = 0.015` and `ScatteringDistribution = 0.65`.
  - When the directional sun penetrates the upper Raintree canopy along Fuller Road, high-contrast volumetric light shafts (god-rays) slice through the humid air.
  - As the player walks through these sun shafts, dynamic light patterns dance across the player character's shoulders and weapon/satchel assets.
