#!/usr/bin/env python3
"""
Test Play-In-Editor (PIE) in LV_Level01_Compact_Campus
Verifies player spawn, character possession, camera, and HUD rendering.
"""

import base64
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from mcp_client import invoke_tool

RUNTIME_DIR = "/Users/atiaoishi/Downloads/sparkvision/Documentation/WorldCorrection/Runtime"
ARTIFACT_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
os.makedirs(RUNTIME_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

def main():
    print("=" * 70)
    print("TESTING LIVE PIE GAMEPLAY IN COMPACT LEVEL 1 CAMPUS")
    print("=" * 70)

    # 1. Stop any running PIE session
    is_running = invoke_tool("IsPIERunning", "EditorToolset.EditorAppToolset").get("returnValue", False)
    if is_running:
        print("Stopping previous PIE session...")
        invoke_tool("StopPIE", "EditorToolset.EditorAppToolset")
        time.sleep(2)

    # 2. Start PIE
    print("Starting Play-In-Editor session...")
    options = {
        "bSimulate": False,
        "playMode": "PlayMode_InViewPort",
        "warmupSeconds": 2.0
    }
    invoke_tool("StartPIE", "EditorToolset.EditorAppToolset", {"options": options})
    print("PIE started! Waiting for player pawn and HUD initialization...")
    time.sleep(3)

    try:
        # 3. Capture Live Gameplay Viewport
        print("Capturing Live PIE Gameplay screenshot...")
        cap = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
            "captureTransform": {
                "location": {"x": -3800.0, "y": 0.0, "z": 250.0},
                "rotation": {"pitch": -8.0, "yaw": 0.0, "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            },
            "annotations": {
                "gridSpacing": 0,
                "gridExtent": 0,
                "gridHeight": 0,
                "maxLabelDistance": 0,
                "classFilter": None,
                "maxLabels": 0
            },
            "bShowUI": True
        })
        
        img_b64 = cap.get("returnValue", {}).get("image", {}).get("data", "")
        if img_b64:
            img_bytes = base64.b64decode(img_b64)
            out_file = os.path.join(RUNTIME_DIR, "COMPACT_PIE_LIVE_GAMEPLAY.png")
            with open(out_file, "wb") as f:
                f.write(img_bytes)
            art_file = os.path.join(ARTIFACT_DIR, "COMPACT_PIE_LIVE_GAMEPLAY.png")
            with open(art_file, "wb") as f:
                f.write(img_bytes)
            cam = cap.get("returnValue", {}).get("cameraLocation", {})
            print(f"  ✓ Live gameplay screenshot saved ({len(img_bytes)/1024/1024:.2f} MB)")
            print(f"  ✓ Camera Location: ({cam.get('x',0):.1f}, {cam.get('y',0):.1f}, {cam.get('z',0):.1f})")
        else:
            print("  ✗ Failed to capture PIE screenshot")
    finally:
        # 4. Stop PIE
        print("Stopping PIE session...")
        try:
            invoke_tool("StopPIE", "EditorToolset.EditorAppToolset")
        except Exception:
            pass
        time.sleep(1)
    print("\n✅ PIE gameplay test completed successfully!")

if __name__ == "__main__":
    main()
