#!/usr/bin/env python3
"""
SPARKVISION — CURZON HALL POND 7-VIEW PHOTOGRAPHIC VERIFICATION SUITE
Captures the 7 canonical viewpoints in LV_Level01_Compact_Campus:
1. POND_01_Curzon_Wide_Reflections
2. POND_02_LowAngle_Water_Reflections
3. POND_03_Ghat_Step_Transition
4. POND_04_WaterLily_Cluster_Meniscus
5. POND_05_Natural_Shoreline_Transition
6. POND_06_Submerged_Life_Shallows
7. POND_07_ThirdPerson_Gameplay_Active
"""

import sys
import os
import base64
import json
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

RUNTIME_DIR = "Documentation/Environment/CurzonPond/Runtime"
ARTIFACT_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"

VIEWPOINTS = [
    {
        "id": "POND_01_Curzon_Wide_Reflections",
        "desc": "Wide panoramic view across Curzon Pond with Curzon Hall and sky mirrored in calm freshwater",
        "loc": {"x": 7100.0, "y": 0.0, "z": 180.0},
        "rot": {"pitch": -5.0, "yaw": 180.0, "roll": 0.0}
    },
    {
        "id": "POND_02_LowAngle_Water_Reflections",
        "desc": "Low-angle water surface skimming view displaying specular sheen, subtle ripples, and sky reflections",
        "loc": {"x": 5200.0, "y": -400.0, "z": 26.0},
        "rot": {"pitch": -3.5, "yaw": 165.0, "roll": 0.0}
    },
    {
        "id": "POND_03_Ghat_Step_Transition",
        "desc": "Stepped brick colonial Ghat transition where bottom tiers submerge into the clear freshwater",
        "loc": {"x": 2150.0, "y": 0.0, "z": 85.0},
        "rot": {"pitch": -22.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "POND_04_WaterLily_Cluster_Meniscus",
        "desc": "Close-up of Shapla water lily clusters floating naturally flush with the water meniscus",
        "loc": {"x": 3350.0, "y": 550.0, "z": 45.0},
        "rot": {"pitch": -18.0, "yaw": -145.0, "roll": 0.0}
    },
    {
        "id": "POND_05_Natural_Shoreline_Transition",
        "desc": "Riparian bank edge transition where reeds, ferns, and silt meet the water surface cleanly",
        "loc": {"x": 4200.0, "y": 1450.0, "z": 65.0},
        "rot": {"pitch": -14.0, "yaw": 30.0, "roll": 0.0}
    },
    {
        "id": "POND_06_Submerged_Life_Shallows",
        "desc": "Clear shallow water showing swimming Koi fish and dark submerged silt bed near the Ghat",
        "loc": {"x": 2500.0, "y": -120.0, "z": 55.0},
        "rot": {"pitch": -32.0, "yaw": -25.0, "roll": 0.0}
    },
    {
        "id": "POND_07_ThirdPerson_Gameplay_Active",
        "desc": "Third-person gameplay view of student protagonist standing by the tranquil pond bank",
        "loc": {"x": 2000.0, "y": -200.0, "z": 110.0},
        "rot": {"pitch": -12.0, "yaw": 15.0, "roll": 0.0}
    }
]

def main():
    print("=" * 70)
    print("CAPTURING CURZON HALL POND 7-VIEW PHOTOGRAPHIC VERIFICATION SUITE")
    print("=" * 70)

    os.makedirs(RUNTIME_DIR, exist_ok=True)
    results = []

    for v in VIEWPOINTS:
        vid = v["id"]
        vdesc = v["desc"]
        vloc = v["loc"]
        vrot = v["rot"]
        print(f"\nCapturing {vid}...")
        print(f"  Transform: Loc=({vloc['x']}, {vloc['y']}, {vloc['z']}), Rot=({vrot['pitch']}, {vrot['yaw']})")

        cam_xform = {
            "location": vloc,
            "rotation": vrot,
            "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
        }
        invoke_tool("SetCameraTransform", "EditorToolset.EditorAppToolset", {
            "transform": cam_xform
        })

        res = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
            "captureTransform": cam_xform,
            "annotations": {
                "gridSpacing": 0.0, "gridExtent": 0.0, "gridHeight": 0.0,
                "maxLabelDistance": 0.0, "classFilter": None, "maxLabels": 0
            },
            "bShowUI": False
        })

        img_data = res.get("returnValue", {}).get("image", {}).get("data", "")
        if img_data:
            out_path = os.path.join(RUNTIME_DIR, f"{vid}.png")
            with open(out_path, "wb") as f:
                f.write(base64.b64decode(img_data))
            
            # Copy to brain artifact directory
            art_path = os.path.join(ARTIFACT_DIR, f"{vid}.png")
            shutil.copyfile(out_path, art_path)
            
            print(f"  ✓ Saved to {out_path} ({len(img_data)} bytes)")
            results.append({"id": vid, "desc": vdesc, "path": out_path, "bytes": len(img_data)})
        else:
            print(f"  ✗ Failed to capture {vid}")

    print("\n" + "=" * 70)
    print(f"SUCCESS: Captured {len(results)} / {len(VIEWPOINTS)} verification views!")
    print("=" * 70)

if __name__ == "__main__":
    main()
