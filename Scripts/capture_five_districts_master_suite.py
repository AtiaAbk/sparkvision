#!/usr/bin/env python3
"""
Captures high-fidelity master hero screenshots for all 5 canonical districts of Dhaka University
in Unreal Engine 5 via MCP:
  1. District 1: Curzon Hall & Lake Sanctuary
  2. District 2: Central Shaheed Minar
  3. District 3: TSC & Raju Memorial Student Hub
  4. District 4: Kala Bhaban & Aparajeyo Bangla
  5. District 5: Doyel Chattar Roundabout
"""

import base64
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

ARTIFACT_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
RUNTIME_DIR = "/Users/atiaoishi/Downloads/sparkvision/Documentation/WorldEnvironment/Screenshots/Runtime"
SHOWCASE_DIR = "/Users/atiaoishi/Downloads/sparkvision/Documentation/Showcase"

os.makedirs(ARTIFACT_DIR, exist_ok=True)
os.makedirs(RUNTIME_DIR, exist_ok=True)
os.makedirs(SHOWCASE_DIR, exist_ok=True)

# Deselect all actors to avoid selection outlines
try:
    invoke_tool("SelectActors", "EditorToolset.EditorAppToolset", {"actors": []})
except Exception as e:
    print(f"Warning deselecting actors: {e}")

DISTRICT_VIEWS = [
    {
        "id": "DISTRICT1_CURZON_HALL_MASTER",
        "name": "District 1: Curzon Hall & Lake Sanctuary Master View",
        "description": "Grand Indo-Saracenic red-brick facade, twin tall fan palms, chhatris, central arched portal, circular ornamental flowerbed, framed by Krishnachura canopy",
        "loc": {"x": -6600.0, "y": 0.0, "z": 380.0},
        "rot": {"pitch": 6.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "DISTRICT2_SHAHEED_MINAR_MASTER",
        "name": "District 2: Central Shaheed Minar Master View",
        "description": "Asymmetrical martyr columns with central inclined red sun disk, tiered granite plinth, and background red-brick university buildings",
        "loc": {"x": -2800.0, "y": -54042.0, "z": 180.0},
        "rot": {"pitch": 5.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "DISTRICT3_TSC_MASTER",
        "name": "District 3: TSC & Raju Memorial Student Hub Master View",
        "description": "Anti-terrorism dynamic sculpture roundabout, TSC modernist cultural auditorium complex",
        "loc": {"x": 57200.0, "y": -62000.0, "z": 250.0},
        "rot": {"pitch": -3.0, "yaw": -35.0, "roll": 0.0}
    },
    {
        "id": "DISTRICT4_KALA_BHABAN_MASTER",
        "name": "District 4: Kala Bhaban & Aparajeyo Bangla Master View",
        "description": "Historic 1971 liberation three-figure monument with Kala Bhaban Faculty of Arts grand colonnade portico in the background",
        "loc": {"x": 71500.0, "y": -95794.0, "z": 240.0},
        "rot": {"pitch": 4.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "DISTRICT5_DOYEL_CHATTAR_MASTER",
        "name": "District 5: Doyel Chattar Roundabout Master View",
        "description": "National bird Magpie-Robin sculpted fountain with cascading water plinth, surrounding ring road, and modern urban towers",
        "loc": {"x": 6300.0, "y": -17600.0, "z": 220.0},
        "rot": {"pitch": 6.0, "yaw": 43.0, "roll": 0.0}
    }
]

print("=== EXECUTING FIVE DISTRICTS MASTER CAPTURE SUITE ===")

results = []

for idx, view in enumerate(DISTRICT_VIEWS, 1):
    print(f"\n[{idx}/5] Capturing {view['name']}...")
    xform = {
        "location": view["loc"],
        "rotation": view["rot"],
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
    }
    
    # Position camera
    invoke_tool("SetCameraTransform", "EditorToolset.EditorAppToolset", {"transform": xform})
    time.sleep(0.4)
    
    # Capture viewport
    cap = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
        "captureTransform": xform,
        "annotations": {
            "gridSpacing": 0, "gridExtent": 0, "gridHeight": 0,
            "maxLabelDistance": 0, "classFilter": None, "maxLabels": 0
        },
        "bShowUI": False
    })
    
    img_b64 = cap.get("returnValue", {}).get("image", {}).get("data", "")
    if img_b64:
        data = base64.b64decode(img_b64)
        art_path = os.path.join(ARTIFACT_DIR, f"{view['id']}.png")
        runtime_path = os.path.join(RUNTIME_DIR, f"{view['id']}.png")
        showcase_path = os.path.join(SHOWCASE_DIR, f"{view['id']}.png")
        
        with open(art_path, "wb") as f:
            f.write(data)
        with open(runtime_path, "wb") as f:
            f.write(data)
        with open(showcase_path, "wb") as f:
            f.write(data)
            
        kb = len(data) / 1024.0
        print(f"  SUCCESS: Captured {view['id']} ({kb:.1f} KB)")
        print(f"    Artifact: {art_path}")
        print(f"    Runtime:  {runtime_path}")
        results.append((view["id"], True, kb, art_path))
    else:
        print(f"  ERROR: Failed to capture {view['id']}")
        results.append((view["id"], False, 0, ""))

print("\n=== MASTER CAPTURE SUITE SUMMARY ===")
for vid, ok, kb, path in results:
    status = f"PASSED ({kb:.1f} KB)" if ok else "FAILED"
    print(f"  {vid:<34}: {status}")
