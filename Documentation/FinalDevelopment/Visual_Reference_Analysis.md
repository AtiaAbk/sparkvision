# SPARKVISION — VISUAL REFERENCE ANALYSIS & DESIGN SPECIFICATION

**Document Version:** 1.0  
**Target Engine:** Unreal Engine 5.8 (Apple Silicon M4 macOS)  
**Project:** SparkVision (Bangladesh Historical Adventure)  
**Level:** `/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus`  

---

## 1. Executive Summary & Methodology

This analysis establishes the concrete visual, architectural, atmospheric, and gameplay design baseline for **SparkVision**. Rather than relying on guesswork or generic assets, all visual adjustments are directly derived from:
1. **User-Supplied Visual References** (25 image and document assets located in workspace `.user_uploaded/`).
2. **Primary Industry Reference: *Where Winds Meet*** (NetEase / Everstone Studio) for third-person camera feel, atmospheric naturalism, combat responsive feedback, and clean, uncluttered UI.
3. **Real-World Architectural & Field Data: University of Dhaka** (Curzon Hall, Shaheed Minar, TSC, Arts Plaza / Kala Bhaban, Central Library) with focus on genuine Indo-Saracenic terracotta materials and July monsoon/summer daylight.

---

## 2. Catalog of Inspected References & Direct Technical Directives

### 2.1 Environmental Lighting & Atmosphere

| Reference File | Type | Key Visual Observations | Technical Translation & Correction |
|---|---|---|---|
| `media_1793641949322_ad7f895a.png` | **Defect Screenshot** (Unreal Engine Viewport) | Excessive yellow/amber smog, blinding solar glare, specular burn on ground plane, red warning: `Cached lighting in Lumen and real-time sky capture lighting is going to be clipped...` | **CRITICAL FIX**: Directional light temperature must be normalized from warm bias to neutral 6500K daylight. Reduce solar illuminance from blown-out ~68k lux to calibrated ~4.5 EV100. Calibrate `PostProcessVolume` Auto-Exposure Min/Max EV100, zero warm color grading gain, and enable neutral filmic tonemapper. |
| `media_1793636219954_c864209c.png` | **Primary Style Reference** (*Where Winds Meet*) | Crisp, clean natural daylight; cerulean blue sky with gentle cumulus clouds; realistic aerial perspective (soft blue Rayleigh haze in distance); rich organic vegetation tones without yellow casts. | Calibrate `SkyAtmosphere` Rayleigh scattering coefficients `(0.175, 0.409, 1.0)` and Mie scattering `0.00399` for a crisp, breathable July sky over Dhaka. Shadow fill must be illuminated by realistic ambient skylight. |

### 2.2 Curzon Hall Architecture & Surface Materials

| Reference File | Type | Key Visual Observations | Technical Translation & Correction |
|---|---|---|---|
| `media_1793478724923_7912ee36.jpg` | **Real Photo** (Front Elevation) | Classical Indo-Saracenic red-brick facade, octagonal minarets, central portal with horse-shoe arch, white jali screens, lush flanking royal palms. | Terracotta facade must be smooth, planar, and architecturally refined. The brick surface has horizontal course lines, not rough protruding rock bumps. |
| `media_1793478885782_bb4d8f50.jpg` | **Real Photo** (Oblique View) | Terracotta red-brown tone under afternoon sunlight (Hex `#A84535` / RGB `0.66, 0.27, 0.21`), thin white mortar joints, white ornamental balustrades, clean green courtyard lawn. | Adjust `MI_Curzon_Brick` and `M_Curzon_AgedBrick`: Remove high-frequency displacement or exaggerated normal strength (set normal flatten to `0.35`). Base color tuned to authentic terracotta with low roughness variation (`0.55 - 0.70`). |
| `media_1793478977280_3c524a8a.jpg` | **Real Photo** (L-Wing & Courtyard) | Paved pedestrian promenade, clean grass verge, student pedestrian wearing casual shirt, jeans, backpack. Department signboards. | Ensure campus pathways feature clean asphalt/concrete textures bordered by manicured lawn verges. Civilian student NPCs should reflect genuine student attire (backpacks, casual wear, ID lanyards). |
| `media_1793478998315_e652db01.docx` | **Architectural Dossier** | Verified proportions, bay counts, dome geometry, chhatri details, and historical context of Curzon Hall (1904). | Strict preservation of Curzon Hall's Indo-Saracenic silhouette: double-height cusped arches, chhatri corner pavilions, arched verandas, and authentic central pavilion dome. |

### 2.3 Foliage, Trees & Botanical Canopy

| Reference File | Type | Key Visual Observations | Technical Translation & Correction |
|---|---|---|---|
| `media_1793636264534_7ced0600.jpg` | **Botanical Canopy Reference** | Spreading umbrella silhouette of Dhaka Rain Tree (*Samanea saman*). Horizontal branching structure, layered foliage clusters, natural green leaves. | Tree mesh crowns must spread broadly horizontally rather than towering vertically like northern conifers. Foliage clusters form soft clouds that capture top-down sunlight. |
| `media_1793636248900_09b970f9.png` | **Foliage Clumping Reference** | Tree leaf volumes organized into distinct light/shadow clumps. Gnarled organic bark trunks. Under-canopy ambient shadowing. | Material shader must support two-sided foliage shading with subtle subsurface scattering (`SubsurfaceProfile` or two-sided foliage model) and ambient occlusion in deep leaf clusters. |
| `media_1793636389892_3c213cb5.png` | **PBR Leaf/Branch Atlas** | High-resolution realistic leaf atlas with twigs, dark forest-green topside, slight olive variation, zero neon artifacts. | Import and wire `T_Foliage_WWM_LeafBranch_D` into tree materials, replacing flat procedural or oversaturated leaf textures. |
| `media_1793636408048_9433ea17.png` | **Subsurface Light Transmission** | Clear contrast between shaded back-face and sunlit translucent face of leaves. | Ensure foliage material transmission is set so back-lit leaves glow softly with sunlight rather than appearing pitch black or opaque grey. |
| `media_1793636430298_91a410db.png` | **Leaf Morphology** | Curled botanical leaves with distinct vein structures, yellow-green margins, and natural asymmetry. | Prevents repetitive billboard appearance; ensures organic naturalism. |
| `media_1793636443424_4964e1bc.png` | **Tropical Flora Spectrum** | Diverse Bangladeshi flora: ferns, ficus, jackfruit leaves, broadleaf tropical shrubs. | Diversify ground vegetation: cluster ferns and rangan flowering shrubs along building plinths and garden beds. |

### 2.4 Combat, UI & HUD Layout (*Where Winds Meet* Paradigm)

| Reference File | Type | Key Visual Observations | Technical Translation & Correction |
|---|---|---|---|
| `media_1793636605482_f03116b6.png` | **In-Game Exploration UI** | Third-person camera tracking behind protagonist along campus trail. Mini-map and objective tracker top-left. Clean action button cluster. | Implement third-person camera with 450cm arm length, subtle shoulder offset `(0, 45, 20)`, smooth lag (`CameraLagSpeed = 12.0`). Compass & objective HUD positioned unobtrusively. |
| `media_1793636626063_948b998a.png` | **In-Game Combat HUD** | Circular mini-map dial with target distance (`979 m`). Combat action diamond: Light Attack, Deflection (Parry), Special, Dash. | HUD must display clear action bindings: LMB (Light Attack), Hold LMB (Heavy Charged Attack), RMB (Block), F (Timed Parry), Q (Dodge/Dash). Objective distance indicator updating in real time. |
| `media_1793636650965_5f161932.png` | **Charged Attack & Reflection** | Radial charge indicator around attack icon ("Light Charged"). Water reflection on pond surface. Stamina and health meters. | Add radial charge feedback when holding attack button. Curzon Hall pond must have planar water shader with sky and facade reflections. |

### 2.5 Hardware & Performance Constraints (Apple Silicon M4 16GB)

| Reference File | Type | Key Visual Observations | Technical Translation & Correction |
|---|---|---|---|
| `media_1793456617886_09c89145.png` | **Activity Monitor Memory Audit** | Memory used: 14.50 GB / 16.00 GB; UnrealEditor using 9.11 GB; Yellow memory pressure with 2.58 GB swap. | Enforce strict memory controls: Cap Texture Streaming Pool at 900 MB (`r.Streaming.PoolSize 900`). Aggressive mesh LOD distance culling (`r.StaticMeshLODDistanceScale 1.1`). Garbage collection frequency tuned to 30s. |

---

## 3. Concrete Implementation Action Items

1. **Phase 1: Environment Lighting & Atmosphere Overhaul**
   - Normalize Directional Light (`Sun_DirectionalLight`): Neutral 6500K color, calibrate intensity, eliminate golden yellow cast.
   - Configure `SkyAtmosphere` & `SkyLight`: Natural blue Rayleigh scattering, realistic ambient light bounce.
   - Refine `PostProcessVolume`: Fix auto-exposure bounds (`Min EV100 = 8.0`, `Max EV100 = 12.0`), zero warm color grading offsets, disable blown-out bloom.
   - Refine Curzon Hall Material (`MI_Curzon_Brick`): Smooth, authentic terracotta finish with subtle horizontal mortar joints and zero bumpy displacement.

2. **Phase 2: Foliage & Tree Integration**
   - Apply realistic leaf atlas `T_Foliage_WWM_LeafBranch_D` to campus trees.
   - Tune tree scales and ensure rain tree umbrella silhouettes.
   - Clean up lawn borders so grass does not clip into paved walkways or building stone foundations.

3. **Phase 3: 6-Mission System Architecture**
   - **Mission 1: The Spark at Curzon Hall** — Investigate Curzon Hall courtyard, speak to student representative Tanvir, retrieve Curzon Historical Archive #1.
   - **Mission 2: Voice of the Martyrs at Shaheed Minar** — Traverse the campus avenue to Shaheed Minar, meet activist Nabila, collect Memorial Archive #2.
   - **Mission 3: Confluence at TSC & Raju Sculpture** — Navigate to Teacher-Student Centre, inspect Raju Memorial, collect Student Union Archive #3.
   - **Mission 4: Fortress of Thought at Kala Bhaban** — Reach the Arts Faculty plaza, speak with Professor Rahman, retrieve Faculty Manifesto Archive #4.
   - **Mission 5: The Vanguard at Central Library** — Traverse to Central Library, meet student organizer Farhan, collect Final Unity Declaration Archive #5.
   - **Mission 6: The Stand at Curzon Plaza** — Confront 6 helmeted hostile student cadres wielding batons and 3 aggressive motorbikes attempting to suppress the assembly. Defeat the cadres using grounded combat (attacks, parries, dodges).

4. **Phase 4: Combat System (*Where Winds Meet* Fluidity)**
   - Input bindings: Light Attack (LMB), Heavy Attack (Hold LMB / RMB+LMB), Block (RMB), Timed Parry (F, 0.25s counter window), Dodge Roll (Q / Space while moving).
   - Stamina meter consuming energy on attack/dodge, regenerating when guarding or neutral.
   - Enemy AI telegraph: hostile cadres flash or raise batons before striking; successful parry staggers the attacker and leaves them open to a critical counter-strike.
   - Checkpoint & retry system: failing Mission 6 allows instant retry at Curzon Plaza without restarting Missions 1–5.

5. **Phase 5: Civilian Protection & Law Enforcement**
   - Ordinary campus students (`SVStudentNPC`) tagged as `Civilian`.
   - Attacking a civilian student immediately halts combat, triggers a police siren/officer spawn event, and transitions to the **"Arrested — University Code of Conduct Violation"** screen with Retry or Main Menu options.

6. **Phase 6: Dual Input & UI System**
   - Full keyboard navigation (Arrow Keys / WASD, Enter, Space, Escape) + full mouse clickable support across all menus (Main Menu, Pause, Settings, Mission Journal [J], Map [M], Game Over, Victory).

7. **Phase 7: Optimization & Quality Assurance**
   - Validate 60 FPS performance on Apple Silicon M4.
   - Keep total process memory strictly below 8 GB.
   - Compile comprehensive QA test report and visual regression comparison.
