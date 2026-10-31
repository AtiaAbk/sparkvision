# SPARKVISION — CAMPUS LANDMARK REGISTER & ASSET CATALOG

## 1. Title & Executive Purpose

* **Document**: `LandmarkRegister.md`
* **Purpose**: Serves as the definitive master inventory of all historic landmarks, architectural monuments, public sculptures, and landscape features across the University of Dhaka semi-open world.

---

## 2. Landmark Master Inventory

| Landmark ID | Official Landmark Name | Real-World Coordinates (WGS 84) | Unreal Location (X, Y, Z in cm) | Mesh Asset Path | Outliner Folder | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **LM-01** | **Curzon Hall Hero Complex** | 23.727326° N, 90.401933° E | `(0, 0, 0)` | `/Game/SparkVision/Campus/CurzonModular/SM_Curzon_*` | `Hero_Buildings/Curzon_Hall` | `COMPLETED` |
| **LM-02** | **Doyel Chattar Monument** | 23.727999° N, 90.400318° E | `(7507, -16487, 20)` | `/Game/SparkVision/Campus/Landmarks/SM_DoyelMonument` | `Hero_Buildings/Doyel_Chattar` | `COMPLETED` |
| **LM-03** | **Shaheed Minar Monument** | 23.727500° N, 90.396800° E | `(-282, -54042, 20)` | `/Game/SparkVision/Campus/Landmarks/SM_ShaheedMinar_Monument` | `Hero_Buildings/Shaheed_Minar` | `COMPLETED` |
| **LM-04** | **Kazi Nazrul Islam Mausoleum**| 23.730300° N, 90.398000° E | `(87224, -71761, 120)` | `/Game/SparkVision/Campus/Landmarks/SM_NazrulMausoleum` | `Hero_Buildings/Nazrul_Mausoleum` | `COMPLETED` |
| **LM-05** | **Teacher-Student Centre (TSC)**| 23.731900° N, 90.392700° E | `(61200, -59500, 20)` | `/Game/SparkVision/Campus/Landmarks/SM_TSC_Building` | `Hero_Buildings/TSC_Raju` | `COMPLETED` |
| **LM-06** | **Raju Memorial Sculpture** | 23.731700° N, 90.392900° E | `(58964, -63725, 20)` | `/Game/SparkVision/Campus/Landmarks/SM_RajuSculpture` | `Hero_Buildings/TSC_Raju` | `COMPLETED` |
| **LM-07** | **DU Central Library** | 23.732500° N, 90.393600° E | `(73459, -71699, 20)` | `/Game/SparkVision/Campus/Landmarks/SM_CentralLibrary` | `Hero_Buildings/Central_Library` | `COMPLETED` |
| **LM-08** | **Aparajeyo Bangla Sculpture** | 23.733500° N, 90.391600° E | `(73486, -95794, 20)` | `/Game/SparkVision/Campus/Landmarks/SM_AparajeyoBangla` | `Hero_Buildings/Arts_Faculty` | `COMPLETED` |
| **LM-09** | **Curzon Botanical Pond** | 23.726500° N, 90.401900° E | `(-2200, 0, 8)` | Level Geometry & Water Plane | `Hero_Buildings/Curzon_Hall` | `COMPLETED` |
| **LM-10** | **Hero Campus Shade Tree** | Distributed Campus Routes | 12 Campus-wide coordinates | `/Game/SparkVision/Campus/Foliage/SM_Campus_Tree_Hero` | `Foliage_And_Nature` | `COMPLETED` |

---

## 3. Metric Dimensions & Architectural Characteristics

### 3.1 Curzon Hall Hero Assembly
* **Central Entrance Portico (`SM_Curzon_Entrance_Portal`)**: Width = 17.0m, Depth = 5.0m, Height = 20.0m. Cusped Indo-Saracenic arch with white sandstone band trim.
* **Veranda Colonnade Bays (`SM_Curzon_Veranda_Arch_Lower/Upper`)**: 8.2m modular bay width, paired octagonal pillars with lotus capitals, jali open balustrades.
* **Corner Octagonal Towers & Chhatris**: Height = 25.2m total (16.6m masonry tower + 8.6m domed chhatri).
* **Parapet Merlons**: Stepped crenellations crowning roof perimeter.

### 3.2 Shaheed Minar Monument
* **Mother Pillar**: 14.0m height, forward slant of 15°, representing the protective mother facing her language martyrs.
* **Crimson Sun Disc**: 5.2m diameter vertical disc mounted directly behind the central pillar.
* **Child Pillars**: 4 symmetrical flanking pillars (2 pairs, 8m and 10m heights).
* **Marble Podium**: 32m × 22m stepped white marble terrace with black granite border.

### 3.3 Doyel Chattar Roundabout
* **Basin**: 18m diameter octagonal fountain basin.
* **Sculpture**: Interlocking pair of Doyel (oriental magpie-robin) birds perched with tails raised.
* **Perimeter**: 4 colonial cast-iron street lamps (`SM_Curzon_Lamp_Colonial`).

---

## 4. Current Status

* **Status**: `COMPLETED`
* **Evidence**:
  - All 10 landmark assets modeled in Blender, exported to FBX, imported into Unreal, textured with PBR materials, and positioned at verified UTM coordinates.
* **Remaining Tasks**:
  - Add secondary academic buildings (Physics Building, Chemistry Building, Geology Hall) in Phase 4.
