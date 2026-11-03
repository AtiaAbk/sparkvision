#!/usr/bin/env python3
import sys
import os
import time
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

test_views = [
    {
        "id": "TEST_TSC",
        "loc": {"x": 53500.0, "y": -54500.0, "z": 420.0},
        "rot": {"pitch": -8.0, "yaw": -35.0, "roll": 0.0}
    },
    {
        "id": "TEST_KALA",
        "loc": {"x": 66500.0, "y": -88000.0, "z": 400.0},
        "rot": {"pitch": -8.0, "yaw": -25.0, "roll": 0.0}
    },
    {
        "id": "TEST_DOYEL",
        "loc": {"x": 5600.0, "y": -18400.0, "z": 220.0},
        "rot": {"pitch": 4.0, "yaw": 45.0, "roll": 0.0}
    }
]

invoke_tool("SelectActors", "EditorToolset.EditorAppToolset", {"actors": []})

for v in test_views:
    xform = {
        "location": v["loc"],
        "rotation": v["rot"],
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
    }
    invoke_tool("SetCameraTransform", "EditorToolset.EditorAppToolset", {"transform": xform})
    time.sleep(0.4)
    
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
        out_path = f"/tmp/{v['id']}.png"
        with open(out_path, "wb") as f:
            f.write(data)
        print(f"Captured {v['id']} -> {out_path} ({len(data)} bytes)")
    else:
        print(f"Failed {v['id']}")
