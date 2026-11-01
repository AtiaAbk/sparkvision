#!/usr/bin/env python3
"""
SparkVision — Dhaka University Open World Interactive Gameplay Launcher
Launches an interactive Play-In-Editor (PIE) game session with full player controls,
third-person camera, authentic campus ecology, and historical archive discovery.
"""

import sys
import os
import time
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

def launch_game(floating=True):
    mode = "PlayMode_InEditorFloating" if floating else "PlayMode_InViewPort"
    print("=" * 70)
    print("  SPARKVISION: UNIVERSITY OF DHAKA — LEVEL 1 GAME LAUNCHER")
    print("=" * 70)
    print(f"Launching game session (Mode: {mode})...")

    try:
        invoke_tool("StartPIE", "EditorToolset.EditorAppToolset", {
            "options": {
                "bSimulate": False,
                "playMode": mode,
                "warmupSeconds": 1.5
            }
        })
        print("\n>>> GAME IS LIVE AND READY TO PLAY! <<<\n")
        print("CONTROLS:")
        print("  • W / A / S / D     : Move Forward, Left, Backward, Right")
        print("  • Left Shift (Hold) : Sprint (Athletic traversal across campus)")
        print("  • Space             : Jump")
        print("  • Mouse Movement    : Look Around (Dynamic Camera Control)")
        print("  • E                 : Inspect Historical Archives & Memorial Plaques")
        print("\nCAMPUS FAST-TRAVEL HOTKEYS:")
        print("  • [1] Curzon Hall South Portico")
        print("  • [2] Doyel Chattar Roundabout (National Bird Monument)")
        print("  • [3] Central Shaheed Minar Memorial Plaza")
        print("  • [4] Teacher-Student Centre (TSC) & Raju Memorial Sculpture")
        print("  • [5] DU Central Library & Hakim Chattar")
        print("  • [6] Arts Faculty (Kala Bhaban) & Aparajeyo Bangla")
        print("=" * 70)
        print("Click into the game window to capture mouse & keyboard.")
        print("Press Shift+F1 or Esc in Unreal Editor to release mouse.")
        print("=" * 70)
    except Exception as e:
        print(f"Error starting game session: {e}")

def stop_game():
    print("Stopping game session...")
    try:
        invoke_tool("StopPIE", "EditorToolset.EditorAppToolset", {})
        print("Game session stopped cleanly.")
    except Exception as e:
        print(f"Notice: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "stop":
        stop_game()
    else:
        launch_game(floating=True)
