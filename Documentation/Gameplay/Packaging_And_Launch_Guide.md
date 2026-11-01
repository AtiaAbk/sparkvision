# SparkVision — Packaging & Launch Guide

## 1. Quick Launch (One-Command Playable Experience)
To run the complete playable game with full player character locomotion, student NPCs, interactive archives, and Java Mission Control:

```bash
# 1. Start Java Mission Control microservice (runs in background on port 8080)
python3 Scripts/start_mission_control.py

# 2. Launch interactive floating game session
python3 Scripts/play_game.py
```

To stop the game session:
```bash
python3 Scripts/play_game.py stop
```

---

## 2. Desktop Controls Quick Reference

- **Move:** `W`, `A`, `S`, `D` (or Arrow Keys)
- **Sprint:** `Left Shift` (Hold) — High-speed traversal across campus avenues (950 cm/s)
- **Jump:** `Space` — Vertical leap and clambering
- **Look Around:** `Mouse Movement` — 360° dynamic third-person camera orbit
- **Interact / Talk:** `E` — Inspect historical archives and talk with student organizers
- **Pause Menu:** `Esc` or `P` — Open in-game menu with Save, Load, Settings
- **Landmark Fast Travel:**
  - `[1]` Curzon Hall South Portico
  - `[2]` Doyel Chattar Roundabout
  - `[3]` Central Shaheed Minar
  - `[4]` Teacher-Student Centre (TSC) & Raju Memorial
  - `[5]` DU Central Library & Hakim Chattar
  - `[6]` Arts Faculty (Kala Bhaban) & Aparajeyo Bangla

---

## 3. Native macOS Packaging Guide
To build a standalone packaged macOS application (`.app`):
```bash
"/Users/Shared/Epic Games/UE_5.8/Engine/Build/BatchFiles/Mac/RunUAT.sh" BuildCookRun \
  -project="/Users/atiaoishi/Downloads/sparkvision/MyProject.uproject" \
  -platform=Mac \
  -clientconfig=Development \
  -cook -allmaps -build -stage -pak -archive \
  -archivedirectory="/Users/atiaoishi/Downloads/sparkvision/Build/Mac"
```
> Note: Native standalone packaging on Apple Silicon requires full macOS Xcode signing credentials configured in Xcode / Unreal Project Settings. For development and tech-demo evaluation on MacBook Air M4, the high-performance floating PIE launcher (`python3 Scripts/play_game.py`) executes using native compiled C++ dylibs at full Metal framerates.
