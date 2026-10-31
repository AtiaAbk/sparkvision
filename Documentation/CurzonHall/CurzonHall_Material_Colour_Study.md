# CURZON HALL MATERIAL & COLOUR STUDY
**Project**: SparkVision — Level 1 University of Dhaka Digital Twin  
**Subject**: Physically Based Rendering (PBR) Calibrations, Color Palettes & Weathering  
**Standard**: PBR Metallic/Roughness workflow calibrated for Unreal Engine 5.8 Lumen.

---

## 1. Primary Material Hierarchy & PBR Values

| Material ID | Asset Name | Base Color (sRGB Hex / Linear) | Metallic | Roughness | Normal / Cavity Detail | Description & Environmental Weathering |
|---|---|---|---|---|---|---|
| **MAT-CH-BRICK** | `M_Curzon_Brick` | `#822B1E` / `(0.22, 0.024, 0.012)` | `0.00` | `0.84` | High (2048 brick bond with recessed lime mortar joints) | Custom local Bengal red-oxide clay brick. Subtle tonal variations between kilned stretchers and weathered headers. |
| **MAT-CH-PLASTER**| `M_Curzon_WhitePlaster`| `#DDD4C1` / `(0.56, 0.51, 0.42)` | `0.00` | `0.72` | Medium (lime-surki wash texture with micro-pitting) | Aged lime-sand-surki plaster applied to arch moldings, capitals, intrados tracery, and chhatri domes. |
| **MAT-CH-SANDSTONE**|`M_Curzon_Sandstone`| `#A87C58` / `(0.39, 0.20, 0.10)` | `0.00` | `0.78` | Medium (dressed sedimentary stone grain) | Carved brackets, plinth moldings, staircase steps, and exterior window sills. |
| **MAT-CH-WOOD** | `M_Curzon_LouverWood`| `#2A1E17` / `(0.024, 0.012, 0.008)`| `0.00` | `0.65` | High (teak wood grain, chipped varnish on outer edges) | Seasoned Burmese teak on louvered shutters, heavy paneled doors, and ceiling beams. |
| **MAT-CH-BRASS** | `M_Curzon_FinialBrass`| `#B89045` / `(0.47, 0.28, 0.06)` | `0.92` | `0.38` | Low (hammered sheet metal with verdigris green patina) | Chhatri kalasa finials, clock dials, door knockers, and colonial lanterns. |
| **MAT-CH-TILES** | `M_Curzon_FloorTiles` | `#7D3123` / `(0.20, 0.03, 0.018)` | `0.00` | `0.55` | Medium (square terracotta floor paving, polished center) | Veranda walkway paving tiles ($300\text{ mm} \times 300\text{ mm}$) with polished central pedestrian wear. |
| **MAT-CH-GLASS** | `M_Curzon_WindowGlass`| `#1A2826` / `(0.008, 0.02, 0.018)`| `0.00` | `0.10` | Low (subtle antique wave distortion, 85% opacity) | Colonial wavy cylinder glass with subtle dust accumulation at lower glazing corners. |

---

## 2. Weathering & Environmental Storytelling (Bengal Delta Climate)
To achieve the photorealistic atmosphere of *Where Winds Meet* while honoring Dhaka University's real identity:
1. **Monsoon Staining & Runoff Trails**:
   - Dark streaks descending from the underside of chhajja drip-eaves and stone window sills.
   - High humidity and seasonal rainfall cause organic staining on white plaster moldings.
2. **Rising Damp & Moss Accumulation**:
   - The bottom $40\text{ cm} - 80\text{ cm}$ of the brick plinth exhibits subtle green-grey moss and salt efflorescence where moisture wicks from the rich deltaic soil.
3. **Sun Fading & Micro-Cracking**:
   - South-facing brick facades receive intense ultraviolet exposure, leading to slightly paler terracotta hues on protruding surfaces compared to deeply shaded interior verandas.
