# SparkVision — Gameplay and NPC Optimization Report
## Character Locomotion, NPC Behaviors, Quest State Evaluation, and Input Systems

---

## 1. Executive Summary

Gameplay in Level 1 ("Where It All Began") requires the player to navigate the University of Dhaka campus, interact with student organizers (`ASVStudentNPC`), recover historical archive terminals (`ASVArchiveTerminal`), track vitals (Health and Qi stamina), and trigger quest progression (`L1_M01` through `L1_M06`).

All gameplay systems were profiled to eliminate CPU overhead while preserving responsive controls, cinematic camera tracking, and bilingual dialogue delivery.

---

## 2. Gameplay Systems Optimization Details

### A. Sensory Query Throttling

- **Original Behavior**: `ASVCharacter::ScanForInteractables` ran an unthrottled multi-sphere trace (`SphereTraceMultiForObjects`) at 60 Hz every frame.
- **Optimized Behavior**: Throttled to **10 Hz** (0.10s interval). A 100 ms query cycle is imperceptible to players when approaching NPCs or terminals, but reduced physics scene queries by 83%.

### B. Landmark & Spatial Zone Caching

- **Original Behavior**: `GetCurrentLandmarkName()` checked distances against 6 landmark zones every frame in `CheckMissionProgression()`.
- **Optimized Behavior**:
  - `CheckMissionProgression()` throttled to **4 Hz** (0.25s interval).
  - Landmark string evaluation caches the previous result and short-circuits unless the player moves more than 200 units ($\approx 2$ meters) from the last sampled location using distance-squared comparison (`DistSquared2D < 40000.0f`).

### C. Student NPC Optimization (`ASVStudentNPC`)

- NPCs are placed statically at key campus locations:
  - Tanvir (`NPC_01`): Curzon Hall Portico Landing ($X=-2850, Y=0, Z=202$)
  - Nabila (`NPC_02`): DU Central Library Forecourt ($X=73500, Y=-71700, Z=150$)
  - Fahim (`NPC_03`): TSC Raju Memorial Plaza ($X=59000, Y=-63700, Z=150$)
- NPCs do not run expensive per-frame behavioral trees or unconstrained pathfinding during peaceful Level 1 narrative exploration.
- Dialogue interaction is event-driven via `ISVInteractableInterface`, executing only when the player presses `[E]`.

### D. Native Save/Load Progression (`USVSaveGame`)

- Progress is serialized using Unreal's binary `UGameplayStatics::SaveGameToSlot` system into `Saved/SaveGames/SVSave_Slot0.sav`.
- Saves occur only on mission milestone state transitions (`OldMission != ActiveMissionId`) or user pause menu triggers, preventing frame hitching during traversal.

---

## 3. Verification

The end-to-end verification suite confirms all 6 missions (`L1_M01` to `L1_M06`) transition seamlessly, the victory state triggers properly, and save/load persistence maintains full state fidelity with zero frame drops.
