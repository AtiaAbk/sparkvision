# SPARKVISION — UNIVERSITY OF DHAKA CAMPUS MASTERPLAN (PHASE 1 BLOCKOUT)

## 1. Executive Summary & Design Vision

**SparkVision** is a cinematic, semi-open-world historical third-person adventure game set across the historic grounds of the **University of Dhaka (DU)**, Bangladesh. Visual presentation and environmental mood are inspired by the open-world composition, organic exploration, and scenic depth of *Where Winds Meet* and *Ghost of Tsushima*, grounded directly in the authentic heritage, architectural identity, and political history of Dhaka University.

The campus is modeled as a connected semi-open world:
- The entire core campus has a recognizable geographic layout matching real-world geospatial and archival references.
- High-priority exploration hubs and historic monuments feature walkable plazas, courtyards, and perimeter routes.
- Secondary academic blocks and restricted departmental wings use authentic physical boundaries (wrought-iron gates, colonial red-brick walls, security checkpoints).
- Distant areas and administrative facilities form atmospheric background scenery without artificial invisible barriers.

---

## 2. World Scale, Coordinate Frame & Spatial Orientation

### 2.1 Engine Scale Standard
* **Engine Scale**: Standard Unreal Engine metric units: **1 Unreal Unit (uu) = 1 centimeter (cm)**.
* **1 meter = 100 uu**.
* **1 kilometer = 100,000 uu**.

### 2.2 Coordinate System & Geographic Orientation
* **Primary Coordinate Anchor (World Origin `(0, 0, 0)`)**: The center of the southern front facade of **Curzon Hall** (`23.727326° N, 90.401933° E`).
* **Unreal +X Axis**: **North** (increasing Latitude towards Shahbagh and Central Mosque).
* **Unreal -X Axis**: **South** (decreasing Latitude towards Old Dhaka, Nimtoli, and Chankharpul).
* **Unreal +Y Axis**: **East** (increasing Longitude towards Supreme Court and Secretariat).
* **Unreal -Y Axis**: **West** (decreasing Longitude towards TSC, Central Library, Arts Faculty, and Nilkhet).
* **Unreal +Z Axis**: **Up** (Elevation above mean ground level).
* **Explicit In-Game Orientation Reference**: A dedicated compass monument (`Marker_NorthCompass_Pillar` and `Marker_NorthCompass_Arrow`) is installed at `(X = 500, Y = 0, Z = 50)` pointing directly along the `+X` axis to provide immediate visual confirmation of North.

---

## 3. Reference Sources & Geospatial Attribution

All landmark positions, distances, and road alignments are derived from verified official sources:
1. **Official University of Dhaka Campus Map**:
   - URL: `https://old.du.ac.bd/footer_widget/footer_widget_item/map`
   - Role: Authoritative baseline for campus boundaries, building footprints, and institutional zones.
2. **OpenStreetMap (OSM)**:
   - Coordinates: `23.7280° N, 90.3975° E`
   - URL: `https://www.openstreetmap.org/#map=17/23.7280/90.3975`
   - Attribution: *Data © OpenStreetMap contributors, licensed under the Open Database License (ODbL).*
3. **University of Dhaka Official Sustainability & Landmark Register (SDG 20)**:
   - URL: `https://sustainability.du.ac.bd/sdg_menu_details/20`
   - Role: Verified landmark classifications, accessibility corridors, and memorial records.
4. **Curzon Hall Architectural Archives**:
   - Wikimedia Commons: `https://commons.wikimedia.org/wiki/Category:Curzon_Hall`
   - Architectural Style: Indo-Saracenic Revival architecture blending Mughal domes, terracotta brickwork, cusped arches, and colonial symmetry.

---

## 4. Landmark Register & Metric Coordinates

The table below details each major campus landmark, its real-world geospatial coordinates, distance from the Curzon Hall anchor, corresponding Unreal Engine vector coordinates, and blockout implementation status.

| Landmark | Real Lat / Lon | Distance from Curzon | Unreal Location (X, Y, Z cm) | Massing / Mesh Spec | Status |
| :--- | :---: | :---: | :---: | :--- | :---: |
| **Curzon Hall (Anchor)** | `23.727326, 90.401933` | 0.0 m | `(0, 0, 1600)` | Central Pavilion (120m×50m×32m), Mughal Dome, Spire, East/West Wings, Octagonal Towers | **PASS** |
| **Doyel Chattar Roundabout** | `23.729650, 90.401150` | 269.5 m | `(25744, -7981, 20)` | Circular Roundabout Hub, Island, Magpie Robin Monument | **PASS** |
| **Central Shaheed Minar** | `23.727211, 90.396637` | 539.9 m | `(-1273, -53973, 20)` | Marble Altar (60m×60m), Mother Pillar (slanted 15°), Crimson Sun, Flanking Pillars | **PASS** |
| **Teacher-Student Centre (TSC)** | `23.732750, 90.395950` | 856.0 m | `(60083, -60974, 800)` | Doxiadis Modernist Auditorium, Cantilevered Roof, Circular Cafeteria Ring, Gathering Lawn | **PASS** |
| **Raju Memorial Sculpture** | `23.732649, 90.395680` | 868.2 m | `(58964, -63725, 100)` | Pedestal + Figure Massing + Custom Art Mesh (`SM_RajuSculpture`) | **PASS** |
| **Hakim Chattar & Central Library** | `23.733836, 90.394774` | 1025.8 m | `(72112, -72959, 1000)` | Multi-Storey Academic Block (80m×50m×20m), Student Discussion Hub | **PASS** |
| **Kazi Nazrul Islam Mausoleum** | `23.734550, 90.394850` | 1077.7 m | `(80021, -72184, 120)` | Open White Marble Cenotaph, Historic Inscribed Wall | **PASS** |
| **DU Central Mosque** | `23.734659, 90.394710` | 1085.0 m | `(81500, -71000, 1200)` | Grand Classical Mosque Dome & Minaret Footprint | **PASS** |
| **Aparajeyo Bangla (Arts Faculty)** | `23.733799, 90.392412` | 1206.5 m | `(71703, -97030, 100)` | Pedestal + Trio Hero Massing + Custom Art Mesh (`SM_AparajeyoBangla`) | **PASS** |
| **Arts Faculty (Kala Bhaban)** | `23.734000, 90.392412` | 1230.0 m | `(74500, -97030, 1200)` | Grand Modernist Academic Block (160m×50m×24m) | **PASS** |

---

## 5. Semi-Open-World Zone Classification

### Zone A: Playable Exploration Areas
* **Curzon Hall Complex**: Front botanical palm gardens, south grand promenade, inner courtyard pond perimeter, arched front portico.
* **Doyel Chattar Hub**: Pedestrian crossing between Curzon Hall, Bangla Academy, and Suhrawardy entrance.
* **TSC Mor & Raju Square**: High-activity campus center, pedestrian gathering lawns, outdoor cafeteria ring.
* **Hakim Chattar & Library Plaza**: Open outdoor study area, shaded brick seating benches, bookstall row.
* **Aparajeyo Bangla Plaza**: Historic student rallying ground in front of Kala Bhaban.
* **Shaheed Minar Memorial Square**: Elevated marble platform and commemorative reflection ground.

### Zone B: Visible Restricted Campus Zones
* **Curzon Hall Science Research Laboratories**: Chemistry and Physics departments bounded by red-brick boundary walls and padlocked iron gates (`Restricted_Curzon_ResearchLab_Gate`).
* **Jagannath Hall Residential Compound**: Historic residential quadrangles behind perimeter boundary wall and barrier (`Restricted_JagannathHall_PerimeterFence`).
* **Arts Faculty Dean's Archival Records Wing**: Controlled administrative archive corridor (`Restricted_ArtsFaculty_DeanArchive_Barrier`).

### Zone C: Non-Playable Scenic Background
* **Suhrawardy Udyan Tree Canopy**: Massive organic green backdrop bordering University Road (`Green_SuhrawardyBuffer`).
* **Supreme Court / High Court Mughal Architecture**: Distant colonial and Mughal silhouettes along the eastern boundary.
* **Shahbagh City Skyline**: Urban silhouette creating the illusion of a bustling capital beyond the northern campus gates.
* **Old Dhaka / Chankharpul Silhouettes**: Historical residential skyline along the southern perimeter.

### Zone D: Story-Specific Locked Areas
* **Curzon Hall North Tower Under-Vault**: Underground archive chamber storing pre-1947 and 1952 archival records.
* **Central Library Rare Books Archive**: Restricted historical manuscripts repository accessed during Chapter 1 climax.

---

## 6. Primary Road Network & Navigation Structure

All primary roads are raised slabs (`Z = 6 cm`) with continuous collision (`ECC_WorldStatic`) to ensure stable player foot movement without snagging or clipping:

1. **Curzon Avenue (`Road_Curzon_To_Doyel`)**:
   - Connects Curzon Hall South Gate to Doyel Chattar Roundabout.
   - Dimensions: Length 270m, Width 14m (`Scale: 270, 14, 0.12`).
2. **Doyel Chattar Roundabout (`Roundabout_DoyelChattar_Ring`)**:
   - 34m diameter traffic rotary connecting Curzon Road, High Court Road, and University Avenue.
3. **University Avenue (`Road_University_Doyel_To_TSC_1` & `_2`)**:
   - Sweeping avenue running North-West past Bangla Academy and Suhrawardy Udyan to TSC Mor.
   - Total Length: ~660m, Width 14m, Heading 301° (Yaw -59.1°).
4. **TSC Mor / Raju Intersection (`Plaza_TSCMor_Intersection`)**:
   - 40m diameter intersection plaza uniting University Ave, Fuller Road, and Kazi Nazrul Islam Ave.
5. **Kazi Nazrul Islam Avenue (`Road_TSC_To_Library` & `Road_Library_To_Shahbagh`)**:
   - Arterial avenue running North from Raju Sculpture past Central Library and Mosque to Shahbagh.
6. **Mall Road (`Road_MallRoad_ArtsFaculty`)**:
   - Grand east-west corridor (240m long) linking Hakim Chattar to Aparajeyo Bangla.
7. **Fuller Road (`Road_FullerRoad_Corridor`)**:
   - 610m diagonal road linking TSC Mor southwards to the Shaheed Minar memorial precinct.

---

## 7. Curzon Hall Hero Massing Architecture

Curzon Hall is the primary hero building of Level 1. Its blockout represents its distinctive Indo-Saracenic silhouette:
- **Central Pavilion (`Curzon_Central_Pavilion`)**: Footprint of `120m × 50m`, height `32m`, finished in custom terracotta red-brick material (`MI_Curzon_Brick`).
- **Mughal Onion Dome (`Curzon_Central_MughalDome`)**: `18m` diameter hemispherical dome centered over the main ceremonial hall.
- **Finial Spire (`Curzon_Central_FinialSpire`)**: Traditional brass/white finial crowning the central dome reaching `43.5m` world height.
- **Flanking East and West Wings (`Curzon_East_WingPavilion` & `Curzon_West_WingPavilion`)**: Double-storey symmetrical pavilions (`70m × 40m × 24m`) housing lecture halls and verandas.
- **Octagonal Corner Towers (`Curzon_East_OctagonalTower` & `Curzon_West_OctagonalTower`)**: Dual towers (`16m × 16m × 32m`) anchoring the outer corners.
- **Front Portico (`Curzon_Front_GrandPortico`)**: Projecting entrance veranda with monumental cusped arch profile.
- **Botanical Pond (`Pond_CurzonHall`)**: Historic rectangular water basin (`55m × 40m`) reflecting the Curzon Hall facade.

---

## 8. Outliner Hierarchy Organization

The map is systematically structured into 10 designated Outliner folders:

| Outliner Folder | Actor Count | Primary Contents |
| :--- | :---: | :--- |
| `Campus_Ground` | 5 | Main terrain slab (1.6km×1.4km), Curzon botanical plaza, pond, North reference needle & pillar |
| `Campus_Boundary` | 4 | South Nimtoli, East High Court, North Shahbagh, West Nilkhet perimeter walls |
| `Primary_Roads` | 10 | Curzon Ave, Doyel Roundabout & Island, University Ave 1 & 2, TSC Mor, Nazrul Ave 1 & 2, Mall Road, Fuller Road |
| `Pedestrian_Paths` | 4 | Curzon South Promenade, Hakim Chattar Hub, Aparajeyo Bangla Plaza, Shaheed Minar Marble Altar |
| `Hero_Buildings` | 24 | Curzon Hall complex (7 components), TSC (2 blocks), Raju Sculpture (3 actors), Central Library, Nazrul Mausoleum, Central Mosque, Aparajeyo Bangla & Kala Bhaban (3 actors), Shaheed Minar (4 pillars & sun) |
| `Supporting_Buildings` | 5 | Bangla Academy, Curzon Science Labs, Jagannath Hall, Surja Sen Hall, Mohsin Hall |
| `Green_Spaces` | 3 | Suhrawardy Udyan Scenic Border, Mall Chattar Open Lawns, TSC Gathering Lawn |
| `Restricted_Areas` | 3 | Curzon North Lab Gate, Jagannath Hall Perimeter Fence, Arts Dean Archive Barrier |
| `Playable_Route` | 1 | `PlayerStart_CurzonPromenade` (Spawn at Curzon South Garden facing North) |
| `Gameplay_Test` | 9 | 5 `SVArchiveTerminal`s, 2 `SVStudentNPC`s, 2 `SVHostileOpponent`s |
| `Lighting_Environment`| 6 | DirectionalLight, SkyLight, SkyAtmosphere, ExponentialHeightFog, VolumetricCloud, PostProcessVolume |

---

## 9. Verification & Screenshots

Three high-resolution verification captures have been saved to `Documentation/Screenshots/`:

1. **Complete Top-Down Overview (`TopDown_CampusMaster_Overview.png`)**:
   - Camera: `X = 35000, Y = -50000, Z = 130000`, `Pitch = -89.9°`.
   - Displays the complete University of Dhaka campus layout, roads, boundaries, and spatial relationships.
2. **Angled Cinematic Aerial View (`AerialView_CurzonToTSC.png`)**:
   - Camera: `X = -15000, Y = 15000, Z = 22000`, `Pitch = -30.0°, Yaw = -125.0°`.
   - Displays Curzon Hall in the foreground, framing the road network sweeping towards Doyel Chattar, Suhrawardy Udyan, and TSC.
3. **Third-Person Player Spawn Perspective (`ThirdPerson_CurzonSpawn_View.png`)**:
   - Camera: `X = -4500, Y = 0, Z = 250`, `Pitch = 10.0°, Yaw = 0.0°`.
   - Frames the player character's initial viewpoint facing North towards the iconic Curzon Hall entrance portico, red-brick verandas, and central Mughal dome.

---

## 10. Geographic Approximations & Design Trade-offs

1. **Terrain Flatness vs. Micro-Topography**:
   - Real DU campus has minor elevation variations (~2–4 meters elevation difference between Curzon Hall and Nilkhet). For Phase 1 blockout, a unified base elevation (`Z = 0`) was maintained with raised road slabs (`Z = 6–8 cm`) to guarantee zero physics catching during initial third-person traversal.
2. **Curzon Hall Inner Courtyard Alignment**:
   - Curzon Hall features a central pond behind the main hall and smaller side quadrangles. The blockout simplifies this into a primary rectangular reflection pond and north departmental lab cluster.
3. **Road Curvature Discretization**:
   - University Avenue curves around the perimeter of Suhrawardy Udyan. In this blockout, this curve is segmented into two angled roadway sections (Heading 301°) matching the primary tangent angles.
4. **Shaheed Minar Altar Alignment**:
   - Shaheed Minar is situated approximately 540m west of Curzon Hall near Dhaka Medical College. The monument orientation faces south towards the expansive gathering square.

---

## 11. Phase 1 Acceptance Matrix

| Criterion | Evaluation | Verification Evidence |
| :--- | :---: | :--- |
| **Original Third Person Level Preserved** | **PASS** | `Content/ThirdPerson/Lvl_ThirdPerson.umap` untouched; Git working tree confirms 0 changes in template directory. |
| **New Campus Blockout Level Exists** | **PASS** | `Content/SparkVision/Maps/Campus/LV_Campus_Blockout.umap` saved, active, and set as default startup level. |
| **Campus Boundaries & Roads Represented** | **PASS** | 4 outer perimeter walls, 10 primary road slabs/roundabouts, and 4 pedestrian plazas generated. |
| **Major Landmarks Placed using Reference Data** | **PASS** | Curzon, Doyel Chattar, Shaheed Minar, TSC, Raju, Library, Nazrul Mausoleum, Arts Faculty all mapped from OSM/DU GIS data. |
| **Building Footprints Have Appropriate Scale** | **PASS** | 1 uu = 1 cm verified; building footprints match real-world proportions (e.g. Curzon 120m×50m, Kala Bhaban 160m×50m). |
| **Curzon Hall Has Identifiable Silhouette** | **PASS** | Indo-Saracenic central pavilion, dome, spire, pavilions, octagonal towers, and portico verified in third-person view. |
| **Primary Route is Navigable** | **PASS** | Ray-traced ground collision (`trace_world`) verified at all 9 primary waypoints from Curzon to Arts Faculty. |
| **Restricted & Scenic Areas Distinguishable** | **PASS** | Amber/hazard physical barriers placed at research labs, residential halls, and archives. |
| **Player Spawning & Camera Operational** | **PASS** | `PlayerStart` positioned at Curzon South Garden facing North; third-person viewport camera captures verified. |
| **Screenshots Captured & Documented** | **PASS** | Top-down, angled aerial, and third-person view saved in `Documentation/Screenshots/`. |
| **CampusMasterplan.md Created** | **PASS** | Complete design document compiled and committed to repository. |
| **Zero Critical Editor Errors** | **PASS** | Engine running stable; MCP session active on port 8000; all assets saved. |
