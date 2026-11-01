# SparkVision — Initial Project State & Environment Audit
**Document ID:** `SPARKVISION-AUDIT-2026-11-01`  
**Target Environment:** macOS (Apple Silicon M4, 16 GB Unified Memory)  
**Engine:** Unreal Engine 5.8 (Native C++ / macOS Metal)  
**Primary Map:** `/Game/SparkVision/Maps/Campus/LV_Campus_Blockout`  
**Backend:** Java Mission Control (`JavaMissionControl/`)  

---

## 1. Executive Summary

This audit establishes the baseline for the SparkVision University of Dhaka Level 1 game project as of **November 1, 2026**.

The project has achieved significant environment and architectural milestones:
- 1:1 metric reconstruction of the University of Dhaka (DU) campus across Curzon Hall, Doyel Chattar, Shaheed Minar, TSC, Central Library, and Arts Faculty (Kala Bhaban).
- Curzon Hall 1:1 Indo-Saracenic colonial reconstruction, authentic facade materials (`MI_Modern_RibbonWindow`, `MI_Modern_GlassDoor`, `MI_Modern_ConcreteFin`), and botanical calibration.
- Initial C++ character locomotion (`ASVCharacter`) and canvas HUD (`ASVHUD`) compiled in native macOS dylib.
- Java Mission Control microservice with SQLite persistence and REST API.

However, critical gameplay gaps previously prevented the project from being a complete, playable, narrative-driven game:
1. Missing in-game startup / main menu flow; the game could only be started via editor or terminal scripts.
2. Incomplete NPC integration: `ASVStudentNPC` actors existed in the level but lacked visual meshes, animation blueprints, and comprehensive dialogue UI.
3. Opponents in Level 1: Helmeted hostile actors were placed in Level 1, contradicting the authoritative story documents (`LEVELS.md` and `2x12_COMPLETE_GAME_PLAN.md`), which mandate that Level 1 ("Where It All Began") is **strictly peaceful** with **combat disabled**.
4. Incomplete Level 1 mission state machine: Objective tracking was limited to raw archive inspection without the full `L1_M01` through `L1_M06` progression sequence, dialogue requirements, or the historic ending decision (*"আমিও থাকব।"* / *"I will be there too."*).
5. Lack of persistent Save/Load UI in the pause/main menus.

---

## 2. Git & Version Control Verification

### 2.1 Branch & Remote State
- **Current Branch:** `main`
- **Working Tree:** Clean (all prior changes committed and synced)
- **Remote Origin:** `https://github.com/AtiaAbk/sparkvision.git`
- **Latest Commit:** `10c9c75` (`feat(gameplay): make open-world campus fully playable with third-person character, controls, and landmark exploration`)

### 2.2 Milestone Verification (`3578639` & `e86f6f0`)
- **Commit `3578639`**: Verified present in Git history (`docs(environment): complete 16-part botanical research, WWM analysis, and open campus masterplan suite`).
- **Commit `e86f6f0`**: Verified present in Git history (`feat(environment): clear Curzon clutter, calibrate flora, relocate pond, and apply authentic building facade materials`). Contains 158 changed files, facade materials, clearance scripts, and 10-camera photographic verification suite.

---

## 3. Discrepancy Analysis: Environment Assets vs. Actors

The previous report stated:
- 105 environment assets existed.
- The clearance audit checked 83 environment actors.
- Zero placement defects were reported.
- 10 verification screenshots were captured.

### 3.1 Why Asset Count (105) Differed from Audited Actor Count (83)
Upon detailed code and outliner inspection of `Scripts/audit_environment_clearance.py`:
1. **Asset Count (105)**: Represents the total number of environment static mesh, material instance, and foliage uassets created in `/Game/SparkVision/Campus/` and `/Game/SparkVision/Materials/`.
2. **Audited Actor Count (83)**: In `audit_environment_clearance.py`, the audit specifically iterates over World Outliner folders matching `folder.startswith("Environment")`:
   - `Environment/Arts_Faculty` (8 actors)
   - `Environment/Curzon_Authentic_Landscape` (6 actors)
   - `Environment/Curzon_Pond/Aquatic_Flora` (8 actors)
   - `Environment/Curzon_Pond/Pond_Architecture` (1 actor)
   - `Environment/Curzon_Pond/Riparian_Trees` (12 actors)
   - `Environment/Curzon_Pond/Wetland_Reeds` (8 actors)
   - `Environment/Doyel_Chattar` (9 actors)
   - `Environment/Fuller_Road` (9 actors)
   - `Environment/Shaheed_Minar` (4 actors)
   - `Environment/Shahidullah_Hall/Lake_Ecology` (10 actors)
   - `Environment/Shahidullah_Hall/Quad_Banyan` (1 actor)
   - `Environment/TSC_Raju` (7 actors)
   - **Total**: $8 + 6 + 8 + 1 + 12 + 8 + 9 + 9 + 4 + 10 + 1 + 7 = 83$ actors.
3. The remaining assets were placed in other outliner hierarchies (`Hero_Buildings/Curzon_Detail`, `Green_Spaces/Hero_Trees`, or unplaced in Content Browser).
4. All 83 actors passed the clearance algorithm (minimum 12m from building perimeters, Z-ground level between -20 and +30 cm, and zero occlusion along the Curzon central sightline).

### 3.2 Viewport vs. PIE Verification of Screenshots
- Inspection of `Scripts/capture_campus_verification_suite.py` reveals that the 10 screenshots (`C01`–`C04`, `ENV_01`–`ENV_06`) were generated via `EditorToolset.EditorAppToolset.CaptureViewport` by positioning the **Unreal Editor Viewport Camera** at prescribed world coordinates with `bShowUI: False`.
- They were **not** captured from a live character pawn during runtime Play-In-Editor (PIE).
- The first authentic PIE screenshot with player pawn, ground contact, and dynamic HUD was captured in commit `10c9c75` at `LIVE_GAMEPLAY_CURZON_HALL_VERIFIED.png`.

---

## 4. Current System Inventory

| System | Component / Path | Current Status | Findings & Action Required |
| :--- | :--- | :--- | :--- |
| **Engine & Build** | Unreal Engine 5.8 (`MyProject.uproject`) | Operational | Native Mac ARM64 build via `Build.sh`. PCH cache cleaned. |
| **Game Map** | `/Game/SparkVision/Maps/Campus/LV_Campus_Blockout` | Loaded | 41 outliner folders, full campus road network, solid collision. |
| **Game Mode** | `/Script/MyProject.SVGameMode` | Active | Spawns `ASVCharacter` and `ASVHUD`. Needs menu gamemode support. |
| **Player Pawn** | `Source/MyProject/SVCharacter` | Playable | Quinn skeletal mesh, `ABP_Unarmed_C`, WASD, sprint, jump, mouse look. |
| **Camera** | `USpringArmComponent` + `UCameraComponent` | Operational | 380cm default distance, 460cm sprint distance, pitch/yaw limits. |
| **Interaction** | `USVInteractableInterface` | Operational | Sphere trace (280cm radius), prompt broadcast. |
| **Archive Terminals**| `Source/MyProject/SVArchiveTerminal` | Operational | 6 terminals placed at authentic landmarks with brass material. |
| **NPC System** | `Source/MyProject/SVStudentNPC` | Partially Functional | Has dialogue array, but lacks skeletal mesh / anim BP assignment. |
| **Opponents** | `Source/MyProject/SVHostileOpponent` | Present (Out of Scope) | Helmeted opponents present in level; violates Level 1 peaceful canon. Must be disabled in Level 1. |
| **HUD** | `Source/MyProject/SVHUD` | Operational | Compass ribbon, vitals gauge, interaction prompt, controls legend. Needs objective tracker & menu integration. |
| **Mission Control** | `JavaMissionControl/` | Operational | Spring-like HttpServer + SQLite on port 8080. Unit tests pass. |
| **Subsystem** | `Source/MyProject/SVMissionControlSubsystem`| Operational | Async HTTP calls to `http://127.0.0.1:8080`. |
| **Menus & Save/Load**| In-game UI / SaveGame | Missing | Requires interactive Main Menu, Pause Menu, and SaveGame persistence. |

---

## 5. Story Authority Baseline (`Where It All Began`)
- **Authority Sources:** `/Users/atiaoishi/Downloads/sparkvision/Documentation/LEVELS.md` & `/Users/atiaoishi/Downloads/2x12_COMPLETE_GAME_PLAN.md`
- **Period:** July 1–14, 2024
- **Tone:** Peaceful student demonstration, historical inquiry, and solidarity.
- **Combat:** **Disabled.** Hostile encounters deferred to Level 2 (July 15).
- **Objectives:**
  - `L1_M01`: Basic campus arrival and locomotion mastery.
  - `L1_M02`: Landmark traversal across Dhaka University.
  - `L1_M03`: Student dialogues (Tanvir at Curzon, Nusrat at Hakim Chattar, Fahim at TSC).
  - `L1_M04`: Inspect the 5 Historical Archives and the 1921 Boundary Stone.
  - `L1_M05`: Peaceful gathering assembly and awareness building.
  - `L1_M06`: The 14 July commitment: *"আমিও থাকব।"* ("I will be there too."), triggering Chapter 1 completion and Level 2 unlock.
