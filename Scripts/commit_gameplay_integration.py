#!/usr/bin/env python3
"""
SparkVision — Final Git Commit for Gameplay Integration
Stages and commits all gameplay-related changes.
"""

import subprocess
import sys
import os

PROJECT = "/Users/atiaoishi/Downloads/sparkvision"

def run(cmd, cwd=PROJECT):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result.stdout.strip(), result.stderr.strip()

print("[1/4] Checking git status...", flush=True)
out, err = run("git status --short")
print(out[:500] if out else "(clean)", flush=True)

print("[2/4] Staging all changes...", flush=True)
run("git add -A")

print("[3/4] Committing...", flush=True)
msg = """feat(gameplay): wire C++ gameplay systems — BP_SVCharacter, BP_SVGameMode, PlayerStart, NPCs, archives

- Created BP_SVCharacter (child of ASVCharacter) and BP_SVGameMode (child of ASVGameMode)
- Created BP_SVPlayerController
- Fixed DefaultEngine.ini: GlobalDefaultGameMode → BP_SVGameMode.BP_SVGameMode_C
- Fixed DefaultGame.ini: GameDefaultMap → LV_Campus_Blockout
- Copied ThirdPerson Input assets (IMC_Default, IMC_MouseLook, IA_Move/Look/Jump/MouseLook)
  to Content/ThirdPerson/Input/Actions/ matching SVCharacter ConstructorHelpers paths
- Created IA_Interact and IA_Sprint placeholder action assets
- Set World Settings DefaultGameMode override to BP_SVGameMode_C
- Placed 1 PlayerStart (CurzonEntrance, Z=150 cm above ground)
- Placed 5 SVArchiveTerminal actors across campus landmarks
- Placed 5 SVStudentNPC actors at key campus interaction zones
- Organized gameplay actors into Outliner folders (Gameplay/Archives, Gameplay/NPCs)
- All gameplay Blueprints saved and assets up to date

Gameplay loop now fully wired:
  PlayerStart → SVCharacter → WASD movement + Enhanced Input
  E key → interact with SVArchiveTerminal → triggers SVGameMode.OnArchiveFound
  5 archives found → TriggerEncounter → OnEncounterCleared → Level1Victory
  SVHUD draws compass, vitals, interaction prompt, archive modal, victory screen
  USVMissionControlSubsystem POSTs events to Java MissionControl (localhost:8080)
  USVSaveGame serializes progress to named save slots"""

out, err = run(f'git commit -m "{msg}"')
print(out[:500] if out else "No changes to commit", flush=True)
if err and "nothing to commit" not in err:
    print(f"  Err: {err[:200]}", flush=True)

print("[4/4] Pushing to origin/main...", flush=True)
out, err = run("git push origin main")
print(out[:300] if out else "(no output)", flush=True)
if err:
    print(f"  {err[:200]}", flush=True)

# Get commit hash
out, _ = run("git log --oneline -1")
print(f"\n✅ Committed: {out}", flush=True)
