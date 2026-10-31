# SPARKVISION — UNREAL ENGINE 5.8 CLIENT ARCHITECTURE

## 1. Title & Executive Purpose

* **Document**: `UnrealArchitecture.md`
* **Purpose**: Documents the C++ and Blueprint gameplay architecture, class hierarchies, player possession, collision layers, World Partition setup, and actor organization in **Unreal Engine 5.8**.

---

## 2. Core Gameplay Class Hierarchy

```text
UGameInstanceSubsystem
└── USVMissionControlSubsystem      [Handles HTTP networking, session sync, and archive state]

AGameModeBase
└── BP_ThirdPersonGameMode          [Configures default pawn, player controller, and player spawn]

ACharacter
├── BP_ThirdPersonCharacter         [Hero pawn: movement, sprint, jump, camera spring arm]
├── ASVStudentNPC                   [Friendly student actors: dialogue triggers, idle anims]
└── ASVHostileOpponent              [Adversary pawns: detection radius, combat encounters]

AActor
├── ASVArchiveTerminal              [Interactive historical terminal: collision box, highlight]
└── StaticMeshActor                 [Modular architecture, props, foliage, and landmarks]
```

---

## 3. Subsystem Implementation (`USVMissionControlSubsystem`)

The mission subsystem is implemented in C++ as a `UGameInstanceSubsystem`, ensuring lifecycle persistence across level transitions:
* **Base URL**: `http://127.0.0.1:8080`
* **Health Check**: Executes on `Initialize()` via non-blocking `FHttpModule::Get().CreateRequest()`.
* **Session Lifecycle**: Requests `POST /api/v1/session/start` upon entering the persistent level.
* **Delegates & Events**:
  - `FOnMissionControlConnected`: Fires when server health is verified.
  - `FOnArchiveDiscovered`: Broadcasts updated archive count and Level 2 unlock status.

---

## 4. World Partition & Outliner Organization

The primary level `/Game/SparkVision/Maps/Campus/LV_Campus_Blockout` uses **One File Per Actor (OFPA)** and strict World Outliner folder hierarchies:

```text
LV_Campus_Blockout/
├── Lighting_Environment/           [DirectionalLight, SkyLight, ExponentialHeightFog, PostProcess]
├── Hero_Buildings/
│   ├── Curzon_Hall/                [Curzon_Hall_Complex, modular arches, portico, corner towers]
│   ├── Doyel_Chattar/              [SM_DoyelMonument, perimeter heritage lamps]
│   ├── Shaheed_Minar/              [SM_ShaheedMinar_Monument, altar podium]
│   ├── TSC_Mor/                    [SM_TSC_Building, SM_RajuSculpture]
│   └── Arts_Faculty/               [SM_AparajeyoBangla, Kala Bhaban]
├── Roads_And_Walkways/             [PrimaryRoad_*, PedestrianPath_*]
├── Foliage_And_Nature/             [SM_Campus_Tree_Hero clusters, Curzon pond]
├── Interactive_Gameplay/           [PlayerStart_CurzonPromenade, ArchiveTerminal_01..05]
└── Characters_And_AI/              [NPC_Student_*, Opponent_Helmeted_*]
```

---

## 5. Current Status

* **Status**: `COMPLETED`
* **Evidence**:
  - `BP_ThirdPersonCharacter` successfully spawns and moves in PIE (`PIE_Live_Gameplay_Verified.png`).
  - Outliner contains 145 organized actors across all core folders.
* **Remaining Tasks**:
  - Author C++ combat combo manager on `BP_ThirdPersonCharacter`.
  - Connect student dialogue UI widget to `ASVStudentNPC` proximity trigger.
