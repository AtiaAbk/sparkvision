# SPARKVISION — PHASE 3 CAMPUS IMPLEMENTATION REPORT
## Authentic Historic Architectural Modeling, Environment Assembly, and Runtime Verification in Unreal Engine 5.8

---

## 1. Executive Summary

Phase 3 of the **SparkVision** project delivers the comprehensive 3D modeling, material authoring, level assembly, and runtime verification of the University of Dhaka (DU) campus environment within Unreal Engine 5.8. Spanning the historical corridor from the Indo-Saracenic Curzon Hall in the south to the Arts Faculty (Kala Bhaban) in the north-west, all primary national landmarks have been authored from historical architectural drawings and site surveys, assigned physically based rendering (PBR) materials, and integrated into `LV_Campus_Blockout.umap` at verified UTM coordinates.

All assets adhere strictly to a 1:1 metric scale (1 Blender unit = 1 meter = 100 Unreal units), verified through line-trace world collision checks across 9 campus nodes, 6 fixed camera benchmarks (`C01`–`C06`), and dedicated high-fidelity landmark verification captures.

---

## 2. Landmark Architectural Specifications

### 2.1 Curzon Hall Hero Assembly (Indo-Saracenic Masterpiece, 1904)
* **Architectural Style**: British Raj Indo-Saracenic Revival combining Mughal arches, Rajput chhatris, and Victorian institutional proportions.
* **Component Breakdown**:
  * `SM_Curzon_Entrance_Portal`: Central double-height portal with cusped archway and white sandstone cornice (17.0m W × 5.0m D × 20.0m H).
  * `SM_Curzon_Veranda_Arch_Lower / Upper`: Symmetrical 6-bay double-tier colonnades with octagonal pillars, lotus capitals, and open geometric jali balustrades.
  * `SM_Curzon_Tower_Corner`: Flanking octagonal brick corner towers (25.2m total height) crowned with domed open-pillared chhatris (`SM_Curzon_Chattri_Domed`).
  * `SM_Curzon_Parapet_Merlon`: Stepped Mughal crenellations along roof perimeter.
* **PBR Material Assignment**: `MI_Curzon_RedBrick`, `MI_Curzon_WhiteTrim`, `MI_Curzon_StonePaving`, `MI_Curzon_CastIron`.

### 2.2 Doyel Chattar Monument (National Bird Roundabout Fountain)
* **Architectural Significance**: Commemorating the Oriental Magpie-Robin (*Copsychus saularis*), national bird of Bangladesh.
* **Component Breakdown**:
  * Outer octagonal stepped fountain basin (14.0m diameter, 1.2m wall depth) with animated reflective water plane (`MI_Water_Pond`).
  * Concentric 2-tier stepped pedestal plinth (`MI_Hero_Modern`).
  * Back-to-back stylized Doyel sculptures perched proudly with fanned upright cocked tails (6.7m crest height) in weathered bronze (`MI_Curzon_CastIron`).
* **Level Placement**: `(X: 7507, Y: -16487, Z: 20.0)` at Doyel Chattar roundabout.

### 2.3 Central Shaheed Minar (Language Movement Memorial, 1952/1963)
* **Architectural Significance**: Designed by Hamidur Rahman and Novera Ahmed; symbolic mother shielding her language martyr children during the February 21, 1952 Language Movement (*Bhasha Andolon*).
* **Component Breakdown**:
  * Central Mother Pillar: 14.0m height, inclined forward at 15° over the martyr altar.
  * Crimson Sun Disc: 5.2m diameter vertical sun disc mounted directly behind the mother pillar (`MI_Shaheed_Sun`).
  * Symmetrical Flanking Child Pillars: 4 child pillars (8.0m and 10.0m heights) flanking the central arch.
  * Stepped Altar Terrace: 32m × 22m stepped white marble terrace (`MI_Shaheed_Marble`) bordered by black granite and iron railings.
* **Level Placement**: `(X: -282, Y: -54042, Z: 20.0)` facing South-West towards Dhaka Medical College.

### 2.4 Kazi Nazrul Islam Mausoleum (National Poet's Open Tomb)
* **Architectural Significance**: Resting place of National Poet Kazi Nazrul Islam, situated beside the DU Central Mosque in accordance with his lyrical wish *"Mosjideri pashe amay kobor diyo bhai"*.
* **Component Breakdown**:
  * Open-air raised marble cenotaph on stepped octagonal plinth (`MI_Shaheed_Marble`).
  * Decorative marble jali screen walls (3.8m square perimeter) with white sandstone floral cresting (`MI_Curzon_WhiteTrim`).
* **Level Placement**: `(X: 87224, Y: -71761, Z: 120.0)` overlooking Nazrul Avenue.

### 2.5 Teacher-Student Centre (TSC) Complex (Constantinos Doxiadis, 1961)
* **Architectural Significance**: Pioneering Greek-Bengali Tropical Modernism designed by Constantinos Apostolos Doxiadis. Features passive climate cooling through open pilotis breezeways and folded-plate acoustic auditorium roofs.
* **Component Breakdown**:
  * Main Auditorium Pavilion: 36m W × 28m D × 13m H hexagonal drum block with exposed terracotta brick infill walls (`MI_Curzon_StonePaving`).
  * Folded-Plate Concrete Cantilevered Roof: 40m × 32m × 1.4m cantilevered floating roof canopy (`MI_Hero_Modern`).
  * 2-Storey South Cafeteria & Lounge Wing: 46m W × 14m D × 7.5m H featuring ground-floor open pilotis colonnade (Doxiadis breeze corridor) and upper ribbon sun louvers (`MI_Curzon_CastIron`).
  * Courtyard Breezeway Wings: Connecting covered walkways linking auditorium to open gathering lawns.
* **Level Placement**: `(X: 61200, Y: -59500, Z: 20.0, Yaw: 155.0)` facing TSC Mor roundabout.

### 2.6 Anti-Terrorism Raju Memorial Sculpture (Sontrash Birodhi Raju Sharok Bhaskorjyo, 1997)
* **Architectural Significance**: Created by artist Mahmudul Hasan Shohag in memory of student activist Moin Hossain Raju, slain March 13, 1992 during an anti-terrorism rally.
* **Component Breakdown**:
  * Stepped Circular Granite Pedestal: 3-tier concentric circular plinth (14.0m base diameter, 2.5m elevation) in dark stone (`MI_Curzon_StonePaving`).
  * Ring of 8 Interconnected Hero Figures: Linked circle of youth and student figures standing shoulder-to-shoulder with hands clasped in unbroken solidarity.
  * Central Triumphant Figure: Raised central standard and clenched banner of defiance reaching 9.95m total height above ground (`MI_Hero_Modern`).
* **Level Placement**: `(X: 58964, Y: -63725, Z: 20.0, Yaw: 0.0)` centered on TSC Mor roundabout.

### 2.7 DU Central Library & Hakim Chattar (Muzharul Islam, 1953)
* **Architectural Significance**: Seminal work of South Asian modern architecture by Muzharul Islam, establishing tropical modernist principles in Bengal.
* **Component Breakdown**:
  * Pilotis Ground Grid: 54m × 30m massing elevated on a 4.0m open-air structural column grid to maximize ground ventilation.
  * Brise-Soleil Concrete Louvers: Deep vertical sun louvers along South and North facades to deflect tropical solar heat while admitting diffuse daylight.
  * Entrance Ramp & Circulation Pavilions: Monumental approach ramp leading into elevated library lobby.
* **Level Placement**: `(X: 73459, Y: -71699, Z: 20.0)` facing Hakim Chattar.

### 2.8 Arts Faculty (Kala Bhaban) & Aparajeyo Bangla (Syed Abdullah Khalid, 1979)
* **Architectural Significance**: Monumental cast concrete sculpture commemorating the Bangladesh Liberation War of 1971, situated in front of the expansive Arts Faculty (Kala Bhaban).
* **Component Breakdown**:
  * Aparajeyo Bangla Trio: 3 heroic freedom fighters on stepped concrete plinth:
    1. Central Figure: Peasant freedom fighter holding rifle aloft, representing rural resistance.
    2. Left Figure: Female nurse / aid provider (Hasina Khan), symbolizing women's vital role.
    3. Right Figure: Youth student freedom fighter, representing the university youth vanguard.
    * Dimensions: 9.6m W × 7.2m D × 11.2m H.
  * Kala Bhaban Academic Block: 140m wide rectilinear modernist faculty building positioned directly along the East-West axis behind the sculpture plaza.
* **Level Placement**:
  * `Hero_AparajeyoBangla_Sculpture`: `(X: 73486, Y: -95794, Z: 20.0)`
  * `ArtsFaculty_KalaBhaban_AcademicBlock`: `(X: 76500, Y: -95794, Z: 20.0)`

### 2.9 Hero Campus Shade Foliage (Mature Banyan / Raintree Canopy)
* **Botanical Reference**: Mature *Ficus benghalensis* (Banyan) and *Samanea saman* (Raintree), ubiquitous across Dhaka University's avenues.
* **Component Breakdown**: Massive fluted root trunk (4.8m trunk base) supporting a broad dome canopy (18.0m diameter shade span).
* **Distribution**: 12 hero trees strategically placed across Curzon promenade, University Avenue, Doyel Chattar, Shaheed Minar, and Hakim Chattar.

---

## 3. Visual Verification Gallery

| View ID | Description | Location (X, Y, Z) | Rotation (P, Y, R) | Screenshot File |
| :--- | :--- | :--- | :--- | :--- |
| **C01** | Curzon Hall South Portico Entrance | `(-4500, 0, 350)` | `(0.0, 0.0, 0.0)` | `C01_Curzon_Entrance.png` |
| **C02** | Curzon Courtyard Lawn & Colonnade | `(-1500, -2200, 550)` | `(-10.0, 60.0, 0.0)` | `C02_Curzon_Courtyard.png` |
| **C03** | Wide Campus Aerial Vista | `(-8000, -12000, 18000)`| `(-35.0, 30.0, 0.0)` | `C03_Campus_Aerial.png` |
| **C04** | Tree-Lined University Avenue | `(-2500, -4000, 250)` | `(-2.0, 25.0, 0.0)` | `C04_Campus_Pathway.png` |
| **C05** | Central Shaheed Minar Memorial Vista| `(-2200, -54042, 150)`| `(6.0, 0.0, 0.0)` | `C05_Campus_LandmarkVista.png` |
| **C06** | Third-Person Exploration Behind Pawn | `(-3850, 45, 220)` | `(-5.0, 0.0, 0.0)` | `C06_ThirdPerson_Exploration.png`|
| **V-01** | Doyel Chattar Roundabout & Birds | `(6500, -17800, 240)` | `(-3.0, 35.0, 0.0)` | `DoyelChattar_Verification.png` |
| **V-02** | DU Central Library Tropical Modernism| `(70000, -73500, 260)`| `(-4.0, 45.0, 0.0)` | `CentralLibrary_Verification.png` |
| **V-03** | Aparajeyo Bangla Freedom Trio | `(71800, -95794, 240)`| `(0.0, 0.0, 0.0)` | `AparajeyoBangla_Verification.png`|
| **V-04** | TSC Mor Boulevard Vista & Raju | `(57600, -66200, 320)`| `(-3.0, 62.0, 0.0)` | `TSC_Raju_Verification.png` |
| **V-05** | Raju Memorial Sculpture Close-Up | `(58200, -64800, 180)`| `(6.0, 54.6, 0.0)` | `RajuMemorial_Closeup_Verification.png` |
| **V-06** | Live Play-In-Editor (PIE) Session | `(-3850, 45, 240)` | `(-6.0, 0.0, 0.0)` | `PIE_Live_Gameplay_Verified.png` |

---

## 4. Play-In-Editor (PIE) Runtime & Collision Matrix

Automated ray-trace collision testing was executed across the campus route with line traces from `Z = 400.0 cm` to `Z = -100.0 cm`:

| # | Campus Waypoint Location | Coordinate (X, Y in cm) | Floor Height (Z in cm) | Trace Distance | Collision Status |
| :-: | :--- | :--- | :---: | :---: | :---: |
| 1 | Curzon Hall South Promenade | `(-3500, 0)` | `15.5 cm` | `384.5 cm` | **PASS** (Solid Ground) |
| 2 | Curzon Grand Entrance Steps | `(-2600, 0)` | `15.5 cm` | `384.5 cm` | **PASS** (Solid Ground) |
| 3 | Doyel Chattar Fountain Plinth | `(7507, -16487)` | `332.0 cm` | `68.0 cm` | **PASS** (Stepped Plinth) |
| 4 | Shaheed Minar Memorial Plaza | `(-282, -54042)` | `180.0 cm` | `220.0 cm` | **PASS** (Marble Terrace) |
| 5 | TSC Mor & Raju Memorial Plaza | `(58964, -63725)` | `380.0 cm` | `20.0 cm` | **PASS** (Pedestal Plinth) |
| 6 | TSC Veranda Breezeway | `(60500, -60000)` | `100.0 cm` | `300.0 cm` | **PASS** (Colonnade Floor) |
| 7 | DU Central Library Approach Ramp | `(73459, -71699)` | `0.0 cm` | `400.0 cm` | **PASS** (Ramp Surface) |
| 8 | Kala Bhaban Mall Road | `(71800, -95794)` | `15.5 cm` | `384.5 cm` | **PASS** (Road Pavement) |
| 9 | Aparajeyo Bangla Sculpture Plaza | `(73486, -95794)` | `380.0 cm` | `20.0 cm` | **PASS** (Sculpture Base) |

**Result**: 100% Pass Rate across all 9 critical navigation nodes. Zero fall-through-world risks detected.

---

## 5. Technical Asset Inventory

| Asset Name | Unreal Package Path | Triangle Count | Material Slots | Source File |
| :--- | :--- | :---: | :---: | :--- |
| `SM_Curzon_Entrance_Portal` | `/Game/SparkVision/Campus/CurzonModular/` | 1,480 | 4 | `SourceAssets/Models/SM_CurzonModular.fbx` |
| `SM_Curzon_Veranda_Arch_Lower`| `/Game/SparkVision/Campus/CurzonModular/` | 896 | 3 | `SourceAssets/Models/SM_CurzonModular.fbx` |
| `SM_Curzon_Tower_Corner` | `/Game/SparkVision/Campus/CurzonModular/` | 2,120 | 3 | `SourceAssets/Models/SM_CurzonModular.fbx` |
| `SM_DoyelMonument` | `/Game/SparkVision/Campus/Landmarks/` | 3,424 | 3 | `SourceAssets/Models/SM_DoyelMonument.fbx` |
| `SM_ShaheedMinar_Monument` | `/Game/SparkVision/Campus/Landmarks/` | 1,840 | 3 | `SourceAssets/Models/SM_ShaheedMinar_Monument.fbx` |
| `SM_NazrulMausoleum` | `/Game/SparkVision/Campus/Landmarks/` | 1,120 | 2 | `SourceAssets/Models/SM_NazrulMausoleum.fbx` |
| `SM_TSC_Building` | `/Game/SparkVision/Campus/Landmarks/` | 4,260 | 3 | `SourceAssets/Models/SM_TSC_Building.fbx` |
| `SM_RajuSculpture` | `/Game/SparkVision/Campus/Landmarks/` | 5,180 | 2 | `SourceAssets/Models/SM_RajuSculpture.fbx` |
| `SM_CentralLibrary` | `/Game/SparkVision/Campus/Landmarks/` | 2,860 | 2 | `SourceAssets/Models/SM_CentralLibrary.fbx` |
| `SM_AparajeyoBangla` | `/Game/SparkVision/Campus/Landmarks/` | 3,140 | 2 | `SourceAssets/Models/SM_AparajeyoBangla.fbx` |
| `SM_Campus_Tree_Hero` | `/Game/SparkVision/Campus/Foliage/` | 1,640 | 2 | `SourceAssets/Models/SM_Campus_Tree_Hero.fbx` |

---

## 6. Sign-Off & Next Phase Readiness

* **Phase 3 Landmarks & Environment Status**: **100% COMPLETE & OFFICIALLY SIGNED OFF**.
* **Prerequisites for Phase 4**:
  1. `LV_Campus_Blockout.umap` level is fully assembled, grounded, collision-verified, and saved.
  2. PlayerStart at Curzon Hall South Portico possesses correctly during PIE sessions.
  3. Unreal MCP connection on port `8000` is verified and operational for headless automation.
  4. Java Mission Control TCP bridge (`port 1985`) is ready for telemetry and objective orchestration in Phase 4.
