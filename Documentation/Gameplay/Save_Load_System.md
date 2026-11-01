# SparkVision — Save & Load Architecture

## 1. Dual-Tier Persistence Architecture
SparkVision implements a dual-tier persistence model:
1. **Tier 1: Unreal Engine Native `USaveGame` (`USVSaveGame`)**:
   - Stores local player transform (world location, rotation), camera settings, graphics scalability presets, audio volume, and offline objective flags.
   - Saved locally to `Saved/SaveGames/SVSave_Slot0.sav`.
2. **Tier 2: Java Mission Control Database (`sparkvision_missions.db`)**:
   - Stores authoritative academic session history, immutable timestamped events, archive verification, and chapter completion records in SQLite.

## 2. Save Data Structure
- `SaveSlotName`: Name of active save slot (default: `SVSave_Slot0`).
- `PlayerTransform`: Transform of player character upon saving.
- `ActiveMissionId`: Current mission identifier (`L1_M01` through `L1_M06`).
- `DiscoveredArchives`: `TSet<FString>` of recovered archive IDs.
- `SpokenNPCs`: `TSet<FString>` of contacted student NPCs.
- `bLevel1Completed`: Boolean flag marking Chapter 1 completion.
- `bLevel2Unlocked`: Boolean flag marking Chapter 2 unlock status.
- `SaveTimestamp`: Real-world save date and time.
