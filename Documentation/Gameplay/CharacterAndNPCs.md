# SPARKVISION — CHARACTER & NPC SPECIFICATION

## 1. Title & Executive Purpose

* **Document**: `CharacterAndNPCs.md`
* **Purpose**: Details the movement physics, animation states, collision parameters, and AI behavior models for the player protagonist, friendly student NPCs, and hostile patrol adversaries.

---

## 2. Protagonist Specification (`BP_ThirdPersonCharacter`)

* **Base Class**: `ACharacter`
* **Capsule Component**:
  - `CapsuleRadius`: 42.0 cm
  - `CapsuleHalfHeight`: 96.0 cm
  - `CollisionProfile`: `Pawn` (blocks WorldStatic, WorldDynamic, PhysicsBody; overlaps triggers)
* **Character Movement Component**:
  - `MaxWalkSpeed`: 500.0 cm/s (Normal jog)
  - `MaxWalkSpeedCrouched`: 200.0 cm/s
  - `MaxSprintSpeed`: 850.0 cm/s (Left Shift hold)
  - `JumpZVelocity`: 500.0 cm/s
  - `AirControl`: 0.35 (fluid aerial momentum)
  - `OrientRotationToMovement`: `true` (character automatically turns towards input direction)
  - `RotationRate`: `Yaw = 540.0 deg/s`
* **Spring Arm & Camera Setup**:
  - `TargetArmLength`: 400.0 cm
  - `SocketOffset`: `(X=0, Y=45, Z=25)` cm (subtle over-the-right-shoulder third-person offset)
  - `bUsePawnControlRotation`: `true` on spring arm, `false` on camera

---

## 3. Student NPCs (`ASVStudentNPC`)

* **Class**: Custom C++ `ASVStudentNPC` deriving from `ACharacter`
* **Current Level Placements**:
  - `NPC_Student_Curzon`: Located near Curzon east colonnade (`X=400, Y=-800, Z=95.62`).
  - `NPC_Student_Raju`: Located at Raju Sculpture roundabout (`X=-4300, Y=-3300, Z=97.65`).
* **Behavior State Machine**:
  - `Idle`: Ambient reading, conversing, or taking notes on a clipboard.
  - `ProximityDetected`: Player enters 250 cm radius -> NPC head-tracks towards player.
  - `DialogActive`: Player presses 'E' -> opens contextual lore interface.

---

## 4. Hostile Adversaries (`ASVHostileOpponent`)

* **Class**: Custom C++ `ASVHostileOpponent` deriving from `ACharacter`
* **Current Level Placements**:
  - `Opponent_Helmeted_01`: Patrols perimeter at `(X=1200, Y=-1500, Z=41.60)`.
  - `Opponent_Helmeted_02`: Stationed at checkpoint `(X=1400, Y=-1600, Z=41.60)`.
* **AI Perception & Combat States**:
  - `Patrol`: Waypoint-based walking along restricted compound boundaries.
  - `Suspicion`: Vision cone ($90^\circ$ angle, $1200\text{ cm}$ range) detects player in restricted zone.
  - `Investigation`: Moves toward last known visual/auditory disturbance.
  - `Engagement`: Initiates baton strike sequence; alerts nearby patrol units.

---

## 5. Current Status

* **Status**: `COMPLETED`
* **Evidence**:
  - Player pawn spawned and verified in live PIE (`PIE_Live_Gameplay_Verified.png`).
  - NPCs and hostile opponents active in scene and verified in World Outliner.
* **Remaining Tasks**:
  - Replace default mannequin skeletal mesh with period-accurate 1950s student attire.
  - Implement AI behavior tree with perception stimulus listeners.
