#!/usr/bin/env python3
import base64
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

ARTIFACT_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
DOCS_DIR = "/Users/atiaoishi/Downloads/sparkvision/Documentation/Showcase"
os.makedirs(DOCS_DIR, exist_ok=True)

# Make sure all actors are deselected
invoke_tool("SelectActors", "EditorToolset.EditorAppToolset", {"actors": []})

views = [
    {
        "id": "DISTRICT5_DOYEL_HERO_GROUND",
        "name": "Doyel Chattar Hero 3/4 Ground View",
        "loc": {"x": 5600.0, "y": -18400.0, "z": 220.0},
        "rot": {"pitch": 4.0, "yaw": 45.0, "roll": 0.0}
    },
    {
        "id": "DISTRICT5_DOYEL_HERO_FRONT",
        "name": "Doyel Chattar Front View",
        "loc": {"x": 7507.0, "y": -19500.0, "z": 240.0},
        "rot": {"pitch": 3.0, "yaw": 90.0, "roll": 0.0}
    },
    {
        "id": "DISTRICT5_DOYEL_HERO_AERIAL",
        "name": "Doyel Chattar Aerial Roundabout & Plaza",
        "loc": {"x": 4800.0, "y": -19200.0, "z": 1600.0},
        "rot": {"pitch": -22.0, "yaw": 45.0, "roll": 0.0}
    }
]

for v in views:
    xform = {
        "location": v["loc"],
        "rotation": v["rot"],
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
    }
    invoke_tool("SetCameraTransform", "EditorToolset.EditorAppToolset", {"transform": xform})
    time.sleep(0.3)
    
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
        art_path = os.path.join(ARTIFACT_DIR, f"{v['id']}.png")
        doc_path = os.path.join(DOCS_DIR, f"{v['id']}.png")
        with open(art_path, "wb") as f:
            f.write(data)
        with open(doc_path, "wb") as f:
            f.write(data)
        print(f"Captured {v['id']}: {len(data)/1024:.1f} KB")
    else:
        print(f"Failed to capture {v['id']}")
