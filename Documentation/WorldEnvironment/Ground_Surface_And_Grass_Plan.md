# SPARKVISION — GROUND SURFACE & GRASS PLAN
## Multi-Layered Tropical Ground Conditions, Turf Typologies & Edge Transitions

---

### Executive Mandate: Overriding the Monolithic Flat Ground

A major historical defect of early game prototypes was the entire campus terrain appearing as a single flat, uniform, artificial green plane. Under the **Open Campus & Natural Density Override**, the ground surface must reflect real tropical Dhaka ground conditions during the July monsoon season: varied moisture levels, maintained lawns, compacted earth paths, tree-pit loam, and soft organic transitions.

---

### 1. Master Ground Surface Typologies

| Ground Category | Texture & PBR Character | Typical Locations | Surface Color & Albedo | Roughness |
| :--- | :--- | :--- | :--- | :---: |
| **A. Maintained Short Lawn** | Fine, uniform Bermuda grass (*Cynodon dactylon*), trimmed to $3 - 5\text{ cm}$. Zero tall weeds. | Curzon Front Lawn, SM Hall Quad, The Mall central strip | Emerald green (`#3B6E22`) | 0.65 |
| **B. Natural Medium Turf** | Mixed tropical carpet grass (*Axonopus compressus*), natural height $8 - 14\text{ cm}$. | Roadside verges, tree under-canopies, perimeter fences | Olive-forest green (`#2F5A1E`) | 0.70 |
| **C. Tall Wild Reeds (Kashful)** | Slender upright stems ($1.2 - 1.8\text{ m}$) with silvery-white feathery plumes. | Curzon Botanical Pond unpaved banks, marshy ditches | Sage-olive green (`#4A6B38`) | 0.60 |
| **D. Shaded Tree-Base Loam** | Moist, rich dark deltaic loam with exposed fine roots and organic humus. | Directly beneath mature Rain Trees, Banyans, and Mahoganies | Dark charcoal-brown (`#2A1D14`) | 0.85 |
| **E. Compacted Footpath Dirt** | Firm, hard-packed earth created by pedestrian foot traffic over grass. | Diagonal desire paths across lawns, tea stall approaches | Warm buff-tan (`#5A4532`) | 0.75 |
| **F. Monsoon Puddle Silt** | Reflective wet mud with shallow standing water puddles. | Low drainage spots along roadside verges after rain | Muddy dark umber (`#1F1610`) | 0.15 (Wet) |
| **G. Fallen Petal Litter** | Decal scatter of crimson-red Krishnachura and yellow Radhachura petals. | Directly beneath blooming canopies | Fiery red (`#B82218`) / Gold | 0.55 |

---

### 2. Multi-Material Blending Architecture in Unreal Engine 5.8

```
+----------------------------------------------------------------------------------------------------+
| UNREAL ENGINE LANDSCAPE MATERIAL: M_Campus_Terrain_Master                                          |
|                                                                                                    |
| Layer 1: Layer_Lawn_Maintained (Curzon Lawn, Quads) --------+                                     |
| Layer 2: Layer_Turf_Natural (Road verges, Campus edges) ----+--> Runtime Height-Blend              |
| Layer 3: Layer_Soil_Loam (Tree bases, Garden beds) ---------+    with Slope & Distance-Field Masks |
| Layer 4: Layer_Dirt_Compacted (Desire paths, Pavement edge) +                                     |
| Layer 5: Layer_Wet_Silt (Pond banks, Monsoon puddles) ------+                                     |
+----------------------------------------------------------------------------------------------------+
```

1. **Height-Blended Layering**: Uses displacement height maps to ensure grass tufts naturally emerge from soil crevices rather than linearly dissolving into mushy gray blends.
2. **Distance-Field Plinth Masks**: Automatically transitions landscape grass to compacted garden soil within $1.5\text{ m}$ of historic stone plinths and concrete kerbs, preventing grass blades from penetrating architectural stonework.
3. **PBR Water Wetness**: Roughness maps modulated by a global wetness scalar (`Scalar_MonsoonWetness`), allowing soil to darken and become specularly reflective during and after rain showers.

---

### 3. Edge Transition Protocols (Zero Abrupt Seams)

To eliminate unnatural geometry seams:

```
[Road Asphalt] 
      ||
      \/ (0.0m - 0.2m) Concrete Kerbstone
      ||
      \/ (0.2m - 0.8m) Compacted Dirt / Tree-Pit Loam Transition Strip
      ||
      \/ (0.8m - 2.5m) Natural Medium Turf with Soft Feathered Edge
      ||
      \/ (> 2.5m) Maintained Open Green Lawn
```

1. **Kerb-to-Grass**: No grass meshes are placed within $25\text{ cm}$ of road kerbs. The verge starts with a compacted dirt/soil fringe, transitioning smoothly into low turf.
2. **Building-to-Lawn**: A $50\text{ cm}$ perimeter apron of decomposed brick dust or gravel drain (*Puka Drain*) separates the brick plinth from the lawn, preventing moisture seepage and graphical clipping.
3. **Pond Shoreline**: Soft gradient transition from wet muddy silt $\rightarrow$ Kashful reeds $\rightarrow$ medium turf $\rightarrow$ stone walkway.
