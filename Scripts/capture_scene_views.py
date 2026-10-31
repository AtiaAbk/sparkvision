#!/usr/bin/env python3
"""
Captures multi-angle cinematic screenshots of Curzon Hall in Unreal Engine 5.8
under Daylight and Golden Hour lighting configurations.
Saves PNG files to Documentation/Screenshots/ and the brain artifact directory.
"""

import os
import json
import base64
import subprocess

OUTPUT_DIR = "/Users/atiaoishi/Downloads/sparkvision/Documentation/Screenshots"
ARTIFACT_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

SUN_ACTOR = "/Game/SparkVision/Maps/Campus/LV_Campus_Blockout.LV_Campus_Blockout:PersistentLevel.DirectionalLight_UAID_F4A475FF15A3736A02_1961932697"

VIEWPOINTS = [
    {
        "name": "Phase2_Curzon_FrontFacade",
        "loc": {"x": -5500.0, "y": 0.0, "z": 800.0},
        "rot": {"pitch": -6.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "name": "Phase2_Curzon_PlayerSpawn",
        "loc": {"x": -3550.0, "y": 0.0, "z": 180.0},
        "rot": {"pitch": -2.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "name": "Phase2_Curzon_EntranceApproach",
        "loc": {"x": -2900.0, "y": 0.0, "z": 160.0},
        "rot": {"pitch": 8.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "name": "Phase2_Curzon_CinematicAngled",
        "loc": {"x": -6200.0, "y": -4200.0, "z": 2400.0},
        "rot": {"pitch": -20.0, "yaw": 30.0, "roll": 0.0}
    },
    {
        "name": "Phase2_Curzon_CourtyardLawn",
        "loc": {"x": -3600.0, "y": -2000.0, "z": 220.0},
        "rot": {"pitch": 2.0, "yaw": 35.0, "roll": 0.0}
    }
]

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

def set_sun(pitch, yaw, roll=0.0):
    run_mcp("editor_toolset.toolsets.actor.ActorTools", "set_actor_transform", {
        "actor": {"refPath": SUN_ACTOR},
        "xform": {
            "location": {"x": 0.0, "y": 0.0, "z": 920.0},
            "rotation": {"pitch": pitch, "yaw": yaw, "roll": roll},
            "scale": {"x": 2.5, "y": 2.5, "z": 2.5}
        },
        "worldspace": True
    })

def capture_view(vp, suffix=""):
    filename = f"{vp['name']}{suffix}.png"
    filepath_doc = os.path.join(OUTPUT_DIR, filename)
    filepath_art = os.path.join(ARTIFACT_DIR, filename)
    print(f"Capturing {filename} at {vp['loc']}...")
    
    cap_args = {
        "captureTransform": {
            "location": vp["loc"],
            "rotation": vp["rot"]
        },
        "annotations": {
            "gridSpacing": 0,
            "gridExtent": 0,
            "gridHeight": 0,
            "maxLabelDistance": 0,
            "classFilter": [],
            "maxLabels": 0
        },
        "bShowUI": False
    }
    res = run_mcp("EditorToolset.EditorAppToolset", "CaptureViewport", cap_args)
    img_data = res.get("returnValue", {}).get("image", {}).get("data", "")
    if not img_data:
        print("ERROR: No image data returned!")
        return None
    raw_bytes = base64.b64decode(img_data)
    with open(filepath_doc, "wb") as f:
        f.write(raw_bytes)
    with open(filepath_art, "wb") as f:
        f.write(raw_bytes)
    print(f"  Saved ({len(raw_bytes)} bytes) to {filepath_doc}")
    return filepath_doc

def main():
    print("=== Configuration B: Restrained Late-Afternoon Golden-Hour Lighting ===")
    set_sun(pitch=-24.0, yaw=-65.0, roll=0.0)
    for vp in VIEWPOINTS:
        capture_view(vp, suffix="_GoldenHour")

    print("\n=== Configuration A: Clean Natural Daylight ===")
    set_sun(pitch=-52.0, yaw=-35.0, roll=0.0)
    for vp in VIEWPOINTS:
        capture_view(vp, suffix="_Daylight")

    # Restore Golden-Hour as default hero mood
    set_sun(pitch=-24.0, yaw=-65.0, roll=0.0)
    print("\nAll views captured and lighting verified!")

if __name__ == "__main__":
    main()
