# SparkVision — Comprehensive Gameplay Test Plan

## Overview
This plan specifies the 8 mandatory end-to-end test scenarios (Test A through Test H) required for runtime validation of Level 1.

| Test ID | Test Category | Target System | Success Criteria |
| :--- | :--- | :--- | :--- |
| **Test A** | **Startup & Menus** | Game entry, Main Menu, New Game | Game starts cleanly without crash; Main Menu renders; New Game loads `LV_Campus_Blockout` at Curzon Promenade. |
| **Test B** | **Player Locomotion** | WASD, Sprint, Jump, Mouse Look | Character walks (550 cm/s), sprints (950 cm/s), jumps (650 cm/s), solid ground contact, smooth 360° camera orbit. |
| **Test C** | **Campus Traversal** | Collision & Level Geometry | Player navigates Curzon Hall, Doyel Chattar, Shaheed Minar, TSC, Library, Arts Faculty without clipping or falling through terrain. |
| **Test D** | **NPC Interaction** | Student NPCs & Bilingual Dialogue | Approaching Tanvir, Nusrat, and Fahim displays `[E]` prompt; interacting displays Bengali and English dialogue; advances state. |
| **Test E** | **Archive Objectives** | Heritage Terminals (1–5) | Interacting with each terminal displays parchment card, increments count to 5/5, prevents duplicate increments. |
| **Test F** | **Java Mission Control**| HTTP REST & SQLite Persistence | Java service running on port 8080 responds to `/api/v1/health`, registers `ARCHIVE_DISCOVERED` events, confirms persistence. |
| **Test G** | **Chapter Completion**| Victory Sequence & Level 2 Unlock | Satisfying all objectives triggers *"আমিও থাকব।"* sequence, unlocks Chapter 2, persists across game restarts. |
| **Test H** | **Pause & Save/Load** | In-Game Pause Menu & Persistence | Pressing `Esc`/`P` pauses game; Save creates valid savegame; Restart + Continue restores exact position and mission state. |
