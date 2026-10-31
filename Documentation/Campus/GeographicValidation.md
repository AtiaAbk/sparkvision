# SPARKVISION — PHASE 1.1: GEOGRAPHIC AUDIT AND MASTER BLOCKOUT VALIDATION REPORT

## 1. Executive Audit Summary

Following the initial Phase 1 campus master blockout, an independent geographic audit and technical validation was conducted across the **University of Dhaka** campus level (`/Game/SparkVision/Maps/Campus/LV_Campus_Blockout`).

The audit addressed key spatial discrepancies, refined the architectural silhouette of Curzon Hall against authentic photo evidence, removed artificial perimeter compound walls to preserve real urban campus geography, verified solid ground collision across all 10 exploration waypoints, and executed live Play-In-Editor (PIE) testing with active C++ GameMode and Java Mission Control synchronization.

---

## 2. Projection & Conversion Methodology (WGS 84 / UTM Zone 46N)

To eliminate visual estimation errors, all landmark coordinates were reprojected using the standard **Universal Transverse Mercator (UTM) Zone 46N (EPSG:32646)** based on the WGS 84 ellipsoid ($a = 6,378,137.0\text{ m}, 1/f = 298.257223563$):
- **Central Meridian ($\lambda_0$)**: $93.0^\circ\text{ E}$
- **Scale Factor ($k_0$)**: $0.9996$
- **False Easting**: $500,000.0\text{ m}$, **False Northing**: $0.0\text{ m}$

### 2.1 Anchor & Engine Axis Mapping
* **Primary Coordinate Anchor**: Curzon Hall Southern Facade Center (`23.727326° N, 90.401933° E`)
  - **UTM Coordinates**: Easting = `235,132.22 m`, Northing = `2,626,455.79 m`
  - **Unreal Engine Origin**: `(X = 0, Y = 0, Z = 0)`
* **Axis Mapping**:
  - `+X = North` (cm): $\Delta \text{Northing} \times 100$
  - `+Y = East` (cm): $\Delta \text{Easting} \times 100$
  - `+Z = Up` (cm): Metric elevation above base ground
  - Metric Scale: **1 Unreal Unit (uu) = 1 centimeter (cm)**

---

## 3. Independent Landmark Coordinate Audit & Corrections

The table below contrasts the preliminary Phase 1 coordinates with the newly audited and verified UTM Zone 46N ground truth from OpenStreetMap (OSM) element nodes and building ways:

| Landmark | Real Lat / Lon | OSM Element ID | True Dist (m) | Bearing | Corrected UE (X, Y cm) | Old UE (X, Y cm) | Discrepancy (m) | Audit Finding & Action |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Curzon Hall (Anchor)** | `23.727326, 90.401933` | `way:264272612` | 0.0 | 0.0° | `(0, 0)` | `(0, 0)` | 0.0 m | **CONFIRMED**: Zero displacement. |
| **Doyel Chattar Roundabout** | `23.727976, 90.400304` | `node:6385028685` | 181.2 | 294.5° | `(7507, -16487)` | `(25744, -7981)` | **201.2 m** | **CRITICAL ERROR CORRECTED**: Was 182m too far North and 85m too far East. Relocated to real traffic rotary. |
| **Raju Memorial Sculpture** | `23.732649, 90.395680` | `node:9150960977` | 868.8 | 313.8° | `(60139, -62695)` | `(58964, -63725)` | 15.6 m | **ADJUSTED**: Snapped to exact TSC Mor roundabout center. |
| **Teacher-Student Centre (TSC)** | `23.731787, 90.396033` | `way:225234221` | 778.8 | 310.4° | `(50519, -59269)` | `(60083, -60974)` | **97.1 m** | **CRITICAL ERROR CORRECTED**: Was placed on top of Raju Sculpture; now placed 102m South-East of Raju as per real Doxiadis building footprint. |
| **Central Shaheed Minar** | `23.727211, 90.396637` | `node:401826555` | 540.4 | 269.7° | `(-282, -54042)` | `(-1273, -53973)` | 9.9 m | **VERIFIED**: Extremely accurate (~9.9m alignment). Fine-tuned altar center. |
| **Central Library** | `23.733836, 90.394774` | `node:2990994435` | 1026.5 | 315.7° | `(73459, -71699)` | `(72112, -72959)` | 18.4 m | **VERIFIED**: Fine-tuned library portico and promenade alignment. |
| **DU Central Mosque** | `23.734659, 90.394710` | `way:295551829` | 1096.8 | 318.8° | `(82582, -72180)` | `(81500, -71000)` | 16.0 m | **VERIFIED**: Fine-tuned dome and prayer hall location. |
| **Nazrul Islam Mausoleum** | `23.735078, 90.394743` | `node:8791763714` | 1129.5 | 320.6° | `(87224, -71761)` | `(80021, -72184)` | **72.2 m** | **CORRECTED**: Relocated directly to the eastern courtyard of DU Central Mosque. |
| **Aparajeyo Bangla** | `23.733799, 90.392412` | `node:2992690009` | 1207.3 | 307.5° | `(73486, -95794)` | `(71703, -97030)` | 21.7 m | **VERIFIED**: Aligned on pedestrian plaza facing Mall Road. |
| **Kala Bhaban (Arts Faculty)** | `23.734232, 90.392793` | `way:1152392502` | 1206.2 | 310.4° | `(78214, -91827)` | `(74500, -97030)` | **63.9 m** | **CORRECTED**: Aligned directly behind Aparajeyo Bangla (58m setback). |

---

## 4. Campus Geographic & Urban Layout Validation

### 4.1 Removal of Artificial Perimeter Walls
* **Problem Identified**: The initial Phase 1 blockout introduced four unbroken perimeter walls (`Wall_South_CurzonBorder`, `Wall_East_HighCourtBorder`, `Wall_North_ShahbaghBorder`, `Wall_West_NilkhetBorder`) around the outer bounds, creating an artificial medieval walled compound.
* **Correction Applied**: The artificial boundary walls were deleted. In real life, Dhaka University is an open urban campus integrated with the city.
* **Preserved Authentic Enclosures**:
  - The historical colonial red-brick wall and wrought-iron entrance gates of the **Curzon Hall Compound**.
  - The residential perimeter enclosure of **Jagannath Hall**.
  - The scenic tree-lined boundary and railing of **Suhrawardy Udyan**.
  - Open urban road entry points at Shahbagh (North), Nilkhet (West), Chankharpul/Nimtoli (South), and High Court (East).

### 4.2 Road Alignment Realignment
With Doyel Chattar and Raju/TSC corrected:
- **Curzon to Doyel Avenue (`Road_Curzon_To_Doyel`)**: Midpoint `(X = 2753, Y = -8243, Z = 6)`, Heading `-60.0°`, Length `190 m`.
- **University Avenue (`Road_University_Doyel_To_TSC_1` & `_2`)**: Connects Doyel Chattar `(7507, -16487)` to TSC Mor `(60139, -62695)` past Bangla Academy along a continuous `-41.3°` heading.
- **Kazi Nazrul Islam Avenue & Mall Road**: Realigned connecting TSC Mor to Central Library, Mosque, and Kala Bhaban.

---

## 5. Curzon Hall Architectural Reference Check

* **Photographic & Archival Reference**: Wikimedia Commons, Curzon Hall Archives (`Category:Curzon_Hall`).
* **Architectural Style**: Indo-Saracenic Revival (1904).
* **Fictional Element Removed**: The oversized central onion dome (`Curzon_Central_MughalDome`, 18m diameter) and conical finial spire were identified as unhistorical and removed. Curzon Hall is not a domed mosque or mausoleum; its roofline is characterized by pitched pavilion roofs, decorative stepped parapets, and corner kiosks.
* **Authentic Elements Added**:
  - Symmetrical **corner chattris (domed kiosks)** atop the octagonal towers (`Curzon_East_Chattri_Dome` and `Curzon_West_Chattri_Dome`).
  - Symmetrical **parapet chattris** flanking the central ceremonial hall (`Curzon_Center_Parapet_Chattri1` & `_2`).
  - Terracotta red-brick facade tone (`MI_Curzon_Brick`), arched verandas, and front grand portico.

---

## 6. Live Gameplay & Navigation Verification (PIE Test)

A live Play-In-Editor (PIE) session was executed via `EditorToolset.EditorAppToolset.StartPIE`:
1. **Engine Level Play Initialization**: `LV_Campus_Blockout` brought up for play in **0.152 seconds**.
2. **GameMode & Controller**: `BP_ThirdPersonGameMode_C` active; Enhanced Input local player subsystem initialized.
3. **Player Spawning**:
   - `PlayerStart` elevation calibrated to `Z = 130 cm` at Curzon South Promenade (`X = -3500, Y = 0, Z = 130`, `Yaw = 0°`).
   - Default character possessed; grounded on solid plaza geometry; camera cleanly framing Curzon Hall's entrance portico and chattris.
4. **Subsystem & Mission Control Synchronization**:
   - `USVMissionControlSubsystem` executed asynchronous HTTP health check to `http://127.0.0.1:8080/api/v1/health`.
   - Health check: **SUCCEEDED** (`HTTP 200 OK`).
   - Session registered: `unreal_session_1793431545` for `chapter-01`.
   - Mission status synchronized: `5 / 5 archives, Level 2 Unlocked: 1`.

### 6.1 Collision Ray-Trace Audit Across All Corrected Waypoints

All 10 major waypoints along the 1.2 km exploration route were verified using `trace_world` down along the `ECC_WorldStatic` collision channel:

| Waypoint | Coordinates (X, Y cm) | Hit Elevation (Z) | Trace Distance (cm) | Result |
| :--- | :---: | :---: | :---: | :---: |
| 1. Curzon South Player Spawn | `(-3500, 0)` | +15.5 cm | 484.5 | **PASS** |
| 2. Curzon Grand Portico Entrance | `(-2200, 0)` | +15.5 cm | 484.5 | **PASS** |
| 3. Curzon-to-Doyel Road Segment | `(2753, -8243)` | +12.0 cm | 488.0 | **PASS** |
| 4. Doyel Chattar Roundabout Hub | `(7507, -16487)` | +0.0 cm | 500.0 | **PASS** |
| 5. University Avenue (Bangla Academy) | `(20500, -28000)` | +0.0 cm | 500.0 | **PASS** |
| 6. TSC Building Center & Promenade | `(50519, -59269)` | +0.0 cm | 500.0 | **PASS** |
| 7. Raju Memorial Sculpture Mor | `(60139, -62695)` | +17.0 cm | 483.0 | **PASS** |
| 8. Hakim Chattar / Library Hub | `(73459, -71699)` | +0.0 cm | 500.0 | **PASS** |
| 9. Aparajeyo Bangla (Arts Plaza) | `(73486, -95794)` | +15.5 cm | 484.5 | **PASS** |
| 10. Shaheed Minar Memorial Altar | `(-282, -54042)` | +40.0 cm | 460.0 | **PASS** |

---

## 7. Updated Verification Visuals

The following high-resolution screenshots were captured from the live Unreal Engine editor:

1. **`TopDown_Campus_Corrected_UTM46N.png`**: Orthographic top-down overview showing the corrected positions of Doyel Chattar, TSC, Raju Sculpture, and the removal of artificial perimeter walls.
2. **`AerialView_CurzonToDoyelAndTSC.png`**: Angled aerial view framing the true road geometry from Curzon Hall along University Avenue towards Doyel Chattar and TSC.
3. **`CurzonHall_Authentic_Silhouette.png`**: Close architectural view of Curzon Hall highlighting the authentic Indo-Saracenic chattris, corner towers, and grand entrance portico (with fictional central dome removed).
4. **`ThirdPerson_PlayerSpawn_Corrected.png`**: Live third-person perspective from the player spawn facing the Curzon Hall southern facade.

---

## 8. Phase 1.1 Acceptance Sign-Off

| Evaluation Item | Status |
| :--- | :---: |
| Template Map (`Lvl_ThirdPerson.umap`) Preserved | **PASS** |
| WGS 84 / UTM Zone 46N Projection Calculation Complete | **PASS** |
| Doyel Chattar Position Corrected | **PASS** |
| TSC vs. Raju Sculpture Distance & Alignment Corrected | **PASS** |
| Artificial Campus Enclosure Walls Removed | **PASS** |
| Curzon Hall Fictional Dome Removed & Chattris Added | **PASS** |
| PIE Execution Verified with EnhancedInput & GameMode | **PASS** |
| Java Mission Control Real-Time Sync Verified in PIE | **PASS** |
| Collision Traces Verified at All 10 Waypoints | **PASS** |
| `GeographicValidation.md` & `CampusMasterplan.md` Updated | **PASS** |
