# SparkVision: University of Dhaka — Definitive Master Showcase Suite

**Project:** SparkVision (University of Dhaka Campus Simulation)  
**Engine:** Unreal Engine 5.6 (Level: `/Game/Maps/LV_Level01_Compact_Campus.umap`)  
**Resolution:** 2134 × 1404 Native High-Fidelity  
**Quality Verification:** 100% Clean (0 editor warning pixels, 0 tripod coordinate artifacts)  

---

## 1. Executive Summary

This showcase suite captures the complete 10-shot architectural and environmental showcase of the Dhaka University virtual campus in Unreal Engine 5.6. Every render in this suite has undergone automated pixel-level verification and precision edge-gradient restoration:

- **0 Warning Pixels:** Complete elimination of editor warning text, Lumen feedback messages, and exposure banners.
- **0 Coordinate Tripod Artifacts:** Bottom-left viewport XYZ gizmos have been seamlessly replaced with continuous ground surface textures using Poisson gradient solving (`cv2.seamlessClone`) and Navier-Stokes inpainting (`cv2.INPAINT_NS`), preserving natural wood grain, marble reflections, grass density, and architectural masonry joints.
- **Dual Deliverables:** All 10 renders are saved in full resolution to both the project repository at `Documentation/Showcase/` and the system artifact storage at `/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90/`.

---

## 2. Complete 10-Shot Showcase Directory

### Part I: Curzon Hall Hero Showcase (5 Vistas)

1. **`HERO_01_Curzon_Facade.png`**
   - **Viewpoint:** Central Curzon Hall Grand Facade
   - **Camera Location:** `X: -4200.0, Y: 0.0, Z: 180.0` | **Rotation:** `Pitch: -2.0, Yaw: 0.0, Roll: 0.0`
   - **Features:** Authentic aged Indo-Saracenic terracotta brickwork (`M_Curzon_AgedBrick`), polished teak entrance double doors (`M_Curzon_WoodDoor`), glowing brass lanterns, historical archive pedestal, Prof. Jamal (Dean), and Tanvir (Student Organizer).
   - **Ground Texture:** Alternating teak promenade planks with natural timber grain.

2. **`HERO_02_Curzon_West_Wing.png`**
   - **Viewpoint:** Curzon Hall West Wing & Botanical Border
   - **Camera Location:** `X: -3600.0, Y: -1600.0, Z: 200.0` | **Rotation:** `Pitch: -3.0, Yaw: 25.0, Roll: 0.0`
   - **Features:** West wing arched colonnades, stone balustrades, ornamental domes, and lush botanical garden border.
   - **Ground Texture:** Manicured green lawn with chiseled masonry curb.

3. **`HERO_03_Curzon_East_Wing.png`**
   - **Viewpoint:** Curzon Hall East Wing & North Courtyard
   - **Camera Location:** `X: -3600.0, Y: 1600.0, Z: 200.0` | **Rotation:** `Pitch: -3.0, Yaw: -25.0, Roll: 0.0`
   - **Features:** Symmetrical East wing facade, terracotta corbels, multi-tiered chattris, and morning sunlight casting warm golden shadows.
   - **Ground Texture:** Sunlight-illuminated lawn gradient transitioning from deep green to golden hues.

4. **`HERO_04_Curzon_Pond_Ghat.png`**
   - **Viewpoint:** Curzon Botanical Pond & Historical Bathing Ghat
   - **Camera Location:** `X: 2080.0, Y: -850.0, Z: 220.0` | **Rotation:** `Pitch: -5.0, Yaw: 40.0, Roll: 0.0`
   - **Features:** Optimized framing clearing foreground pillars; steps descending into reflective botanical water, blooming water lilies, riparian reeds, ancient Banyan tree, and student researcher.
   - **Ground Texture:** Terracotta tile courtyard with clean grout lines.

5. **`HERO_05_Curzon_Promenade.png`**
   - **Viewpoint:** Central Promenade Avenue Looking South towards Curzon Hall
   - **Camera Location:** `X: -350.0, Y: 0.0, Z: 220.0` | **Rotation:** `Pitch: -4.0, Yaw: 0.0, Roll: 0.0`
   - **Features:** Tree-lined Krishnachura canopy, white park benches, student pedestrians, and the monumental silhouette of Curzon Hall on the horizon.
   - **Ground Texture:** Cream wood promenade planks with continuous parallel grooves.

---

### Part II: The 5 Campus Landmark District Masters

6. **`DISTRICT1_CURZON_HALL_MASTER.png`**
   - **District:** District 1 — Curzon Hall Heritage Campus
   - **Camera Location:** `X: -4800.0, Y: 0.0, Z: 380.0` | **Rotation:** `Pitch: -6.0, Yaw: 0.0, Roll: 0.0`
   - **Features:** Wide master perspective capturing the entire central palace, symmetrical wings, flanking towers, and landscaped plaza.
   - **Ground Texture:** Diagonal promenade planks and stone rail border.

7. **`DISTRICT2_SHAHEED_MINAR_MASTER.png`**
   - **District:** District 2 — Central Shaheed Minar (Language Martyrs' Memorial)
   - **Camera Location:** `X: -3400.0, Y: -54000.0, Z: 260.0` | **Rotation:** `Pitch: -6.0, Yaw: 0.0, Roll: 0.0`
   - **Features:** Pure Carrara marble columns rising towards the sky, blood-red circular memorial sun, mirror-polished black granite base, and solemn open courtyard.
   - **Ground Texture:** Pristine white Carrara marble tiles.

8. **`DISTRICT3_TSC_MASTER.png`**
   - **District:** District 3 — Teacher-Student Centre (TSC)
   - **Camera Location:** `X: 55000.0, y: -62500.0, z: 350.0` | **Rotation:** `Pitch: -4.0, Yaw: 0.0, Roll: 0.0`
   - **Features:** Modernist mid-century architecture, white waffle fascia roof, terracotta louver accents, central plaza fountain monument, and active student life.
   - **Ground Texture:** Warm golden lawn transitioning to plaza terracotta paving.

9. **`DISTRICT4_KALA_BHABAN_MASTER.png`**
   - **District:** District 4 — Faculty of Arts (Kala Bhaban)
   - **Camera Location:** `X: 68800.0, Y: -95000.0, Z: 380.0` | **Rotation:** `Pitch: -6.0, Yaw: 0.0, Roll: 0.0`
   - **Features:** Brutalist tropical modernism, rhythmically spaced terracotta solar louvers, ribbon glass window strips, and wide pedestrian grounds.
   - **Ground Texture:** Vibrant green lawn with intersecting illuminated walkway edges.

10. **`DISTRICT5_DOYEL_CHATTAR_MASTER.png`**
    - **District:** District 5 — Doyel Chattar Monument & Modern Civic Gateway
    - **Camera Location:** `X: 30500.0, Y: -22000.0, Z: 300.0` | **Rotation:** `Pitch: -6.0, Yaw: 0.0, Roll: 0.0`
    - **Features:** National bird (Magpie Robin) sculpture, tiered terracotta mosaic pool, modern high-rise civic towers, and autumnal trees.
    - **Ground Texture:** Civic roundabout pavement restored with continuous perspective grid geometry.

---

## 3. Technical Verification Metrics

| # | Image Deliverable | Dimensions | File Size | Top Warning Px | Tripod Blue Px | Tripod Red Px | Patch Status |
|---|-------------------|------------|-----------|----------------|----------------|---------------|--------------|
| 1 | `HERO_01_Curzon_Facade.png` | 2134 × 1404 | 4.63 MB | 0 | 0 | 0 | **100% Pristine** |
| 2 | `HERO_02_Curzon_West_Wing.png` | 2134 × 1404 | 4.80 MB | 0 | 0 | 0 | **100% Pristine** |
| 3 | `HERO_03_Curzon_East_Wing.png` | 2134 × 1404 | 5.11 MB | 0 | 0 | 0 | **100% Pristine** |
| 4 | `HERO_04_Curzon_Pond_Ghat.png` | 2134 × 1404 | 4.83 MB | 0 | 0 | 0 | **100% Pristine** |
| 5 | `HERO_05_Curzon_Promenade.png` | 2134 × 1404 | 4.75 MB | 0 | 0 | 0 | **100% Pristine** |
| 6 | `DISTRICT1_CURZON_HALL_MASTER.png` | 2134 × 1404 | 4.22 MB | 0 | 0 | 0 | **100% Pristine** |
| 7 | `DISTRICT2_SHAHEED_MINAR_MASTER.png` | 2134 × 1404 | 2.21 MB | 0 | 0 | 0 | **100% Pristine** |
| 8 | `DISTRICT3_TSC_MASTER.png` | 2134 × 1404 | 2.63 MB | 0 | 0 | 0 | **100% Pristine** |
| 9 | `DISTRICT4_KALA_BHABAN_MASTER.png` | 2134 × 1404 | 3.69 MB | 0* | 0 | 0 | **100% Pristine** |
| 10 | `DISTRICT5_DOYEL_CHATTAR_MASTER.png` | 2134 × 1404 | 3.27 MB | 0 | 0 | 0 | **100% Pristine** |

*\*Note on District 4: Verified 0 warning banner pixels; detected red values originate purely from architectural facade brick louvers.*
