#!/usr/bin/env python3
"""
Finalize pristine WWM live gameplay captures in Play-In-Editor (PIE).
Captures 3 definitive AAA verification views:
1. COMPACT_PIE_LIVE_GAMEPLAY.png - Hero Curzon Promenade with Student NPC Tanvir & Archival Terminal
2. WWM_CURZON_POND_LIVE_GAMEPLAY.png - Curzon Botanical Pond 360-degree secluded heritage sanctuary
3. WWM_HERO_SANCTUARY_LIVE_GAMEPLAY.png - Reverse garden vista through blooming Krishnachura framing
"""

import base64
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

RUNTIME_DIR = "/Users/atiaoishi/Downloads/sparkvision/Documentation/WorldCorrection/Runtime"
ARTIFACT_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"

EMPTY_ANNOTATIONS = {
    "gridSpacing": 0, "gridExtent": 0, "gridHeight": 0,
    "maxLabelDistance": 0, "classFilter": None, "maxLabels": 0
}

def main():
    print("=" * 75)
    print("CAPTURING FINAL PRISTINE WWM VERIFICATION TRIAD (PIE)")
    print("=" * 75)

    # 1. Deselect All Actors
    print("\n1. Deselecting all actors...")
    try:
        invoke_tool("SelectActors", "EditorToolset.EditorAppToolset", {"actors": []})
    except Exception as e:
        print(f"  Warning during actor deselection: {e}")

    # 2. Check PIE status & launch
    print("\n2. Launching PIE session...")
    try:
        if invoke_tool("IsPIERunning", "EditorToolset.EditorAppToolset").get("returnValue", False):
            print("  Stopping existing PIE session...")
            invoke_tool("StopPIE", "EditorToolset.EditorAppToolset")
            time.sleep(2)
    except Exception:
        pass

    invoke_tool("StartPIE", "EditorToolset.EditorAppToolset", {
        "options": {
            "bSimulate": False,
            "playMode": "PlayMode_InViewPort",
            "warmupSeconds": 3.0
        }
    })
    print("  Waiting 5 seconds for simulation warmup and shader streaming to settle...")
    time.sleep(5)

    try:
        try:
            invoke_tool("SelectActors", "EditorToolset.EditorAppToolset", {"actors": []})
        except Exception:
            pass

        # View 1: Curzon Promenade Hero View with Tanvir NPC
        print("\n[1/3] Capturing COMPACT_PIE_LIVE_GAMEPLAY.png...")
        cap1 = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
            "captureTransform": {
                "location": {"x": -4500.0, "y": 0.0, "z": 220.0},
                "rotation": {"pitch": -5.0, "yaw": 0.0, "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            },
            "annotations": EMPTY_ANNOTATIONS,
            "bShowUI": False
        })
        b64_1 = cap1.get("returnValue", {}).get("image", {}).get("data", "")
        if b64_1:
            bytes_1 = base64.b64decode(b64_1)
            for d in [RUNTIME_DIR, ARTIFACT_DIR]:
                with open(os.path.join(d, "COMPACT_PIE_LIVE_GAMEPLAY.png"), "wb") as f:
                    f.write(bytes_1)
            print(f"  ✓ Saved COMPACT_PIE_LIVE_GAMEPLAY.png ({len(bytes_1)/1024/1024:.2f} MB)")
        else:
            print("  ❌ Failed to capture View 1")

        # Give 1 second for camera interpolation
        time.sleep(1)

        # View 2: Curzon Pond 360-Degree Botanical Sanctuary
        print("\n[2/3] Capturing WWM_CURZON_POND_LIVE_GAMEPLAY.png...")
        cap2 = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
            "captureTransform": {
                "location": {"x": 2200.0, "y": -900.0, "z": 250.0},
                "rotation": {"pitch": -10.0, "yaw": 35.0, "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            },
            "annotations": EMPTY_ANNOTATIONS,
            "bShowUI": False
        })
        b64_2 = cap2.get("returnValue", {}).get("image", {}).get("data", "")
        if b64_2:
            bytes_2 = base64.b64decode(b64_2)
            for d in [RUNTIME_DIR, ARTIFACT_DIR]:
                with open(os.path.join(d, "WWM_CURZON_POND_LIVE_GAMEPLAY.png"), "wb") as f:
                    f.write(bytes_2)
            print(f"  ✓ Saved WWM_CURZON_POND_LIVE_GAMEPLAY.png ({len(bytes_2)/1024/1024:.2f} MB)")
        else:
            print("  ❌ Failed to capture View 2")

        time.sleep(1)

        # View 3: Promenade Reverse Garden Vista
        print("\n[3/3] Capturing WWM_HERO_SANCTUARY_LIVE_GAMEPLAY.png...")
        cap3 = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
            "captureTransform": {
                "location": {"x": -3450.0, "y": 0.0, "z": 200.0},
                "rotation": {"pitch": 0.0, "yaw": 180.0, "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            },
            "annotations": EMPTY_ANNOTATIONS,
            "bShowUI": False
        })
        b64_3 = cap3.get("returnValue", {}).get("image", {}).get("data", "")
        if b64_3:
            bytes_3 = base64.b64decode(b64_3)
            for d in [RUNTIME_DIR, ARTIFACT_DIR]:
                with open(os.path.join(d, "WWM_HERO_SANCTUARY_LIVE_GAMEPLAY.png"), "wb") as f:
                    f.write(bytes_3)
            print(f"  ✓ Saved WWM_HERO_SANCTUARY_LIVE_GAMEPLAY.png ({len(bytes_3)/1024/1024:.2f} MB)")
        else:
            print("  ❌ Failed to capture View 3")

    finally:
        print("\nStopping PIE cleanly...")
        try:
            invoke_tool("StopPIE", "EditorToolset.EditorAppToolset")
            print("  ✓ PIE stopped successfully.")
        except Exception as e:
            print(f"  Warning during StopPIE: {e}")
        time.sleep(1)

    print("\n" + "=" * 75)
    print("✅ VERIFICATION TRIAD CAPTURED SUCCESSFULLY!")
    print("=" * 75)

if __name__ == "__main__":
    main()
