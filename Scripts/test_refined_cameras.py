#!/usr/bin/env python3
import sys
import os
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

def capture_one(name, loc, rot, out_path):
    cam_xform = {
        "location": loc,
        "rotation": rot,
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
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(img_data))
        print(f"[{name}] OK -> {out_path} ({len(img_data)} bytes)")
    else:
        print(f"[{name}] FAILED to capture")

# Test 03: Ghat steps descending into water
capture_one(
    "POND_03_Ghat_Step_Transition",
    {"x": 2080.0, "y": -400.0, "z": 115.0},
    {"pitch": -18.0, "yaw": 24.0, "roll": 0.0},
    "Documentation/Environment/CurzonPond/Runtime/Test_03_Ghat.png"
)

# Test 04: Lily cluster floating on water
capture_one(
    "POND_04_WaterLily_Cluster_Meniscus",
    {"x": 2860.0, "y": 520.0, "z": 55.0},
    {"pitch": -20.0, "yaw": 58.0, "roll": 0.0},
    "Documentation/Environment/CurzonPond/Runtime/Test_04_Lily.png"
)

# Test 06: Submerged Koi and silt shallows
capture_one(
    "POND_06_Submerged_Life_Shallows",
    {"x": 2580.0, "y": 160.0, "z": 48.0},
    {"pitch": -32.0, "yaw": 55.0, "roll": 0.0},
    "Documentation/Environment/CurzonPond/Runtime/Test_06_Koi.png"
)

# Test 07: Over the shoulder student standing by bank looking at pond
capture_one(
    "POND_07_ThirdPerson_Gameplay_Active",
    {"x": 2180.0, "y": -750.0, "z": 180.0},
    {"pitch": -8.0, "yaw": 28.0, "roll": 0.0},
    "Documentation/Environment/CurzonPond/Runtime/Test_07_Student.png"
)
