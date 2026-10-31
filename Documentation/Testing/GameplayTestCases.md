# SPARKVISION — GAMEPLAY TEST MATRIX & EXECUTION LOG

## 1. Title & Executive Purpose

* **Document**: `GameplayTestCases.md`
* **Purpose**: Detailed test cases and verification records validating character mechanics, input responsiveness, physics collisions, and quest triggers in active gameplay.

---

## 2. Test Cases Matrix

| Test ID | Test Scenario | Preconditions | Expected Outcome | Execution Result | Status |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **TC-GP-01** | **Player Pawn Possession** | Level `LV_Campus_Blockout` loaded | Player pawn spawns at `PlayerStart_CurzonPromenade` (`Z=107.65`), possessed by controller | Character stands firmly on promenade; camera attached | `PASSED` |
| **TC-GP-02** | **Zero Ground Encroachment** | `PlayerStart` bounds evaluated | Bounds min Z ($72\text{ cm}$) exceeds terrain hit Z ($15.5\text{ cm}$) | Character does not fall into abyss or spawn at (0,0,0) | `PASSED` |
| **TC-GP-03** | **WASD Locomotion** | PIE session active | Character walks forward, backward, left, right at $500\text{ cm/s}$ | Smooth animation blending and orientation | `PASSED` |
| **TC-GP-04** | **Jump & Air Control** | Character moving forward | Pressing Spacebar executes $500\text{ cm/s}$ vertical impulse with air control | Clean jump apex and landing recovery | `PASSED` |
| **TC-GP-05** | **Curzon Promenade Collision** | Character walks to entrance | Pavement and steps provide solid blocking collision | Zero sinking or clipping through stone steps | `PASSED` |
| **TC-GP-06** | **Archive Terminal Interaction** | Step inside $180\text{ cm}$ sphere | Context prompt `[E] Examine Archive` displays; 'E' triggers server call | Server logs `archive registered`; UI updates | `PASSED` |
| **TC-GP-07** | **Student NPC Proximity** | Approach within $250\text{ cm}$ | NPC head rotates to face player; interaction available | Dialogue trigger initiates successfully | `PASSED` |
| **TC-GP-08** | **Mission Control Offline Failover**| Terminate port 8080 process | Subsystem logs connection warning; gameplay continues unhitched | Subsystem queues events; no crash | `PASSED` |

---

## 3. Current Status

* **Status**: `COMPLETED`
* **Evidence**:
  - Live PIE gameplay verified and captured in `PIE_Live_Gameplay_Verified.png`.
  - TC-GP-01 through TC-GP-08 executed and validated.
* **Remaining Tasks**:
  - Author automated PIE input playback script for continuous regression testing.
