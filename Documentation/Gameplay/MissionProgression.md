# SPARKVISION — MISSION PROGRESSION & STATE SYNCHRONIZATION

## 1. Title & Executive Purpose

* **Document**: `MissionProgression.md`
* **Purpose**: Defines quest progression structures, archive collection thresholds, chapter gating logic, and synchronization between Unreal Engine gameplay events and the persistent Java Mission Control database.

---

## 2. Chapter 1 Milestone Architecture

```mermaid
stateDiagram-v2
    [*] --> Chapter1_Active: Game Start / Player Spawns
    Chapter1_Active --> Archive1_Found: Discover Curzon Portico Archive
    Archive1_Found --> Archive2_Found: Discover Doyel Chattar Archive
    Archive2_Found --> Archive3_Found: Discover Shaheed Minar Archive
    Archive3_Found --> Archive4_Found: Discover TSC Mor Archive
    Archive4_Found --> Archive5_Found: Discover Arts Faculty Archive
    Archive5_Found --> Chapter1_Complete: 5 / 5 Archives Validated by Server
    Chapter1_Complete --> Chapter2_Unlocked: Server sets level2Unlocked = true
    Chapter2_Unlocked --> [*]: Transition to Level 2
```

---

## 3. Server Milestone Verification Contract

Whenever the player retrieves an archive terminal, `USVMissionControlSubsystem` executes `POST /api/v1/chapter-01/archive`:

```json
{
  "sessionId": "unreal_session_1793434577",
  "archiveId": "archive_03",
  "location": "Shaheed Minar",
  "timestamp": 1793434580000
}
```

The Java server responds with updated chapter telemetry:

```json
{
  "success": true,
  "chapterId": "chapter-01",
  "archivesFound": 3,
  "totalArchivesRequired": 5,
  "level2Unlocked": false,
  "message": "Archive registered: archive_03"
}
```

When `archivesFound == 5`:
* `level2Unlocked` flips to `true`.
* `USVMissionControlSubsystem` broadcasts `OnLevel2UnlockedDelegate`.
* The game triggers a victory cinematic and opens the transit portal at the Arts Faculty gate.

---

## 4. Current Status

* **Status**: `COMPLETED`
* **Evidence**:
  - Session registration and mission milestone telemetry verified in live PIE logs:
    `[SVMissionControlSubsystem] Missions updated: 5 / 5 archives, Level 2 Unlocked: 1`.
  - SQLite persistence verified across application restarts.
* **Remaining Tasks**:
  - Connect dynamic on-screen quest notification banner to `OnMissionUpdatedDelegate`.
