# SPARKVISION — VEGETATION DENSITY & CANOPY MAP
## Controlled Density Strategy, Species Spacing & Traversal Clearance Envelopes

---

### Executive Mandate: Overriding Excessive Density

To fulfill the **Open Campus & Natural Density Override**, SparkVision strictly rejects packing the level with dense vegetation. The target density is **low-to-moderate**, strategically distributed to enhance architectural visibility, maintain spacious open lawns, and preserve clear player sightlines.

---

### 1. Species Spacing Matrix (Minimum Clearance Between Trunks)

Different species exhibit radically different canopy spreads and root architectures. A single universal spacing distance leads to either overlapping crowns or unnatural sparse grids.

| Species Category | Example Species | Mature Canopy Diameter | Minimum Trunk-to-Trunk Spacing | Minimum Distance to Building Wall | Minimum Distance to Road Kerb |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Monumental Banyan** | *Ficus benghalensis* | $25.0 - 40.0\text{ m}$ | **$35.0\text{ m}$** | **$20.0\text{ m}$** | **$8.0\text{ m}$** |
| **Large Avenue Canopy** | *Albizia saman*, *Swietenia mahagoni* | $18.0 - 26.0\text{ m}$ | **$22.0\text{ m}$** | **$14.0\text{ m}$** | **$4.5\text{ m}$** |
| **Medium Flowering Shade** | *Delonix regia*, *Peltophorum pterocarpum* | $11.0 - 15.0\text{ m}$ | **$15.0\text{ m}$** | **$8.0\text{ m}$** | **$4.0\text{ m}$** |
| **Moist Woodland / Riparian** | *Lagerstroemia speciosa*, *Neolamarckia cadamba* | $8.0 - 12.0\text{ m}$ | **$12.0\text{ m}$** | **$7.0\text{ m}$** | **$3.5\text{ m}$** |
| **Light Airy Shade** | *Azadirachta indica*, *Polyalthia longifolia* | $6.0 - 9.0\text{ m}$ | **$8.0\text{ m}$** | **$5.0\text{ m}$** | **$3.0\text{ m}$** |
| **Columnar / Vertical Palms** | *Roystonea regia*, *Areca catechu* | $4.0 - 6.5\text{ m}$ | **$6.0\text{ m}$** | **$3.5\text{ m}$** | **$2.5\text{ m}$** |
| **Clumping Bamboo Clusters** | *Bambusa tulda* | $3.5 - 5.0\text{ m}$ | **$7.0\text{ m}$** | **$6.0\text{ m}$** | **$4.0\text{ m}$** |
| **Manicured Hedges** | *Duranta repens* | $0.7 - 0.9\text{ m}$ | Continuous linear | **$0.3\text{ m}$** (along plinth) | **$1.0\text{ m}$** |

---

### 2. Sector Tree Count Targets & Density Budget

The campus environment is budgeted to ensure high visual quality and 60 FPS performance on Apple Silicon M4:

```
+----------------------------------------------------------------------------------------------------+
| SECTOR 1: CURZON & SCIENCE PRECINCT                                                                |
| - Palms: 2 Royal Palms (Front Hero) + 4 Coconut Palms (Pond)                                       |
| - Mature Canopy Trees: 8 Raintrees (Perimeter) + 2 Banyan (Northwest boundary)                     |
| - Flowering Trees: 8 Krishnachura + 4 Radhachura + 6 Jarul (Pond)                                  |
| - Hedges: 4 Low Manicured Boxwood segments along plinth                                            |
| - Water Edge: 6 Kashful reed clumps + 12 Shapla lily pads                                          |
| -> Total Large Trees: 28 | Open Lawn Area: 54%                                                     |
+----------------------------------------------------------------------------------------------------+
| SECTOR 2: DOYEL CHATTAR & UNIVERSITY AVENUE                                                        |
| - Avenue Trees: 14 Raintrees + 8 Krishnachura (Lined along boulevard)                              |
| - Roundabout Greenery: 4 Radhachura + Low hedge ring                                               |
| -> Total Large Trees: 26 | Traversal Sightline: 100% Clear                                         |
+----------------------------------------------------------------------------------------------------+
| SECTOR 3: FULLER ROAD & MEMORIAL PRECINCT                                                          |
| - Fuller Road Tree Tunnel: 16 Mahoganies + 8 Raintrees                                             |
| - Shaheed Minar Perimeter: 4 Sacred Peepal + 2 Banyan (Set back >18m)                              |
| - SM & Shahidullah Quads: 8 Fruit/Shade Trees                                                      |
| -> Total Large Trees: 38 | Plaza Visibility: 100% Unobstructed                                     |
+----------------------------------------------------------------------------------------------------+
| SECTOR 4: TSC & CENTRAL LIBRARY                                                                    |
| - Raju Sculpture Plaza: 6 Setback Shade Trees                                                      |
| - Library Pilotis & Hakim Chattar: 10 Neem + 4 Debdaru                                             |
| - Central Mosque & Nazrul Tomb: 6 Betel Nut Palms + 2 Frangipani                                   |
| -> Total Large Trees: 28 | Architectural Visibility: 100% Open                                     |
+----------------------------------------------------------------------------------------------------+
| SECTOR 5: KALA BHABAN & THE MALL                                                                   |
| - Arts Faculty Frontage: 6 Krishnachura + 4 Sonalu (Framing Aparajeyo)                            |
| - The Mall Open Lawn: 2 Massive Ancient Specimen Banyans                                           |
| -> Total Large Trees: 12 | Open Lawn Area: 60%                                                     |
+----------------------------------------------------------------------------------------------------+
```

* **Grand Total Campus Large Trees**: **~132 carefully positioned specimen trees**.
* **Zero Jungle Overgrowth**: Replaces uncalibrated random clutter with deliberate, picturesque, botanically authentic placements.

---

### 3. Vertical & Horizontal Clearance Envelopes

To prevent any possibility of clipping or traversal obstruction:

```
                  [Tree Canopy: Minimum 4.5m Clear Overhead]
                             , - ~ ~ ~ - ,
                         , '               ' ,
                       ,                       ,
                      ,                         ,
                     ,                           ,
                     ,                           ,
                      ,                         ,
                       ,                       ,
                         ,                  , '
                   -----------' - ~ ~ ~ - '-----------
                        |     |  |       |
                        |     |  |       |
                        |     |  |       |
         <-- 12m min -->|     |  | Trunk |<-- 4.5m min --> [Road Edge]
       [Building Wall]  |     |  |       |
  ======================================================================== [Ground Level]
```

1. **Building Clearance**:
   * Minimum **12.0 meters** horizontal distance between any tree trunk and any historic building facade (Curzon Hall, Central Library, Kala Bhaban, SM Hall).
   * Ensures that no branches, leaves, or roots penetrate brickwork, windows, or veranda corridors.
2. **Roadway & Path Clearance**:
   * Minimum **4.5 meters** horizontal distance between trunk base and road kerb edge.
   * Lower foliage pruned to at least **4.5 meters** ($450\text{ cm}$) above ground, ensuring double-decker bus, car, and player clearance.
3. **Plinth & Stair Clearance**:
   * Zero trees planted on raised pedestrian stone plinths or within 8 meters of public entrance staircases.
