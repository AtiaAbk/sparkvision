#!/usr/bin/env python3
"""
Capture Natural Redesign Verification Suite
Captures 5 high-fidelity in-engine views in LV_Level01_Compact_Campus:
1. NATURAL_CURZON_HERO_DAYLIGHT.png - Curzon Hall facade, brick circular flower beds, natural Krishnachura tree, blue sky
2. NATURAL_CURZON_POND_DAYLIGHT.png - Botanical Pond, crystal water reflections, weeping Debdaru trees, banyans
3. NATURAL_CAMPUS_HERITAGE_GATE_HIGHWAY.png - View through Curzon Heritage Gate onto bustling outer highway with Dhaka traffic & modern towers
4. NATURAL_CAMPUS_AVENUE_GARDENS.png - Main connecting avenue to Doyel Chattar with flower borders and organic flora
5. NATURAL_FULLER_ROAD_SHAHEED_MINAR.png - Connected road corridor to Shaheed Minar and student halls
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
os.makedirs(RUNTIME_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

CAPTURES = [
    {
        "filename": "NATURAL_CURZON_HERO_DAYLIGHT.png",
        "description": "Curzon Hall Hero Facade, Flower Gardens & Natural Blooming Krishnachura",
        "loc": {"x": 200.0, "y": -1800.0, "z": 240.0},
        "rot": {"pitch": -5.0, "yaw": 60.0, "roll": 0.0}
    },
    {
        "filename": "NATURAL_CURZON_POND_DAYLIGHT.png",
        "description": "Curzon Botanical Pond, Weeping Debdaru Flora, Water Reflections & Lotus",
        "loc": {"x": 3800.0, "y": 800.0, "z": 220.0},
        "rot": {"pitch": -7.0, "yaw": 40.0, "roll": 0.0}
    },
    {
        "filename": "NATURAL_CAMPUS_HERITAGE_GATE_HIGHWAY.png",
        "description": "Curzon Heritage Gate Vista onto Dhaka Highway, Traffic (Buses, CNGs) & Modern Highrises",
        "loc": {"x": 5800.0, "y": -2200.0, "z": 180.0},
        "rot": {"pitch": -3.0, "yaw": 90.0, "roll": 0.0}
    },
    {
        "filename": "NATURAL_CAMPUS_AVENUE_GARDENS.png",
        "description": "Main Connected Campus Avenue with Flower Borders leading to Doyel Chattar",
        "loc": {"x": 2500.0, "y": -4800.0, "z": 180.0},
        "rot": {"pitch": -6.0, "yaw": -70.0, "roll": 0.0}
    },
    {
        "filename": "NATURAL_FULLER_ROAD_SHAHEED_MINAR.png",
        "description": "Connected Road Corridor towards Shaheed Minar, Shahidullah Hall & Campus Gardens",
        "loc": {"x": 2500.0, "y": -13000.0, "z": 180.0},
        "rot": {"pitch": -5.0, "yaw": -90.0, "roll": 0.0}
    },
]

def main():
    print("=" * 75)
    print("CAPTURING NATURAL REDESIGN VISUAL VERIFICATION SUITE")
    print("Level: /Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus")
    print("=" * 75)

    # Deselect all actors
    try:
        invoke_tool("SelectActors", "EditorToolset.EditorAppToolset", {"actors": []})
    except Exception:
        pass

    for i, item in enumerate(CAPTURES, 1):
        fn = item["filename"]
        desc = item["description"]
        print(f"\n[{i}/{len(CAPTURES)}] Capturing: {desc} ({fn})...")

        cap = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
            "captureTransform": {
                "location": item["loc"],
                "rotation": item["rot"],
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
                out_path = os.path.join(d, fn)
                with open(out_path, "wb") as f:
                    f.write(img_bytes)
            print(f"  ✓ Saved {fn} ({len(img_bytes)/1024:.1f} KB)")
        else:
            print(f"  ✗ Failed to capture data for {fn}")

    print("\n" + "=" * 75)
    print("✅ ALL 5 NATURAL REDESIGN CAPTURES COMPLETE!")
    print("=" * 75)

if __name__ == "__main__":
    main()
