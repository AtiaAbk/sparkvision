#!/usr/bin/env python3
"""
Capture Compact Campus Verification Suite
Captures 10 high-resolution camera angles across LV_Level01_Compact_Campus
Saves to Documentation/WorldCorrection/Runtime/ and artifact directory.
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

CAMERAS = [
    {
        "id": "COMPACT_01_Curzon_To_DoyelChattar_Avenue",
        "title": "Curzon North Approach Promenade to Doyel Chattar",
        "loc": {"x": -1500.0, "y": 0.0, "z": 450.0},
        "rot": {"pitch": -12.0, "yaw": -70.0, "roll": 0.0}
    },
    {
        "id": "COMPACT_02_Curzon_Pond_Ecology_Compact",
        "title": "Curzon Botanical Pond and Southern Ghat",
        "loc": {"x": 2000.0, "y": 2500.0, "z": 400.0},
        "rot": {"pitch": -15.0, "yaw": -135.0, "roll": 0.0}
    },
    {
        "id": "COMPACT_03_Doyel_Chattar_And_BanglaAcademy",
        "title": "Doyel Chattar Roundabout & Bangla Academy Burdwan House",
        "loc": {"x": 3000.0, "y": -6000.0, "z": 500.0},
        "rot": {"pitch": -18.0, "yaw": -55.0, "roll": 0.0}
    },
    {
        "id": "COMPACT_04_Shaheed_Minar_Plaza_Sanctuary",
        "title": "Central Shaheed Minar Plinth & Flanking Marble Altar",
        "loc": {"x": -3500.0, "y": -19000.0, "z": 450.0},
        "rot": {"pitch": -10.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "COMPACT_05_Fuller_Road_Corridor_SMHall",
        "title": "Fuller Road Avenue facing Salimullah Muslim Hall",
        "loc": {"x": 5500.0, "y": -22000.0, "z": 450.0},
        "rot": {"pitch": -14.0, "yaw": -120.0, "roll": 0.0}
    },
    {
        "id": "COMPACT_06_TSC_Raju_Student_Hub",
        "title": "TSC Crossroads & Raju Memorial Sculpture",
        "loc": {"x": 14000.0, "y": -26000.0, "z": 500.0},
        "rot": {"pitch": -16.0, "yaw": 35.0, "roll": 0.0}
    },
    {
        "id": "COMPACT_07_Hakim_Chattar_And_Central_Library",
        "title": "Hakim Chattar Student Plaza & DU Central Library",
        "loc": {"x": 21000.0, "y": -24000.0, "z": 550.0},
        "rot": {"pitch": -15.0, "yaw": -40.0, "roll": 0.0}
    },
    {
        "id": "COMPACT_08_Central_Mosque_And_Nazrul_Tomb",
        "title": "DU Central Mosque & Kazi Nazrul Islam Mausoleum",
        "loc": {"x": 27000.0, "y": -25000.0, "z": 550.0},
        "rot": {"pitch": -14.0, "yaw": -20.0, "roll": 0.0}
    },
    {
        "id": "COMPACT_09_Aparajeyo_Bangla_And_Kala_Bhaban",
        "title": "Aparajeyo Bangla Sculpture & Arts Faculty Portico",
        "loc": {"x": 25000.0, "y": -33000.0, "z": 500.0},
        "rot": {"pitch": -12.0, "yaw": -25.0, "roll": 0.0}
    },
    {
        "id": "COMPACT_10_Full_Campus_Panoramic_Vista",
        "title": "Elevated Panoramic Master Vista of Compact University of Dhaka",
        "loc": {"x": -8000.0, "y": -12000.0, "z": 3500.0},
        "rot": {"pitch": -32.0, "yaw": -45.0, "roll": 0.0}
    }
]

def main():
    print("=" * 70)
    print("CAPTURING COMPACT CAMPUS 10-CAMERA VERIFICATION SUITE")
    print("=" * 70)

    for idx, cam in enumerate(CAMERAS, start=1):
        cid = cam["id"]
        title = cam["title"]
        print(f"\n[{idx}/10] Capturing {cid}: {title}...")

        # 1. Set Camera transform
        xform = {
            "location": cam["loc"],
            "rotation": cam["rot"],
            "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
        }
        invoke_tool("SetCameraTransform", "EditorToolset.EditorAppToolset", {
            "transform": xform
        })
        time.sleep(0.5)

        # 2. Capture Viewport with captureTransform & annotations
        cap = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
            "captureTransform": xform,
            "annotations": {
                "gridSpacing": 0,
                "gridExtent": 0,
                "gridHeight": 0,
                "maxLabelDistance": 0,
                "classFilter": None,
                "maxLabels": 0
            },
            "bShowUI": False
        })
        img_b64 = cap.get("returnValue", {}).get("image", {}).get("data", "")
        if not img_b64:
            print(f"  ✗ Failed to capture image for {cid}")
            continue

        img_bytes = base64.b64decode(img_b64)
        
        # Save to Runtime dir
        file_path = os.path.join(RUNTIME_DIR, f"{cid}.png")
        with open(file_path, "wb") as f:
            f.write(img_bytes)
            
        # Save to Artifact dir
        art_path = os.path.join(ARTIFACT_DIR, f"{cid}.png")
        with open(art_path, "wb") as f:
            f.write(img_bytes)

        print(f"  ✓ Saved {len(img_bytes)/1024/1024:.2f} MB -> {file_path}")

    print("\n" + "=" * 70)
    print("VERIFICATION SUITE CAPTURE COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    main()
