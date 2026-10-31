# CURZON HALL 3D RECONSTRUCTION & MODULAR PIPELINE PLAN
**Project**: SparkVision — Level 1 University of Dhaka Digital Twin  
**Target Engine**: Unreal Engine 5.8 (Apple Silicon M4, 16 GB Unified Memory)  
**DCC Pipeline**: Procedural Bmesh Python Scripting $\rightarrow$ Blender 5.2.3 LTS $\rightarrow$ FBX Export $\rightarrow$ Unreal Engine 5.8 Asset Import & Scene Assembly.

---

## 1. Modular Asset Architecture & Mesh Budget

| Mesh Asset Name | Dimensions ($X \times Y \times Z$ in cm) | Triangle Budget (Target / Max) | UV Channels | Material Slots | Description |
|---|---|---|---|---|---|
| **`SM_Curzon_Entrance_Portal`** | $1800 \times 480 \times 2340$ | 12,500 / 16,000 | 2 (UV0 PBR, UV1 Lightmap/Nanite) | 4 (Brick, Plaster, Sandstone, Brass) | Monumental central portal: 2-storey 9-cusp grand iwan arch, recessed porch, clock tower pediment, and twin rooftop chhatris. |
| **`SM_Curzon_Veranda_Arch_Lower`**| $800 \times 260 \times 640$ | 4,200 / 5,500 | 2 (UV0 PBR, UV1 Lightmap/Nanite) | 3 (Brick, Plaster, Floor Tiles) | Ground-floor module: paired load-bearing horseshoe arches, interior corridor walkway, ceiling beams, and lower chhajja eave. |
| **`SM_Curzon_Veranda_Arch_Upper`**| $800 \times 260 \times 620$ | 6,800 / 8,500 | 2 (UV0 PBR, UV1 Lightmap/Nanite) | 4 (Brick, Plaster, Jali, Floor Tiles) | First-floor module: paired 7-lobed cusped arches, slender octagonal colonnettes, pierced jali balustrade, and upper chhajja eave. |
| **`SM_Curzon_Tower_Octagon`** | $720 \times 720 \times 2520$ | 9,800 / 12,000 | 2 (UV0 PBR, UV1 Lightmap/Nanite) | 4 (Brick, Plaster, Sandstone, Brass) | Full $25.2\text{ m}$ octagonal tower: base plinth, arrow-slit windows, arched louver tiers, corbelled observation balcony, and domed chhatri cupola. |
| **`SM_Curzon_Parapet_Merlons`** | $800 \times 40 \times 120$ | 1,800 / 2,400 | 2 (UV0 PBR, UV1 Lightmap/Nanite) | 2 (Brick, Plaster Coping) | Modular $8.0\text{ m}$ roof parapet with authentic stepped pointed Indo-Saracenic battlements. |
| **`SM_Curzon_Chattri_Dome`** | $320 \times 320 \times 460$ | 3,400 / 4,200 | 2 (UV0 PBR, UV1 Lightmap/Nanite) | 3 (Plaster, Sandstone, Brass) | Independent 8-pillared octagonal chhatri kiosk with fluted cupola dome and brass kalasa finial. |
| **`SM_Curzon_Lamp_Colonial`** | $40 \times 40 \times 120$ | 1,200 / 1,600 | 2 (UV0 PBR, UV1 Lightmap/Nanite) | 2 (Cast Iron, Glass Emissive) | Cast-iron heritage wall lantern bracket with soft amber glow. |

---

## 2. Structural Assembly & World Placement Matrix
The modular assets assemble symmetrically along the $Y$-axis centered at $Y = 0$:

```
World Coordinates:
- Anchor: (X = -2500, Y = 0, Z = 0)
- West Wing Extents: Y = -900 to -5700 cm (6 bays @ 800 cm = 4800 cm span)
- East Wing Extents: Y = +900 to +5700 cm (6 bays @ 800 cm = 4800 cm span)
- Southwest Tower Center: (X = -2500, Y = -6100, Z = 0)
- Southeast Tower Center: (X = -2500, Y = +6100, Z = 0)
- Northwest Tower Center: (X = -4180, Y = -6100, Z = 0)
- Northeast Tower Center: (X = -4180, Y = +6100, Z = 0)
- Central Portal Center: (X = -2500, Y = 0, Z = 0)
```

### Storey Stacking Rules:
1. **Lower Tier**: `SM_Curzon_Veranda_Arch_Lower` placed at $Z = 0$ (Plinth base sits on terrain, walkway slab at $Z = 80$).
2. **Upper Tier**: `SM_Curzon_Veranda_Arch_Upper` placed at $Z = 640$ (Walkway slab at $Z = 720$, ceiling at $Z = 1340$).
3. **Parapet Tier**: `SM_Curzon_Parapet_Merlons` placed at $Z = 1340$ (Base of parapet wall, merlon tips reach $Z = 1460$).
4. **Towers**: `SM_Curzon_Tower_Octagon` placed at $Z = 0$ extending continuously to $Z = 2520$.

---

## 3. Collision, LOD & Optimization Strategy
* **Nanite & LODs**:
  - Nanite enabled on all static architectural meshes for sub-millimeter geometric fidelity without runtime performance penalty.
  - Proxy fallbacks generated for streaming LODs.
* **Complex-As-Simple Collision**:
  - `CollisionComplexity = CTF_UseComplexAsSimple` enabled on walkways, portals, and staircases to guarantee 100% snag-free third-person player traversal.
  - Blocking volumes placed around intricate chhatri railings and parapet edges to prevent unintended player falling.
* **Apple Silicon M4 Memory Budget**:
  - Total Curzon Hall mesh geometry footprint: $\approx 18.5\text{ MB}$.
  - Texture streaming footprint: $\le 65\text{ MB}$ (using 2K BC7 compressed textures with virtual texturing).
  - Maintained well within the $1,000\text{ MB}$ texture streaming pool size.
