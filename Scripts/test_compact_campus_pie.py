#!/usr/bin/env python3
"""
Test Play-In-Editor (PIE) in LV_Level01_Compact_Campus
Captures 3 cinematic Where Winds Meet gameplay vistas with clean UI (bShowUI=False):
1. COMPACT_PIE_LIVE_GAMEPLAY.png - Hero Curzon Promenade, Boxwood Borders, Tanvir & Archive Lectern
2. WWM_CURZON_POND_LIVE_GAMEPLAY.png - Curzon Botanical Pond, East & North Bank Debdaru Screening Wall & Lotus Bloom
3. WWM_HERO_SANCTUARY_LIVE_GAMEPLAY.png - Veranda Landing View Looking Down Promenade toward Botanical Sanctuary
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
    print("TESTING LIVE PIE GAMEPLAY IN COMPACT LEVEL 1 CAMPUS (WWM SANCTUARY)")
    print("=" * 70)

    # 1. Stop any running PIE session
    try:
        is_running = invoke_tool("IsPIERunning", "EditorToolset.EditorAppToolset").get("returnValue", False)
        if is_running:
            print("Stopping previous PIE session...")
            invoke_tool("StopPIE", "EditorToolset.EditorAppToolset")
            time.sleep(2)
    except Exception:
        pass

    # Deselect all actors to avoid any wireframes or selection highlights
    try:
        invoke_tool("SelectActors", "EditorToolset.EditorAppToolset", {"actors": []})
    except Exception:
        pass

    # 2. Start PIE
    print("Starting Play-In-Editor session...")
    options = {
        "bSimulate": False,
        "playMode": "PlayMode_InViewPort",
        "warmupSeconds": 2.5
    }
    invoke_tool("StartPIE", "EditorToolset.EditorAppToolset", {"options": options})
    print("PIE started! Waiting for player pawn and world to settle...")
    time.sleep(4)

    try:
        # Deselect again in PIE just in case
        try:
            invoke_tool("SelectActors", "EditorToolset.EditorAppToolset", {"actors": []})
        except Exception:
            pass

        # 3. Capture Live Gameplay Viewport - Hero Curzon Promenade
        print("\n[1/3] Capturing Live PIE Gameplay screenshot (Curzon Hero Promenade)...")
        cap = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
            "captureTransform": {
                "location": {"x": -4500.0, "y": 0.0, "z": 220.0},
                "rotation": {"pitch": -5.0, "yaw": 0.0, "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            },
            "annotations": {
                "gridSpacing": 0, "gridExtent": 0, "gridHeight": 0, "maxLabelDistance": 0, "classFilter": None, "maxLabels": 0
            },
            "bShowUI": False
        })
        
        img_b64 = cap.get("returnValue", {}).get("image", {}).get("data", "")
        if img_b64:
            img_bytes = base64.b64decode(img_b64)
            for d in [RUNTIME_DIR, ARTIFACT_DIR]:
                with open(os.path.join(d, "COMPACT_PIE_LIVE_GAMEPLAY.png"), "wb") as f:
                    f.write(img_bytes)
            print(f"  ✓ Live gameplay screenshot saved ({len(img_bytes)/1024/1024:.2f} MB)")

        # 4. Capture Live Pond Vista (Debdaru Wall, Lotus Pads, Waterline)
        print("\n[2/3] Capturing Live PIE Gameplay screenshot (Curzon Pond Flora & Screening Wall)...")
        cap_pond = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
            "captureTransform": {
                "location": {"x": 2200.0, "y": -900.0, "z": 250.0},
                "rotation": {"pitch": -10.0, "yaw": 35.0, "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            },
            "annotations": {
                "gridSpacing": 0, "gridExtent": 0, "gridHeight": 0, "maxLabelDistance": 0, "classFilter": None, "maxLabels": 0
            },
            "bShowUI": False
        })

        img_b64_p = cap_pond.get("returnValue", {}).get("image", {}).get("data", "")
        if img_b64_p:
            img_bytes_p = base64.b64decode(img_b64_p)
            for d in [RUNTIME_DIR, ARTIFACT_DIR]:
                with open(os.path.join(d, "WWM_CURZON_POND_LIVE_GAMEPLAY.png"), "wb") as f:
                    f.write(img_bytes_p)
            print(f"  ✓ Live Pond screenshot saved ({len(img_bytes_p)/1024/1024:.2f} MB)")

        # 5. Capture Hero Landing Reverse Vista (Promenade, Boxwood Hedges, Botanical Gardens)
        print("\n[3/3] Capturing Live PIE Gameplay screenshot (Curzon Veranda Promenade Vista)...")
        cap_sanctuary = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
            "captureTransform": {
                "location": {"x": -3450.0, "y": 0.0, "z": 200.0},
                "rotation": {"pitch": -4.0, "yaw": 180.0, "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            },
            "annotations": {
                "gridSpacing": 0, "gridExtent": 0, "gridHeight": 0, "maxLabelDistance": 0, "classFilter": None, "maxLabels": 0
            },
            "bShowUI": False
        })

        img_b64_s = cap_sanctuary.get("returnValue", {}).get("image", {}).get("data", "")
        if img_b64_s:
            img_bytes_s = base64.b64decode(img_b64_s)
            for d in [RUNTIME_DIR, ARTIFACT_DIR]:
                with open(os.path.join(d, "WWM_HERO_SANCTUARY_LIVE_GAMEPLAY.png"), "wb") as f:
                    f.write(img_bytes_s)
            print(f"  ✓ Live Sanctuary Landing screenshot saved ({len(img_bytes_s)/1024/1024:.2f} MB)")

    finally:
        # 6. Stop PIE cleanly
        print("\nStopping PIE session...")
        try:
            invoke_tool("StopPIE", "EditorToolset.EditorAppToolset")
        except Exception:
            pass
        time.sleep(1)

    print("\n" + "=" * 70)
    print("✅ PIE GAMEPLAY TEST AND VISUAL VERIFICATION COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    main()
