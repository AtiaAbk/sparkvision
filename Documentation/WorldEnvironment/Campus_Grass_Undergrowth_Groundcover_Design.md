# CAMPUS GRASS, UNDERGROWTH & GROUNDCOVER DESIGN
**Project**: SparkVision — Level 1 University of Dhaka Digital Twin  
**Artistic Benchmark**: *Where Winds Meet* / *Ghost of Tsushima*  
**Technical Delivery**: Foliage instancing + Vertex-Color Wind displacement + Pixel Depth Offset (PDO) ground blending.

---

## 1. Groundcover Stratification & Flora Types

```
[Layer 0: Mud & Earth Soil] -> [Layer 1: Moss & Lichen] -> [Layer 2: Turf Grass (10-25cm)] -> [Layer 3: Clumped Meadow Grass (40-75cm)] -> [Layer 4: Ferns & Understory (60-120cm)]
```

### A. Lawn Turf: Durba Grass (*Cynodon dactylon*)
* **Characteristics**: Fine-textured, resilient stoloniferous Bermuda grass native to the Bengal delta.
* **Height**: $10\text{ cm} - 25\text{ cm}$ in height.
* **Shading**: Vibrantly responds to directional sunlight; subtle specular sheen when dew-covered in early morning.
* **Distribution**: Curzon Hall front parterres, Mall playground, TSC green lawns.

### B. Meadow & Field Grass: Ulu Ghas (*Imperata cylindrica*)
* **Characteristics**: Clumped, upright blades with serrated margins and silky white seed plumes.
* **Height**: $40\text{ cm} - 75\text{ cm}$.
* **Distribution**: Unmanicured perimeter zones, botanical garden borders, railway corridor buffers.
* **Wind Response**: High-frequency wave rippling creating dynamic visual "wind currents" across fields.

### C. Riparian Reeds & Kashful (*Saccharum spontaneum*)
* **Characteristics**: Towering wild sugarcane grass with feathery silver-white plumes.
* **Height**: $1.8\text{ m} - 2.5\text{ m}$.
* **Distribution**: Fringing Curzon Botanical Pond and Shahidullah Pond.

### D. Understory Ferns & Wild Arum (*Colocasia esculenta*)
* **Characteristics**: Lush moisture-loving deltaic undergrowth.
* **Height**: $60\text{ cm} - 120\text{ cm}$.
* **Distribution**: Shaded tree bases, foundation wall perimeters, drainage ditch banks.

---

## 2. Fallen Petal & Leaf Decal Systems
Inspired by the vibrant foliage shedding in *Ghost of Tsushima*:
* **Scarlet Krishnachura Petal Decals (`M_Decal_KrishnachuraPetals`)**:
  - Densely scatter under Krishnachura tree canopies during summer/monsoon seasons.
  - Features individual curved scarlet petal geometry with normal map micro-relief.
* **Golden Radhachura Blossom Carpets (`M_Decal_RadhachuraBlossoms`)**:
  - Golden-yellow petal scatters forming organic rings around roadside avenues.
* **Aged Raintree Leaf Detritus (`M_Decal_RaintreeLeaves`)**:
  - Fine brown/amber bipinnate leaf mats accumulating along curbs and tree roots.
