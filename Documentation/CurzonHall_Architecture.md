# SPARKVISION — PHASE 2: CURZON HALL HERO ARCHITECTURE & CINEMATIC ENVIRONMENT REPORT

## 1. Executive Summary & Architectural Benchmark

As part of **Phase 2 Implementation**, Curzon Hall was transformed from the Phase 1/1.1 blockout into the first fully polished, recognizable **Hero Architectural Environment** of *SparkVision: University of Dhaka*.

The environmental presentation is inspired by the atmospheric world design, natural lighting, and scenic composition of *Where Winds Meet* and *Ghost of Tsushima*, strictly grounded in authentic 1904 Indo-Saracenic Revival heritage:
- **Red-Brick Masonry**: Handcrafted terracotta red-brick tones (`MI_Curzon_Brick`, `MI_Curzon_Brick_Aged`).
- **Two-Tiered Verandas**: Ground-floor rusticated arches beneath upper-floor cusped multi-foil arches with lotus capitals and ornamental jali railings.
- **Monumental Entrance Portico**: 16-meter-wide, 18-meter-high projecting portal crowned with stepped merlons and symmetrical chhatris.
- **Rooftop & Corner Chhatris**: Authentic 8-pillared domed kiosks with ribbed hemispherical roofs and finials.
- **Removal of Fictional Domes**: The unhistorical oversized central onion dome from the preliminary blockout was completely removed, matching photographic and archival ground truth.
- **Cinematic Environment**: Central brick-paved promenade flanked by manicured lawns, colonial teak/iron benches, and heritage street lamps.

---

## 2. Modular Architectural Asset Kit

All modular assets were modeled to true metric scale in **Blender 5.2.3 LTS** (1 Blender unit = 1 meter = 100 Unreal units) and imported via **Unreal MCP** into `/Game/SparkVision/Campus/CurzonModular/`:

| Asset Name | Dimensions (W × D × H) | Architectural Features & Detail | Material Slots |
| :--- | :---: | :--- | :---: |
| **`SM_Curzon_Entrance_Portal`** | 16.0m × 4.0m × 19.1m | Monumental 2-storey central portico, deep cusped arch aperture, white sandstone trim string courses, projecting chhajja eaves, and stepped ornamental parapet. | 2 slots: Brick, WhiteTrim |
| **`SM_Curzon_Veranda_Arch_Lower`** | 8.0m × 1.2m × 7.0m | Ground-floor veranda bay, massive brick piers, contrasting white sandstone impost bands, molded arch rim, and upper cornice. | 2 slots: Brick, WhiteTrim |
| **`SM_Curzon_Veranda_Arch_Upper`** | 8.0m × 1.2m × 7.0m | Second-storey veranda bay, cusped multi-foil arches, paired slender octagonal columns, lotus flower capitals, projecting chhajja eaves, and jali perforated balustrade. | 2 slots: Brick, WhiteTrim |
| **`SM_Curzon_Tower_Octagon`** | 6.0m × 6.0m × 16.0m | 8-sided corner turret bay, alternating white trim string courses, and bracketed top cornice. | 2 slots: Brick, WhiteTrim |
| **`SM_Curzon_Chattri_Dome`** | 6.4m × 6.4m × 8.6m | Authentic octagonal open kiosk, 8 slender pillars, overhanging chhajja eaves, ribbed hemispherical dome, and pointed brass finial needle. | 2 slots: Brick, WhiteTrim |
| **`SM_Curzon_Parapet_Merlons`** | 8.0m × 0.8m × 2.0m | Stepped Indo-Saracenic roofline parapet, 5 stepped brick merlons with pointed white sandstone coping caps and continuous base coping band. | 2 slots: Brick, WhiteTrim |
| **`SM_Curzon_Bench_Colonial`** | 2.2m × 0.6m × 0.9m | Heritage campus park bench, cast-iron curved legs and armrests, 4 teak seat slats, and 3 backrest slats. | 2 slots: CastIron, WhiteTrim |
| **`SM_Curzon_Lamp_Colonial`** | 0.8m × 0.8m × 4.8m | Victorian colonial campus post lamp, fluted base plinth, tapering octagonal shaft, capital ring, and 4-sided frosted glass lantern. | 2 slots: CastIron, WhiteTrim |

---

## 3. PBR Material System

Eight reusable Material Instances were authored under `/Game/SparkVision/Materials/` derived from `/Engine/BasicShapes/BasicShapeMaterial`:

1. **`MI_Curzon_Brick`**: Natural terracotta red brick (`R=0.52, G=0.15, B=0.10`, Roughness `0.78`).
2. **`MI_Curzon_Brick_Aged`**: Weathered darker brick for plinths and lower verandas (`R=0.40, G=0.12, B=0.08`, Roughness `0.85`).
3. **`MI_Curzon_WhiteTrim`**: Warm sandstone plaster for impost bands, capitals, balustrades, and cornices (`R=0.90, G=0.86, B=0.80`, Roughness `0.55`).
4. **`MI_Curzon_Terracotta`**: Rich terracotta ornamental accents (`R=0.62, G=0.22, B=0.12`, Roughness `0.70`).
5. **`MI_Curzon_StonePaving`**: Neutral stone paving for courtyards and plinth steps (`R=0.68, G=0.65, B=0.60`, Roughness `0.65`).
6. **`MI_Curzon_WindowRecess`**: Deep shadow window apertures (`R=0.06, G=0.07, B=0.08`, Roughness `0.95`).
7. **`MI_Curzon_RoofTile`**: Weathered reddish-brown dome and roof surfaces (`R=0.35, G=0.14, B=0.10`, Roughness `0.80`).
8. **`MI_Curzon_CastIron`**: Satin-finished dark wrought iron for benches and lamps (`R=0.10, G=0.10, B=0.12`, Roughness `0.40`).

---

## 4. Assembly & Scene Hierarchy

All detailed elements were assembled over the verified geographic footprint at `(X = 0, Y = 0, Z = 0)` and organized into the Outliner folder **`Hero_Buildings/Curzon_Detail`** (53 total assembled actors):

- **Central Monumental Portico**: `X = -2500, Y = 0, Z = 0`, `Yaw = 90°`.
- **Portico Rooftop Chhatris**: Flanking the central portal at `Y = -750` and `Y = +750` at elevation `Z = 2000 cm`.
- **West Wing Verandas (6 Bays = 48m)**:
  - Ground Floor: `X = -2500, Y = [-1200, -2000, -2800, -3600, -4400, -5200], Z = 0 cm`.
  - Upper Floor: `X = -2500, Y = [-1200, -2000, -2800, -3600, -4400, -5200], Z = 700 cm`.
  - Roofline Merlons: `X = -2500, Y = [-1200, -2000, -2800, -3600, -4400, -5200], Z = 1400 cm`.
- **East Wing Verandas (6 Bays = 48m)**:
  - Ground Floor: `X = -2500, Y = [1200, 2000, 2800, 3600, 4400, 5200], Z = 0 cm`.
  - Upper Floor: `X = -2500, Y = [1200, 2000, 2800, 3600, 4400, 5200], Z = 700 cm`.
  - Roofline Merlons: `X = -2500, Y = [1200, 2000, 2800, 3600, 4400, 5200], Z = 1400 cm`.
- **Corner Octagonal Towers**:
  - West Tower at `Y = -6000`, East Tower at `Y = +6000`, capped with `SM_Curzon_Chattri_Dome` at `Z = 1920 cm`.
- **Campus Furniture & Lighting**:
  - 6 Heritage Victorian Post Lamps lining the promenade.
  - 4 Colonial Park Benches facing the garden walkways.

---

## 5. Cinematic Lighting Configurations

Two distinct lighting passes were evaluated and captured from identical camera transforms:

### Configuration A: Clean Natural Daylight
- **Directional Light**: Pitch `-52.0°`, Yaw `-35.0°`, high sun elevation simulating crisp mid-afternoon tropical daylight.
- **Atmosphere & Fog**: Low haze density (`0.005`), high visual clarity across distant campus landmarks.

### Configuration B: Restrained Late-Afternoon Golden-Hour Lighting (Default Hero Mood)
- **Directional Light**: Pitch `-24.0°`, Yaw `-65.0°`, low sun elevation casting elongated architectural shadows through the cusped veranda arches.
- **Color Grading**: Warm amber sunlight (`R=1.0, G=0.82, B=0.62`), illuminating the red-brick facade and contrasting white sandstone string courses inspired by *Where Winds Meet* and *Ghost of Tsushima*.

---

## 6. Visual Verification Captures

Screenshots captured from Unreal Engine 5.8:

| View Description | Camera Position (X, Y, Z cm) | Rotation (P, Y, R) | Golden-Hour Capture | Daylight Capture |
| :--- | :---: | :---: | :---: | :---: |
| **Front Facade View** | `(-5500, 0, 800)` | `(-6°, 0°, 0°)` | `Phase2_Curzon_FrontFacade_GoldenHour.png` | `Phase2_Curzon_FrontFacade_Daylight.png` |
| **Player Spawn Perspective** | `(-3550, 0, 180)` | `(-2°, 0°, 0°)` | `Phase2_Curzon_PlayerSpawn_GoldenHour.png` | `Phase2_Curzon_PlayerSpawn_Daylight.png` |
| **Entrance Approach** | `(-2900, 0, 160)` | `(8°, 0°, 0°)` | `Phase2_Curzon_EntranceApproach_GoldenHour.png` | `Phase2_Curzon_EntranceApproach_Daylight.png` |
| **Cinematic Angled Aerial** | `(-6200, -4200, 2400)` | `(-20°, 30°, 0°)` | `Phase2_Curzon_CinematicAngled_GoldenHour.png` | `Phase2_Curzon_CinematicAngled_Daylight.png` |
| **Courtyard Lawn & Promenade** | `(-3600, -2000, 220)` | `(2°, 35°, 0°)` | `Phase2_Curzon_CourtyardLawn_GoldenHour.png` | `Phase2_Curzon_CourtyardLawn_Daylight.png` |

---

## 7. Gameplay, Navigation & Collision Audit

Live Play-In-Editor (PIE) testing verified:
1. **Player Spawning**: Possessed default character at `(-3500, 0, 130)` without capsule embedding or fall-through.
2. **Ground Collisions**: Downward ray traces (`ObjectTypeQuery1`) confirmed continuous solid collisions:
   - Player Start Plaza: `Z = 15.5 cm` (**SOLID**)
   - Curzon South Promenade: `Z = 15.5 cm` (**SOLID**)
   - Entrance Portico Approach: `Z = 15.5 cm` (**SOLID**)
   - West/East Lawns: `Z = 7.5 cm` (**SOLID**)
   - Veranda Colonnade: `Z = 472.5 cm` (**SOLID**)
3. **Java Mission Control**: Running continuously on port 8080 (`http://127.0.0.1:8080/api/v1/health` returning `HTTP 200 OK`). Chapter 1 status preserved with all 5 archives registered.

---

## 8. Hardware & Performance Target (MacBook Air M4, 16 GB)

- **Draw Call Efficiency**: High modular reuse across 53 actors using 8 core static meshes.
- **Memory Footprint**: Total modular FBX disk footprint is under 200 KB; texture and material footprint is lightweight PBR.
- **Frame Rate**: Smooth, hitch-free performance on Apple Silicon Metal backend without Nanite / Lumen overhead.
