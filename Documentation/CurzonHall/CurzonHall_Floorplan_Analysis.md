# CURZON HALL FLOORPLAN ANALYSIS & SPATIAL TAXONOMY
**Project**: SparkVision — Level 1 University of Dhaka Digital Twin  
**Typology**: Colonial Academic Complex / Double-Tier Colonnaded Hall  
**Orientation**: Primary facade faces South (True Bearing $180^\circ$) overlooking the historic botanical garden and central fountain plaza.

---

## 1. Spatial Organization & Circulation
Curzon Hall is structured around a central monumental axis intersected by continuous lateral circulation corridors:

```
[West Wing Laboratories] <==== [CENTRAL EXAMINATION HALL] ====> [East Wing Laboratories]
          ||                                   ||                                  ||
[South Veranda Colonnade] <==== [South Grand Entrance Portal] ====> [South Veranda Colonnade]
                                               ||
                                    [Promenade & Botanical Lawn]
```

### A. Ground Floor Level (+0.80m Datum)
1. **South Entrance Portico (Iwan Porch)**: Monumental covered carriage porch ($18.0\text{ m} \times 4.8\text{ m}$) granting pedestrian access via a five-step ceremonial staircase.
2. **Central Examination Hall (Great Hall)**: Spans two storeys in clear height ($128.0\text{ m}^2$ floor area, $18.0\text{ m} \times 24.0\text{ m}$), with a mezzanine gallery supported by fluted cast-iron and brick Corinthian pilasters. Used for university convocations, senate sessions, and historic political conventions.
3. **Continuous South Veranda Walkway**: Deep $2.6\text{ m}$ wide covered colonnade connecting the central portal to the east and west wings. Provides shade and cross-ventilation.
4. **East Wing (Faculty of Science / Physics)**: Four main lecture halls ($12.0\text{ m} \times 10.0\text{ m}$) flanked by professors' research chambers and apparatus storage.
5. **West Wing (Chemistry & Mathematics)**: Laboratory rooms with tall arched casement windows and fume-extraction flues integrated into rear masonry chimneys.
6. **North Courtyard & Colonnade**: Enclosed landscaped quadrangle bordered by a matching northern arcaded veranda.

### B. First Floor Level (+7.20m Datum)
1. **Upper Veranda Balcony**: Continuous shaded arcade with pierced white jali balustrades overlooking the south lawns. Serves as primary upper-level circulation.
2. **Mezzanine Gallery (Central Hall)**: Wraps three sides of the central hall, allowing spectators to view proceedings on the main hall floor below.
3. **Departmental Libraries & Reading Rooms**: Tall bookshelves and teak wood study carrels beneath high vaulted plaster ceilings.
4. **Corner Tower Access**: Circular winding masonry staircases located inside the four octagonal corner towers granting access to the rooftop terraces.

---

## 2. Ingress, Egress & Gameplay Waypoint Anchors
For gameplay traversal, player interaction, and AI navigation in SparkVision:

| Waypoint ID | Location Name | UE5 World Coordinates `(X, Y, Z)` | Function / Gameplay Significance |
|---|---|---|---|
| **WP-CURZON-PORTAL** | South Ceremonial Portal | `(-2500, 0, 80)` | Primary player spawn & mission briefing anchor. |
| **WP-CURZON-VERANDA-W** | West Veranda Arcade | `(-2500, -2800, 80)` | Covered sprint corridor, dynamic rain shelter. |
| **WP-CURZON-VERANDA-E** | East Veranda Arcade | `(-2500, 2800, 80)` | Physics lab entrance, academic lore collectible pickup. |
| **WP-CURZON-TOWER-SW** | Southwest Octagonal Tower | `(-2500, -6400, 80)` | Corner defensive observation post, stair access. |
| **WP-CURZON-TOWER-SE** | Southeast Octagonal Tower | `(-2500, 6400, 80)` | High-vantage sniper / panoramic observation point. |
| **WP-CURZON-COURTYARD** | Inner North Courtyard | `(-4500, 0, 80)` | Shaded garden, debate meeting point, secret archives entrance. |
| **WP-CURZON-ROOF-TERRACE**| Central Roof Terrace | `(-2500, 0, 1420)` | Rooftop traversal, wind-responsive audio/visual showcase. |

---

## 3. Modular Architectural Breakdown for 3D Assets
To achieve authentic visual fidelity while adhering to the 16 GB unified memory budget:

1. **`SM_Curzon_Entrance_Portal`**: 
   - Central $18.0\text{ m}$ monumental portico with grand cusped arch, recessed porch, upper clock pediment, and twin domed chhatris.
2. **`SM_Curzon_Veranda_Arch_Lower`**: 
   - $8.0\text{ m}$ wide module containing paired horseshoe arches, $0.85\text{ m}$ masonry piers, walk-through floor slab, and lower chhajja overhang.
3. **`SM_Curzon_Veranda_Arch_Upper`**: 
   - $8.0\text{ m}$ wide module containing paired multi-cusped scalloped arches, slender octagonal colonnettes, jali balustrade, and upper chhajja overhang.
4. **`SM_Curzon_Tower_Octagon`**: 
   - $7.2\text{ m}$ diameter, $25.2\text{ m}$ tall octagonal tower featuring base plinth, two tiers of arched louvered windows, corbelled upper balcony, and crown Rajput domed chhatri with brass finial.
5. **`SM_Curzon_Parapet_Merlons`**: 
   - $8.0\text{ m}$ tileable modular parapet wall featuring stepped pointed battlements and decorative stone molding.
6. **`SM_Curzon_Chattri_Dome`**: 
   - Standalone 8-pillared octagonal chhatri for rooftop embellishments and courtyard gazebos.
